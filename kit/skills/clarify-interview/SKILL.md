---
name: clarify-interview
description: >-
  Clarify-phase sub-skill. Asks the human only the questions an AI genuinely
  could not infer — compiled into a needs_clarify list by Pass 1 — and folds the
  answers back into the spec. Runs once per milestone, after Pass 1.
version: 0.1.0
---

# Clarify Interview — Ask Only What an AI Cannot Infer

Turn the compiled `needs_clarify` list into concise questions and fold the answers into the spec.

## Input
- The compiled `needs_clarify` list — a set of `{section, problem, why_it_matters}` items compiled by Pass 1 from critics' `needs_clarify`-tagged issues, persisted as a Markdown bullet list at `outputs/milestones/milestone_N/needs_clarify.md` — each entry written `- **section**: problem — why_it_matters` (single-milestone: `outputs/needs_clarify.md`).

## Output
- Human answers folded into the spec (the authoritative *what*).

## Procedure
1. Read the compiled list. If it is empty, **skip gracefully and ask nothing**.
2. Otherwise ask each question concisely; ask only what an AI could not infer. (Start from the brief's open decisions where relevant.)
3. Fold each answer into the spec. The plan is drafted afterwards, so it reflects the answers by construction.

## Edge cases / rules
- A folded answer that breaks consistency elsewhere → surfaced again in Pass 2 (a consistency edit, not a second Clarify round; Clarify runs once per milestone).
- If the human declines or gives an invalid answer → record the refusal in the PHR, drop that question, and note it in the milestone's Out of Scope rather than silently defaulting.
- Clarify itself runs **once per milestone**.