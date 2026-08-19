---
name: specify
description: >-
  Specify-phase sub-skill. Drafts a milestone's spec — the authoritative "what"
  this milestone needs to do and why, never the "how". Produces the document
  that Pass 1 of the critique loop and the G1 gate are run against.
version: 0.1.0
---

# Specify — Draft the Milestone Spec

Write `spec_milestone_N.md` (or `spec.md` for a single-milestone project).

## Input
- The adopted constitution (`outputs/constitution.md`).
- The Requirement Category Checklist from `research-ct-scan`.
- The cumulative history inherited from prior milestones.

## Output
A spec with a real, substantive section for every category on the checklist: Goal, User Scenarios, Functional Requirements, Edge Cases & Rules, Out of Scope, Acceptance Criteria, plus the conditional categories. Each section states *what* is needed and *why* it matters to the user — never *how*.

## Procedure
1. Open with a **Cumulative History** summarizing the goal, key decisions, what already exists, and constraints in force.
2. Draft each checklist category in full (no stubs, no placeholders).
3. Name in **Out of Scope** anything deliberately deferred to a later milestone.
4. End with a fixed **Cross-Reference** section pointing to the milestone's `plan`, `tasks`, `workflow`, and `tests`.

## Edge cases / rules
- A category on the checklist may not be left out or stubbed — that is a missing section, caught by the G1 gate, not something the critique loop may "improve".
- Acceptance Criteria must be concrete and testable (used later by `scenario-tester` and the Stranger Test).
- The spec answers what/why only; if a technical choice is needed, leave it to `plan-builder`.