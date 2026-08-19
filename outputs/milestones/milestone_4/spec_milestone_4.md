# SDD Multi-Agent Kit — Milestone 4 Spec

**Document:** `spec_milestone_4.md`
**Milestone:** 4 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_4/spec_milestone_4.md`

## Cumulative History

Inherited from M1 (kit content), M2 (critique engine), M3 (installer + adapters + package.json), all verified. This milestone produces the repository documentation layer that PLAN.md §11 requires: the root files (§11.2) and `docs/` that make the repository fully self-describing — readable without any additional context by a human contributor or an unfamiliar AI tool — what it is, how it works, how to extend it — with the plan/tasks + constitution + PHR/ADR patterns credited (§11.2, §5).

## Goal

Deliver the open-source repository documentation: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `LICENSE`, `CHANGELOG.md`, and `docs/{GUIDE,ARCHITECTURE,BOOTSTRAP}.md`. Together they let anyone pick the repo up cold and understand, install, use, contribute to, and extend it without anything explained outside the repo.

## User Scenarios

**US-1 — A human contributor reads the repo.** README explains what/why + quickstart; CONTRIBUTING walks through adding a new AI tool (adapter) and a new critic model; ARCHITECTURE explains the system; SUPPORT says where to ask; SECURITY says how to report privately.

**US-2 — An unfamiliar AI tool picks it up cold.** AGENTS.md (cross-tool convention) plus CLAUDE.md (Claude-family) give an agent everything needed to work inside the repo, and ARCHITECTURE is readable without source.

**US-3 — Credit for adapted patterns.** The plan/tasks split, constitution-as-articles, and PHR/ADR history are acknowledged as adapted from `github/spec-kit` and `panaversity/spec-kit-plus` (§11.2), clearly marked in README.

## Functional Requirements

**FR-1 — `README.md`.** What the project is, why it exists, a quickstart (`npm install -g sdd-multiagent-kit && sdd-setup`, where `sdd-multiagent-kit` is the npm package name and `npm install -g` puts its `bin` — `sdd-setup` — on PATH as a global command, `sdd-setup` is its `bin`, and `sdd-setup` is an interactive wizard that takes no arguments or flags; the npm quickstart is the *install* mechanism — the kit has no third-party runtime dependencies: the critique engine uses only the Python 3 standard library, the installer wizard runs on Node ≥18, and the skills ship as plain Markdown files; the npm package (whose `bin` field exports `sdd-setup`, delivered by M3) carries only the wizard), and a link to `docs/GUIDE.md`. Includes a clearly-marked acknowledgement of the adapted patterns (§11.2).

**FR-2 — `docs/GUIDE.md`.** The complete usage guide: the setup-wizard walkthrough, how the critique loop works, how milestones work.

**FR-3 — `docs/ARCHITECTURE.md`.** A readable explanation of the system's architecture for someone who wants to understand it deeply without reading source.

**FR-4 — `docs/BOOTSTRAP.md`.** A historical record of how the kit was built the first time, using its own process on itself before any automation existed; not part of ongoing operation.

**FR-5 — `CONTRIBUTING.md`.** How to contribute, including a full walkthrough of adding a new AI tool (one `installers/*.js` adapter + registration, §11.4) and a new critic model (`kit/config/providers.yaml`).

**FR-6 — `CLAUDE.md` + `AGENTS.md`.** Project instructions for agents working in the repo. `AGENTS.md` is the cross-tool convention (the widely supported root file) and is the **precedence base**; `CLAUDE.md` is Claude-family-specific and may reference `AGENTS.md` for shared instructions rather than duplicating them — it may rely entirely on `AGENTS.md` (reference without repeating), but it is itself a non-stub prose file (≥200 words) regardless of how much it references. Future tool-specific instruction files (e.g., a `GITHUB.md`) must not contradict the precedence base. A conflict between two non-base tool files is not a conflict in the FR-6 sense (which is base-vs-file); each tool file must be consistent with the base, and the kit requires no cross-tool consistency beyond that. They must not conflict — a "conflict" is a direct contradiction on the same fact or command (e.g., one says the trigger is `/sdd`, the other says `/foo`); where one merely adds detail the other omits, they do not conflict (omission is not a contradiction — CLAUDE.md may omit facts that AGENTS.md includes without conflicting). Where they do contradict, the statement in the precedence base (`AGENTS.md`) governs. Both cover the repo's conventions (layout, facts, the no-build/no-deps note — "no runtime dependencies and no build system") — there is no build or test command for the kit itself; the commands AGENTS.md documents are limited to the engine invocation (`python3 kit/scripts/orchestrate_critique_loop.py --doc <doc> --name <name> --pass {1,2} --round <n>`), its validator (`kit/scripts/validate_critique.py --file <json>`), and the env-loading line (`set -a; source .env; set +a`).

**FR-7 — `SECURITY.md`, `SUPPORT.md`, `LICENSE`, `CHANGELOG.md`, `.gitignore`.** Private security reporting + scope (scope = the kit's own components — the installer, the adapters, the critique engine, the skills content, and the documentation files themselves, including the `docs/` files — and what constitutes a security issue: disclosure of secrets (including a doc leaking a secret), malicious skill content, supply-chain tampering); where to ask questions and file issues; MIT license text; version history; a `.gitignore` at the repo root excluding secrets and transient artifacts; and repository initialization — this milestone runs `git init` at the repo root (the repo has no prior history; nothing is committed during the milestone itself; `.gitignore` itself is a deliverable — present at the repo root, part of the twelve under AC-1 — and becomes tracked when the maintainer makes the first commit after the milestone).

**FR-8 — Kit identity constants.** The spec pins the facts the docs must reference consistently:
- **Package name:** `sdd-multiagent-kit`; **installer bin:** `sdd-setup`; **current version:** `0.1.0`.
- **Trigger:** `/sdd` — a slash-command (skill name `sdd-multiagent-kit`) recognized automatically by Claude Code, Claude Desktop, and OpenCode (recognition is automatic via the skill's `name:` frontmatter; no configuration beyond installation — installation locations per M3 §10.3: Claude Code/Desktop → `.claude/skills/sdd-multiagent-kit/`; OpenCode reads the same shared `.claude/skills/`; Antigravity → `~/.agents/skills/sdd-multiagent-kit/`), and embedded in the Antigravity master SKILL.md as the literal `Invocation:` line — `Invocation: /sdd` — which is the mechanism the Antigravity tool reads to expose the skill; the same skill works in the other tools through their own slash-command mechanism.
- **The three env-var names** the setup wizard collects (M3): `NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY`. (Not `SDD_*` names; these are the provider keys from M1/M3.) They are consumed at runtime by the critique engine (`kit/scripts/orchestrate_critique_loop.py`), which reads them from the process environment.
- **`kit/` paths:** `kit/SKILL.md`, `kit/config/providers.yaml`, `kit/scripts/orchestrate_critique_loop.py`, `kit/skills/` (directory of the eleven sub-skill folders).
- **Pakistani-guide placeholder:** `docs/GUIDE.md` carries a reserved `## Guide for Pakistani users` section (slot only — the content is supplied separately, never fabricated), so the deferred PLAN.md §12 content has a documented home. The placeholder is the exact heading `## Guide for Pakistani users` with a one-line pointer stating that content for the section is provided separately and never fabricated by the kit.

## Edge Cases & Rules

**Terminology** (used throughout the milestone set): **FR** = functional requirement, **US** = user scenario, **AC** = acceptance criterion, **PHR** = prompt-handoff record (the repository's design-change log), **ADR** = architecture decision record. PHRs and ADRs are stored under `outputs/history/prompts/<milestone>/` and `outputs/history/adr/` respectively; the README's acknowledgement section credits the *source repositories* (spec-kit, spec-kit-plus) — the kit's own PHR/ADR records are not part of that credit.

- **Clearly-marked acknowledgement:** README (US-3/FR-1) must contain a top-level `## Acknowledgements` section (not a footnote) stating: "This project adapts patterns from `github/spec-kit` and `panaversity/spec-kit-plus`."
- **Non-stub defined:** a deliverable is non-stub iff it is substantive (≥200 words for prose files — count all words including table/bullet content and inline-code text; strip markdown marker characters (`#`, `*`, backticks) before counting; exclude fenced code blocks; a rough threshold, not a lint), contains no placeholder text (`TODO`, `lorem ipsum`, `TBD` as content), and has no empty/one-line bodies. This applies to all prose deliverables: `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `docs/GUIDE.md`, `docs/ARCHITECTURE.md`, `docs/BOOTSTRAP.md`. **Fixed-format files** (`LICENSE`, `.gitignore`, `CHANGELOG.md`) are exempt from the word-count threshold; they must simply be present and correct (LICENSE = the MIT license text with the kit's fixed copyright line "Copyright (c) 2026 SDD Multi-Agent Kit contributors" placed as the standard MIT text's first copyright line, immediately after the title); `.gitignore` = at least the mandated patterns below; `CHANGELOG.md` = at least one versioned entry for the released version (e.g., a `0.1.0` section or an `Unreleased` section), not empty).
- **`.gitignore` (repo root) must include:** the mandatory patterns `.env`, `.env.*`, `node_modules/`, `*.log`, `.DS_Store` — and temp/transient artifacts (the parenthetical examples — editor droppings like `.vscode/`/`.idea/` user settings, `__pycache__/`, `*.pyc`, OS/editor transient files like `Thumbs.db`, `*.swp` — are illustrative, not a closed list) — while never excluding legitimate source, meaning the repo's real files (`kit/`, `bin/`, `installers/`, `docs/`, `examples/`, root `*.md`, `LICENSE`, `package.json`). `outputs/critique-log/` is **deliberately not ignored** (ADR-002): the raw critique evidence is kept versioned so it is auditable. Additional patterns (e.g., `dist/`) are permitted; the mandated exclusions are a minimum. Exactly one `.gitignore` at the repo root; nested `.gitignore` files are not required.
- **Examples pointer:** README and GUIDE include an "Examples" pointer to the repo-root `examples/` directory (the M5 location), even though the content ships in M5.
- BOOTSTRAP.md is historical/read-only: it records how the kit was built, it is not instructions for using it.
- Docs must be consistent with the built kit (paths, commands, `/sdd`, env-var names in FR-8) — stale docs fail the completeness gate.
- LICENSE is the MIT text; CHANGELOG starts at 0.1.0 (initial release).

## Out of Scope (deferred)

- Examples / sample-project — **M5**.
- The kit content, engine, and installer (already M1/M2/M3) — M4 documents them, does not rebuild them.
- The actual "Guide for Pakistani users" content (a reserved slot, PLAN.md §12).

## Acceptance Criteria

**AC-1.** The repository contains the twelve deliverables: (1)–(11) the eleven files — eight at the repo root (`README`, `CLAUDE`, `AGENTS`, `CONTRIBUTING`, `SECURITY`, `SUPPORT`, `LICENSE`, `CHANGELOG`) and three inside the `docs/` directory (`docs/GUIDE`, `docs/ARCHITECTURE`, `docs/BOOTSTRAP`) — and (12) `.gitignore` at the repo root — each non-stub per the Edge-Cases definition (fixed-format files exempt from the word count).

**AC-2.** README has the quickstart, a link to GUIDE, and a top-level `## Acknowledgements` section (non-footnote) crediting `github/spec-kit` and `panaversity/spec-kit-plus`. README and GUIDE include an "Examples" pointer to the repo-root `examples/` directory (M5).

**AC-3.** CONTRIBUTING contains a worked example for adding a new AI tool and a new critic model.

**AC-4.** All docs are consistent with the built kit: correct `sdd-setup` command, `/sdd` trigger, the three env-var names (`NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY`), and the `kit/` paths.

**AC-5.** The repo is a git repository — `git init` executed, a `.git` directory present at the repo root after `git init`; `git init` alone (no commit) satisfies this criterion; `.gitignore` is a plain file and the order of its creation relative to `git init` is irrelevant — with a `.gitignore` (repo root) that excludes secrets/env files and transient artifacts per the Edge-Cases patterns.

## Cross-Reference

| Document | Path |
|---|---|
| Spec (this file) | `outputs/milestones/milestone_4/spec_milestone_4.md` |
| Plan | `outputs/milestones/milestone_4/plan_milestone_4.md` |
| Tasks | `outputs/milestones/milestone_4/tasks_milestone_4.md` |
| Workflow | `outputs/milestones/milestone_4/workflow_milestone_4.md` |
| Tests | `outputs/milestones/milestone_4/tests_milestone_4.md` |