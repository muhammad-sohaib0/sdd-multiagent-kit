# SDD Multi-Agent Kit — Milestone 2 Tests

**Document:** `tests_milestone_2.md`
**Milestone:** 2 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_2/spec_milestone_2.md`

## Cumulative History

Same as the spec/plan. Verification suite for the critique engine. Article III: written before implementation (T1).

## 1. Node Tests (per workflow node)

| # | Node | Test | Pass criterion |
|---|---|---|---|
| NT1 | R0 config-driven panel | run with a mock provider set | seven `critic_slots` read from `providers.yaml` in order; model→provider binding correct; no hard-coded list (AC-2) |
| NT2 | R1/R2 validity rule | feed valid + invalid critique shapes to `validate_critique.py`; feed a score<10-with-zero-issues critique to the orchestrator | valid shape passes; malformed shape fails; the score<10-with-zero-issues semantic rule is enforced by the orchestrator, not the validator (FR-1/FR-2, AC-4) |
| NT3 | R2 retry (unparseable) | mock critic returns unparseable then valid | ≤1 retry; then counted (AC-3) |
| NT4 | R3 transport | mock critic returns 429 then 200 | ≤5 tries with growing backoff; then counted or absent this round (AC-3) |
| NT5 | R2 recurring invalid | mock critic invalid across several rounds | no persistent flag or exclusion; critic participates again each round; loop continues with valid critics (AC-3) |
| NT6 | R5 round cap | `--round-cap` accepted and validated (`0` OK; `-1` → exit 2); `--round` beyond cap runs (no script-side cap) | script-side contract matches FR-1: the cap is validated but enforced by the sub-skill, never by the script (AC-3) |
| NT7 | T9 output path+schema | real short run | JSON at `outputs/critique-log/passP-roundR-N.json` matching the §4.3 schema (AC-4) |
| NT8 | T10 sub-skill | read `critique-loop/SKILL.md` | covers invoke, triage (objective/needs_clarify/false-positive), stopping (AC-5) |
| NT9 | T11 secret scan | scan the three new files | zero matches of `sk-[A-Za-z0-9]{20,}`, `AIza[0-9A-Za-z_-]{35}`, `Bearer [A-Za-z0-9._-]{20,}` (AC-6) |

## 2. Acceptance-Criterion Mapping

| Acceptance | Covered by |
|---|---|
| AC-1 (three files exist, non-stub) | NT8 + build presence |
| AC-2 (config-driven panel) | NT1 |
| AC-3 (retry policy) | NT3, NT4, NT5, NT6 |
| AC-4 (schema + output path + validation) | NT2, NT7 |
| AC-5 (sub-skill instructions) | NT8 |
| AC-6 (no secrets) | NT9 |

## 3. End-to-End Walkthrough

Run Pass 1 on a short excerpt (the M2 spec's Goal section) via `orchestrate_critique_loop.py --doc <excerpt> --name m2excerpt --pass 1 --round 1`. Expect: panel loads from providers.yaml (seven models, ordered), each model called concurrently (staggered), valid critiques counted, any transport failures retried/backed-off then logged, output JSON written to `outputs/critique-log/pass1-round1-m2excerpt.json`, and `validate_critique.py` confirms its shape. Some models may drop on 429 (free tier) — `n_valid` < 7 is acceptable and recorded. This proves the engine turns the described invariant into working automation.

## 4. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_2/spec_milestone_2.md` |
| Plan | `outputs/milestones/milestone_2/plan_milestone_2.md` |
| Tasks | `outputs/milestones/milestone_2/tasks_milestone_2.md` |
| Workflow | `outputs/milestones/milestone_2/workflow_milestone_2.md` |
| Tests (this file) | `outputs/milestones/milestone_2/tests_milestone_2.md` |