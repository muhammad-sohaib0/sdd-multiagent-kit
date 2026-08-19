# SDD Multi-Agent Kit — Milestone 5 Plan

**Document:** `plan_milestone_5.md`
**Milestone:** 5 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_5/spec_milestone_5.md`

## Cumulative History

Same as the spec. M5 realizes the worked example.

## 1. Tech Stack / Format

- **Format:** Markdown for the brief, the example milestone set, and the examples README.
- **Dependencies:** none beyond the kit itself (the sample project is dependency-free).

## 2. Architecture / Structure

```
examples/
  README.md                                # FR-3
  sample-project/
    PLAN.md                                # FR-1 — the sample brief
    outputs/milestones/milestone_1/        # FR-2 — one completed example milestone set
      spec_milestone_1.md
      plan_milestone_1.md
      tasks_milestone_1.md
      workflow_milestone_1.md
      tests_milestone_1.md
```

## 3. Content

The sample project is a small, dependency-free command-line tool — a "quote" CLI that prints a rotating programming-related quote to the terminal. It is small enough to demo quickly but non-trivial (input handling, a small data store, output formatting, exit codes) so the example milestone set exercises real spec content. The example milestone set is written to the same five-document standard the kit enforces, so it doubles as a teaching template.

## 4. Consistency

The example milestone set mirrors the kit's own milestone-set shape and naming (as used in M1–M4). `examples/README.md` shows exactly how to invoke the kit against `PLAN.md`, matching `docs/GUIDE.md` and `AGENTS.md` commands.

## 5. Security

The example contains no secrets and no API keys (it is a local CLI).

## 6. Rationale (Simplicity Justifications)

| Choice | Justification |
|---|---|
| One small dependency-free CLI | Fits the simplicity rule and the "small enough to demo, non-trivial enough to exercise the loop" goal. |
| One completed example milestone set | Teaches the output shape without shipping a bloated full-milestone demo. |
| Example is a local CLI (no keys) | Avoids any secret-handling in the example and keeps it runnable anywhere. |

## 7. Acceptance Mapping

AC-1 (invokable PLAN.md) / AC-2 (five-doc example set) / AC-3 (examples README + guide link) / AC-4 (no secrets/deps) — verified in `tasks_milestone_5.md` / `tests_milestone_5.md`.

## 8. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_5/spec_milestone_5.md` |
| Plan (this file) | `outputs/milestones/milestone_5/plan_milestone_5.md` |
| Tasks | `outputs/milestones/milestone_5/tasks_milestone_5.md` |
| Workflow | `outputs/milestones/milestone_5/workflow_milestone_5.md` |
| Tests | `outputs/milestones/milestone_5/tests_milestone_5.md` |