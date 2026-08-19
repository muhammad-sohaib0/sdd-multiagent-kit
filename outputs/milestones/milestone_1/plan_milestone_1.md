# SDD Multi-Agent Kit — Milestone 1 Plan

**Document:** `plan_milestone_1.md`
**Milestone:** 1 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_1/spec_milestone_1.md`

## Cumulative History

Same inherited context as the spec: the kit is an npm-distributed Spec-Driven Development framework for CLI coding agents; constitution is fixed (seven articles, `outputs/constitution.md`); critic panel locked at seven models/three keys/one free tier per ADR-001; retry policy per PHR milestone_0/003; deliverables under `outputs/`; shipped kit in the `PLAN.md` §11.3 repo layout. This plan realizes **Milestone 1's "how"** — the technical choices behind the core process content.

## 1. Tech Stack

- **Content format:** Agent-Skills-format Markdown (`SKILL.md` with YAML frontmatter: `name`, `description`, `version`), the shared standard all four target tools read (PLAN.md §10.3). No proprietary format — the kit ships exactly what the tools ingest.
- **Configuration format:** YAML (`kit/config/providers.yaml`). YAML is the natural fit for structured key/value configuration and is dependency-free to parse.
- **Dependencies:** **none for M1 content.** The 13 files are plain Markdown/YAML. No runtime library is introduced (Article V — Framework Trust, Article IV — Simplicity). The M2 orchestration scripts may add a parser library later; M1 itself adds none.
- **Language for prose/instructions:** Markdown, consistent with the Agent-Skills standard and with how the four target tools surface skill content.

**Rationale:** matching the Agent-Skills standard means one identical content set installs into all four tools with only the install location differing (PLAN.md §10.3) — no per-tool content forks, which keeps US-4 extensibility and the Stranger Test (AC-7) tractable.

## 2. Architecture

A **master skill + ten sub-skills** composition, each sub-skill an independent SKILL.md unit:

```
kit/SKILL.md                         # master orchestrator (the pipeline + the two gates)
kit/skills/{research-ct-scan, specify, plan-builder, task-breakdown,
            clarify-interview, milestone-builder, workflow-builder,
            scenario-tester, stranger-test, history-logger}/SKILL.md
