# SDD Multi-Agent Kit — Milestone 3 Plan

**Document:** `plan_milestone_3.md`
**Milestone:** 3 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_3/spec_milestone_3.md`

## Cumulative History

Same as the spec. M3 realizes the "how" of the installer.

## 1. Tech Stack

- **Language:** Node.js (CommonJS) for `bin/setup-wizard.js` and all four `installers/*.js`. Node is the natural home for an npm package and needs no build step.
- **Dependencies:** **none** for the wizard at runtime — interactive prompts are read from `process.stdin` and `readline` (stdlib). `fs`/`path`/`os` for detection and copying. Zero runtime deps keeps `npm install` trivial (Article IV/V).
- **Kit content:** copied from the shipped `kit/` folder (M1+M2) as-is.

## 2. Architecture

```
bin/setup-wizard.js          # entry point (bin: sdd-setup); orchestrates the flow
installers/claude-code.js    # detect/install/confirmEnabled
installers/claude-desktop.js
installers/opencode.js
installers/antigravity.js
```

- **Wizard** owns the flow: read the three keys → offer Pakistani-guide slot → discovery guards → run each adapter's `detect()` → let the user choose → `install()` each chosen → `confirmEnabled()` → report. It never contains tool-specific path logic; it delegates to adapters.
- **Adapters** are the only place tool-specific logic lives (`detect`, `install`, `confirmEnabled`). This is what makes adding a tool a one-file change (PLAN.md §11.4): files under `installers/` are auto-discovered — no central registry.
- **Shared copy helper:** the wizard derives the kit source by walking parents to a `package.json` with `name: sdd-multiagent-kit` + sibling `kit/SKILL.md`, then passes the single `kit` dir path to `install(kitPath)`; each adapter decides the destination per §10.3.

## 3. Data Model

- **Kit source:** a single absolute `kit/` directory path (nearest matching ancestor; monorepo-safe). The copy writes each source file at its relative path into the destination; it never deletes other files in the destination.
- **Install destination per tool (§10.3):**
  - Claude Code: `${HOME}/.claude/skills/sdd-multiagent-kit/` (user-level; no project-local install in this milestone).
  - Claude Desktop: same path as Claude Code (shared config); `detect()` verifies the desktop app's own config dir (per-platform).
  - OpenCode: reads `.claude/skills/` — no separate copy when already kit-populated; real copy (refresh) otherwise.
  - Antigravity: `${HOME}/.agents/skills/sdd-multiagent-kit/` — separate copy, canonical `Invocation: /sdd` re-asserted.
- **Env config:** keys are onboarding-only — held in memory, never written/echoed/used, discarded on exit; the wizard reminds the user to set the env vars in their own shell profile or `.env`.

## 4. Integration Approach

- `package.json` `bin` exposes `sdd-setup` → the wizard. `files` ships `kit/`, `bin/`, `installers/`, plus `LICENSE`/`README.md` when present.
- The `/sdd` trigger: the three native tools derive it from the copied skill folder/frontmatter (`name: sdd-multiagent-kit`); for Antigravity the adapter writes the canonical `Invocation: /sdd` phrase into the copied `SKILL.md` description (replacing any stale invocation line; the injection is adapter-owned content layered on the kit-owned copy).
- The wizard reads keys from the terminal (TTY-only, masked); on completion it reminds the user to set the three env vars in their shell profile or `.env`. Keys never enter the repo or any file.

## 5. Security

- **Security:**
  - Keys collected in-memory only; never written to `kit/`, the repo, or logs; discarded on exit. Key-entry hygiene: empty/whitespace-only = skip; internal whitespace/control rejected + re-prompted.
  - Install copies only the kit content; it never reads or writes other secrets.
  - No secrets in logs: engine/PTY runs verified no key-shaped values leak into `kit/` or `outputs/`.

## 6. Rationale (Simplicity Justifications)

| Choice | Justification |
|---|---|
| Node stdlib only, zero runtime deps | npm package; keeps install trivial (Article IV). |
| Adapter pattern | Adding a tool = one file dropped into `installers/`, auto-discovered, no `kit/` change (PLAN.md §11.4, US-4). |
| Wizard owns flow, adapters own paths | Single place per tool for tool-specific logic; single place for the flow. |
| Env-var indirection for keys | Keys never committed; onboarding-only collection; matches M1/M2 security stance. |

M3 introduces 1 standalone component beyond the kit (the installer) — under the Simplicity default of 3.

## 7. Acceptance Mapping

AC-1 (five files + adapter interface) / AC-2 (keys + guide slot) / AC-3 (graceful detection/failure) / AC-4 (locations + trigger per §10.3) / AC-5 (package.json + no secrets) / AC-6 (sdd-setup runnable) — verified in `tasks_milestone_3.md` / `tests_milestone_3.md`.

## 8. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_3/spec_milestone_3.md` |
| Plan (this file) | `outputs/milestones/milestone_3/plan_milestone_3.md` |
| Tasks | `outputs/milestones/milestone_3/tasks_milestone_3.md` |
| Workflow | `outputs/milestones/milestone_3/workflow_milestone_3.md` |
| Tests | `outputs/milestones/milestone_3/tests_milestone_3.md` |