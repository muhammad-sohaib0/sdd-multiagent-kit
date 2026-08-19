# SDD Multi-Agent Kit — Example Milestone 1 Plan (Quote CLI)

**Document:** `plan_milestone_1.md` (example)
**Milestone:** 1 of 1
**Status:** Example

## Tech Stack / Format

- **Language:** Python 3, standard library only (argparse or manual parsing; a small `quote.py`).
- **Dependencies:** none.

## Architecture / Structure

```
examples/sample-project/
  quote.py                 # the CLI (single file)
  quotes.txt               # default store, seeded with a few quotes
  tests/test_quote.py      # stdlib unittest, written before implementation
  PLAN.md                  # the brief (top-level)
```

- **Store path resolution:** a `data` subdirectory under the platform user-data directory; overridable via an environment variable (`QUOTE_DATA_DIR`) so tests run hermetically without touching a real store.
- **Data model:** one quote per line, plain UTF-8 text, appended on `--add`, read whole on `--list` and on a random pick; blank lines are skipped when printing. No quoting, escaping, or concurrency handling is needed — out of scope.
- **CLI contract:** `quote` (random), `quote --list`, `quote --add "<text>"`, unknown flags and missing arguments produce a usage message on stderr with exit code `2`; all successful paths exit `0`.

## Implementation Notes

- Flag handling via `argparse` (stdlib) gives correct exit `2` behavior on unknown flags and missing required arguments automatically.
- Random selection via `random.choice`; empty store handled explicitly.
- `--add` writes a line; `--list` reads all lines; the file is created on first write/read.

## Security

No network, no secrets, no external input beyond argv; store writes append a single line.

## Rationale

| Choice | Justification |
|---|---|
| `argparse` | Stdlib; gives the required exit-2 and usage-message behavior for free. |
| Single-file CLI | Fits the simplicity rule and demo scope. |
| Env-var-overridable data dir | Lets the tests run without touching the user's real store. |

## Acceptance Mapping

AC-1 (commands+exit codes) / AC-2 (store lifecycle) / AC-3 (exit-2 on errors) / AC-4 (stdlib) — verified in `tests_milestone_1.md`.

## Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan (this file) | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests | `outputs/milestones/milestone_1/tests_milestone_1.md` |