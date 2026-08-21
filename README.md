# SDD Multi-Agent Kit

[![npm](https://img.shields.io/npm/v/sdd-multiagent-kit)](https://www.npmjs.com/package/sdd-multiagent-kit)
[![CI](https://github.com/muhammad-sohaib0/sdd-multiagent-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/muhammad-sohaib0/sdd-multiagent-kit/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Spec-Driven Development for CLI coding agents: a disciplined, multi-model process that turns a brief into tested, milestone-ordered deliverables you can trust.

## Why

LLM-written software is fast but often sloppy. The SDD Multi-Agent Kit replaces improvisation with a real engineering loop: a brief is turned into a spec, a plan, tasks, a workflow, and tests; seven independent critic models attack the design in a multi-lab critique loop; completeness and simplicity gates enforce discipline; and a zero-context Stranger Test catches gaps that authors are blind to.

## Quickstart

```bash
npm install -g sdd-multiagent-kit
sdd-setup
```

`sdd-setup` collects your API keys, detects your AI tools (Claude Code, Claude Desktop, OpenCode, Antigravity), and installs the kit into each one. You then invoke it in any of those tools with the trigger:

```
/sdd
```

For a complete walkthrough see [docs/GUIDE.md](docs/GUIDE.md).

## What you get

- A **master skill** (`kit/SKILL.md`) plus eleven sub-skills: research scan, specify, plan, task breakdown, Clarify, milestone builder, workflow, scenario tester, critique loop, Stranger Test, and history logger.
- A **critique engine** (`kit/scripts/orchestrate_critique_loop.py`) that runs seven independent critic models in rounds until the design is clean.
- An **installer** (`bin/setup-wizard.js` + four adapters) that wires the kit into your tools.
- An **examples project** under `examples/` (see below).

## API keys

`sdd-setup` collects three provider keys in one pass (kept in your environment only, never written to files): `NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY`.

## Installation locations

| Tool | Location | Trigger |
|---|---|---|
| Claude Code / Claude Desktop | `.claude/skills/sdd-multiagent-kit/` | `/sdd` |
| OpenCode | reads `.claude/skills/` (shared) | `/sdd` |
| Antigravity | `~/.agents/skills/sdd-multiagent-kit/` | invocation phrase in SKILL.md |

## Examples

Working example projects ship under `examples/`. You can run the kit against any folder that contains a `PLAN.md`.

## Documentation

- [GUIDE.md](docs/GUIDE.md) — full usage walkthrough.
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) — how the system is built.
- [BOOTSTRAP.md](docs/BOOTSTRAP.md) — historical record of building the kit on itself.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) — includes worked examples for adding a new AI tool and a new critic model, plus how releases work.

## Releases

Published to npm from GitHub Actions using [Trusted Publishing](https://docs.npmjs.com/trusted-publishers), so every release carries **provenance**: the npm page links back to the exact commit and workflow run that built the tarball, and you can verify it yourself:

```bash
npm audit signatures
```

No publish token exists in the repository — releases are authenticated by a short-lived OIDC token, and no maintainer runs `npm publish` by hand. See [CHANGELOG.md](CHANGELOG.md) for what changed in each version.

## Security

See [SECURITY.md](SECURITY.md) to report vulnerabilities privately.

## License

[MIT](LICENSE)

## Acknowledgements

This project adapts patterns from `github/spec-kit` and `panaversity/spec-kit-plus`.