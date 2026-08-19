# SDD Multi-Agent Kit — Bootstrap Plan

**What this document is:** `PLAN.md` describes what the SDD Multi-Agent Kit is and how it works once it exists. This document describes something narrower and temporary: how the kit gets built for the first time, using its own process, before any of its automation exists yet to help. Where `PLAN.md` is the permanent architecture, this document is a one-time recipe — see §6 for what happens to it once that first build is done.

---

## 1. Why This Exists

The kit is going to be built by handing `PLAN.md` to an AI tool and letting the kit's own process — the computational thinking scan, the constitution, the milestone split, the two documents-plus-plan-plus-tasks-plus-workflow-plus-tests set, the gates, the two-pass critique loop, Clarify, the history log, the Stranger Test — run against it. This is not a shortcut and not just a convenient way to get the work done. It is the strongest test the system could possibly face before anyone else touches it.

Every check this system runs is built on one core belief, stated directly in `PLAN.md` §4.5: agreement between models is not proof of correctness. That belief has to apply here too. If the kit is used to build itself and the result is wrong, that is not a special case to explain away — it means the design itself has a real gap, found before a single outside user ever saw it. If the kit is used to build itself and the result is right, that is the first genuine evidence the design works, independent of anyone's confidence in it going in.

## 2. The Cold-Start Problem

None of the kit's automation exists yet to run its own process. There is no `npm install`, no setup wizard, no `/sdd` command already sitting in a tool, because those are the very things being built. Something has to exist manually, once, just long enough to get the very first cycle running.

## 3. Manual Bootstrap Steps

1. **Build a minimal seed skill by hand.** Create `.claude/skills/sdd-multiagent-kit-seed/SKILL.md` inside a Claude Code or OpenCode session, containing just enough of the process from `PLAN.md` §4 through §8 to run one real cycle — the critique loop mechanics, the CT scan, the constitution articles, the milestone document set, the two gates, and the PHR/ADR logging rules. This seed does not need to be polished; it only needs to be correct enough to bootstrap the real thing.
2. **Hand the seed skill `PLAN.md`.** Invoke the seed skill and give it the plan, exactly as `PLAN.md` §13 describes.
3. **Let the process run untouched, milestone by milestone.** For each milestone: CT scan, `spec.md`, Pass 1, `plan.md`, `tasks.md`, `workflow.md`, `tests.md`, the Structural Completeness and Simplicity Gates, Clarify, Pass 2, the Stranger Test — in that order, with no steps skipped (see §4) — while the process logs its own PHRs and ADRs as it goes, exactly as it would for anyone else's project.
4. **Adopt a real constitution for the kit's own build.** The seed skill should produce an actual `constitution.md` for this project from the article set in `PLAN.md` §6, not skip it because "it's just the kit building itself."
5. **Build the real kit from the milestones this produces.** The actual `kit/skills/*/SKILL.md` files, the real installer, the real adapters, the real `history/` and `critique-log/` folders — all of it comes out of this run, not out of the hand-written seed.
6. **Retire the seed.** Once the real kit exists and its own installer works, delete the seed skill. From that point forward the kit installs, updates, and maintains itself the normal way, described in `PLAN.md` §10.

## 4. Non-Negotiables During This Run

It will be tempting to cut corners on the one build nobody else will ever see the inside of. That temptation is exactly why this section exists. During the bootstrap run:

- The full two-pass critique loop runs, with all six critics, exactly as specified in `PLAN.md` §4.2 — no reduced panel, no skipped rounds.
- The Structural Completeness Gate and the Simplicity Gate in `PLAN.md` §5.3 and §5.4 are not waived. A milestone with a missing section, or with an unjustified extra layer of complexity, is blocked, the same as it would be for anyone else's project — including, pointedly, any temptation to over-build the critique engine itself before it's proven necessary.
- Every milestone produces the full five-document set from `PLAN.md` §7.2 — `plan.md` and `tasks.md` included, not just spec, workflow, and tests.
- PHRs and ADRs are logged for real, per `PLAN.md` §8, even though it can feel unnecessary to log decisions about a project only its own builder will read at first. That log is exactly what a future contributor will need.
- The Stranger Test in `PLAN.md` §4.5 runs on every finished milestone's full document set, using a genuinely fresh session with no memory of this conversation or this plan's history — not a session that already knows what the kit is supposed to do.

If any of these get skipped "just this once," the first real test of the system becomes invalid, and every claim made about the system afterward rests on nothing.

## 5. Success Criteria — the Real Bar

Successfully building the kit is not, by itself, proof that the kit works — a system can build one specific thing correctly by coincidence, or because whoever ran it already knew the right answer. The actual bar is this:

**Once the kit is finished and installed through its own installer, give it a brief for a completely unrelated project — something with no connection to this plan or this conversation — and it must produce a correct, properly-ordered milestone breakdown, with real plan and task documents, without any leftover context from having built itself.**

That is the kit's own Stranger Test, run against the whole system rather than a single milestone. Passing it is what actually confirms the design works, not the fact that it managed to describe itself correctly.

## 6. Lifecycle of This Document

This document has a natural end point. Once the bootstrap run succeeds and the kit is self-hosting, this file has done its job — it is not part of the kit's ongoing operation and nothing in the running system depends on it. It stays in the repository under `docs/BOOTSTRAP.md` as a historical record of how the project came to exist, useful to a future contributor who wants to understand the origin of the design, but it is not referenced by the kit itself once v1 is live.
