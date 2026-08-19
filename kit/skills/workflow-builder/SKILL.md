---
name: workflow-builder
description: >-
  Workflow-phase sub-skill. Produces the scenario-branching tree for a milestone:
  every path the milestone must handle, expressed as states and transitions.
  Every feature named in the spec/plan must be traceable to a node here.
version: 0.1.0
---

# Workflow Builder — the Scenario-Branching Tree

Write `workflow_milestone_N.md` (or `workflow.md`).

## Input
- The accepted spec and plan.

## Output
A scenario-branching tree: every path the milestone must handle, mapped to states and transitions (start, decision branches, terminal states, failure paths).

## Procedure
1. Carry the cumulative history and the cross-reference to the spec.
2. Enumerate the pipeline run states (start → each phase → build).
3. Add failure/retry states and verification states, each with pass/fail branches.
4. Add a feature-to-node traceability mapping.

## Edge cases / rules
- **No orphan features:** every feature in the spec/plan is traceable to a node; conversely every node is backed by a task and a test (Structural Completeness).
- Every scenario node must be covered by a test in `scenario-tester` (one test per node) — the Simplicity gate rejects untraceable features, and the completeness gate rejects untested nodes.