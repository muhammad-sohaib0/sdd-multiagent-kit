# SDD Multi-Agent Kit — Architecture

A readable explanation of how the system is put together. Read this if you want to understand it deeply without reading the source.

## 1. Overview

The kit is a small collection of Markdown skills plus a critique engine plus an installer. It has no runtime server and no build system — it is instructions and scripts your coding agent runs, wired into your tools by the installer.

```
                   /sdd trigger
                        |
                   MASTER SKILL (kit/SKILL.md)
                        |
        +---------------+----------------+
        |               |                |
   RESEARCH   SPECIFY -> PLAN -> TASKS -> WORKFLOW -> TESTS
   (scan)      |            (five-document milestone set)
               |
          CRITIQUE LOOP (kit/scripts/orchestrate_critique_loop.py)
               |  seven models x providers, rounds until clean
               |
          GATES (completeness, simplicity)
               |
          STRANGER TEST (fresh zero-context re-derivation)
               |
          BUILD (produces content against tests)
               |
          HISTORY LOGGER (PHRs, ADRs)
```

## 2. Components

- **Master skill** (`kit/SKILL.md`) — the entry point. Its frontmatter (`name: sdd-multiagent-kit`) is what makes the `/sdd` trigger work in the native tools.
- **Eleven sub-skills** (`kit/skills/*`) — each a focused capability: `research-ct-scan`, `specify`, `plan-builder`, `task-breakdown`, `clarify-interview`, `milestone-builder`, `workflow-builder`, `scenario-tester`, `critique-loop`, `stranger-test`, `history-logger`. Each is its own SKILL.md so agents can load capability on demand.
- **Critique engine** (`kit/scripts/orchestrate_critique_loop.py`) — runs the multi-lab loop. It reads `kit/config/providers.yaml` for the locked critic panel, launches all critics in parallel each round, retries on transport/rate/timeout errors, and stops on either a clean verdict or the round budget. Its response handling is deliberately tolerant of free-tier quirks: it extracts JSON via a balanced-brace scan (accepting fenced JSON anywhere in the response, surrounding prose including prose with braces, trailing commas, and output-cap truncation which it repairs best-effort), carries generous per-provider output caps (NIM 8000, Google 8000, Ollama 12000 tokens), backs off adaptively on 429s (30 × attempt) and 5xx/timeouts (8 × attempt) across up to 5 transport tries, staggers each critic's first call to avoid rate-limit bursts, enforces each attempt with a hard wall-clock deadline (per-model `timeout` keys in `providers.yaml`, default 600s), and logs a snippet of the raw response when a critic fails all attempts. It has no third-party dependencies (it ships a minimal YAML reader) so it runs anywhere Python 3 does.
- **Validator** (`kit/scripts/validate_critique.py`) — checks critique output structure.
- **Installer** (`bin/setup-wizard.js` + `installers/*.js`) — Node-based. Each `installers/<tool>.js` exports `detect()`, `install()`, `confirmEnabled()`. The wizard orchestrates them and collects API keys in one pass.

## 3. The critic panel

`kit/config/providers.yaml` pins a seven-model panel across three providers (NVIDIA NIM, Google AI Studio, Ollama Cloud), locked by Architectural Decision Records (ADR-001, ADR-003). The engine treats the panel as fixed: the models, their order, their providers, and the retry policy are all configuration, not hardcoded.

## 4. Data flow

1. A brief becomes a five-document milestone set (spec, plan, tasks, workflow, tests) via the builder sub-skills.
2. The critique engine sends each document to the panel. Verdicts feed back as issues; the author adjudicates, applies genuine fixes, and re-runs until the panel converges or the round budget is spent.
3. The gates check structural completeness and simplicity; a pass here permits the build.
4. The Stranger Test re-derives the contract from a fresh session; mismatch blocks release.
5. The history logger records PHRs and ADRs so the reasoning trail is auditable.

## 5. Install locations

See [GUIDE.md §2](GUIDE.md). Each adapter knows its tool's convention: Claude Code/Desktop use `.claude/skills/`, OpenCode reads that same shared folder, and Antigravity needs a separate `~/.agents/skills/` copy with the trigger embedded in the SKILL.md description.

## 6. Design constraints

- **Standalone-first:** each sub-skill and script works alone, not only when driven by the master skill.
- **Observable interfaces:** adapters and scripts have explicit `detect`/`install`/`confirmEnabled` contracts and CLI flags.
- **Simplicity by default:** no runtime dependencies, no framework, plain Markdown + Python + Node.
- **Tests before implementation:** every milestone's tests are written before its content.