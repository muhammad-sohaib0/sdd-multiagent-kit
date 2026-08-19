---
name: research-ct-scan
description: >-
  Research-phase sub-skill. Decomposes a project brief using computational
  thinking to produce a Requirement Category Checklist — the base categories a
  spec always needs plus the conditional categories this specific project calls
  for. Use this first, before any document is written.
version: 0.1.0
---

# Research — Computational-Thinking Requirement Scan

Produce a Requirement Category Checklist specific to this exact project.

## Input
- The project brief (PLAN.md, README, or the furnished prompt).

## Output
A Markdown table with columns `category | required (base|conditional) | why needed` (or `n/a` for a rejected conditional category, with the reason). Row order: base categories first (in the fixed order Goal, User Scenarios, Functional Requirements, Edge Cases & Rules, Out of Scope, Acceptance Criteria), then conditional categories in the order derived.

**Write it to `outputs/requirement-checklist.md`.** It is a runtime working artifact, not one of the five milestone documents: `specify` reads it for every milestone, and the Structural Completeness Gate measures each spec against it, so it must be on disk at a fixed path rather than held in the session.

## Procedure
1. Read the brief. If it is empty, **HALT and ask the user for a brief**; never fabricate one.
2. Include the six base categories unconditionally.
3. Reason about what category of project this is and add only the conditional categories it genuinely needs — e.g. UI/UX, Data Model, API/Integration, Authentication/Security, CLI & Arguments, Performance/Scale, Deployment/Environment, Accessibility, Concurrency. Reject (with reason) any the project does not call for.

## Edge cases / rules
- **Installed-skill awareness:** for every conditional category, direct the invoking agent to list the skill/plugin directories of the tool it is running in (inspect the agent's own runtime). If it cannot enumerate them, treat installed-skill awareness as "none detected" and use generic boilerplate. If a skill matches a conditional category, draft that category with that skill's conventions; if several match, use the one whose description matches most closely; if none clearly matches, use generic boilerplate.
- Every category on this checklist is answered twice: `spec.md` states *what* and *why*; `plan.md` states *how*. Keep them separate.
- This scan also decides whether the project is large enough to need milestone splitting (handed to `milestone-builder`).