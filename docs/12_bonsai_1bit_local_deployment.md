# 12. Running a 1-Bit LLM Locally on AMD ROCm

*April 2026 — AMD ROCm, Docker, a custom non-mainline quantization format, and a local 108 tokens-per-second observation*

> **Status:** Single-machine deployment case study. Performance and quality statements are local observations unless an external source is linked; they are not independent model benchmarks.

---

## The Paper That Started It

In early 2024, [BitNet b1.58](https://arxiv.org/abs/2402.17764) made the rounds and felt almost too good to be true. Its ternary weights use `-1`, `0`, and `+1`, corresponding to an information density of about 1.58 bits per weight. The paper reported that models trained with this approach could approach full-precision performance at comparable parameter counts while reducing memory and arithmetic costs.

The approach differed from ordinary post-training quantization: the BitNet result depended on training for ternary weights rather than simply converting an existing FP16 checkpoint. The paper reported substantial memory and arithmetic advantages; practical gains still depended on model quality, kernels, and hardware support.

For a while, I had not found a 1-bit model and inference path that I could deploy on this hardware.

Then PrismML shipped Bonsai.

## PrismML and the Q1_0_g128 Format

PrismML took low-bit research into a deployable model and inference implementation. Their Bonsai series uses a custom, non-mainline format called `Q1_0_g128`:

- Every 128 weights share a single FP16 scale factor
- Each binary weight selects `-scale` or `+scale`
- Result: **1.125 bits per weight average**, with the scale factors providing just enough precision for coherent outputs

External references: [Bonsai-8B model card](https://huggingface.co/prism-ml/Bonsai-8B-gguf) and [PrismML llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp).

Bonsai-8B — an 8.19 billion parameter model based on the Qwen3 architecture — compresses to **1.07 GiB**. For comparison, the same model in standard 4-bit quantization (Q4_K_M) would be roughly 5 GiB. In FP16, about 16 GiB.

One gigabyte. For an 8B parameter model.

The catch at the time of this deployment: Q1_0_g128 was not supported by the standard Ollama distribution or mainline llama.cpp. PrismML published a custom llama.cpp fork with the required kernels. “Custom” is the important distinction here; the public model and fork carry open-source licenses, so the original description of the whole stack as proprietary was too broad.

## Why Not Just Use Ollama

The first instinct was to download the GGUF from HuggingFace and pull it into Ollama. In this test, that path failed without a useful user-facing explanation.

Ollama downloads the file, creates a model entry, and appears to load it. When you send a prompt, you get garbage output — or no output at all. Ollama's backend is standard llama.cpp, which encounters the Q1_0_g128 quantization type and either errors out internally or misinterprets the weight layout.

The correct path is: PrismML's llama.cpp fork → compiled with GPU support → serving via `llama-server` → any OpenAI-compatible frontend on top. AnythingLLM fit the last requirement perfectly: it supports generic OpenAI endpoints, has built-in RAG, and runs as a Docker container.

## The Build Plan

The architecture is two containers:

```
┌─────────────────────────────┐     ┌────────────────────────────┐
│  bonsai-llama               │     │  bonsai-anythingllm        │
│  PrismML llama.cpp fork     │◄────│  Chat UI + RAG             │
│  AMD ROCm/HIP               │     │  OpenAI-compatible client  │
│  Port 8080 (/v1 API)        │     │  Port 3001 (Web UI)        │
└─────────────────────────────┘     └────────────────────────────┘
        │
        ▼
  /dev/kfd + /dev/dri
  RX 6750 XT (gfx1031)
  HSA_OVERRIDE_GFX_VERSION=10.3.0
```

The llama-server container builds PrismML's fork inside a ROCm base image and serves the model via HTTP. AnythingLLM points its LLM connection at `http://llama-server:8080/v1`, treating it as a generic OpenAI endpoint.

Hardware: AMD Ryzen 7 5700X, RX 6750 XT (Navi 22, gfx1031), 64 GB RAM.

## The Five Errors

Getting from "plan" to "working container" required fixing five distinct failures. Each one was uninformative in isolation. Together they trace the path from CPU-only inference through full GPU acceleration.

### Error 1: SQLite Can't Open Database

**Symptom**: AnythingLLM container crashed on startup with a loop of:
```
SQLiteError: unable to open database file
```

**Root cause**: The bind-mounted `anythingllm-storage/` directory was owned by root on the host, while the AnythingLLM process used a non-root UID and could not write to it.

**Historical workaround**: Add `user: "0:0"` to the AnythingLLM service in Docker Compose. The container then ran as root and bypassed the ownership mismatch.

```yaml
anythingllm:
  image: mintplexlabs/anythingllm
  user: "0:0"    # run as root to avoid volume permission issues
```

It worked, but it is not the recommended security fix. “Local-only” does not make a root process harmless. A reusable deployment should align the host directory ownership with the image's documented runtime UID, use a correctly owned named volume, or perform a narrow initialization step before dropping privileges.

### Error 2: hipblas Not Found

**Symptom**: cmake configuration failed during the llama-server build:
```
Could not find a package configuration file provided by "hipblas"
```

**Root cause**: The `rocm/dev-ubuntu-22.04:latest` base image includes ROCm runtime libraries but not the development headers. Building llama.cpp with HIP requires `hipblas-dev` and `rocblas-dev`.

**Fix**: Add the -dev packages to the apt-get install step:

```dockerfile
RUN apt-get update && apt-get install -y \
    git cmake build-essential curl wget \
    hipblas-dev rocblas-dev \
    && rm -rf /var/lib/apt/lists/*
```

After this, cmake found hipblas and the build proceeded.

### Error 3: Segfault on Launch (Exit Code 139)

**Symptom**: The container started, printed a few lines of initialization, then died with exit code 139 (SIGSEGV). The crash happened during slot initialization, before any model was loaded.

**Root-cause assessment**: The initial Dockerfile built only for `gfx1030`, while `rocminfo` reported the RX 6750 XT as `gfx1031`. The target mismatch was the leading explanation for the crash; rebuilding for the reported target removed this failure. The test did not independently isolate the exact failing instruction.

`rocminfo` reports the device as `gfx1031`. The `-DAMDGPU_TARGETS` flag must match the actual hardware, or include it.

**Fix**: Build for both targets to cover both the actual hardware and a fallback:

```dockerfile
RUN cmake -B build \
    -DGGML_HIP=ON \
    -DAMDGPU_TARGETS="gfx1031;gfx1030" \
    ...
```

### Error 4: TensileLibrary Illegal Seek (The Tricky One)

**Symptom**: After fixing the segfault, the container started successfully, loaded the model, then printed:
```
rocBLAS error: /opt/rocm/lib/librocblas.so: TensileLibrary.dat: Illegal seek for GPU arch: gfx1031
```
...and hung or exited.

**Root-cause assessment**: In this ROCm 7.2.1 container, rocBLAS reported that the packaged Tensile library did not contain a usable entry for the detected `gfx1031` target.

The binary was compiled for gfx1031, the runtime found gfx1031 hardware, but then rocBLAS couldn't find matching Tensile kernels.

**Fix**: Override the GPU version that ROCm reports to itself:

```yaml
environment:
  - HSA_OVERRIDE_GFX_VERSION=10.3.0   # gfx1031 → pretend to be gfx1030
```

`10.3.0` makes the runtime report a `gfx1030` target. This compatibility override worked on the documented RX 6750 XT setup, but it is an unsupported workaround rather than a general guarantee. It should be retested after ROCm, driver, image, or hardware changes.

### Error 5: Healthcheck Timeout

**Symptom**: AnythingLLM refused to start because `llama-server` wasn't passing its healthcheck. The healthcheck was set to `start-period=60s`, but llama-server was taking longer than that to initialize.

**Root cause**: The default `start-period` was too short. llama.cpp's warmup phase (loading weights, initializing GPU buffers) can take 2-3 minutes on first launch, especially when 37 model layers are being transferred to GPU memory.

**Fix**: Two changes — increase the healthcheck start period and disable llama-server's warmup pass:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=180s \
    CMD curl -f http://localhost:8080/health || exit 1
```

```
CMD ["--no-warmup", ...]
```

`--no-warmup` skips the initial inference pass that llama.cpp runs at startup. The model loads faster, the healthcheck passes within 180 seconds, and AnythingLLM connects.

## The Moment It Worked

After fix five, the sequence looked like this:

```
bonsai-llama    | ggml_cuda_init: GGML_CUDA_FORCE_MMQ:   no
bonsai-llama    | ggml_cuda_init: GGML_CUDA_FORCE_CUBLAS: no
bonsai-llama    | ggml_cuda_init: found 1 ROCm devices
bonsai-llama    | Device 0: AMD Radeon RX 6750 XT, vram: 12282 MiB
bonsai-llama    | llm_load_tensors: offloading 37 repeating layers to GPU
bonsai-llama    | llm_load_tensors: offloaded 37/37 layers to GPU
bonsai-llama    | llm_load_tensors:        ROCm0 buffer size =  1016.00 MiB
bonsai-llama    | llm_load_tensors:   ROCm0 KV buffer size =  1152.00 MiB
bonsai-llama    | server listening at http://0.0.0.0:8080
```

37 out of 37 layers on GPU. 1016 MiB for the model, 1152 MiB for the KV cache. Total GPU usage for a full 8B parameter model: under 2.2 GiB out of 12 GiB available.

The first observed run reported:

```
prompt eval: 147 tokens/sec
generation:  108 tokens/sec
```

The server reported 108 tokens per second generation on this RX 6750 XT setup.

My reaction, after all that was : *"It is alive!!"*

## Honest Model Evaluation

108 tokens per second creates a certain enthusiasm. It's worth grounding that with an honest capability assessment.

### What Bonsai-8B Does Well

**Language and reasoning tasks** are strong. The model explains concepts clearly, maintains context across a conversation, and writes grammatically correct output in both German and English. When asked to reflect on the philosophical implications of 1-bit quantization — whether something is lost when a weight can only be -1, 0, or +1 — it produced a thoughtful, multi-paragraph response about the nature of information compression and the difference between precision and meaning.

**RAG document analysis** was promising in a small qualitative test. We uploaded a 15-page German business document on AI readiness for SMEs. The model produced a useful summary, extracted recommendations, and identified the intended audience without additional prompt engineering. This was a single author assessment, not a blinded comparison against human analysts.

### Where It Struggles

**Arithmetic** is unreliable. We tested with a lateral thinking question: a man leaves shirts out to dry, some dry in 1 hour, some take longer depending on placement. How long does everything take to dry?

The model calculated **3.33 hours**. The correct answer requires noticing that all items dry simultaneously (it's a lateral thinking trick, not a calculation problem). A standard reasoning chain would catch this. Bonsai-8B did not.

One failed lateral-thinking prompt does not establish a general arithmetic limitation or its cause. The result is recorded as a local observation; a defensible capability claim would require a repeatable evaluation set and comparison models.

### A Context-Contamination Hypothesis

This was the most interesting discovery of the evaluation.

We tested a multi-step math puzzle in a chat thread that had already covered several other topics. The model gave a wrong answer. We then opened a **fresh chat thread** and asked the same question. The model answered correctly.

Same model. Same weights. Different context window history.

One plausible hypothesis is that previous turns changed the effective task and attention context. The observation does not isolate causality: sampling variation, chat templates, and frontend behavior could also contribute.

Practical recommendation: **prefer fresh contexts for independent analytical tasks**, then evaluate whether this improves results on a repeatable task set. For conversational tasks, continuity may be part of the requirement.

**Verdict from this test**: Bonsai-8B was deployable on the documented consumer hardware and useful for selected language and document tasks. The test does not establish that it was the first production 1-bit model, that its quality generalizes, or that arithmetic weakness is inherent to the format. It is better understood as a fast local model with unusually low parameter memory and task-dependent capability.

## The Docker Setup Used for This Test

> **Reproducibility boundary:** The historical setup below used mutable container tags, an unpinned Git branch, and a model download without a recorded checksum. It documents the successful path but is not bit-for-bit reproducible. A production reuse should pin the ROCm image digest, PrismML fork commit, model revision, and SHA-256 checksum.

The complete setup lives in three files:

**`Dockerfile`** — builds PrismML's llama.cpp fork with ROCm:
```dockerfile
FROM rocm/dev-ubuntu-22.04:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git cmake build-essential curl wget \
    hipblas-dev rocblas-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
RUN git clone https://github.com/PrismML-Eng/llama.cpp.git --depth=1
WORKDIR /app/llama.cpp
RUN cmake -B build \
    -DGGML_HIP=ON \
    -DAMDGPU_TARGETS="gfx1031;gfx1030" \
    -DLLAMA_BUILD_TESTS=OFF \
    -DLLAMA_BUILD_EXAMPLES=OFF \
    && cmake --build build --config Release --target llama-server -j$(nproc)
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=10s --start-period=180s \
    CMD curl -f http://localhost:8080/health || exit 1
ENTRYPOINT ["/app/llama.cpp/build/bin/llama-server"]
CMD ["-m", "/models/Bonsai-8B.gguf", "--host", "0.0.0.0", \
     "--port", "8080", "-c", "8192", "-ngl", "99", \
     "--no-warmup", "--temp", "0.6", "--top-k", "30", "--top-p", "0.9"]
```

**`docker-compose.yml`** — wires llama-server and AnythingLLM together:
```yaml
services:
  llama-server:
    build: .
    image: bonsai-llama-server-rocm
    container_name: bonsai-llama
    volumes:
      - ./models:/models:ro
    ports:
      - "127.0.0.1:8080:8080"
    devices:
      - /dev/kfd:/dev/kfd
      - /dev/dri:/dev/dri
    group_add:
      - video
      - render
    environment:
      - HSA_OVERRIDE_GFX_VERSION=10.3.0
    restart: unless-stopped
  anythingllm:
    image: mintplexlabs/anythingllm
    container_name: bonsai-anythingllm
    # Historical workaround used user: "0:0". Prefer a volume owned by
    # the image's documented runtime UID instead of running as root.
    volumes:
      - ./anythingllm-storage:/app/server/storage
    ports:
      - "127.0.0.1:3001:3001"
    environment:
      - STORAGE_DIR=/app/server/storage
      - LLM_PROVIDER=generic-openai
      - GENERIC_OPEN_AI_BASE_PATH=http://llama-server:8080/v1
      - GENERIC_OPEN_AI_MODEL_PREF=bonsai-8b
      - GENERIC_OPEN_AI_MODEL_TOKEN_LIMIT=8192
      - GENERIC_OPEN_AI_API_KEY=not-needed
    depends_on:
      llama-server:
        condition: service_healthy
    restart: unless-stopped
```

**`download_model.sh`** — fetches the GGUF with resume support:
```bash
wget -c "https://huggingface.co/prism-ml/Bonsai-8B-gguf/resolve/main/Bonsai-8B.gguf" \
     -O ./models/Bonsai-8B.gguf --progress=bar:force 2>&1
```

Run sequence:
```bash
./download_model.sh
docker compose up --build
# → AnythingLLM at http://localhost:3001
```

## Credit Where It's Due

The BitNet b1.58 research showed that 1-bit training was theoretically possible. PrismML turned that into Bonsai: a real model, a real quantization format, a real llama.cpp fork with working HIP kernels. The gap between "interesting paper" and "running on your GPU in a Docker container" is substantial, and they bridged it.

The `HSA_OVERRIDE_GFX_VERSION=10.3.0` trick, the dual `gfx1031;gfx1030` build target, the `hipblas-dev` dependency that the base image omits — none of these are documented anywhere in a single place. They're scattered across GitHub issues, ROCm forums, and AMD hardware compatibility tables. Debugging them required understanding the GPU stack from the driver level (HSA) through the compute library (rocBLAS/Tensile) to the build system (cmake -DAMDGPU_TARGETS).

That debugging is the actual work. The Dockerfile is only 42 lines. The knowledge that makes those 42 lines correct took considerably longer to acquire.

## Reflections

### On 1-Bit as a Category Shift

There's a meaningful difference between a 4-bit quantized model and a 1-bit model. Both are compressed. But a 4-bit model is still fundamentally a reduced-precision floating point representation — the original weight structure is intact, just approximated. A 1-bit model trained natively is something else: a sparse, ternary weight matrix where each parameter encodes a direction (-1/+1) or silence (0). It's closer to a binary decision tree than to a neural network in the classical sense.

Whether this architectural difference matters for capability — beyond the currently observed arithmetic weakness — remains an open research question. The fact that 1-bit models work at all for language tasks is still surprising if you think about it carefully.

### On the GPU as Infrastructure

In this run, the server reported 108 tokens per second from a 12 GB consumer GPU with about 1 GB of parameter memory, served through an OpenAI-compatible HTTP API with a local RAG frontend. After images and model files were downloaded, inference could run without a cloud-model API. Loopback binding and local authentication still matter even in that configuration.

The same class of experiment has become much more accessible on consumer hardware. The short Compose file hides the time spent resolving driver, kernel, model-format, and container-integration details.

The infrastructure story of local AI is not “it is as good as the cloud” at the top end. The local observation is narrower: a model with about 1 GB of parameter memory produced useful language and document output at high reported throughput on this system. That is enough to justify further controlled evaluation without turning one run into a universal benchmark.

### On Context Contamination as Design Information

The fresh-thread observation is not yet a general finding. It is a useful hypothesis for workflow design and evaluation.

For batch analysis tasks (processing documents, answering independent questions), each task should get a fresh context window. For conversational tasks where continuity is the feature, the accumulated context is doing useful work.

Most chat UIs default to one long thread. For analytical work, that's the wrong default. This is worth building into workflow design explicitly.

---

*Credit and gratitude: the Bonsai models and Q1_0_g128 quantization format are the work of PrismML. The underlying 1.5-bit research originates from Microsoft Research's BitNet b1.58 paper. This chapter documents the deployment process, not any original model work.*

---

*Published as part of the [Lyttek AI Journey](https://github.com/GLyttek/lyttek-ai-journey)*
