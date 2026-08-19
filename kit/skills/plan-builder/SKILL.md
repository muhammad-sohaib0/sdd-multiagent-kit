---
name: plan-builder
description: >-
  Plan-phase sub-skill. Produces the milestone's technical "how": tech stack,
  architecture, data model, integration contracts, and rationale for each choice.
  Drafts `plan_milestone_N.md` from the accepted spec, reflecting any Clarify
  answers by construction.
version: 0.1.0
---

# Plan Builder — the Technical How

Write `plan_milestone_N.md` (or `plan.md`).

## Input
- The accepted spec (after Clarify, so the plan reflects the answers by construction).
- The constitution.

## Output
A plan with: tech stack, architecture, data model, API/integration approach, security notes, and a rationale for each key choice.

## Procedure
1. Carry the cumulative history and the cross-reference back to the spec.
2. State the tech stack and dependencies (prefer what is already in play — Article V Framework Trust).
3. Describe the architecture and data model with concrete paths/formats.
4. Explain the integration approach and security posture.
5. For each key choice, justify it; any standalone component beyond the Simplicity default (3) needs a written justification here.

## Edge cases / rules
- The plan states *how*; the spec states *what*. Never rewrite the spec's decisions in the plan.
- Every feature in the spec/plan must be traceable to a `workflow.md` scenario (Simplicity gate).
- Do not wrap a tool in a custom abstraction where using it directly would work (Article V).
- Forward references to a future milestone are gate violations.