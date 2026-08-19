---
name: task-breakdown
description: >-
  Task-phase sub-skill. Produces the ordered, executable steps for a milestone
  derived from the plan: exact file paths, dependency order, [P] markers for
  parallel tasks, and tests ordered before the code they verify (Article III).
version: 0.1.0
---

# Task Breakdown — Ordered Executable Steps

Write `tasks_milestone_N.md` (or `tasks.md`).

## Input
- The accepted plan (and the spec it builds on).

## Output
An ordered task list with exact file paths, dependency order, `[P]` parallel markers, and a status table.

## Procedure
1. Open with the cumulative history and the back-reference to the spec — the first line is `> Companion to: <path to this milestone's spec>` (§7.4: all four companions carry it, so the five files stay traceable from any starting point).
2. Derive the steps from the plan, with exact paths.
3. Give every task a stable id (`T-01`, `T-02`, …) so `workflow.md` and `tests.md` can reference it. Ids are permanent once assigned — renumbering breaks the other documents' traceability tables.
4. Sequence so nothing runs before what it depends on; mark independent tasks `[P]` and state each task's dependencies by id.
5. Order **tests before implementation** (Article III) — the verification contract is defined before the content it verifies. Ordering alone is not enough: include an explicit task that **runs the new tests and confirms they fail** before the task that implements against them. Article III requires tests "confirmed to fail first", which a pure ordering rule permits you to skip.
6. End with a status table and a dependency note confirming no forward references to a future milestone.

## Edge cases / rules
- A task depending on an unlisted prior task → reorder; never leave an orphan dependency.
- A task may not depend on a future milestone's artifact (forward-reference gate); if one does, reorder.
- `[P]` = this task is parallelizable. It is independent of every other task in **its own group** — a group being the set of tasks that share the same dependency prerequisites and can therefore start together. Name the groups (`Group A`, `Group B`, …) so `[P]` has a defined scope; `[P]` with no group boundary is not checkable.
- **Status table values:** `pending`, `in_progress`, `done`, `blocked`. Use exactly these.
- Verification tasks include remediation: on failure, fix the artifact and re-run (internal); the Stranger Test failure feeds back as a new critique-loop issue.