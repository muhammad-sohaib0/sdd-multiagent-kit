# SDD Multi-Agent Kit — Milestone 5 Tests

**Document:** `tests_milestone_5.md`
**Milestone:** 5 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_5/spec_milestone_5.md`

## Cumulative History

Same as the spec/plan. Verification suite for the example. Article III: written before content (T1).

## 1. Node Tests (per build/reader node)

| # | Node | Test | Pass criterion |
|---|---|---|---|
| NT1 | T1 PLAN.md invokable | read the sample brief | `examples/sample-project/PLAN.md` exists, is self-contained, and contains a brief the kit can run against (AC-1) |
| NT2 | T2 example set | check the five docs | `spec/plan/tasks/workflow/tests` exist under `examples/sample-project/outputs/milestones/milestone_1/`, non-stub, follow the kit's five-document standard (AC-2) |
| NT3 | T3 examples README | read `examples/README.md` | exists, explains running the kit against `sample-project/PLAN.md`, links to `docs/GUIDE.md` (AC-3) |
| NT4 | T4 secrets/deps | scan + inspect | no secret-looking values; no external dependencies required (AC-4) |

## 2. Acceptance-Criterion Mapping

| Acceptance | Covered by |
|---|---|
| AC-1 (invokable PLAN.md) | NT1 |
| AC-2 (five-doc example set) | NT2 |
| AC-3 (examples README + guide link) | NT3 |
| AC-4 (no secrets/deps) | NT4 |

## 3. End-to-End Walkthrough

A user opens `examples/README.md`, reads how to run the kit against `sample-project/PLAN.md`, and studies the completed example milestone set to learn the output shape. The sample brief is self-contained and invokable; the example set mirrors the kit's standard; nothing in the example needs secrets or external dependencies.

## 4. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_5/spec_milestone_5.md` |
| Plan | `outputs/milestones/milestone_5/plan_milestone_5.md` |
| Tasks | `outputs/milestones/milestone_5/tasks_milestone_5.md` |
| Workflow | `outputs/milestones/milestone_5/workflow_milestone_5.md` |
| Tests (this file) | `outputs/milestones/milestone_5/tests_milestone_5.md` |