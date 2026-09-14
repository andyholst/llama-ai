# `--download-top-tier` stocks five agent GGUFs that fit (download-only)

Parent: GitHub [#76](https://github.com/asimov-agent/llama-ai/issues/76).
Implements: [#77](https://github.com/asimov-agent/llama-ai/issues/77).

Not in scope: compiling `llama-server` ([#78](https://github.com/asimov-agent/llama-ai/issues/78)).

## Why

Today `--count 5` means five Hugging Face **owners** × high+lower quants. Filters are trending + family + fit. Instruct/coder/tool is ignored, so the shelf is not five **agent** models that run here.

## What Changes

- `--count` (default 5) = **5 files**, not 5 providers.
- After the existing fit/junk gates, keep only **agent** GGUFs (`instruct` / `coder` / `tool` as word-boundary on repo id or filename). Skip and refill from the next owner.
- Do not pad with a non-agent lower quant.
- Exhausted list → honest `N/5`, never pad with non-agent files.
- `--download-top-tier` still **never** starts `llama-server`.
- One path: existing `discover_top_tier` → probe → `hf` CLI.

## Capabilities

### New Capabilities
- None (extends llama-ai-tooling).

### Modified Capabilities
- `llama-ai-tooling`: top-tier download is five **agent** files that fit.

## Impact

- `scripts/llama_serve.py` (`discover_top_tier`, `_main_download_top_tier`, `--count` help)
- tests that assumed 5 providers × 2 quants
- README `--download-top-tier` section
