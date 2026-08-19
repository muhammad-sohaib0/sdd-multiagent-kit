# SDD Multi-Agent Kit — Example Milestone 1 Spec (Quote CLI)

**Document:** `spec_milestone_1.md` (example, produced by running the kit against `examples/sample-project/PLAN.md`)
**Milestone:** 1 of 1
**Status:** Example — demonstrates the kit's output shape

## Goal

A small, dependency-free Python 3 CLI `quote` that prints programming quotes, manages a plain-text store, and follows an observable CLI contract. This example milestone set mirrors the standard the kit enforces (spec / plan / tasks / workflow / tests) and is meant to be imitated, not shipped.

## Functional Requirements

- **FR-1** — `quote` with no arguments prints a random quote from the store and exits `0`.
- **FR-2** — `quote --list` prints all quotes, one per line, exits `0`.
- **FR-3** — `quote --add "<text>"` appends a quote to the store and prints a confirmation.
- **FR-4** — The store is a plain-text file (one quote per line) in a user-data directory, created on first use.
- **FR-5** — Unknown flags / missing arguments print a usage message to stderr and exit `2`.
- **FR-6** — Standard library only (no dependencies).

## Edge Cases & Rules

- Empty store: random quote on an empty store prints a friendly message and exits `0`; `--list` on an empty store prints nothing and exits `0`.
- Missing argument to `--add` → usage to stderr, exit `2`.
- Quotes are stored/retrieved verbatim; lines are trimmed for printing.
- Local, no network, no secrets.

## Acceptance Criteria

- **AC-1** — All four commands behave per FR-1..FR-3 and exit codes.
- **AC-2** — Store file is created on first use and read/written in the user-data directory.
- **AC-3** — Unknown flags and missing `--add` argument exit `2` with a usage message on stderr.
- **AC-4** — Runs on Python 3 with no third-party packages.

## Cross-Reference

| Document | Path |
|---|---|
| Spec (this file) | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests | `outputs/milestones/milestone_1/tests_milestone_1.md` |