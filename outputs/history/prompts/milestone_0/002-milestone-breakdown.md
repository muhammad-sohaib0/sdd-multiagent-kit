# PHR 002 — Milestone Breakdown (CT, Dependency-Ordered)

- **Phase:** Research — milestone split (PLAN.md §7)
- **Input:** PHR 000 decomposition; PLAN.md §11.3 repository structure
- **Date:** bootstrap run, session start

## What was requested

Decide whether the kit is large enough to require milestone splitting (§7.1), and if so, produce the ordered, dependency-safe milestone breakdown.

## What was produced

**Verdict: large enough — 5 milestones.**

The kit is a multi-part framework (process content + automation + installer + distribution + documentation) where each part is a separate deliverable with distinct dependencies. It is not a single-purpose project.

### The breakdown, in dependency order

| # | Milestone | Contents | Depends on | Why here |
|---|---|---|---|---|
| 1 | **Core process content** | `kit/SKILL.md`, `kit/constitution.template.md`, `kit/config/providers.yaml`, and ten pure-process sub-skills (research-ct-scan, specify, plan-builder, task-breakdown, clarify-interview, milestone-builder, workflow-builder, scenario-tester, stranger-test, history-logger) | — | The definition of the process is load-bearing: the scripts automate it, the installer copies it, the docs describe it. Nothing meaningful exists until this does. |
| 2 | **Critique engine** | `kit/scripts/orchestrate_critique_loop.py`, `kit/scripts/validate_critique.py`, and the `critique-loop` sub-skill | M1 | The loop skill must reference the scripts (they are its automation), and the scripts implement contracts defined in M1's providers.yaml and the critique schema — so both move here together, keeping the forward-reference gate closed. |
| 3 | **Installer system** | `bin/setup-wizard.js`, `installers/claude-code.js`, `installers/claude-desktop.js`, `installers/opencode.js`, `installers/antigravity.js` | M1, M2 | The installer copies the kit — the kit must be complete first. The adapter pattern is self-contained to this milestone. |
| 4 | **Distribution & repository** | `package.json`, npm packaging, `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `LICENSE`, `CHANGELOG.md`, `docs/GUIDE.md`, `docs/ARCHITECTURE.md`, `docs/BOOTSTRAP.md` | M1–M3 | Docs describe a real system and a real install flow; they cannot be written honestly before the thing they document exists. |
| 5 | **Examples** | `examples/sample-project/` | M1–M4 | A worked example demonstrates the finished kit — it is the last thing to produce because it exercises everything. |

### Why this split and not another

- **M1/M2 split** is driven by the forward-reference gate: the critique-loop skill's automation scripts do not exist until M2, so the skill itself must ship in M2 alongside them. All other sub-skills are pure process instructions with no script dependency and belong in M1.
- **M3 before M4**: GUIDE.md documents the setup wizard walkthrough; the wizard must be real first.
- **M5 last**: an example that demonstrates the system requires the system to exist.

## Rationale

Every milestone is self-contained (produces its full five-document set), dependency-ordered (nothing references a future milestone), and small enough that its documents remain reviewable. The gate in §5.3 will check each milestone's files for forward references as they are drafted.