---
name: scenario-tester
description: >-
  Test-phase sub-skill. Produces one test per node in the workflow tree plus one
  end-to-end real-user walkthrough of the whole tree, and maps each acceptance
  criterion to its covering test. Writes tests_milestone_N.md.
version: 0.1.1
---

# Scenario Tester — One Test per Workflow Node

Write `tests_milestone_N.md` (or `tests.md`).

## Input
- The workflow tree (from `workflow-builder`).
- The spec's acceptance criteria.

## Output
A test document with: a node-test table (one test per workflow node, each with a pass criterion), an acceptance-criterion mapping, and an end-to-end walkthrough.

## Procedure
1. Carry the cumulative history and the back-reference to the spec — first line `> Companion to: <path to this milestone's spec>`.
2. For each **leaf** node of the workflow tree (terminal states, decision branches, failure paths — not grouping parents, not `START`), write a test with a concrete pass criterion (not vague).
3. Give every test a stable id (`NT1`, `NT2`, …) and name the node it covers, so the traceability tables in `workflow.md` and `tasks.md` resolve.
4. Map each acceptance criterion to the test(s) that cover it.
5. Add one end-to-end real-user walkthrough of the whole tree — and make sure `tasks.md` has a task that creates it. A walkthrough named here but never built is the commonest way this document and the task list drift apart.

## Edge cases / rules
- This document is the verification contract, written **before** implementation (Article III).
- Pass criteria must be concrete and checkable — define terms like "perfect", "contract parity", and any thresholds inline so the test is self-contained.
- A branch with no test node → add the test; never leave a path untested. Any workflow node without a test is a completeness-gate violation.