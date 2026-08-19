# Stranger Test — Milestone 4 (repository documentation)

**Artifact type:** Stranger Test record (`PLAN.md` §9 layout, §4.5 grounding anchor)
**Milestone:** 4 of 5 — the open-source repository documentation layer
**Input:** the full five-document set, together (`PLAN.md` §7.6):
`spec_milestone_4.md`, `plan_milestone_4.md`, `tasks_milestone_4.md`, `workflow_milestone_4.md`, `tests_milestone_4.md`
— and, as this milestone's deliverable under test, the repository documentation itself
**Instruction given:** *implement this, ask no questions*
**Session:** fresh, zero-context — given only the repo docs
**Result: PASS** — all eight answers derived; non-blocking gaps only

> Transcribed from the primary evidence in PHR `milestone_4/001`, which remains
> authoritative.

## Why this milestone's test is shaped differently

M4's deliverable *is* documentation, so the property under test is the one
`PLAN.md` §11.1 states directly: any human contributor, or any AI tool
encountering the repository cold — including tools not on the supported list —
must be able to understand what this project is, how it works, and how to extend
it, entirely from what is inside the repository. The stranger was therefore asked
to answer, from the docs alone, the questions such a reader arrives with.

## What the zero-context session independently derived

| # | Question answered from the docs alone | Verdict |
|---|---|---|
| A | The install command(s) | Derived |
| B | The `/sdd` trigger and its per-tool origin | Derived |
| C | The three provider env-var names | Derived |
| D | The four-tool install-location table | Derived |
| E | How to add a new AI tool | Derived |
| F | How to add a new critic model | Derived |
| G | Private security reporting and its scope | Derived |
| H | The version, the license, and the `.gitignore` protections | Derived |

## Gaps found — recorded, non-blocking

1. **No hardcoded contact email** for security reports. `SECURITY.md` routes
   reporters through a security advisory or `SUPPORT.md` instead. Deliberate:
   the repository does not publish a maintainer address.
2. **Panel details are not restated in the docs** — they live in
   `kit/config/providers.yaml` (M1), which is the single source of truth by
   design (FR-4). A doc copy would be a second authority to drift.

Neither gap blocks a cold reader from installing, using, or extending the kit, so
neither re-entered the loop as a contract divergence.

## Follow-up defect found *outside* this test

The Stranger Test passed on the docs' *coverage*. A later completion pass found a
correctness defect this test's question set did not reach: `CONTRIBUTING.md`'s
worked example A (check E above — "how to add a new AI tool") omitted the
mandatory `name` export and returned a bare boolean from `confirmEnabled()`, so
an adapter built by following it literally made the wizard exit `2` at startup and
blocked every tool. The stranger derived *that* the docs explain how to add a
tool; it did not execute the example. Recorded here because it is exactly the kind
of blind spot §4.5 exists to surface: agreement that a doc is complete is not
evidence that its code runs. Fixed in the completion pass — see PHR
`milestone_5/003`, which added an executed-example check.

## Cross-reference

| Record | Path |
|---|---|
| Primary evidence (PHR) | `outputs/history/prompts/milestone_4/001-repo-docs-complete.md` |
| Test contract | `outputs/milestones/milestone_4/tests_milestone_4.md` |
| Raw critique rounds | `outputs/critique-log/m4-pass2/` |
