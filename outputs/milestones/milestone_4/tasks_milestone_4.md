# SDD Multi-Agent Kit — Milestone 4 Tasks

**Document:** `tasks_milestone_4.md`
**Milestone:** 4 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_4/spec_milestone_4.md`

## Cumulative History

Same as the spec/plan. Ordered build plan for the documentation layer.

## Build Order

### Group A — Verification contract (before content)

- **T1 — Define the M4 verification suite** (`tests_milestone_4.md`). Contract the docs must pass (AC-1..AC-5).

### Group B — Root docs `[P]` (independent)

- **T2 — Write `README.md`** — what/why, quickstart (`npm install -g sdd-multiagent-kit && sdd-setup`), link to GUIDE, and the clearly-marked acknowledgement of `github/spec-kit` + `panaversity/spec-kit-plus` (AC-2).
- **T3 — Write `CLAUDE.md`** and **T4 — `AGENTS.md`** — agent instructions for the repo.
- **T5 — Write `CONTRIBUTING.md`** — contribution guide with a full worked example for adding a new AI tool (one `installers/*.js` adapter + registration, §11.4) and a new critic model (`kit/config/providers.yaml`) (AC-3).
- **T6 — Write `SECURITY.md`** and **T7 — `SUPPORT.md`** — private reporting + scope; where to ask/file.
- **T8 — Write `LICENSE`** (MIT text) and **T9 — `CHANGELOG.md`** (0.1.0 initial release).

### Group C — `docs/` guides

- **T10 — Write `docs/GUIDE.md`** — setup-wizard walkthrough, how the critique loop works, how milestones work.
- **T11 — Write `docs/ARCHITECTURE.md`** — readable architecture explanation (master skill, sub-skills, critique engine, installer adapters).
- **T12 — Write `docs/BOOTSTRAP.md`** — historical record of building the kit on itself (M1–M5), read-only.

### Group D — Repo hygiene

- **T13 — Write `.gitignore`** and **init the git repository** — `.gitignore` excludes `.env`, secrets, `node_modules`, `outputs/critique-log`, temp (AC-5).

### Group E — Verification

- **T14 — Presence + non-stub check** — all eleven files exist and are substantive (AC-1).
- **T15 — Consistency check** — docs' commands/paths/env-var names/trigger match the built kit (AC-4).
- **T16 — Credit check** — README acknowledges the two sources (AC-2).
- **T17 — CONTRIBUTING check** — contains add-a-tool and add-a-model examples (AC-3).
- **T18 — Secret scan** — no secret values in the docs or staged files.

**Verification failure handling:** T14–T18 failure → fix and re-run (internal).

## Status

| Task | Status |
|---|---|
| T1 | done (tests doc) |
| T2–T13 | done (all eleven deliverables + `.gitignore` + git init) |
| T14–T18 | done (all verification passed) |