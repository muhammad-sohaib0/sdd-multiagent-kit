# SDD Multi-Agent Kit — Example Milestone 1 Tests (Quote CLI)

**Document:** `tests_milestone_1.md` (example)
**Milestone:** 1 of 1
**Status:** Example
> Companion to: `examples/sample-project/outputs/milestones/milestone_1/spec_milestone_1.md`

This file is the verification suite the sample milestone's build must pass (Article III: written before implementation, as task T1) and the mapping of one test to each node in `workflow_milestone_1.md`, plus an end-to-end walkthrough of the whole tree.

## Node Tests

One test per workflow node (C1–C8 in `workflow_milestone_1.md`):

| # | Workflow node | Test | Pass criterion |
|---|---|---|---|
| NT1 | C1 (`quote`, no args) | run with no arguments | prints a quote from the store, exits `0` |
| NT2 | C2 (`quote --list`) | run `--list` | prints all quotes, one per line, exits `0` |
| NT3 | C3 (`quote --add "X"`) | add a quote, then list | appends the quote, prints a confirmation, exits `0`; `--list` then shows it |
| NT4 | C4 (unknown flag) | run `quote --bogus` | prints a usage message to stderr, exits `2` |
| NT5 | C5 (missing argument) | run `quote --add` with no argument | prints a usage message to stderr, exits `2` |
| NT6 | C6 (empty store) | run against an empty store | `quote` prints a friendly message, exits `0`; `--list` prints nothing, exits `0` |
| NT7 | C7 (store lifecycle) | run once with no store present | store file is created on first use under the environment-overridable data directory |
| NT8 | C8 (dependency check) | inspect imports and runtime | runs on Python 3 using the standard library only, no third-party packages |

## Acceptance-Criterion Mapping

| Acceptance | Covered by |
|---|---|
| AC-1→NT1 | random quote, exit 0 |
| AC-1→NT2 | list, exit 0 |
| AC-1→NT3 | add + confirmation, exit 0 |
| AC-2→NT7 | store file lifecycle in the data directory |
| AC-3→NT4 | unknown flag → usage, exit 2 |
| AC-3→NT5 | missing argument → usage, exit 2 |
| AC-4→NT8 | stdlib only, no third-party packages |

Every acceptance criterion in the spec is covered by at least one node test above: AC-1 (commands per FR-1..FR-3 with correct exit codes) → NT1–NT3, AC-2 (store created on first use) → NT7, AC-3 (exit `2` with usage on stderr) → NT4–NT5, AC-4 (Python 3, no third-party packages) → NT8.

## End-to-End Walkthrough

A user clones the repo, opens `examples/sample-project/PLAN.md`, and follows the build: tests are written first (T1) as the node tests above, then `quote.py` is implemented against them (T2), the store is seeded (T3), and the suite plus manual CLI checks are run (T4). A single real-user path through the tree: `quote --add "Code is poetry."` succeeds (C3, NT3); `quote` prints a random quote (C1, NT1); `quote --list` shows the seeded quotes plus the new one (C2, NT2); `quote --bogus` fails with usage on stderr and exit `2` (C4, NT4). The store file appears in the data directory on first use (C7, NT7), and the whole run uses only the standard library (C8, NT8).

**Expected end state:** all NT1–NT8 pass, AC-1..AC-4 satisfied, the milestone's build completes exactly as `tasks_milestone_1.md` orders it.

## Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests (this file) | `outputs/milestones/milestone_1/tests_milestone_1.md` |