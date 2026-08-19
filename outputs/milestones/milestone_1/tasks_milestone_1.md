# SDD Multi-Agent Kit — Milestone 1 Tasks

**Document:** `tasks_milestone_1.md`
**Milestone:** 1 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_1/spec_milestone_1.md`

## Cumulative History

Same as the spec/plan. This file is the ordered, executable build plan for the 13 kit-content files. It follows the plan's tech stack (Markdown/YAML, zero deps), the spec's §4.1 inventory, and the constitution. **Tests are ordered before the implementation they verify** (Article III).

## Build Order

Tests-first grouping: the verification contract (T1–T4) is defined before the content it checks is authored; the content files are then built and verified against it.

### Group A — Verification contract (before any content)

- **T1 — Define the M1 verification suite** (`outputs/milestones/milestone_1/tests_milestone_1.md`). Define every node test and the end-to-end walkthrough that M1's build must pass. This is the contract the build is checked against. (Article III: tests exist and are reviewable before implementation.) *Note: this document is already produced in the milestone-doc phase (it is `tests_milestone_1.md`); T1 is the ordering guarantee that verification exists before the content is authored, and the build simply consumes the existing tests doc.*

### Group B — Content scaffold `[P]` (independent, can run in parallel)

- **T2 — Create the kit directory structure.** Create `kit/`, `kit/config/`, and the ten sub-skill folders: `kit/skills/research-ct-scan`, `kit/skills/specify`, `kit/skills/plan-builder`, `kit/skills/task-breakdown`, `kit/skills/clarify-interview`, `kit/skills/milestone-builder`, `kit/skills/workflow-builder`, `kit/skills/scenario-tester`, `kit/skills/stranger-test`, `kit/skills/history-logger`. Nothing else (no `critique-loop` in M1).
- **T3 — Author `kit/config/providers.yaml`** per spec §4.3 (version, three providers, ordered `critic_slots`; ADR-001 model set; env-var names only; no secrets). Verify against AC-2.

### Group C — Content files (each is one task; internally sequential, independent of each other) `[P]`

- **T4 — Author `kit/constitution.template.md`** — seven articles verbatim from PLAN.md §6 (AC-6).
- **T5 — Author `kit/skills/research-ct-scan/SKILL.md`** — contract per spec FR-2.
- **T6 — Author `kit/skills/specify/SKILL.md`** — contract per spec FR-2.
- **T7 — Author `kit/skills/plan-builder/SKILL.md`** — contract per spec FR-2.
- **T8 — Author `kit/skills/task-breakdown/SKILL.md`** — contract per spec FR-2.
- **T9 — Author `kit/skills/clarify-interview/SKILL.md`** — contract per spec FR-2.
- **T10 — Author `kit/skills/milestone-builder/SKILL.md`** — contract per spec FR-2.
- **T11 — Author `kit/skills/workflow-builder/SKILL.md`** — contract per spec FR-2.
- **T12 — Author `kit/skills/scenario-tester/SKILL.md`** — contract per spec FR-2.
- **T13 — Author `kit/skills/stranger-test/SKILL.md`** — contract per spec FR-2.
- **T14 — Author `kit/skills/history-logger/SKILL.md`** — contract per spec FR-2.

### Group D — Orchestration (depends on the ten sub-skills existing)

- **T15 — Author `kit/SKILL.md`** — the master orchestrator: pipeline order, G1/G2 gate checkpoints, sub-skill dispatch, critique invariant "(automation arrives in M2)", standing adjudication/stopping rules (AC-5). Depends on T5–T14 (it references them by name).

### Group E — Verification (depends on all content)

- **T16 — Frontmatter & inventory check (AC-1/AC-4).** Assert the 13 files exist at spec §4.1 paths; assert each SKILL.md carries `name`/`description`/`version` (schema per spec §4.2, e.g. `version: 0.1.0`); assert exactly ten sub-skills (no `critique-loop`). Checked by directory+frontmatter inspection.
- **T17 — providers.yaml validation (AC-2).** Parse YAML; assert `critic_slots` order, model→provider binding, no duplicates, seven models, env-var names only (spec §4.3).
- **T18 — Secret scan (AC-3).** Run the detection patterns (spec §6 / tests NT20) against the 13 files; assert zero matches (allowlist empty).
- **T19 — Constitution verbatim check (AC-6).** Assert `constitution.template.md` renders the seven articles verbatim from PLAN.md §6.
- **T20 — Stranger Test (AC-7).** Hand the finished five-document set — `spec_milestone_1`, `plan_milestone_1`, `tasks_milestone_1`, `workflow_milestone_1`, `tests_milestone_1` — to a fresh zero-context session; assert contract parity (13 paths, seven models + ordered `critic_slots`, seven articles verbatim).

**Verification failure handling (T16–T20):** on T16–T19 failure → fix the artifact and re-run that check (internal to build; not a critique-loop round). On T20 failure → the divergence is fed back as a new critique-loop issue (the one rule the loop may not reason around). Every failure logs a PHR. Mirrors workflow §4 B4.

### Dependency note

T15 depends on T5–T14 (references them). All Group C tasks are independent of each other (`[P]`). No task depends on a future milestone's artifact — nothing references `critique-loop`, the M2 scripts, the installer, or docs (forward-reference gate). T20 is the last task and the milestone's final gate.

## Status

| Task | Status |
|---|---|
| T1 | completed (tests doc = `tests_milestone_1.md`) |
| T2–T15 | completed (13 kit files built under `kit/`) |
| T16 | completed (13 files + frontmatter verified) |
| T17 | completed (providers.yaml validated) |
| T18 | completed (secret scan clean) |
| T19 | completed (constitution verbatim) |
| T20 | completed (Stranger Test passed) |