# SDD Multi-Agent Kit — Milestone 4 Workflow

**Document:** `workflow_milestone_4.md`
**Milestone:** 4 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_4/spec_milestone_4.md`

## Cumulative History

Same as the spec/plan. Scenario tree for the docs' build/verification.

## 1. Build States

```
B0 start (T1 tests first)
 B1 root docs T2–T9  [P]
 B2 docs/ guides T10–T12
 B3 repo hygiene T13 (git init + .gitignore)
 B4 verify: T14 presence | T15 consistency | T16 credit | T17 contributing | T18 secret scan
   └─ failure → fix + re-run (internal)
```

## 2. Reader States (the docs must serve)

```
R1 human contributor picks repo up cold
 ├─ README → what/why/quickstart → GUIDE for deep use
 ├─ CONTRIBUTING → how to add a tool / model
 └─ ARCHITECTURE → deep understanding
R2 unfamiliar AI tool picks repo up cold
 ├─ AGENTS.md (cross-tool) + CLAUDE.md (Claude-family) → repo instructions
 └─ ARCHITECTURE → readable without source
R3 security/user
 └─ SECURITY (private reporting + scope) / SUPPORT (where to ask)
```

## 3. Feature-to-Node Traceability

Quickstart → README/R1; credit → README/§1; guide walkthrough → GUIDE/R1; architecture → ARCHITECTURE/R1/R2; bootstrap record → BOOTSTRAP; contribute → CONTRIBUTING/R1; agent instructions → AGENTS+CLAUDE/R2; security → SECURITY/R3; support → SUPPORT/R3; git+gitignore → B3. Every feature maps here; every node is backed by a task (T2–T18) and a test (NT1–NT5). No orphan features; no untested nodes.

## 4. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_4/spec_milestone_4.md` |
| Plan | `outputs/milestones/milestone_4/plan_milestone_4.md` |
| Tasks | `outputs/milestones/milestone_4/tasks_milestone_4.md` |
| Workflow (this file) | `outputs/milestones/milestone_4/workflow_milestone_4.md` |
| Tests | `outputs/milestones/milestone_4/tests_milestone_4.md` |