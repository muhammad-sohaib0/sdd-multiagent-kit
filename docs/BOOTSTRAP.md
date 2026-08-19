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

## How the critique loop actually ended

Worth stating plainly, because it is the most instructive thing the bootstrap
produced. Pass 2's ideal exit is every critic scoring a perfect 10. **That never
happened on any milestone.** Scores plateaued in the 6–8 band and `n_valid` degraded
as free-tier providers failed; the loop exited when rounds stopped producing new
findings — one critic's round-13 issue list was verbatim identical to its rounds 11
and 12.

That exit is legitimate, but it was not in the original brief. `PLAN.md` §4.4 now
carries it as an explicit stopping condition (two consecutive non-progressing rounds
→ escalate to the human with a full summary), recorded in ADR-004, with the five
escalation summaries the rule requires in PHR `milestone_5/003`.

The loop still earned its cost. M2's round 6 caught the engine contradicting its own
spec (a 2-second stagger where the spec said 4), and round 11 forced deterministic
slot ordering in the output — defects a single reviewer would plausibly have missed.
In M4, critics *guessed wrong* env-var names (`SDD_API_KEY`) and adjudication
correctly rejected the guess; deferring to the panel would have introduced the bug.

## The whole-system test

`BOOTSTRAP.md` §5 insists that building the kit is not proof the kit works. That test
was run on 2026-08-20: the finished kit, installed through `sdd-setup`, was handed an
unrelated brief by a fresh zero-context session. It produced a correct
dependency-ordered milestone breakdown and a full five-document set — **PASS** — and
in doing so exposed 13 real gaps in the kit, every one a convention the bootstrap's
author knew but never wrote down. Full record:
`outputs/critique-log/stranger-test-whole-system.md`.

The seed skill and the scratch `.bootstrap/` harness were deleted at that point, per
§3.6. The kit is self-hosting.