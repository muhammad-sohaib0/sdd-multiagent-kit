# SDD Multi-Agent Kit — Milestone 2 Plan

**Document:** `plan_milestone_2.md`
**Milestone:** 2 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_2/spec_milestone_2.md`

## Cumulative History

Same as the spec. M2 realizes the "how" of the critique engine.

## 1. Tech Stack

- **Language:** Python 3 (stdlib only — `urllib`, `json`, `re`, `concurrent.futures`, `argparse`). No third-party runtime dependency; YAML is parsed with a tiny built-in subset reader (see Data Model) to honor the kit's zero-dependency stance (Article IV, V).
- **Content:** the `critique-loop` sub-skill is an Agent-Skills SKILL.md like M1's.

## 2. Architecture

```
kit/scripts/orchestrate_critique_loop.py   # entry point: runs the loop for a doc+pass
kit/scripts/validate_critique.py           # schema re-validation of a critique-log JSON
kit/skills/critique-loop/SKILL.md          # agent-facing instructions (invoke, triage, stop)
```

- **`orchestrate_critique_loop.py`** is the sole network/machinery owner. It reads providers.yaml → the panel models + keys, builds the prompt, calls all of them concurrently, applies the retry policy, and writes the round JSON. It does **not** adjudicate issues — that is the agent's job via the sub-skill (maker ≠ checker separation, PLAN.md §3).
- **`validate_critique.py`** is a pure function over a critique-log JSON: shape-check against the schema. It is invoked both by the loop (before writing, as a self-check) and by verification tests.
- **`critique-loop/SKILL.md`** is the human-guided layer: how the agent invokes the script, reads the JSON, separates objective vs needs_clarify vs false-positive, and applies stopping conditions. It references the script's CLI but holds no network logic.

## 3. Data Model

- **Panel:** read from `kit/config/providers.yaml` (M1). `providers[].models` gives the pool; the ordered `critic_slots` gives critique order. Env vars by `key_env` name, read at runtime; never hard-coded.
- **YAML parsing:** a small reader supporting nested maps/lists/scalars and `#` comments, sufficient for providers.yaml. (Chosen over a dependency to keep the kit installable with zero deps; documented in ARCHITECTURE for M4.)
- **Critique JSON (output):** `{document, pass, round, critics: [ {model, document, round, pass, overall_score, scores:{clarity,completeness,edge_case_coverage,internal_consistency,testability}, issues:[{section,category,problem,why_it_matters?,suggested_fix?}], verdict} ], n_valid}` — schema per PLAN.md §4.3.
- **Failure state:** per-model retry counters within the round (unparseable ≤2 attempts, transport ≤5 tries with adaptive backoff; no cross-round state — a failed critic participates again next round); a `--round-cap` arg (default 25, `0` to disable).

## 4. Integration Approach

- The loop is invoked by the agent (per `critique-loop` sub-skill) with `--doc <path> --name <id> --pass 1|2 --round N`. Output lands in `outputs/critique-log/`. The master skill (M1) already names these checkpoints; M2 provides the automation it points to.
- A `.bootstrap/orchestrate.py` harness was used during the bootstrap; M2's `orchestrate_critique_loop.py` is the production version that reads providers.yaml (the harness predates/parallels it and is not shipped).

## 5. Security

- Env-var **names** only in config and code; values read at runtime from the environment. No key material written or logged.
- Failed responses may echo the model's raw text only as a truncated, sanitized snippet on transport error; never keys.

## 6. Rationale (Simplicity Justifications)

| Choice | Justification |
|---|---|
| Python stdlib, zero deps | Kit must install with one `npm install` with nothing else (PLAN.md §1); a self-contained YAML-subset reader avoids a dependency. |
| Scripts own machinery; sub-skill owns judgement | Preserves maker≠checker; mechanical scoring is scripted, adjudication stays human/agent. |
| Config-driven panel (no hard-coded models) | US-4; keeps model additions data-only (M1 `providers.yaml`). |
| Concurrent calls + per-model timeout | A slow model must not block the round; matches the observed slowest free-tier critic behavior. |

M2 introduces 1 standalone component beyond the kit content (the critique-engine scripts) — under the Simplicity default of 3, no extra justification required.

## 7. Acceptance Mapping

AC-1 (files exist) / AC-2 (config-driven) / AC-3 (retry policy) / AC-4 (schema + output path + validation) / AC-5 (sub-skill instructions) / AC-6 (no secrets) — each is verified in `tasks_milestone_2.md` / `tests_milestone_2.md`.

## 8. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_2/spec_milestone_2.md` |
| Plan (this file) | `outputs/milestones/milestone_2/plan_milestone_2.md` |
| Tasks | `outputs/milestones/milestone_2/tasks_milestone_2.md` |
| Workflow | `outputs/milestones/milestone_2/workflow_milestone_2.md` |
| Tests | `outputs/milestones/milestone_2/tests_milestone_2.md` |