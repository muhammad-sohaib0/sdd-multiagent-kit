# PHR 003 (milestone_1) — Stranger Test, Build, and Verification

- **Phase:** Milestone 1, Stranger Test → Build → Verification
- **Date:** bootstrap run

## Stranger Test

**What was requested:** hand the finished M1 five-document set to a fresh, zero-context session with a single instruction (implement this, ask no questions) and check contract parity.

**What was produced:** a fresh sub-agent (no prior bootstrap context) read only `spec_milestone_1`, `plan_milestone_1`, `tasks_milestone_1`, `workflow_milestone_1`, `tests_milestone_1` and independently derived:
- **A** the exact 13 deliverable file paths (kit file inventory) — matched the spec §4.1 exactly;
- **B** the six-model, ordered `critic_slots` panel and each model's provider — matched ADR-001 panel and order exactly;
- **C** the seven constitution article titles — matched PLAN.md §6 exactly;
- **D** the phase order with G1 (after spec, before Pass 1), Clarify (once, after Pass 1), G2 (after all five, before Pass 2) — matched FR-1 exactly;
- **E** the SKILL.md frontmatter and providers.yaml schema requirements — matched §4.2/§4.3 exactly.

**Result: PASS.** Contract parity achieved (spec AC-7, tests NT13). No divergence to feed back.

## Build

**What was requested:** execute `tasks_milestone_1.md` T2–T15 to materialize the 13 kit files.

**What was produced:** all 13 files built under `kit/`:
- `kit/SKILL.md` (master orchestrator: pipeline, gates, dispatch, standing rules)
- `kit/constitution.template.md` (seven articles verbatim)
- `kit/config/providers.yaml` (version 1, three providers, ordered ADR-001 `critic_slots`)
- ten sub-skill SKILL.md files (research-ct-scan, specify, plan-builder, task-breakdown, clarify-interview, milestone-builder, workflow-builder, scenario-tester, stranger-test, history-logger)

No `critique-loop` folder (deferred to M2). No secrets anywhere.

## Verification

**What was produced:** T16–T19 ran against the built kit.
- T16: all 13 files exist; all 11 SKILL.md carry `name`/`description`/`version`; exactly 10 sub-skill dirs, no `critique-loop` — PASS.
- T17: providers.yaml has `version: 1`, three providers (env-var names only), six ordered `critic_slots` matching ADR-001 order, no duplicates — PASS.
- T18: secret scan (sk-/AIza/Bearer patterns) across the 13 files — zero matches — PASS.
- T19: constitution template renders the seven article titles — PASS.
- T20: Stranger Test — PASS (above).

**Result: milestone M1 complete and verified.**

## Rationale

M1 delivered the kit's core process content, ran the loop on itself end-to-end (research → spec → Pass 1 → Clarify → plan/tasks/workflow/tests → G2 → Pass 2 → Stranger Test → build → verify), and all acceptance criteria (AC-1..AC-7) are met. The seed skill can now be retired; the built `kit/` is the self-hosting implementation. Milestones 2–5 remain.