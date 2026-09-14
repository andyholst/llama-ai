# Tasks: clone+build llama-server for this GPU (#78)

- [x] 1. OpenSpec + issue #78 in sync; parent #76 linked.
- [x] 2. `scripts/ensure_llama_server.py`: detect metal vs cuda vs neither; clone URL/path; exact cmake; symlink; no rebuild if resolvable.
- [x] 3. `make install`/`link` and serve path call ensure; `--download-top-tier` does not.
- [x] 4. Tests: Darwin-arm64 → Metal flags not CUDA; nvidia-smi → CUDA flags not Metal; neither → fail, no cmake; binary present → no cmake; dry download → no clone/cmake; cmake fail → non-zero no hosted URL.
- [x] 5. README two-host table.
- [x] 6. `make openspec-validate NAME=feat-clone-build-llama-server-for-host-gpu` green.
