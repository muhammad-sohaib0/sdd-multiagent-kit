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
1. Derive the steps from the plan, with exact paths.
2. Sequence so nothing runs before what it depends on; mark independent tasks `[P]`.
3. Order **tests before implementation** (Article III) — the verification contract is defined before the content it verifies.
4. End with a status table and a dependency note confirming no forward references to a future milestone.

## Edge cases / rules
- A task depending on an unlisted prior task → reorder; never leave an orphan dependency.
- A task may not depend on a future milestone's artifact (forward-reference gate); if one does, reorder.
- `[P]` = this task is parallelizable (independent of the others in its group).
- Verification tasks include remediation: on failure, fix the artifact and re-run (internal); the Stranger Test failure feeds back as a new critique-loop issue.