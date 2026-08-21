# Agent Instructions (SDD Multi-Agent Kit)

This file is the cross-tool convention for AI agents working in this repository. It is tool-agnostic; Claude-family-specific notes live in `CLAUDE.md`, which references this file rather than duplicating it.

## Project at a glance

The SDD Multi-Agent Kit is a Spec-Driven Development framework for CLI coding agents. It is a collection of Markdown skills (`kit/`), a Python critique engine (`kit/scripts/`), and a Node installer (`bin/` + `installers/`). It has no runtime dependencies and no build system.

## Layout

- `kit/SKILL.md` — master skill (frontmatter `name: sdd-multiagent-kit` drives the `/sdd` trigger).
- `kit/skills/*` — eleven sub-skills.
- `kit/config/providers.yaml` — the locked seven-model critic panel.
- `kit/scripts/orchestrate_critique_loop.py` — the critique loop (Python 3, zero deps).
- `kit/scripts/validate_critique.py` — critique validator.
- `bin/setup-wizard.js` + `installers/*.js` — installer (Node >= 18).
- `docs/` — GUIDE, ARCHITECTURE, BOOTSTRAP.
- `outputs/` — the bootstrap run's specs, critique logs, PHRs, and ADRs (historical; not shipped).

## Key facts you must keep consistent

- Package name: `sdd-multiagent-kit`; installer bin: `sdd-setup`; license: MIT. The version lives in `package.json` and nowhere else — read it from there, and change it only via `node scripts/bump-version.js <version>`.
- Trigger: `/sdd` (skill name `sdd-multiagent-kit`).
- Env vars the wizard collects: `NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY`.
- Install locations: Claude Code/Desktop → `.claude/skills/sdd-multiagent-kit/`; OpenCode → reads the same shared `.claude/skills/`; Antigravity → `~/.agents/skills/sdd-multiagent-kit/` with the trigger embedded in SKILL.md.

## Working in this repo

- **Tests before implementation.** Find the relevant `tests_milestone_*.md` (under `outputs/milestones/milestone_N/`) and satisfy it.
- **Simplicity.** Do not add dependencies, frameworks, or servers without strong reason.
- **Standalone-first.** New skills/scripts must work on their own.
- **Never write secrets** into any file; `.gitignore` excludes `.env`, `node_modules/`, and transient artifacts. `outputs/critique-log/` is deliberately **not** ignored (ADR-002): raw critique evidence stays versioned for auditability.
- **Log PHRs/ADRs** for design changes under `outputs/history/`.
- **Verify before pushing.** `python3 outputs/milestones/milestone_2/verify_milestone_2.py` and `.../milestone_3/verify_milestone_3.py` are the two executable suites; neither needs API keys. `.github/workflows/ci.yml` runs both on every push and pull request.
- **Never hand-edit a version.** `bin/setup-wizard.js` reads it from `package.json`, and twelve `SKILL.md` frontmatters must agree; `node scripts/bump-version.js <version>` sets them together and `--check` asserts agreement. Releasing is automated from the version number — see [CONTRIBUTING.md](CONTRIBUTING.md#releasing). Never run `npm publish` by hand.

## Invoking the kit while working on it

You can run the kit against any folder containing a `PLAN.md`. The engine:

```bash
python3 kit/scripts/orchestrate_critique_loop.py --doc <doc> --name <name> --pass {1,2} --round <n>
```

Verify critique output with `kit/scripts/validate_critique.py`. The engine requires the provider keys in the environment (`set -a; source .env; set +a`).

See `docs/ARCHITECTURE.md` for the full design, and `CLAUDE.md` for Claude-specific guidance.