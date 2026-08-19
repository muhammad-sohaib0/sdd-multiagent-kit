# Stranger Test — Milestone 3 (installer)

**Artifact type:** Stranger Test record (`PLAN.md` §9 layout, §4.5 grounding anchor)
**Milestone:** 3 of 5 — the npm installer and tool adapters
**Input:** the full five-document set, together (`PLAN.md` §7.6):
`spec_milestone_3.md`, `plan_milestone_3.md`, `tasks_milestone_3.md`, `workflow_milestone_3.md`, `tests_milestone_3.md`
**Instruction given:** *implement this, ask no questions*
**Session:** fresh, zero-context — given only the five M3 documents
**Result: PASS** — all derived items matched the built artifacts

> Transcribed from the primary evidence in PHR `milestone_3/000`, which remains
> authoritative.

## What the zero-context session independently derived

| # | Check | Derived | Verdict |
|---|---|---|---|
| A | Deliverables | All six artifact paths (the wizard, the four adapters, `package.json`) | Matched |
| B | Extension contract | The three-function adapter interface and what each function means per tool | Matched |
| C | Install locations | The four `PLAN.md` §10.3 destinations, and Antigravity's embedded trigger vs the three native slash-command tools | Matched |
| D | Wizard flow | The order of the wizard's steps (keys → detect → select → install → confirm) | Matched |
| E | Environment + exit codes | The three env-var names and the `0`/`1`/`2`/`130` exit codes | Matched |
| F | Package shape | The `package.json` requirements (`bin`, `engines`, MIT, no dependencies) | Matched |

Check C is the milestone's sharpest boundary: three of the four tools share one
destination while Antigravity needs a separate copy with a trigger line written
into the skill's frontmatter. A stranger deriving that split from the documents
alone is the evidence that §10.3 is genuinely specified rather than assumed.

## Divergences fed back into the loop

**None.** No failure to re-enter.

## Cross-reference

| Record | Path |
|---|---|
| Primary evidence (PHR) | `outputs/history/prompts/milestone_3/000-installer-complete.md` |
| Test contract | `outputs/milestones/milestone_3/tests_milestone_3.md` |
| Executable suite | `outputs/milestones/milestone_3/verify_milestone_3.py` |
| Raw critique rounds | `outputs/critique-log/m3-pass2/` |
