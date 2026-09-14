# Clone and build `llama-server` for this GPU (Metal or CUDA)

Parent: GitHub [#76](https://github.com/asimov-agent/llama-ai/issues/76) (umbrella).
Implements: [#78](https://github.com/asimov-agent/llama-ai/issues/78).

Not in scope: which GGUFs `--download-top-tier` picks ([#77](https://github.com/asimov-agent/llama-ai/issues/77)).

## Why

llama-ai only **finds** `llama-server`. The error hint is always Metal. NVIDIA boxes are told the wrong cmake. Source is never cloned. CI CPU is not a Metal or CUDA proof.

## What Changes

- Detect **Apple Silicon** (`darwin` + `arm64`/`aarch64`) → Metal.
- Detect **NVIDIA** (`nvidia-smi` lists a GPU) → CUDA.
- Neither → fail closed (no CPU fallback, no Metal-on-NVIDIA, no CUDA-on-Mac).
- If binary already resolvable → do not clone/cmake.
- Else clone `https://github.com/ggml-org/llama.cpp.git` to `$HOME/repository/git/llama.cpp` (or `LLAMA_CPP_SRC`).
- Metal: `cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_METAL=ON -DGGML_CUDA=OFF`
- CUDA: requires `nvcc`; then `cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON -DGGML_METAL=OFF`
- Build `--target llama-server`, symlink `~/bin/llama-server`.
- Call from `make install` and first **serve**, never from `--download-top-tier`.

## Capabilities

### New Capabilities
- `llama-server-host-build`: detect GPU, clone, cmake, symlink.

### Modified Capabilities
- None required for download.

## Impact

- `scripts/ensure_llama_server.py` (new)
- `Makefile` `link`/`install`
- `scripts/llama_serve.py` serve path calls ensure before `build_command`
- hermetic tests for cmake argv per host
