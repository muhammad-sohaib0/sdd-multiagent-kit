# Stranger Test — Milestone 2 (critique engine)

**Artifact type:** Stranger Test record (`PLAN.md` §9 layout, §4.5 grounding anchor)
**Milestone:** 2 of 5 — the critique engine automation
**Input:** the full five-document set, together (`PLAN.md` §7.6):
`spec_milestone_2.md`, `plan_milestone_2.md`, `tasks_milestone_2.md`, `workflow_milestone_2.md`, `tests_milestone_2.md`
**Instruction given:** *implement this, ask no questions*
**Session:** fresh, zero-context — given only the five M2 documents
**Result: PASS** — all derived items matched the built artifacts

> Transcribed from the primary evidence in PHR `milestone_2/000`, which remains
> authoritative.

## What the zero-context session independently derived

| # | Check | Derived | Verdict |
|---|---|---|---|
| A | Deliverables | The three artifact paths (`orchestrate_critique_loop.py`, `validate_critique.py`, `critique-loop/SKILL.md`) | Matched |
| B | Interfaces | Both CLIs — flags, defaults, and exit codes | Matched |
| C | Retry policy | ≤1 unparseable retry; transport tries with growing backoff; the non-progressing escalation; the 25-per-pass round cap | Matched |
| D | Output contract | The output path and the required vs optional schema fields | Matched |
| E | Sub-skill | The three sub-skill steps (invoke → read/triage → stop) | Matched |
| F | Config-driven panel | That the panel is read from `providers.yaml`, not hard-coded | Matched |

## Divergences fed back into the loop

**None blocking.** One cosmetic note was recorded: some `workflow`/`tests` CLI
examples abbreviate `--out`, while the real script's CLI matches the spec. This
was a documentation-example abbreviation, not a contract divergence, so nothing
re-entered the loop.

## Note on the transport-retry figure

The PHR records the stranger deriving "≤3 transport tries" — the figure in force
when this test ran. The transport budget was subsequently raised to ≤5 tries (the
value `PLAN.md` §4.3, the M2 spec, and the shipped engine now carry; see the
errata on ADR-003). The finding stands: the stranger derived *that a bounded
transport-retry budget with growing backoff exists and is specified in the
documents*, which is the contract-parity property under test. The specific bound
is a magnitude the documents own and later revised.

## Cross-reference

| Record | Path |
|---|---|
| Primary evidence (PHR) | `outputs/history/prompts/milestone_2/000-critique-engine-complete.md` |
| Test contract | `outputs/milestones/milestone_2/tests_milestone_2.md` |
| Executable suite | `outputs/milestones/milestone_2/verify_milestone_2.py` |
| Raw critique rounds | `outputs/critique-log/m2-pass2/` |
