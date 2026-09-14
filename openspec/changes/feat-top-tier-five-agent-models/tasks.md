# Tasks: five agent GGUFs that fit (#76 / #77)

- [x] 1. OpenSpec + issue #76/#77 in sync (this change).
- [x] 2. `is_agent_gguf(repo, filename)` — word-boundary `instruct`|`coder`|`tool`.
- [x] 3. `discover_top_tier`: agent filter after fit gate; refill; `--count` = file cap.
- [x] 4. `_main_download_top_tier`: pass `limit=count` (not count×per_provider); print agent-file readout; no llama-server.
- [x] 5. Tests: mix instruct/coder vs base/IQ2/mmproj; 2-of-5 honest; dry run no server; update old provider×quant tests.
- [x] 6. README: five agent files; download ≠ serve.
- [x] 7. `make openspec-validate NAME=feat-top-tier-five-agent-models` green.
