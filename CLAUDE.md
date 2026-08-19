# CLAUDE.md — Claude-family agent guidance

This file supplements the cross-tool convention in [AGENTS.md](AGENTS.md). Follow AGENTS.md first; this file adds Claude-specific notes and does not duplicate shared instructions.

## Claude-specific setup

- **Skills install** to `.claude/skills/` (Claude Code) and the shared desktop config; the `/sdd` trigger comes from the skill name `sdd-multiagent-kit` in SKILL.md frontmatter.
- Install the kit with `sdd-setup`, or symlink/copy `kit/` into `.claude/skills/sdd-multiagent-kit/`.
- After installing, confirm the skill is visible: in Claude Code the skill list shows `sdd-multiagent-kit`, and in Claude Desktop the skills directory contains the `SKILL.md`. The trigger `/sdd` is only available once the skill is present at the right path.

## Working in this repo (Claude)

- Prefer reading `AGENTS.md` for the authoritative cross-tool rules (tests-before-implementation, simplicity, standalone-first, no secrets, PHR/ADR logging).
- When the kit runs the critique loop, provider keys come from `.env` via `set -a; source .env; set +a` — never inline the values.
- Claude-specific decisions still log PHRs/ADRs under `outputs/history/`, matching the cross-tool process.
- Do not edit `kit/` content directly without running the milestone's verification suite first; the milestone tests under `outputs/milestones/` are the contract.

## Invoking the kit from Claude

Use `/sdd` with a brief (a `PLAN.md` is ideal). The kit then runs its full milestone loop. You can also call the engine directly:

```bash
python3 kit/scripts/orchestrate_critique_loop.py --doc <doc> --name <name> --pass 2 --round 1
```

Validate with `kit/scripts/validate_critique.py`. See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for the loop's design.

## Guidance for Claude Desktop users

Claude Desktop is supported through the same `.claude/skills/` convention. If the wizard reports the desktop install as WARN, verify the desktop app's skills path exists and re-run `sdd-setup` with the desktop option selected; the kit's other tools are unaffected.