# SDD Multi-Agent Kit — Bootstrap Record

This document is a **historical record** of how the kit was built the first time. It is not part of ongoing operation and is not instructions for using the kit. For usage, see [GUIDE.md](GUIDE.md).

## What happened

The kit was built by running its own future process on itself, before any automation existed. A bootstrap seed skill drove one real cycle of the Spec-Driven Development process against the kit's own `PLAN.md`, and the process produced the kit that now automates the process.

The bootstrap run worked through five dependency-ordered milestones, each gated through the same discipline the kit now enforces:

1. **M1 — Core process content** — the master skill, constitution, provider config, and ten sub-skills.
2. **M2 — Critique engine** — the orchestrator, validator, and critique-loop skill.
3. **M3 — Installer** — the setup wizard, four tool adapters, and package manifest.
4. **M4 — Distribution/repo docs** — this documentation layer.
5. **M5 — Examples / sample-project** — worked example projects.

## How it ran

Each milestone produced a five-document set (spec, plan, tasks, workflow, tests). Designs passed through a real multi-model critique loop — seven independent critic models from three providers, run in parallel rounds with retries — plus completeness and simplicity gates, and a zero-context Stranger Test on the documentation. Genuine critiques were adjudicated and fixed; the milestone was built only after its tests were written; and the whole trail was preserved as Prompts-History-Records and Architectural Decision Records under `outputs/history/`.

## Outcome

The bootstrap's output **is this repository**. The process, applied to itself, produced the standalone skills and scripts that anyone can now install with `sdd-setup` and invoke with `/sdd`. The critique log under `outputs/critique-log/` records the actual rounds that shaped each design.

This record is preserved for auditability and as a worked example of the process applied end-to-end.