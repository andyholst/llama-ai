# Spec: llama-server clone and build for this GPU

## ADDED Requirements

### Requirement: Detect Apple Silicon vs NVIDIA, fail if neither
WHEN ensuring `llama-server` and no binary is already resolvable
THEN the host is classified as:
- **metal** if `sys.platform == "darwin"` and `os.uname().machine` is `arm64` or `aarch64`
- **cuda** if `nvidia-smi` runs successfully and lists a GPU
- otherwise **cpu** — cmake with Metal off and CUDA off (no opposite GPU)

#### Scenario: Darwin arm64 is Metal
GIVEN platform darwin and machine arm64
WHEN detect runs
THEN gpu is `metal`

#### Scenario: nvidia-smi success is CUDA
GIVEN nvidia-smi exits 0 with a GPU name
WHEN detect runs
THEN gpu is `cuda`

#### Scenario: neither GPU builds CPU
GIVEN linux without nvidia-smi
WHEN ensure runs and no binary exists
THEN cmake contains `-DGGML_METAL=OFF` and `-DGGML_CUDA=OFF`

### Requirement: Clone llama.cpp then cmake for that GPU
WHEN the binary is missing and a GPU class is known
THEN source is `git clone --depth 1 https://github.com/ggml-org/llama.cpp.git` into
`$HOME/repository/git/llama.cpp` (or `LLAMA_CPP_SRC`) if the directory is missing.
THEN cmake is **exactly**:
- metal: `-DCMAKE_BUILD_TYPE=Release -DGGML_METAL=ON -DGGML_CUDA=OFF`
- cuda: `-DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON -DGGML_METAL=OFF` and `nvcc` must exist or fail closed (NVIDIA present, toolkit missing — not a CPU machine)
- cpu: `-DCMAKE_BUILD_TYPE=Release -DGGML_METAL=OFF -DGGML_CUDA=OFF`
THEN `cmake --build build --config Release --target llama-server` and symlink `~/bin/llama-server`.
WHEN a resolvable `llama-server` already exists
THEN clone and cmake MUST NOT run.

#### Scenario: Metal cmake flags
GIVEN Apple Silicon and missing binary
WHEN ensure builds
THEN cmake argv contains `-DGGML_METAL=ON` and `-DGGML_CUDA=OFF`

#### Scenario: CUDA cmake flags
GIVEN NVIDIA and missing binary and nvcc present
WHEN ensure builds
THEN cmake argv contains `-DGGML_CUDA=ON` and `-DGGML_METAL=OFF`

#### Scenario: Existing binary skips build
GIVEN `~/bin/llama-server` is executable
WHEN ensure runs
THEN cmake is not invoked

### Requirement: Download-top-tier never builds llama.cpp
WHEN `llama-ai --download-top-tier` (including `--dry`) runs
THEN it MUST NOT clone llama.cpp or invoke cmake.

#### Scenario: Dry top-tier does not compile
GIVEN `--download-top-tier --dry`
WHEN the CLI runs
THEN ensure/clone/cmake are not invoked
