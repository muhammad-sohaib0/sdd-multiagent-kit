# SDD Multi-Agent Kit — Milestone 2 Workflow

**Document:** `workflow_milestone_2.md`
**Milestone:** 2 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_2/spec_milestone_2.md`

## Cumulative History

Same as the spec/plan. Scenario tree for the critique engine's runtime + M2 build/verification.

## 1. Critique Loop Runtime States

```
R0 invoke: orchestrate_critique_loop.py --doc D --name N --pass P --round R
 ├─ read providers.yaml
 │   ├─ panel loads → proceed
 │   └─ config error → HALT, report (no models to call)
 ├─ build prompt (Pass-1 light | Pass-2 full) → send
 └─ per model, one critique:
     ├─ R1 valid (parses to schema, high score w/ issues OR score≥10)
     │   └─ validate via validate_critique.py → OK → counted
     ├─ R2 invalid (unparseable, or score<10 with zero issues)
     │   ├─ retry ≤1 → valid → counted
     │   └─ still invalid → no signal from that critic this round; participates again next round
     ├─ R3 transport (timeout/5xx/429)
     │   └─ retry ≤5 with growing backoff (429→30×n, 5xx/timeout→8×n) → valid → counted; else absent this round (logged)
     └─ R4 result written → outputs/critique-log/passP-roundR-N.json
 R5 round stopping (the AGENT applies via the sub-skill)
 ├─ Pass 1: objective issues resolved + needs_clarify compiled → advance to Clarify
 ├─ Pass 2: every currently-valid critic scores perfect → advance to Stranger Test
 └─ round cap reached (default 25/pass) → escalate to human with full summary (never silent)
```

## 2. Adjudication (agent layer, via critique-loop sub-skill)

```
A1 read round JSON
 ├─ objective issue → resolve → next round
 ├─ needs_clarify issue → compile into the list → Clarify
 ├─ false positive / measurement decay → reject with reason → log PHR
 └─ no new genuine issues → advance per R5
```

## 3. M2 Build/Verification States

```
B0 start (T1 tests first)
 B1 validate_critique.py (T2) + YAML reader (T3)  [P]
 B2 orchestrate_critique_loop.py (T4)
 B3 critique-loop sub-skill (T5)
 B4 verify: T6 unit-validate | T7 config-driven | T8 retry-policy | T9 real output+schema | T10 sub-skill | T11 secret
   └─ failure → fix + re-run (internal); T9 real run may drop models on 429 (n_valid < 6 is acceptable, logged)
```

## 4. Feature-to-Node Traceability

Retry policy → R2/R3; round cap → R5; validity rule → R1/R2; config-driven panel → R0/§3; adjudication → §2; maker≠checker → §2 (script scores, agent adjudicates). Every feature in spec/plan maps here; every node is backed by a task (T2–T11) and a test (NT1–NT6 in `tests_milestone_2.md`). No orphan features; no untested nodes.

## 5. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_2/spec_milestone_2.md` |
| Plan | `outputs/milestones/milestone_2/plan_milestone_2.md` |
| Tasks | `outputs/milestones/milestone_2/tasks_milestone_2.md` |
| Workflow (this file) | `outputs/milestones/milestone_2/workflow_milestone_2.md` |
| Tests | `outputs/milestones/milestone_2/tests_milestone_2.md` |