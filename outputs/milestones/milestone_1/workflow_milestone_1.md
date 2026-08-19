# SDD Multi-Agent Kit — Milestone 1 Workflow

**Document:** `workflow_milestone_1.md`
**Milestone:** 1 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_1/spec_milestone_1.md`

## Cumulative History

Same as the spec/plan. This document is the scenario-branching tree for Milestone 1: the states and transitions the *kit content itself* must support when it runs (the master skill + ten sub-skills pipeline), plus the states the *M1 build/verification* must handle. Every feature named in the spec's plan is traceable to a node here (Simplicity gate: no orphan features).

## 1. Pipeline Run States (the kit running a user project)

```
S0 start: brief furnished
 ├─ S1 CT scan runs
 │   ├─ S1a brief non-empty → checklist produced → proceed
 │   └─ S1b brief empty → HALT, ask user for a brief (no fabricate)
 ├─ S2 constitution adopted once (from template) → proceed
 ├─ S3 milestone-builder decides split
 │   ├─ S3a multi-milestone → ordered milestone folders
 │   └─ S3b single-milestone → root outputs/ layout
 └─ S4 per milestone M:
     ├─ M1 specify → spec draft
     │   ├─ G1 gate: pass → continue
     │   └─ G1 gate: fail → return to specify with findings (blocked, logged)
     ├─ M2 Pass 1 critique → issues
     │   ├─ objective issues → resolve, re-run Pass 1
     │   └─ needs_clarify list compiled
     ├─ M3 clarify-interview
     │   ├─ M3a list empty → skip (no questions)
     │   ├─ M3b list non-empty → ask; answers folded in
     │   │   ├─ answers given → fold into spec
     │   │   └─ answer refused/invalid → record refusal, drop item, note in Out of Scope
     ├─ M4 plan-builder → plan
     ├─ M5 task-breakdown → tasks
     ├─ M6 workflow-builder → workflow
     ├─ M7 scenario-tester → tests
     ├─ M8 G2 gate (all five) → pass: continue; fail: return to responsible drafting sub-skill
     ├─ M9 Pass 2 critique (full rigor on all five) → pass: continue; fail: re-enter loop
     ├─ M10 stranger-test
     │   ├─ pass → proceed to build
     │   └─ fail → failure becomes a new loop issue (re-enter; bounded by round cap → escalate to human at cap)
     └─ M11 build → artifacts materialized at tasks.md paths
```

## 2. Sub-skill Runtime Failure (applies to any sub-skill node above)

```
F1 sub-skill fails to produce required output
 ├─ F1a log PHR, retry once (same input, no backoff)
 │   ├─ retry succeeds → continue pipeline
 │   └─ retry fails → F1b
 └─ F1b BLOCKING escalation: report to human with summary, stop (never silent, never unbounded)
```

## 3. Critique Loop States (within M2 Pass 1 and M9 Pass 2)

```
C1 per model (seven-model panel), one critique
 ├─ valid (parses to schema) → counted
 └─ invalid (unparseable, or low-score-with-empty-issues — "low" = overall_score < 10)
     ├─ ≤1 retry → valid → counted
     ├─ invalid → retry once (≤2 attempts); still invalid → absent this round, participates again next round (no cross-round exclusion)
     └─ transport failure (timeout/5xx/429) → up to 3 tries with backoff, then excluded for the round (logged)
 C2 round stopping
 ├─ Pass 1: every objective issue resolved + needs_clarify compiled → advance to Clarify
 ├─ Pass 2: every currently-valid critic scores perfect → advance to Stranger Test
 └─ round cap reached (default 25) → escalate to human with full summary (never silent)

C2 note: the round cap is a **per-pass** budget — Pass 1 and Pass 2 each have their own 25-round cap, so a long Pass 1 cannot exhaust Pass 2's budget (and vice versa).
C1/§2 note (two distinct retry policies — do not conflate): (a) **sub-skill execution retry** (§2) is once, same input, no backoff; (b) **per-critic network retry** (C1) is up to 3 tries with transport backoff. They apply at different layers: the sub-skill call, vs the individual model's HTTP call inside the critique engine. Both are bounded; neither is unbounded.
```

## 4. M1 Build/Verification States

```
B0 start M1 build — the verification suite is authored first: this is **T1** (the `tests_milestone_1.md` document), per Article III (tests before implementation)
 B1 scaffold + providers.yaml (T2–T3)
 B2 ten sub-skills authored (T5–T14)  [P]   # [P] = parallelizable; these tasks are independent of each other
 B3 master skill authored (T15)
 B4 verification
 ├─ T16 inventory+frontmatter → pass/fail
 ├─ T17 providers validation → pass/fail
 ├─ T18 secret scan → pass/fail (zero matches)
 ├─ T19 constitution verbatim → pass/fail
 └─ T20 Stranger Test → pass: milestone complete; fail: re-enter critique loop as a new issue

B4 failure handling: on any T16–T19 failure → fix the artifact, re-run that verification (internal to build; not a critique-loop round). On T20 failure → the failure is fed back as a new critique-loop issue (this is the one rule the loop may not reason around). All four B4 checks log a PHR on failure.
```

**PHR logging throughout:** per spec §4.5, the master skill logs a PHR at *every* enumerated phase transition (after CT scan, constitution adoption, milestone breakdown, and per milestone: after specify, G1, Pass 1, clarify, plan/tasks/workflow/tests, G2, Pass 2, stranger-test, build) — not only in the failure path F1a. F1a's "log PHR" is the *failure-specific* record; normal transitions log too.

## 5. Feature-to-Node Traceability

Every named behavior in the spec/plan maps to a node above: installed-skill awareness (a sub-behavior of the S1 CT-scan node, feeding the conditional-category check), single vs multi-milestone (S3a/b), gates G1/G2 (M1/M8), Pass 1/Pass 2 (M2/M9), Clarify empty vs non-empty (M3a/b), clarify refusal (M3b), stranger-test pass/fail (M10), sub-skill failure policy (F1), critique validity/retry (C1), round cap (C2), and the build/verification steps (B1–B4). There are **no orphan features** (Simplicity gate). Conversely, every node is backed by a task in `tasks_milestone_1.md` and a test in `tests_milestone_1.md` (Structural Completeness gate).

**Constitution principles in this tree:** *Framework Trust* → "no wrapping", "no unbounded retry" (F1/F1b, C1 backoff bounds); *Observable Interfaces* → each sub-skill's input/output is a defined contract (nodes are transitions across those contracts); *Amendment Process* → the ADR path that any constitution/config override (e.g. Simplicity default, a panel swap) must take (PHR/ADR history, §4.5). These are implicit in the nodes, not separate states, so they do not appear as isolated boxes.

## 6. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow (this file) | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests | `outputs/milestones/milestone_1/tests_milestone_1.md` |