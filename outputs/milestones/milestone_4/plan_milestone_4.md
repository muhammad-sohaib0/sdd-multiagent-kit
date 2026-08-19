# SDD Multi-Agent Kit — Milestone 4 Plan

**Document:** `plan_milestone_4.md`
**Milestone:** 4 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_4/spec_milestone_4.md`

## Cumulative History

Same as the spec. M4 realizes the "how" of the documentation layer.

## 1. Tech Stack / Format

- **Format:** Markdown for all eleven files (docs and root guides). MIT license text for LICENSE. Plain text/git for the repo metadata.
- **Dependencies:** none — this is documentation, not code.

## 2. Architecture / Structure (PLAN.md §11.2, §11.3)

```
README.md            # what/why/quickstart + adapted-patterns credit + link to GUIDE
CLAUDE.md            # agent instructions for Claude-family tools
AGENTS.md            # cross-tool agent instructions (AGENTS.md convention)
CONTRIBUTING.md      # how to contribute; add-a-tool + add-a-model worked examples
SECURITY.md          # private reporting + scope
SUPPORT.md           # where to ask questions / file issues
LICENSE              # MIT text
CHANGELOG.md         # 0.1.0 initial release
docs/GUIDE.md        # setup wizard walkthrough, critique loop, milestones
docs/ARCHITECTURE.md # readable architecture explanation
docs/BOOTSTRAP.md    # historical record of building the kit on itself
.gitignore           # exclude .env, node_modules, outputs/, critique-log, temp
```

## 3. Content Sources

- README quickstart: `npm install -g sdd-multiagent-kit && sdd-setup` (M3).
- Trigger: `/sdd`; env vars: `NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY` (M1/M3).
- Critique loop / milestones: drawn from the M1 master skill and the process the bootstrap actually ran.
- ARCHITECTURE: master skill + ten sub-skills + critique engine + installer adapter pattern.
- BOOTSTRAP: the historical narrative of this run (M1–M5) using the kit on itself.

## 4. Consistency

All commands, paths, env-var names, and the trigger must match the built kit. Verification cross-checks each doc's key strings against the actual `kit/`, `bin/`, `installers/` content (AC-4).

## 5. Security

Docs never contain secret values; `.gitignore` excludes `.env`, secrets, `node_modules`, and transient `outputs/critique-log`/temp artifacts so secrets and noise never enter version control (AC-5).

## 6. Rationale (Simplicity Justifications)

| Choice | Justification |
|---|---|
| Markdown everywhere | Zero tooling; matches the Agent-Skills/AGENTS conventions. |
| One README + three docs/ guides | Covers contributor, agent, and deep-dive readers without a docs site. |
| Credit in README | Required by §11.2 and good attribution. |

M4 introduces 0 standalone components beyond the kit content set. No Simplicity-justification burden.

## 7. Acceptance Mapping

AC-1 (eleven files non-stub) / AC-2 (README credit) / AC-3 (CONTRIBUTING examples) / AC-4 (consistency) / AC-5 (git + .gitignore) — verified in `tasks_milestone_4.md` / `tests_milestone_4.md`.

## 8. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_4/spec_milestone_4.md` |
| Plan (this file) | `outputs/milestones/milestone_4/plan_milestone_4.md` |
| Tasks | `outputs/milestones/milestone_4/tasks_milestone_4.md` |
| Workflow | `outputs/milestones/milestone_4/workflow_milestone_4.md` |
| Tests | `outputs/milestones/milestone_4/tests_milestone_4.md` |