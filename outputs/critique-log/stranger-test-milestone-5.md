# Stranger Test — Milestone 5 (examples)

**Artifact type:** Stranger Test record (`PLAN.md` §9 layout, §4.5 grounding anchor)
**Milestone:** 5 of 5 — the worked example project
**Input:** the full five-document set, together (`PLAN.md` §7.6):
`spec_milestone_5.md`, `plan_milestone_5.md`, `tasks_milestone_5.md`, `workflow_milestone_5.md`, `tests_milestone_5.md`
— and, as this milestone's deliverable under test, the shipped example files
**Instruction given:** *implement this, ask no questions*
**Session:** fresh, zero-context — given only the example files
**Result: PASS** — all five areas derived; non-blocking gaps only, both consistent with stated Out-of-Scope

> Transcribed from the primary evidence in PHR `milestone_5/000`, which remains
> authoritative.

## What the zero-context session independently derived

| # | Area | Derived | Verdict |
|---|---|---|---|
| A | Project identity | The sample project's purpose, language, and dependency posture (Python 3, stdlib only) | Matched |
| B | CLI contract | The exact contract — four commands plus two error cases, with exit codes | Matched |
| C | Store behavior | The store's location and lifecycle, including the `QUOTE_DATA_DIR` hermetic-test override | Matched |
| D | Document shape | The five-document milestone structure and each document's contents | Matched |
| E | How to run it | How to run the kit against the sample brief, plus the GUIDE link | Matched |

Area B is the load-bearing one: the example ships *no* `quote.py`, so a stranger
deriving the complete CLI contract — every command and both error paths with their
exit codes — is the evidence that the brief is genuinely sufficient to implement
the tool without shipped source (FR-1).

## Gaps found — recorded, non-blocking

1. **No shipped `quote.py` implementation.** Explicitly Out of Scope: the example
   ships the kit's *output shape*, not a compiled artifact or source code.
2. **The default data-directory path is not pinned** to an exact string. The store
   is specified as a well-known user-data location, created on first use; the
   exact path is an implementation choice the brief deliberately leaves open.

Both are consistent with the spec's stated Out-of-Scope, so neither re-entered the
loop.

## Cross-reference

| Record | Path |
|---|---|
| Primary evidence (PHR) | `outputs/history/prompts/milestone_5/000-examples-complete.md` |
| Test contract | `outputs/milestones/milestone_5/tests_milestone_5.md` |
| Raw critique rounds | `outputs/critique-log/m5-pass1/`, `outputs/critique-log/m5-pass2/` |
| Example deliverables | `examples/sample-project/` |
