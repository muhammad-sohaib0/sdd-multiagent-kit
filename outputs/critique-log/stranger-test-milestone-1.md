# Stranger Test — Milestone 1 (core process content)

**Artifact type:** Stranger Test record (`PLAN.md` §9 layout, §4.5 grounding anchor)
**Milestone:** 1 of 5 — the kit's core process content
**Input:** the full five-document set, together (`PLAN.md` §7.6 — never any single file alone):
`spec_milestone_1.md`, `plan_milestone_1.md`, `tasks_milestone_1.md`, `workflow_milestone_1.md`, `tests_milestone_1.md`
**Instruction given:** *implement this, ask no questions*
**Session:** a fresh sub-agent with no prior bootstrap context
**Result: PASS** — contract parity (spec AC-7, tests NT13)

> This file is the record PLAN.md §9 places under `outputs/critique-log/`. It is
> transcribed from the primary evidence in PHR `milestone_1/003`, which remains
> authoritative; nothing here is reconstructed or inferred.

## Why this test exists

Seven critics agreeing is not proof of correctness — models can share a blind
spot, which is exactly the measurement decay `PLAN.md` §4.5 warns about. So once
Pass 2 concluded, the finished document set went to a session that had never seen
this project, with one instruction and no chance to ask questions. What that
session derives *from the documents alone* is the only evidence that the
documents, rather than the conversation around them, carry the contract.

Parity here means **contract parity, not byte parity** (spec AC-7): the stranger
must land on the same deliverables, panel, articles, and phase order — not the
same prose.

## What the zero-context session independently derived

| # | Check | Derived | Verdict |
|---|---|---|---|
| A | Deliverable file inventory | The exact 13 kit file paths | Matched spec §4.1 exactly |
| B | Critic panel | The ordered `critic_slots` panel and each model's provider | Matched the then-current ADR-001 panel and order exactly |
| C | Constitution | The seven constitution article titles | Matched `PLAN.md` §6 exactly |
| D | Phase order | G1 after the spec and before Pass 1; Clarify once, after Pass 1; G2 across all five before Pass 2 | Matched FR-1 exactly |
| E | Formats | The SKILL.md frontmatter fields and the `providers.yaml` schema | Matched §4.2 / §4.3 exactly |

The session also correctly derived that `critique-loop` is **not** among the 13
M1 deliverables — the milestone's most easily-missed boundary, since the sub-skill
is named throughout the pipeline while being owned by M2.

## Divergences fed back into the loop

**None.** No failure to re-enter, so the re-entry path (`PLAN.md` §4.4's round
safety cap, then escalation to the human) was not exercised for this milestone.

## Panel-composition note

Check B was run against the six-model ADR-001 panel, the panel in force when this
Stranger Test ran. ADR-003 later replaced the DeepSeek slot with
`mistralai/mistral-nemotron` and `meta/muse-glimmer-30b`, making the shipped panel
seven models. The finding — that the stranger derives the ordered slot list and
each slot's provider binding from the document set alone — is about the panel
being *fully specified in the documents*, and is unaffected by which models fill
the slots. Post-ADR-003, confirmation rounds 3–4 re-ran Pass 2 on the new panel
(critique-log `m1-pass2/`); a full Stranger Test re-run was waived for those
pin-level edits, with mechanical contract-parity re-verification performed
instead — recorded in PHR `milestone_1/002` and re-verified in PHRs
`milestone_1/004` and `milestone_1/005`.

## Cross-reference

| Record | Path |
|---|---|
| Primary evidence (PHR) | `outputs/history/prompts/milestone_1/003-stranger-test-build-and-verification.md` |
| Build completion re-verification | `outputs/history/prompts/milestone_1/004-build-completion-re-verification.md` |
| Strict re-verification | `outputs/history/prompts/milestone_1/005-build-strict-re-verification.md` |
| Test contract (NT13/NT14) | `outputs/milestones/milestone_1/tests_milestone_1.md` |
| Acceptance criterion | `spec_milestone_1.md` AC-7 |
