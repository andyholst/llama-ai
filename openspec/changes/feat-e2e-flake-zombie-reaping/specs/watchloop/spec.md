# watchloop — hung-worker e2e kill check must be reaping-tolerant

Extends the existing `watchloop` capability (spec of record:
`openspec/changes/fix-dispatch-stuck-detector-false-liveness/specs/watchloop/spec.md`)
with a test-robustness requirement for the real-subprocess e2e.

## ADDED Requirements

### Requirement: hung-worker e2e death check tolerates async SIGKILL reaping

WHEN the e2e test asserts that a reclaimed (killed) hung worker's process tree is
dead,
THEN the assertion must be robust against the kernel's `SIGKILL` reaping latency:
a killed process may transiently remain a zombie (visible to `os.kill(pid, 0)`,
which `pid_alive()` uses) until it is reaped, so the death check must poll for a
bounded window rather than assert immediately.

#### Scenario: freshly-killed worker is reaped within a bounded window
Given a hung worker whose process tree was just SIGKILLed by
`kill_process_tree`,
When   the test checks `pid_alive(first_pid)` for "original hung worker must be
       dead",
Then   the check succeeds as soon as the process is gone,
And    the bounded poll window (a few hundred ms) is enough to cover the
       reaper on any CI runner,
And    the test does not flake under load where reaping lags a tick behind the
       kill.

#### Scenario: healthy worker still never killed (regression guard)
Given the e2e healthy-worker test (a live, log-growing worker),
When the dispatcher checks the lock,
Then no kill occurs,
And    the death-check change does not alter the "healthy worker must not be
       killed" assertion.

## VERIFICATION

- `tests/test_watchloop_dispatch_e2e.py::TestDispatchE2EHealthyWorker::test_healthy_worker_log_grows_and_is_not_killed` stays green.
- `tests/test_watchloop_dispatch_e2e.py::TestDispatchE2EStuckReclaim::test_hung_worker_is_killed_and_respawned_does_readme_work`
  stays green across repeated runs (flake eliminated — verified by a 30-run loop
  on the real container).
- `make test-agents-e2e` green.
- `make loop` green (all containerized stages); CI `dispatch-e2e` job stable.
