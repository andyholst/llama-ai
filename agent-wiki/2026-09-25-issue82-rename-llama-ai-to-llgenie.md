# 2026-09-25 — issue #82: rename llama-ai → llgenie

## What
Global brand rename of the project from `llama-ai` to `llgenie` across the
launcher, install/uninstall flow, container image tags, watch-loop paths,
docs, OpenSpec specs, and the live GitHub repo slugs.

## Branch / PR
- Branch: `feat/rename-llama-ai-to-llgenie`
- Pushed to: `origin` (andyholst/llgenie)
- PR: [#83](https://github.com/asimov-agent/llgenie/pull/83) against `upstream`
  (`asimov-agent/llgenie`), mergeable, references issue #82
- OpenSpec change: `feat-rename-llama-ai-to-llgenie` (proposal + specs + tasks),
  all tasks ticked, `make openspec-validate` green.

## GitHub repos renamed
- Upstream `asimov-agent/llama-ai` → `asimov-agent/llgenie`.
- Fork `andyholst/llama-ai` → `andyholst/llgenie`.
- Old URLs auto-redirect. Loop API constants (API in
  `scripts/watchloop_dispatch.py`, the Contents-API probe URLs in
  `scripts/load_token_to_env.sh` ×3), the `.env.example` token comment, the
  `README.md` issue link, and the local git remotes (`origin`/`upstream`) all
  now point at the new `llgenie` slugs.

## What changed (verified)
- Launcher: `~/bin/llama-ai` → `~/bin/llgenie`, `~/bin/llama_ai.py` →
  `~/bin/llgenie.py` (Makefile `LAUNCHER`/`link:`/`uninstall:` + launcher
  self-text + error hints).
- Docker image tags: `llama-ai/test` → `llgenie/test`,
  `llama-ai/openspec` → `llgenie/openspec` (local builds only — nothing is
  pushed to a registry).
- Watch-loop worktree base: `../llama-ai-wt` → `../llgenie-wt` in
  `scripts/watchloop_dispatch.py`, `AGENTS.md`, `tests/test_watchloop_dispatch.py`,
  the e2e dispatch test, and `tests/fixtures/fake-crontab.sh`.
- User-facing strings: README, AGENTS.md, agent-wiki, CLI help/error, HF
  `User-Agent` (`llama-ai/1.0` → `llgenie/1.0`).
- Existing `openspec/changes/**` specs/proposals/tasks updated.
- `tests/test_install.py` / `test_health.py` / `conftest.py` now assert
  `~/bin/llgenie`.

## Deliberately NOT renamed (verified intact)
- Upstream `llama-server` / `llama.cpp` names.
- Internal launcher module `scripts/llama_serve.py` (path unchanged).
- Test file `tests/test_llama_ai.py` and its `as llama_ai` test aliases.

## Gates (all GREEN)
- `make lint` — LINT OK.
- `make test-unit` — 186 passed.
- `make test-install-ci` — 7 passed (real `make install` produced
  `~/bin/llgenie`, seeded the model, smoke `--list` ran, new-name assertions
  green).
- `make openspec-validate NAME=feat-rename-llama-ai-to-llgenie` — valid.
- No remaining `llama-ai` / `llama_ai.py` in user-facing strings beyond the
  deliberately-preserved items above (verified with `grep`).

## Status
PR #83 open and mergeable (APPROVED, CI green). GitHub repos renamed to `llgenie`.
Issue #82 to be closed when the PR merges.
