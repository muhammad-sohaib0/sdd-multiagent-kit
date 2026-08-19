---
name: scenario-tester
description: >-
  Test-phase sub-skill. Produces one test per node in the workflow tree plus one
  end-to-end real-user walkthrough of the whole tree, and maps each acceptance
  criterion to its covering test. Writes tests_milestone_N.md.
version: 0.1.0
---

# Scenario Tester — One Test per Workflow Node

Write `tests_milestone_N.md` (or `tests.md`).

## Input
- The workflow tree (from `workflow-builder`).
- The spec's acceptance criteria.

## Output
A test document with: a node-test table (one test per workflow node, each with a pass criterion), an acceptance-criterion mapping, and an end-to-end walkthrough.

## Procedure
1. Carry the cumulative history and the cross-reference to the spec.
2. For each workflow node, write a test with a concrete pass criterion (not vague).
3. Map each acceptance criterion to the test(s) that cover it.
4. Add one end-to-end real-user walkthrough of the whole tree.

## Edge cases / rules
- This document is the verification contract, written **before** implementation (Article III).
- Pass criteria must be concrete and checkable — define terms like "perfect", "contract parity", and any thresholds inline so the test is self-contained.
- A branch with no test node → add the test; never leave a path untested. Any workflow node without a test is a completeness-gate violation.