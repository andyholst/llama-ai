# Rename llama-ai to llgenie

## Why

The project is rebranded from `llama-ai` to **`llgenie`** — a short, distinctive name that captures the tool's value: auto-discover the trending GGUF that fits the local card and feed it to the compiled `llama-server`. `llama-ai` was too close to Meta's "Llama" branding and did not convey the smart, hardware-aware selection. This change renames the **user-facing brand** across the launcher, CLI docs, image tags, watch-loop paths, and the live GitHub repo slugs (both the upstream `asimov-agent/llgenie` and the fork `andyholst/llgenie` are now renamed on GitHub; GitHub auto-redirects the old names), without touching upstream `llama.cpp` / `llama-server` names.

## What Changes

- **Launcher + symlinks**: `make install` writes `~/bin/llgenie` (was `llama-ai`) and symlinks `~/bin/llgenie.py` (was `llama_ai.py`) to the repo launcher `scripts/llama_serve.py`; `make uninstall` removes them. The launcher content's self-comment and error hints use the new name.
- **Container image tags**: `llama-ai/test` → `llgenie/test`, `llama-ai/openspec` → `llgenie/openspec` (local builds only; nothing is pushed to a registry).
- **Watch-loop paths**: the worktree base convention `../llama-ai-wt` → `../llgenie-wt` in `scripts/watchloop_dispatch.py`, `AGENTS.md`, and the dispatch tests/fixture, kept in lock-step.
- **User-facing strings**: README, AGENTS.md, agent-wiki, CLI `--help`/error text, and the HF `User-Agent` header use `llgenie`.
- **OpenSpec docs**: every existing `openspec/changes/**` file references the project name as `llama-ai`/`llama_ai.py`; those are updated to the new brand.

## Capabilities

- **llgenie-brand**: the user-facing launcher, install/uninstall artifacts, image tags, and documentation consistently use `llgenie`.
- **llama-served-unchanged**: the served binary and upstream deps are untouched; the internal launcher module stays at `scripts/llama_serve.py`.

## Impact

No change to downstream consumers of the GGUF download or serve pipeline; the served command, flags, and API contract are unchanged. Only the project brand and the install paths change. The live GitHub repo slugs used by the loop's API URLs (`asimov-agent/llama-ai` → `asimov-agent/llgenie`, fork `andyholst/llama-ai` → `andyholst/llgenie`) are now renamed on GitHub and GitHub auto-redirects the old names, so the API constants point at the new `llgenie` slugs.
