---
name: workflow-builder
description: >-
  Workflow-phase sub-skill. Produces the scenario-branching tree for a milestone:
  every path the milestone must handle, expressed as states and transitions.
  Every feature named in the spec/plan must be traceable to a node here.
version: 0.1.1
---

# Workflow Builder — the Scenario-Branching Tree

Write `workflow_milestone_N.md` (or `workflow.md`).

## Input
- The accepted spec and plan.

## Output
A scenario-branching tree: every path the milestone must handle, mapped to states and transitions (start, decision branches, terminal states, failure paths).

## Procedure
1. Carry the cumulative history and the back-reference to the spec — first line `> Companion to: <path to this milestone's spec>`.
2. Enumerate the states of **what this milestone builds** — for a CLI, its runtime paths; for a service, its request paths. (Do not model the kit's own pipeline phases here; that is this skill's process, not the product's behavior.)
3. Add failure/retry states and verification states, each with pass/fail branches.
4. Give every node a stable id (`N1`, `N2`, …; sub-branches `N4a`, `N4b`). Ids are permanent — `tests.md` and `tasks.md` reference them.
5. Add a feature-to-node traceability mapping.

## Edge cases / rules
- **Which nodes need a test:** every **leaf** node — a terminal state, a decision branch actually taken, or a failure path. A parent node that only groups its children is covered by them and needs no test of its own; structural markers like `START` are not nodes for testing purposes. State this explicitly in the tree so `scenario-tester` and the completeness gate agree on the count.
- **No orphan features:** every feature in the spec/plan is traceable to a node; conversely every leaf node is backed by a task and a test (Structural Completeness).
- Every leaf node must be covered by a test in `scenario-tester` (one test per leaf) — the Simplicity gate rejects untraceable features, and the completeness gate rejects untested nodes.