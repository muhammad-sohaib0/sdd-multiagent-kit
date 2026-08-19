# SDD Multi-Agent Kit — Milestone 5 Workflow

**Document:** `workflow_milestone_5.md`
**Milestone:** 5 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_5/spec_milestone_5.md`

## Cumulative History

Same as the spec/plan. Scenario tree for the example.

## 1. Build States

```
B0 start
 B1 PLAN.md brief (T1)
 B2 example milestone set (T2)
 B3 examples README (T3)
 B4 verify: invokable | non-stub+consistent | no secrets/deps (T4)
   └─ failure → fix + re-run (internal)
```

## 2. Reader States

```
R1 user studies example to learn the workflow
 ├─ examples/README.md → how to run the kit → GUIDE for context
 └─ sample-project/PLAN.md + example milestone set → the output shape
R2 user runs the kit against the sample brief
 └─ PLAN.md is directly invokable (/sdd or the critique engine)
```

## 3. Feature-to-Node Traceability

Sample brief → PLAN.md/R2; example milestone set → milestone_1 five docs/R1; run instructions + guide link → examples README/R1; self-contained no-deps → PLAN.md/R2. Every feature maps here; every node is backed by a task (T1–T4) and a test (NT1–NT4). No orphans; no untested nodes.

## 4. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_5/spec_milestone_5.md` |
| Plan | `outputs/milestones/milestone_5/plan_milestone_5.md` |
| Tasks | `outputs/milestones/milestone_5/tasks_milestone_5.md` |
| Workflow (this file) | `outputs/milestones/milestone_5/workflow_milestone_5.md` |
| Tests | `outputs/milestones/milestone_5/tests_milestone_5.md` |