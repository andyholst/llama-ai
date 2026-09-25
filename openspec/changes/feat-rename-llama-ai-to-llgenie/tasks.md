# feat-rename-llama-ai-to-llgenie

## Implementation tasks

- [x] 1.1 Rename user-facing launcher: `~/bin/llama-ai` → `~/bin/llgenie` and
      `~/bin/llama_ai.py` → `~/bin/llgenie.py` in `Makefile`
      (`LAUNCHER`, `link:`, `uninstall:`, and all echo/help strings).
- [x] 1.2 Rename the launcher's self-documenting content (the `link:` printf
      template): comment + error hint use `llgenie`, not `llama-ai`/`llama_ai.py`.
- [x] 1.3 Rename container image tags: `OS_IMG` (`llama-ai/openspec`) and
      `TEST_IMG` (`llama-ai/test`) → `llgenie/...` in `Makefile`, and the
      container prune `grep -q "llama-ai/test"` → `llgenie/test`; also
      `docker-compose-files/openspec.yaml` + `test.yaml` image refs.
- [x] 1.4 Rename the watch-loop worktree base convention `../llama-ai-wt` →
      `../llgenie-wt` in `scripts/watchloop_dispatch.py` (REPO/WORKTREE_BASE +
      all `wd` f-strings), `AGENTS.md` (worktree + crontab sections), and
      `tests/test_watchloop_dispatch.py` fixtures (path string), plus the
      fake-crontab default `llama-ai-fake-crontab` path.
- [x] 1.5 Update user-facing brand strings in `README.md`, `AGENTS.md`,
      `scripts/llama_serve.py` docstring/error hint, and `scripts/hf_download.py`
      `User-Agent` header (currently `llama-ai/{label}`).
- [x] 1.6 Update every existing `openspec/changes/**` file (proposal/spec/tasks)
      where the project brand appears as `llama-ai`/`llama_ai.py` so it reads
      `llgenie`/`llgenie.py` (keep the capability dir `llama-ai-tooling` intact).
- [x] 1.7 Update `tests/test_install.py` + `tests/test_health.py` to assert the
      new launcher path `~/bin/llgenie` (and tolerate the old `llama-ai`
      symlink on cleanup) — NOT the served `llama-server`.
- [x] 1.8 Update `agent-wiki/` dated entries for the new brand (historical
      entries may keep the old name for traceability — decision: update).
- [x] 1.9 Point all loop/API/token references at the renamed GitHub slugs:
      upstream `asimov-agent/llama-ai` → `asimov-agent/llgenie` and fork
      `andyholst/llama-ai` → `andyholst/llgenie` (admin rename; GitHub
      auto-redirects the old URLs). Updated `API` in `scripts/watchloop_dispatch.py`,
      the Contents-API probe URLs in `scripts/load_token_to_env.sh` (×3), the
      token comment in `.env.example`, the issue link in `README.md`, and the
      local remote URLs (`origin` → `andyholst/llgenie`, `upstream` →
      `asimov-agent/llgenie`).

## Explicitly NOT renamed (still remain after rename)

- [x] 2.1 `llama-server` (upstream llama.cpp binary name) everywhere, including
      `~/bin/llama-server` symlink and `LLAMA_SERVER` env var.
- [x] 2.2 `scripts/llama_serve.py` (internal launcher module path, stable).
- [x] 2.3 The internal test import alias `scripts.llama_serve as llama_ai` in
      `tests/test_llama_ai.py`/`test_top_tier_acceptance.py`/`test_top_tier_serve.py`
      /`conftest.py` (a Python variable name, not user-facing).

## Tests

- [x] 3.1 Add `tests/test_install.py` assertions that `~/bin/llgenie` is
      created/executable and `~/bin/llama_ai.py`/`~/bin/llama-ai` are gone,
      with a NO-SKIP guard (missing artifacts are a loud failure).
- [x] 3.2 Ensure `make test-install-ci` still performs a REAL `make install`
      and asserts the new `llgenie` launcher end-to-end in the container.

## Verification

- [x] 4.1 `make lint` green (every tracked text file ends in a newline).
- [x] 4.2 `make test-unit` green (containerized).
- [x] 4.3 `make test-install-ci` green (REAL install, no skips, new launcher name).
- [x] 4.4 `make lint-fix` not needed after edits (trailing newlines preserved).
- [x] 4.5 No remaining `llama-ai`/`llama_ai.py` in user-facing strings — verified
      with `grep -rn 'llama-ai|llama_ai\\.py' --exclude-dir=.git` returning only
      the deliberately-preserved items in "Explicitly NOT renamed".
- [x] 4.6 `make openspec-validate NAME=feat-rename-llama-ai-to-llgenie` exit 0.
- [x] 4.7 On a host with the gguf venv + a model: `make install` then
      `~/bin/llgenie --list` and `~/bin/llgenie --download-top-tier --dry` both
      work (local host proof).
- [x] 4.8 Commit (Conventional Commit `feat:`), push to `origin` (andyholst's
      repo), and open a cross-repo PR to `upstream` (`asimov-agent/llgenie`)
      with body referencing **#76/#82** and the OpenSpec change.