```

The ten sub-skills are exactly the spec §4.1 inventory: `research-ct-scan`, `specify`, `plan-builder`, `task-breakdown`, `clarify-interview`, `milestone-builder`, `workflow-builder`, `scenario-tester`, `stranger-test`, `history-logger`. There is no `critique-loop` folder in M1 (it and the scripts are M2).

- **Master skill:** defines the phase order (spec §3 FR-1), the G1/G2 gate checkpoints, and dispatches to sub-skills. It is deliberately *thin* in the sense that it does **not** duplicate a sub-skill's procedure — it still holds the orchestration responsibilities (pipeline order, gate checkpoints, dispatch map, standing adjudication/stopping rules), which are coordination, not sub-skill procedure. Keeps a single source of truth for the pipeline.
- **Each sub-skill:** a self-contained unit with its input → output and edge-case rules (spec §3 FR-2). Because they are independent, a sub-skill can be tested alone (Article I — Standalone-First) and replaced without touching the others (Article II — Observable Interfaces: each exposes a defined contract).
- **Gates:** implemented as master-skill checkpoints (not sub-skills), per spec §3A — they run on the spec (G1) and on all five documents (G2). This keeps the deliverable inventory at exactly ten sub-skills and avoids a "gates as components" inflation the Simplicity gate forbids.
- **`critique-loop` + scripts:** explicitly deferred to M2 (spec §3, §7); M1 states the critique invariant and marks the executable step "(automation arrives in M2)".

**Rationale:** the composition mirrors the natural decomposition the CT scan produced (PHR milestone_0/000). Each sub-skill maps to one phase; the master is the only place the whole sequence lives — so reordering phases is a one-file change.

## 3. Data Model (kit content)

All paths under the kit repo layout (`PLAN.md` §11.3); the 13-file inventory is the spec's §4.1 table verbatim. Key contracts:

- **`kit/SKILL.md`** — frontmatter `name: sdd-multiagent-kit`, `description`, `version`; body: pipeline order, G1/G2 checkpoint rules, sub-skill dispatch map, and the standing adjudication/stopping rules.
- **`kit/constitution.template.md`** — the seven articles rendered verbatim from PLAN.md §6 (spec §3 FR-3). Preamble notes it is adopted once and edited only via amendments.
- **`kit/config/providers.yaml`** — the spec §4.3 schema: `version: 1`, three providers each with `id`/`key_env`/`tier`/`models`, and the ordered `critic_slots` list binding model→provider. Validation: every slot.model exists under its provider's models; no duplicates (spec §3 FR-4).
- **Each `kit/skills/<name>/SKILL.md`** — frontmatter `name`/`description`/`version`; body: input, output, edge-case rule(s) per the spec's FR-2 table, and (for the phase sub-skills) pointers to the outputs they read/write (spec §4.5).

## 4. Integration Approach

- **Provider integrations:** expressed as configuration only (providers.yaml), on the free tier, with each provider reading exactly one env var by name. The actual HTTP calls are M2. M1's contract is that the config carries the seven verified-reachable model IDs (incl. the ADR-001 correction) and the ordered `critic_slots`.
- **Target-tool integration:** none in M1 (installer is M3). M1 content is already in the Agent-Skills format, so M3's adapters only need to copy the folder into the right directory — no content transformation.
- **The kit running itself:** the master skill orchestrates *user* projects; for the bootstrap, the process now authors the 13 files, which then become the running kit (spec §3 FR-1 "About build").

## 5. Security

- No secrets anywhere: the kit stores only env-var **names** (e.g. `NVIDIA_NIM_API_KEY`) in providers.yaml and skill instructions — a name is an identifier, not a secret value; no key material is ever written. The shipped kit contains no key values (spec §6).
- No logging of key material; PHR/critique-log never embed secrets.
- Secret-detection is a verification step (tests), not a runtime feature, in M1 — detection patterns per spec §6 / tests NT20 (T18).

## 6. Rationale for Key Choices (Simplicity Justifications)

| Choice | Justification |
|---|---|
| Master + ten sub-skills, no gate sub-skills | Matches the CT decomposition; gates as checkpoints avoids component inflation. Per the spec §3A rule, the kit's 13 files count as **one** deliverable (the kit), so the Simplicity gate measures **0** standalone components added beyond the kit — under the default of 3, no written justification required. |
| YAML + Markdown, zero runtime deps | Matches the Agent-Skills standard; nothing to install or maintain for M1 content. |
| `critic_slots` data-driven (M1) | Prevents hard-coded panel in M2 and keeps model additions data-only (US-4). |
| Critique engine deferred to M2 | The scripts are M2's deliverable; pulling them into M1 would force a forward reference and bloat this milestone. Named in Out of Scope, not forgotten. |
| No per-tool content forks | One content set, four install locations (PLAN.md §10.3) — simplest structure that works (Article IV). |

The 13 content files form a single deliverable (the kit), so this plan introduces **0 standalone components** beyond the kit — under the 3-per-milestone Simplicity default, so no justification is required.

## 7. Acceptance Mapping

This plan satisfies the spec's §8 criteria: AC-1 (13 files at §4.1 paths), AC-2 (providers.yaml per §4.3, ADR-001 panel, ordered critic_slots), AC-3 (no secrets), AC-4 (ten sub-skills with contracts), AC-5 (pipeline order + deferrals), AC-6 (constitution template verbatim), AC-7 (Stranger Test contract parity). Verification of each is the job of `tasks_milestone_1.md` and `tests_milestone_1.md`.

## 8. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan (this file) | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests | `outputs/milestones/milestone_1/tests_milestone_1.md` |