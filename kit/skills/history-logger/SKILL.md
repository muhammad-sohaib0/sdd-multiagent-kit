---
name: history-logger
description: >-
  Traceability sub-skill. Logs Prompt History Records (PHR) at every significant
  interaction and suggests Architecture Decision Records (ADR) when a decision
  meets the significance test. Every milestone's reasoning is preserved in
  written, human-readable form.
version: 0.1.0
---

# History Logger — PHR and ADR Records

Record every significant interaction and consequential decision.

## Input
- The phase transition or decision to record.

## Output
- A PHR file at `outputs/history/prompts/milestone_N/NNN-phase-name.md` (or `outputs/history/prompts/single-milestone/`).
- An ADR file at `outputs/history/adr/NNN-decision-title.md` when the significance test is met.

## Procedure
1. On every phase transition (after CT scan, constitution adoption, milestone breakdown, and per milestone: after specify, G1, Pass 1, clarify, plan/tasks/workflow/tests, G2, Pass 2, stranger-test, build) and every sub-skill failure, write a PHR capturing what was requested, what was produced, and a short rationale.
2. Assess each decision against the ADR significance test: real alternatives existed, the choice is hard to reverse, or it affects more than one milestone.
3. If the test is met, **suggest** an ADR and wait for human confirmation — never create one silently.

## Edge cases / rules
- A transition that produced no artifact is still recorded — `What was produced` is the literal string `none`; never skip the record.
- Constitution amendments (Article VII) **always** produce an ADR — no significance test for those, they're automatic.
- PHR/critique-log never embed secrets; env-var names only.
- PHRs are the readable narrative; the raw critique JSON lives separately in `critique-log/`.