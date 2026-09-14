# Spec delta: five agent GGUFs that fit

## ADDED Requirements

### Requirement: A-agent — Top-tier download yields agent files that fit, count is files
WHEN a user runs `llama-ai --download-top-tier` with default `--count 5`, THEN discovery
returns at most **five GGUF files** that (1) pass the existing fit + junk gates and
(2) are **agent** models: repo id or filename matches `instruct`, `coder`, or `tool` as a
word boundary (case-insensitive). Non-agent files MUST NOT pad the list. `--per-provider`
MUST NOT add a lower quant that fails the agent check. If fewer than `--count` agent files
exist, return those and report honestly. `--download-top-tier` MUST NOT start `llama-server`
and MUST NOT compile llama.cpp.

#### Scenario: Mix of instruct, coder, base, IQ2, mmproj
GIVEN a mocked HF list with instruct, coder, base, IQ2, and mmproj files that all "fit"
WHEN `discover_top_tier` runs with count 5
THEN only instruct and coder files are returned; base, IQ2, and mmproj never appear

#### Scenario: Only two agent files in the world
GIVEN only two agent GGUFs pass the gates
WHEN download/discover runs with count 5
THEN exactly those two are returned with an honest shortfall; no non-agent padding

#### Scenario: Dry run does not start the server
GIVEN `--download-top-tier --dry`
WHEN the CLI runs
THEN no `llama-server` process is started

### Requirement: A-agent-tokens — Agent match is word-boundary
WHEN judging a candidate
THEN filenames/repos containing the whole words instruct, coder, or tool match;
a base-only `model-Q8_0.gguf` does not.

#### Scenario: Instruct in filename is kept, base-only Q8 is skipped
GIVEN `model-Instruct-Q8_0.gguf` and `model-Q8_0.gguf` from otherwise equal repos
WHEN discovery runs
THEN only the Instruct file is a candidate
