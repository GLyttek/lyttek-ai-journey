# 12. One Bit to Rule Them All: Running the World's Most Efficient LLM Locally

*April 2026 — AMD ROCm, Docker, proprietary quantization, and 108 tokens per second from a 1-gigabyte model*

---

## The Paper That Started It

In early 2024, a research paper made the rounds that felt almost too good to be true: 1-bit Large Language Models. The idea was to reduce transformer weights not to 8-bit integers, not to 4-bit integers, but to a single bit — values of -1, 0, or +1. The BitNet b1.58 paper from Microsoft Research showed that a transformer trained from scratch at 1.58 bits per weight could match full-precision models at equivalent parameter counts, while requiring dramatically less memory and compute.

The AI community was divided. Skeptics pointed out that the models had to be trained natively in 1-bit — you couldn't quantize an existing model down to 1 bit without catastrophic quality loss. True. But the training-time efficiency gains were real, and the inference-time implications were staggering: a 1-bit model would fit in less than 20% of the memory required for its FP16 equivalent.

For a while, this remained an academic curiosity. There were no production-grade 1-bit models you could actually run.

Then PrismML shipped Bonsai.

## PrismML and the Q1_0_g128 Format

PrismML is a small company that took the 1.5-bit research and turned it into deployable models. Their Bonsai series runs on a custom quantization format called `Q1_0_g128`:

- Every 128 weights share a single FP16 scale factor
- The weights themselves are stored as 1-bit values
- Result: **1.125 bits per weight average**, with the scale factors providing just enough precision for coherent outputs

Bonsai-8B — an 8.19 billion parameter model based on the Qwen3 architecture — compresses to **1.07 GiB**. For comparison, the same model in standard 4-bit quantization (Q4_K_M) would be roughly 5 GiB. In FP16, about 16 GiB.

One gigabyte. For an 8B parameter model.

The catch: Q1_0_g128 is proprietary. It's not supported by the standard Ollama distribution, not in the mainline llama.cpp, and not in any off-the-shelf inference runtime. PrismML maintains their own llama.cpp fork with custom dequantization kernels for this format. To run Bonsai locally, you have to build from that fork.

## Why Not Just Use Ollama

The first instinct was to download the GGUF from HuggingFace and pull it into Ollama. This fails silently.

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

**Root cause**: The `anythingllm-storage/` directory was created by the host as root (because docker-compose runs as root by default). The AnythingLLM container process ran as a non-root user and couldn't write to a root-owned directory.

**Fix**: Add `user: "0:0"` to the anythingllm service in docker-compose. The container runs as root, which eliminates the permission mismatch.

```yaml
anythingllm:
  image: mintplexlabs/anythingllm
  user: "0:0"    # run as root to avoid volume permission issues
```

Not elegant, but it works. AnythingLLM's storage is local-only anyway.

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

**Root cause**: The initial Dockerfile built with `-DAMDGPU_TARGETS=gfx1030`. The RX 6750 XT (Navi 22) is actually `gfx1031`. A binary compiled only for gfx1030 executing on a gfx1031 GPU encounters undefined instruction behavior — which manifests as a segfault.

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

**Root cause**: ROCm 7.2.1 ships with a TensileLibrary (pre-compiled matrix multiplication kernels for rocBLAS) that only contains kernels for certain GPU architectures. The RX 6750 XT's `gfx1031` arch is absent — ROCm's Tensile kernel set covers `gfx1030` (RX 6700/6800 series) but not `gfx1031` specifically.

The binary was compiled for gfx1031, the runtime found gfx1031 hardware, but then rocBLAS couldn't find matching Tensile kernels.

**Fix**: Override the GPU version that ROCm reports to itself:

```yaml
environment:
  - HSA_OVERRIDE_GFX_VERSION=10.3.0   # gfx1031 → pretend to be gfx1030
```

`10.3.0` corresponds to `gfx1030`. This tells the ROCm runtime to use gfx1030's Tensile kernels on gfx1031 hardware. The architectures are nearly identical (both Navi 22 family) — the compute compatibility is real, not a hack.

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

The first benchmark came back:

```
prompt eval: 147 tokens/sec
generation:  108 tokens/sec
```

108 tokens per second generation. On a mid-range consumer GPU, from a 1-gigabyte model.

