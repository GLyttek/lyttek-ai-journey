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

PrismML published a Bonsai model and inference implementation using a custom, non-mainline format called `Q1_0_g128`:

- Every 128 weights share a single FP16 scale factor
- Each binary weight selects `-scale` or `+scale`
- Result: **1.125 bits per weight average**, counting one sign bit plus the shared scale metadata

External references: [Bonsai-8B model card](https://huggingface.co/prism-ml/Bonsai-8B-gguf) and [PrismML llama.cpp fork](https://github.com/PrismML-Eng/llama.cpp).

Bonsai-8B uses a Qwen3 architecture and has 8.19 billion parameters. Its model card reports **1.15 GB** of parameter memory, a **1.16 GB** GGUF file, and **16.38 GB** for the FP16 comparison.

That parameter-memory figure was the practical reason I wanted to test the deployment.

At the time of this deployment, Q1_0_g128 was not supported by the standard Ollama distribution or mainline llama.cpp. PrismML published a custom llama.cpp fork with the required kernels. “Custom” is the important distinction here; the public model and fork carry open-source licenses, so the original description of the whole stack as proprietary was too broad.

## Why Not Just Use Ollama

The first instinct was to download the GGUF from Hugging Face and pull it into Ollama. In this historical test, the import path created a model entry, but prompting produced unusable output or no output. The retained evidence did not isolate whether the failure occurred during import, format handling, or inference.

The support boundary is the defensible explanation: `Q1_0_g128` required PrismML's custom kernels and was not supported by the standard Ollama distribution or mainline llama.cpp used in this test. I should not infer a specific silent weight-layout failure from the user-visible symptom alone.

The path that worked in this test was: PrismML's llama.cpp fork → compiled with GPU support → serving via `llama-server` → an OpenAI-compatible frontend. I used AnythingLLM because it supported a generic OpenAI endpoint, included RAG features, and ran as a Docker container.

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

## The Observed Working Run

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

My reaction, after all that, was: *"It is alive!!"*

## Small Qualitative Evaluation

The throughput result was useful, but it did not measure model quality. The following observations came from a small number of prompts and one uploaded document, without a comparison set or blinded review.

### Language output in the prompts I tried

The model produced clear German and English prose in the prompts I tried. In one discussion about low-bit compression, it returned a coherent multi-paragraph response. That shows the model could generate useful language in that interaction; it does not establish general reasoning ability or stable long-context behavior.

**RAG document analysis** was useful in one small qualitative test. I uploaded a 15-page German business document on AI readiness for SMEs. The model produced a summary, extracted recommendations, and identified the intended audience without additional prompt engineering. This was one author's assessment, not a blinded comparison against human analysts or other models.

### One reasoning failure

I tested a lateral-thinking question: a man leaves shirts out to dry, some dry in one hour, and the question asks how long everything takes to dry.

The model calculated **3.33 hours**. The expected answer treats the items as drying simultaneously; Bonsai-8B did not reach that answer in this prompt.

One failed lateral-thinking prompt does not establish a general arithmetic or reasoning limitation, and the prompt is not an arithmetic benchmark. A defensible capability claim would require a repeatable evaluation set and comparison models.

### Context history as a possible variable

This observation made context history a variable for a future test.

I tested a multi-step math puzzle in a chat thread that had already covered several other topics. The model gave a wrong answer. I then opened a **fresh chat thread** and asked the same question. The model answered correctly.

The model and weights were unchanged; the context-window history differed.

One plausible hypothesis is that previous turns changed the effective task and attention context. The observation does not isolate causality: sampling variation, chat templates, and frontend behavior could also contribute.

This is a reason to control context history in a repeatable evaluation, not a workflow rule derived from two prompts.

**Verdict from this test**: Bonsai-8B was deployable on the documented consumer hardware and produced useful output in selected language and document prompts. The test does not establish that it was the first production 1-bit model, that its quality generalizes, or that the observed reasoning failure is inherent to the format. It is a local deployment result with unusually low reported parameter memory and a quality question that still needs controlled evaluation.

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

The BitNet b1.58 paper documented a ternary low-bit training approach. PrismML later published Bonsai with a different binary sign-plus-scale format and a llama.cpp fork with HIP kernels. This chapter records that their public artifacts produced a working local deployment on the documented machine; it does not claim that Bonsai is an implementation of BitNet b1.58.

I did not find one source that covered the `HSA_OVERRIDE_GFX_VERSION=10.3.0` workaround, the dual `gfx1031;gfx1030` build target, and the `hipblas-dev` dependency together. I assembled the path from the observed errors and separate ROCm, build, and community references. The result should therefore be treated as a dated compatibility receipt, not a general AMD deployment recipe.

That debugging is the actual work. The Dockerfile is only 42 lines. The knowledge that makes those 42 lines correct took considerably longer to acquire.

## Reflections

### Distinguishing BitNet, Bonsai, and 4-bit quantization

BitNet b1.58 uses ternary weights `{-1, 0, 1}`. The Bonsai model card instead describes binary sign choices with one FP16 scale shared by each group of 128 weights, yielding 1.125 effective bits per weight. Common 4-bit formats encode a larger set of quantized values plus scaling metadata. These are different numerical representations and kernel requirements.

None of them changes the model into a decision tree. Bonsai remains a neural Transformer model. This deployment also cannot attribute a capability difference to bit width because it did not compare matched models, training runs, or quantizations.

### On the GPU as Infrastructure

In this run, the server reported 108 tokens per second from a 12 GB consumer GPU with about 1 GB of parameter memory, served through an OpenAI-compatible HTTP API with a local RAG frontend. After images and model files were downloaded, inference could run without a cloud-model API. Loopback binding and local authentication still matter even in that configuration.

This setup made the experiment possible on the documented consumer hardware. The short Compose file hides the time spent resolving driver, kernel, model-format, and container-integration details.

This experiment did not compare the local setup with leading cloud models. It showed that a model with about 1 GB of parameter memory produced useful language and document output at the reported throughput on this system. That result justifies further controlled evaluation, not a universal benchmark claim.

### Testing context history

The fresh-thread observation is not yet a general finding. It is a useful hypothesis for workflow design and evaluation.

For a future batch evaluation, I would start each independent case in a fresh context and compare that condition with accumulated conversation history. Conversational tasks need a separate condition because continuity may be part of the requirement.

The two prompts observed here do not prove that long chat threads are generally the wrong default. They identify context history as a variable that the next evaluation should control.

---

*Credit and gratitude: the Bonsai models and Q1_0_g128 quantization format are the work of PrismML. The BitNet b1.58 paper referenced here was published by Microsoft Research authors. This chapter documents the deployment process, not any original model work.*

---

*Published as part of the [Lyttek AI Journey](https://github.com/GLyttek/lyttek-ai-journey)*
