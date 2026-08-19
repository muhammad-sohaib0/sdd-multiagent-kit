# SDD Multi-Agent Kit — User Guide

This guide explains how to install, invoke, and work with the SDD Multi-Agent Kit.

## 1. Prerequisites

- Node.js >= 18 (for the installer).
- One or more of the supported AI tools: Claude Code, Claude Desktop, OpenCode, or Antigravity.
- API keys for the critic providers you want to use (see §2).

## 2. Install

```bash
npm install -g sdd-multiagent-kit
sdd-setup
```

The wizard:

1. **Collects API keys** in one pass. It asks for `NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, and `OLLAMA_API_KEY`. (Skip any you don't have yet; tools needing a missing key will fail at runtime, which is why the kit's retry machinery exists.) Under the NVIDIA prompt it offers a *Learn more* link to the reserved Guide for Pakistani users.
2. **Detects your tools** by checking their config locations (no network).
3. **Asks which** detected tools to install into.
4. **Installs** the kit into each chosen tool and confirms the trigger is active.
5. **Reports** per-tool OK/WARN/FAIL.

Exit codes: `0` everything installed and confirmed; `1` partial success; `2` usage/config error before any install.

## 3. Invoke

In any supported tool, start the process with the trigger:

```
/sdd
```

Provide a brief (a `PLAN.md` works well). The kit runs the full loop (§4).

## 4. The loop

1. **Research / computational-thinking scan** — reads the brief and surfaces requirements and open questions.
2. **Constitution** — the kit adopts a small set of non-negotiable rules (standalone-first, observable interfaces, tests before implementation, simplicity by default, framework trust, real-world testing, amendment).
3. **Milestones** — dependency-ordered, each with a five-document set: **spec, plan, tasks, workflow, tests**.
4. **Critique loop** — seven independent critic models review each design document in rounds until clean; then completeness and simplicity gates run; then a **Stranger Test** (a zero-context agent re-derives the contract) catches blind spots.
5. **Build + verify** — only then is content produced, against the tests.
6. **History** — progress, Prompts-History-Records (PHRs) and Architectural Decision Records (ADRs) are logged.

## 5. Milestones

Each milestone is built in dependency order and fully verified before the next starts. This repo itself was built by running the kit on its own plan — see [BOOTSTRAP.md](BOOTSTRAP.md).

## 6. Example projects

See the `examples/` directory for complete worked projects you can copy or run the kit against.

## Guide for Pakistani users

Reserved slot. Content is supplied separately by the maintainer and never fabricated by the kit. When the `sdd-setup` wizard asks about the NVIDIA signup gap, this is the documentation location it points to.