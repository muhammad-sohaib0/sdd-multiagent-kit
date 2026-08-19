# SDD Multi-Agent Kit — Example Milestone 1 Workflow (Quote CLI)

**Document:** `workflow_milestone_1.md` (example)
**Milestone:** 1 of 1
**Status:** Example
> Companion to: `examples/sample-project/outputs/milestones/milestone_1/spec_milestone_1.md`

This document is the scenario-branching tree for the sample milestone: the states and transitions the `quote` CLI must support, plus the states the milestone's own build/verification must handle. Every feature named in the spec is traceable to a node here (Simplicity gate: no orphan features), and every node is backed by a task in `tasks_milestone_1.md` and a test in `tests_milestone_1.md` (Structural Completeness gate).

## Build States

```
B0 start
 B1 tests authored first (T1, Article III) → B2 quote.py (T2) → B3 seed store (T3) → B4 verify (T4)
   ├─ B4 pass → milestone complete
   └─ B4 fail → fix the artifact and re-run that verification (internal to build)
```

## 2. Command States (the CLI contract)

```
C1 `quote`            → random quote printed, exit 0
C2 `quote --list`     → all quotes printed, one per line, exit 0
C3 `quote --add "X"`  → quote appended, confirmation printed, exit 0
C4 `quote --bogus`    → usage message on stderr, exit 2
C5 `quote --add`      → usage message on stderr, exit 2 (missing argument)
C6 empty store        → friendly message (random pick) / nothing (list), exit 0
C7 store lifecycle    → store file created on first use in the user-data directory
C8 dependency check   → runs on Python 3 with the standard library only
```

C1–C3 are the success paths of the three commands; C4–C5 are the two error paths the contract fixes; C6 covers the empty-store edge case from the spec; C7 covers the store-file lifecycle requirement; C8 covers the stdlib-only constraint. Each failure branch above is terminal for that invocation: the usage message is the last output and the exit code is `2` — there is no recovery path, by design (the spec fixes the contract, not a recovery flow).

## Feature-to-Node Traceability

```
FR-1→C1
FR-2→C2
FR-3→C3
FR-4→C7
FR-5→C4
FR-5→C5
FR-6→C8
```

Every functional requirement in the spec maps to at least one command-state node above: FR-1 (random quote, exit 0) → C1, FR-2 (`--list`) → C2, FR-3 (`--add`) → C3, FR-4 (store file lifecycle) → C7, FR-5 (unknown flags and missing arguments) → C4 and C5, FR-6 (stdlib only) → C8. The empty-store edge case from the spec's Edge Cases & Rules section maps to C6. There are no orphan features, and conversely no node here lacks a task (T1–T4 in `tasks_milestone_1.md`) and a test (NT1–NT8 in `tests_milestone_1.md`).

## Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow (this file) | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests | `outputs/milestones/milestone_1/tests_milestone_1.md` |