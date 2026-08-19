---
name: milestone-builder
description: >-
  Builds the dependency-ordered milestone breakdown for a project. Decides
  whether a brief is large enough to need splitting and, if so, orders the
  milestones so nothing ever depends on something not yet established.
version: 0.1.0
---

# Milestone Builder — Split and Order

Turn the Requirement Category Checklist and brief into ordered delivery milestones.

## Input
- The project brief and the Requirement Category Checklist.
- The cumulative history (goal, constraints, constitution).

## Output
- A decision: single-milestone or ordered multi-milestone.
- For multi-milestone: an ordered list of milestones with a one-line scope each, in dependency order (nothing depends on a future milestone's artifact).

## Procedure
1. Decide whether the project is large enough to need splitting (computational thinking). Small, single-purpose projects stay as **one milestone**.
2. If splitting, order the milestones so each depends only on what earlier milestones established.
3. For each milestone, hand the goal and its dependency context to `specify`.

## Edge cases / rules
- **Single-milestone layout:** the five documents sit at the root of `outputs/` (`spec.md`, `plan.md`, `tasks.md`, `workflow.md`, `tests.md`) — no `_milestone_N` suffix — and use `outputs/history/prompts/single-milestone/` for PHRs.
- **Multi-milestone layout:** ordered folders `outputs/milestones/milestone_N/`, each with the five `_milestone_N` documents.
- If a milestone references a future milestone's artifact, that is a forward-reference gate violation: the milestones are in the wrong order and must be reordered.