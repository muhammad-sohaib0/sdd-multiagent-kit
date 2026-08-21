---
name: history-logger
description: >-
  Traceability sub-skill. Logs Prompt History Records (PHR) at every significant
  interaction and suggests Architecture Decision Records (ADR) when a decision
  meets the significance test. Every milestone's reasoning is preserved in
  written, human-readable form.
version: 0.1.1
---

# History Logger — PHR and ADR Records

Record every significant interaction and consequential decision.

## Input
- The phase transition or decision to record.

## Output
- A PHR file at `outputs/history/prompts/milestone_N/NNN-phase-name.md`.
- **Pre-milestone phases** — the CT scan, constitution adoption, and the milestone breakdown all run *before* milestone 1 exists, so their PHRs go in `outputs/history/prompts/milestone_0/`. Use this folder for every transition that precedes the first milestone; do not invent a per-project name for it.
- Single-milestone projects use `outputs/history/prompts/single-milestone/` for their milestone PHRs (their pre-milestone PHRs still go in `milestone_0/`).
- An ADR file at `outputs/history/adr/NNN-decision-title.md` when the significance test is met.

## Numbering
- **PHR numbering resets per folder** — each milestone folder starts again at `001` (and `milestone_0/` has its own `001`, `002`, …).
- **ADR numbering is global** across the project and never resets, so ADR-004 is the fourth decision of the whole project regardless of which milestone raised it.

## Procedure
1. On every phase transition and every sub-skill failure, write a PHR capturing what was requested, what was produced, and a short rationale. The transitions: after the CT scan, constitution adoption, and milestone breakdown (all three in `milestone_0/`), then per milestone after `specify`, G1, Pass 1, `clarify-interview`, **each of `plan`, `tasks`, `workflow`, `tests` separately**, G2, Pass 2, `stranger-test`, and build. `critique-loop` logs one PHR per round on top of these.
2. Name the file `NNN-phase-name.md`, where `phase-name` is a short kebab-case slug for the transition (`specify`, `g1-gate`, `pass1-critique`, `clarify`, `plan-builder`, `stranger-test`, `build`).
3. Assess each decision against the ADR significance test: real alternatives existed, the choice is hard to reverse, or it affects more than one milestone.
4. If the test is met, **suggest** an ADR and wait for human confirmation — never create one silently.

## Edge cases / rules
- A transition that produced no artifact is still recorded — `What was produced` is the literal string `none`; never skip the record.
- Constitution amendments (Article VII) **always** produce an ADR — no significance test for those, they're automatic.
- PHR/critique-log never embed secrets; env-var names only.
- PHRs are the readable narrative; the raw critique JSON lives separately in `critique-log/`.