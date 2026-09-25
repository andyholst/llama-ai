# feat-e2e-flake-zombie-reaping

## Implementation tasks

- [x] 1.1 In `tests/test_watchloop_dispatch_e2e.py::test_hung_worker_is_killed_and_respawned_does_readme_work`,
      replace the immediate `assert not wd.pid_alive(first_pid)` with a bounded
      poll (<= ~0.5s) that breaks once the worker is gone, then asserts it is
      dead.
- [x] 1.2 Keep the assertion's meaning identical: the hung worker's process tree
      must actually be dead (the poll only waits for the kernel reaper).
- [x] 2.1 (No production code change) — confirm `scripts/watchloop_dispatch.py`
      is untouched; the fix is test-only.

## Tests

- [x] 3.1 Re-run the e2e test in a 30-run loop against the real `llgenie/test`
      container; all 30 pass (flake eliminated; previously ~1/15 failed).

## Verification

- [x] 4.1 `make test-agents-e2e` green.
- [x] 4.2 `make loop` green (all containerized stages).
- [x] 4.3 `make openspec-validate NAME=feat-e2e-flake-zombie-reaping` exit 0.
- [x] 4.4 Commit (Conventional Commit `fix:`), push to `origin`
      (andyholst's repo), and open a cross-repo PR to `upstream`
      (`asimov-agent/llgenie`) with body referencing #85 and this OpenSpec
      change.
