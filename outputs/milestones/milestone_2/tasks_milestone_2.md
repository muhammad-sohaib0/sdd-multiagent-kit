# SDD Multi-Agent Kit — Milestone 2 Tasks

**Document:** `tasks_milestone_2.md`
**Milestone:** 2 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_2/spec_milestone_2.md`

## Cumulative History

Same as the spec/plan. Ordered build plan for the critique engine. Tests first (Article III).

## Build Order

### Group A — Verification contract (before implementation)

- **T1 — Define the M2 verification suite** (`tests_milestone_2.md`). Contract the build must pass (AC-1..AC-6).

### Group B — Reusable machinery `[P]`

- **T2 — Write `kit/scripts/validate_critique.py`** — schema re-validation of a critique-log JSON against PLAN.md §4.3. (Depends on nothing; the loop will use it.)
- **T3 — Write the YAML-subset reader** as a module inside `orchestrate_critique_loop.py` (load providers.yaml: nested maps/lists, scalars, comments). Small, self-contained, unit-testable (Article I).

### Group C — Orchestration

- **T4 — Write `kit/scripts/orchestrate_critique_loop.py`** — CLI: `--doc --name --pass --round --out --round-cap --timeout`. Reads providers.yaml (T3), builds the Pass-1/Pass-2 prompt, calls all seven models concurrently (staggered first call) with the retry policy (≤1 retry unparseable, i.e. up to 2 attempts, with truncation repair; ≤5 tries with adaptive backoff on 429/5xx/timeout; no cross-round exclusion), enforces the validity rule, validates each output via T2, writes `outputs/critique-log/pass{1|2}-round{N}-{name}.json`. Depends on T2+T3.

### Group D — Agent-facing layer

- **T5 — Write `kit/skills/critique-loop/SKILL.md`** — the 11th sub-skill: how to invoke T4, read the JSON, triage (objective/needs_clarify/false-positive), and apply stopping conditions. Depends on T4 (references its CLI).

### Group E — Verification

- **T6 — Unit check `validate_critique.py`** — feed a valid and a malformed critique-log; assert valid passes and malformed is reported.
- **T7 — Config-driven check** — run a dry call path (mock network) and assert the seven `critic_slots` order and provider binding come from `providers.yaml`, not code (AC-2).
- **T8 — Retry-policy check** — assert the ≤1 unparseable retry, ≤5 transport tries with adaptive backoff, truncation repair, and no-cross-round-exclusion logic (AC-3) via a mock provider.
- **T9 — Output-path + schema check** — run once against a real document (a short excerpt) and assert the JSON path `outputs/critique-log/pass2-round1-*.json` and schema (AC-4).
- **T10 — Sub-skill check** — assert `critique-loop/SKILL.md` covers invoke/triage/stop (AC-5).
- **T11 — Secret scan** — assert no secret-pattern matches in the three new files (AC-6).

**Verification failure handling:** T6–T10 failure → fix and re-run (internal). T9's real run may drop models to 429 (free tier) — acceptable; the log records `n_valid`.

## Status

| Task | Status |
|---|---|
| T1 | **done** (`tests_milestone_2.md` — NT1–NT9, E2E walkthrough) |
| T2 | **done** (`kit/scripts/validate_critique.py`) |
| T3 | **done** (YAML-subset reader inside `kit/scripts/orchestrate_critique_loop.py`) |
| T4 | **done** (`kit/scripts/orchestrate_critique_loop.py`) |
| T5 | **done** (`kit/skills/critique-loop/SKILL.md`) |
| T6 | **done** (NT2: valid → exit 0; malformed → exit 1 with the field named) |
| T7 | **done** (NT1: ordered 7 `critic_slots` + provider binding from `providers.yaml`, no hard-coded models; US-4: 8th model added via config picked up with zero code change) |
| T8 | **done** (NT3/NT4/NT5: ≤1 unparseable retry, ≤5 transport tries with adaptive backoff 30s×n / 8s×n, truncation repair, bad-repair-never-counts, no cross-round exclusion) |
| T9 | **done** (NT7 + E2E: real run wrote `outputs/critique-log/pass1-round1-m2excerpt.json`, 5/7 valid, schema-validated) |
| T10 | **done** (NT8: sub-skill covers invoke/read/triage/stop + Pass-2 Clarify re-check + non-progressing escalation) |
| T11 | **done** (NT9: secret scan 0 matches on all three files; keys read at runtime via `key_env`) |

Verification suite: `outputs/milestones/milestone_2/verify_milestone_2.py` — 26 tests, all PASS (see PHR 000 addendum).