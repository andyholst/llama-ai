# Fix: e2e flake — hung-worker kill check races zombie reaping

## Why

The `dispatch-e2e` CI job (which runs `make test-agents-e2e` →
`tests/*_e2e*.py`) flakily failed on the merged rename commit `841c2bc`
(main CI run `36150843377`), even though the identical code passed on the PR
branch. The failing test is
`tests/test_watchloop_dispatch_e2e.py::TestDispatchE2EStuckReclaim::test_hung_worker_is_killed_and_respawned_does_readme_work`.

After `wd.kill_process_tree(first_pid)` sends `SIGKILL`, the killed worker can
remain a zombie until its parent reaps it. `pid_alive()` uses `os.kill(pid, 0)`
(signal 0), which returns success including for zombies. So the test's assertion
`assert not wd.pid_alive(first_pid)` races the kernel reaper and can flake.
This is a timing flake in the test's assertion, not a defect in
`kill_process_tree` (which correctly kills the whole process tree).

## What Changes

- `tests/test_watchloop_dispatch_e2e.py`: the "original hung worker must be
  dead" assertion now polls `wd.pid_alive(first_pid)` with a bounded deadline
  (a few hundred ms) before asserting the worker is dead, so the check
  tolerates `SIGKILL` reaping latency instead of racing it.
- No change to `scripts/watchloop_dispatch.py` — the production kill/reclaim
  logic is unchanged.
- The happy-path behavior is unchanged: a healthy worker is still never killed,
  and a stuck worker is still reclaimed and the fresh worker still completes the
  README issue-work.

## Capabilities

- **watchloop** — the dispatcher's real-subprocess e2e test for the
  hung-worker kill/reclaim lifecycle must be robust against async `SIGKILL`
  reaping, so it does not flake in CI.

## Impact

No change to production dispatcher behavior. Only the **e2e test's death-check**
changes (a bounded poll instead of an immediate `pid_alive` assertion), which
removes the flake while preserving the test's real assertion that the hung
worker's process tree is actually dead.

## Related

- Issue #85.
- Issue #63 (real agent-spawn e2e — the test this change hardens).
- Capability `watchloop` (spec of record:
  `openspec/changes/fix-dispatch-stuck-detector-false-liveness/specs/watchloop/spec.md`).