My reaction, after all that was : *"It is alive!!"*

## Honest Model Evaluation

108 tokens per second creates a certain enthusiasm. It's worth grounding that with an honest capability assessment.

### What Bonsai-8B Does Well

**Language and reasoning tasks** are strong. The model explains concepts clearly, maintains context across a conversation, and writes grammatically correct output in both German and English. When asked to reflect on the philosophical implications of 1-bit quantization — whether something is lost when a weight can only be -1, 0, or +1 — it produced a thoughtful, multi-paragraph response about the nature of information compression and the difference between precision and meaning.

**RAG document analysis** was genuinely impressive. We uploaded a 15-page German business document on AI readiness for SMEs. The model summarized the document accurately, extracted the key recommendations, and identified the target audience — all without any prompt engineering. The summary was indistinguishable from what a capable analyst would produce.

### Where It Struggles

**Arithmetic** is unreliable. We tested with a lateral thinking question: a man leaves shirts out to dry, some dry in 1 hour, some take longer depending on placement. How long does everything take to dry?

The model calculated **3.33 hours**. The correct answer requires noticing that all items dry simultaneously (it's a lateral thinking trick, not a calculation problem). A standard reasoning chain would catch this. Bonsai-8B did not.

It's worth noting: arithmetic was a known weakness of the original BitNet b1.58 research. Single-bit weights appear to capture language patterns and relational reasoning well, but struggle with the precise numerical representations that arithmetic requires.

### The Context Contamination Effect

This was the most interesting discovery of the evaluation.

We tested a multi-step math puzzle in a chat thread that had already covered several other topics. The model gave a wrong answer. We then opened a **fresh chat thread** and asked the same question. The model answered correctly.

Same model. Same weights. Different context window history.

The hypothesis: previous turns in the conversation introduce noise that competes with the current question during attention computation. The model isn't "confused" — it's responding to a much larger input than you intend when you ask a question in a loaded thread. Clean context produces cleaner reasoning.

Practical implication: **for analytical tasks, use fresh threads**. For conversational tasks where context is the point, the effect is less pronounced. This mirrors a known pattern in cloud LLM usage but becomes more visible when you can measure it directly against a fixed local model.

**Verdict**: Bonsai-8B is the first genuinely deployable 1-bit model. It's excellent at language tasks, solid at document analysis, and weak at arithmetic. For a model that fits in 1 GiB and runs at 108 tok/s on a mid-range GPU, those tradeoffs are entirely reasonable. It's not a replacement for Chat GPT or Claude. It's a new category: a **fast, private, local model for language-intensive tasks** that runs on hardware most people already own.

## The Docker Setup (Reproducible)

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
      - "8080:8080"
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
    user: "0:0"
    volumes:
      - ./anythingllm-storage:/app/server/storage
    ports:
      - "3001:3001"
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

108 tokens per second from a 12 GB consumer GPU running a 1 GB model, served via an OpenAI-compatible HTTP API, with RAG on top. The entire stack — GPU, driver, ROCm runtime, compiled inference engine, HTTP server, vector database, chat UI — is running on a single machine, offline, with no API costs.

Three years ago this would have required a data center. Today it's a docker-compose file and a weekend afternoon.

The infrastructure story of local AI isn't "it's as good as the cloud" — it isn't, at the top end. The story is: **the floor has risen dramatically**. A 1 GB model doing 108 tok/s with solid language reasoning and RAG is a floor, not a ceiling.

### On Context Contamination as Design Information

The context contamination finding — fresh thread produces better reasoning — isn't a bug to fix. It's information about how to design workflows around LLMs.

For batch analysis tasks (processing documents, answering independent questions), each task should get a fresh context window. For conversational tasks where continuity is the feature, the accumulated context is doing useful work.

Most chat UIs default to one long thread. For analytical work, that's the wrong default. This is worth building into workflow design explicitly.

---

*Credit and gratitude: the Bonsai models and Q1_0_g128 quantization format are the work of PrismML. The underlying 1.5-bit research originates from Microsoft Research's BitNet b1.58 paper. This chapter documents the deployment process, not any original model work.*

---

*Published as part of the [Lyttek AI Journey](https://github.com/GLyttek/lyttek-ai-journey)*
