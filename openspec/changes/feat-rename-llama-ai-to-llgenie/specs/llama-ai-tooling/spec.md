# llama-ai Tooling (renamed) — MODIFIED install contract

This change updates the existing `llama-ai-tooling` capability so the one-command
install produces the new `llgenie` launcher instead of `llama-ai`, and so the
served binary / upstream names are explicitly left untouched.

## MODIFIED Requirements

### Requirement: one-command install into ~/bin (new name)
The system MUST provide a `make install` target that creates the gguf venv,
installs an executable `~/bin/llgenie` launcher that runs `scripts/llama_serve.py`
with the venv's Python, symlinks `~/bin/llgenie.py` to the repo launcher copy,
symlinks `~/bin/llama-server` to the llama.cpp binary, and runs a smoke test.
`make uninstall` MUST remove ONLY `~/bin/llgenie`, `~/bin/llgenie.py`, and
`~/bin/llama-server` (the venv and repo source are left untouched).

#### Scenario: install produces a runnable launcher
- **Given** a fresh checkout on a host where `make install` can run,
- **When** `make install` completes successfully,
- **Then** `~/bin/llgenie` exists and is executable,
- **And** `~/bin/llgenie.py` is a symlink to the repo launcher (`scripts/llama_serve.py`),
- **And** running `~/bin/llgenie --list` returns a listing (or a clear empty result) without a module error.

#### Scenario: uninstall removes only the new-name artifacts
- **Given** a host with a previous `make install` having written `~/bin/llama-ai`
  artifacts (or any launcher under `~/bin`),
- **When** `make uninstall` runs,
- **Then** `~/bin/llgenie`, `~/bin/llama_ai.py`, and `~/bin/llama-server` are all
  removed (removal of the old `llama-ai`/`llama_ai.py` names is tolerated),
- **And** `~/bin/llama-server` is removed while the repo's `scripts/llama_serve.py`
  is left untouched.

### Requirement: installed launcher is venv-based (name-agnostic)
The launcher MUST exec the repo launcher with the gguf venv python and MUST
prepend `~/bin` to PATH so the `llama-server` symlink resolves. The launcher's
self-documenting comment and its missing-module error hint MUST use the `llgenie`
brand, and the missing-module fallback path MUST still resolve to the repo launcher.

#### Scenario: launcher resolves the venv python
- **Given** an installed launcher at `~/bin/llgenie`,
- **When** the launcher is inspected,
- **Then** its text references `scripts/llama_serve.py` and `llama-gguf-tools/.venv`,
- **And** it exports `PATH` including `~/bin` before exec.
