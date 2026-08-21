---
name: sdd-multiagent-kit
description: >-
  Master orchestrator for Spec-Driven Development (SDD). Runs the full
  Research -> Specify -> Clarify -> Build pipeline against a project brief,
  with a seven-model multi-lab critique loop, a computational-thinking
  completeness gate, a simplicity gate, and a zero-context Stranger Test.
  Use this when a user furnishes a project brief (PLAN.md, README, prompt) and
  wants an ordered, dependency-safe set of milestones each producing its own
  five-document set (spec, plan, tasks, workflow, tests).
version: 0.1.1
---

# SDD Multi-Agent Kit — Master Skill

This is the orchestrator. It sequences the phase order, runs the two gates, dispatches to the eleven sub-skills, and enforces the standing adjudication and stopping rules. It does **not** duplicate a sub-skill's procedure.

## When to use

The user provides a project brief and the kit is installed. Run the pipeline below. The trigger to start is `/sdd`, derived from this skill's `name` frontmatter and set up by the installer (`sdd-setup`) — Claude Code, Claude Desktop, and OpenCode recognize it natively from the skill folder; Antigravity reads the `Invocation: /sdd` line the installer writes into this file's frontmatter. If the kit was placed manually rather than installed, the same content works from the tool's skills directory per the Agent-Skills standard (`.claude/skills/sdd-multiagent-kit/` for Claude-family and OpenCode, `~/.agents/skills/sdd-multiagent-kit/` for Antigravity); invoke it by this skill's name.

## Pipeline (phase order)

1. **`research-ct-scan`** — decompose the brief via computational thinking into a Requirement Category Checklist. (If the brief is empty, HALT and ask for a brief; never fabricate.)
2. **Adopt the constitution** — create `outputs/constitution.md` from `constitution.template.md`, once at project start. Reused for every milestone; changed only via amendments (Article VII / ADR).
3. **`milestone-builder`** — decide the milestone split (single vs. ordered multi-milestone) in dependency order. For each milestone, run steps 4–12.
4. **`specify`** — draft the milestone spec (the authoritative *what*).
5. **G1 gate** — Structural Completeness + Simplicity on the spec alone. Fail → log PHR, return to `specify` with findings (blocked).
6. **Critique — Pass 1** — light pass; objective dimensions only; compile the `needs_clarify` list. Run via the `critique-loop` sub-skill (kit/scripts). Invariant: every issue must survive independent scrutiny from more than one lab before it is considered resolved.
7. **`clarify-interview`** — once per milestone, after Pass 1. Ask only what an AI could not infer from the compiled `needs_clarify` list (starting with the PLAN.md open decisions); fold answers into the spec. Empty list → ask nothing. Fold the answers in; the plan is drafted afterwards so it reflects them by construction.
8. **`plan-builder` → `task-breakdown` → `workflow-builder` → `scenario-tester`** — produce `plan`, `tasks`, `workflow`, `tests`.
9. **G2 gate** — both gates on all five documents together. Fail → return to the responsible drafting sub-skill.
10. **Critique — Pass 2** — full rigor on all five documents. Run via the `critique-loop` sub-skill. Also re-checks that Clarify answers did not break consistency elsewhere.
11. **`stranger-test`** — hand the finished five-document set to a fresh zero-context session; contract parity required. This is the one rule the loop may not reason its way around.
12. **Build the milestone** — execute the milestone's ordered tasks to materialize its artifacts at the `tasks_milestone_N.md` paths.

Log a PHR at **every** phase transition. The full list: after the CT scan, constitution adoption, and milestone breakdown (these three land in `outputs/history/prompts/milestone_0/`, since they run before milestone 1 exists), and per milestone: after `specify`, G1, Pass 1, `clarify-interview`, **each of `plan`, `tasks`, `workflow`, and `tests` separately** (four records — one per sub-skill, since each has its own input, output, and failure mode), G2, Pass 2, `stranger-test`, and build. The `critique-loop` sub-skill additionally logs one PHR per round. On any decision meeting the ADR significance test (real alternatives existed, hard to reverse, or affects more than one milestone), suggest an ADR — the suggestion is a **blocking** human-confirmation step, never async.

## The two gates (master-skill checkpoints, not sub-skills)

- **Structural Completeness:** every checklist category has a real, substantive section (no stub, no placeholder); nothing references something that doesn't exist in the document set or its inherited history (constitution + PHRs + ADRs).
- **Simplicity:** no more standalone components than the milestone needs. A standalone component is a separately installed/deployed unit the milestone *adds*; the kit's content set counts as one deliverable, not N components. Default limit **3** per milestone; each beyond it needs a written justification in `plan.md`. The default is overridable once, project-wide, by appending `simplicity_default: N` to the project's adopted `constitution.md` (a constitution change — requires an ADR); the override then applies to all subsequent milestones. No wrapping a tool in a custom abstraction where using it directly works. No feature untraceable to a `workflow.md` scenario.

**What each gate can actually check.** G1 runs on the spec alone, so three sub-checks have no evidence to run against yet. They are **deferred to G2, not passed at G1** — record them as scheduled:

| Sub-check | At G1 | Why |
|---|---|---|
| Every checklist category is substantive | **Runs** | The spec is the only input it needs |
| Content forward references (a section citing a milestone or artifact that does not exist) | **Runs** | Judged against the spec plus inherited history |
| The mandatory **Cross-Reference** section naming `plan`/`tasks`/`workflow`/`tests` | **Exempt** | `specify` requires this section, and those four files do not exist until step 8. It is a forward *pointer*, not a forward *dependency* — a spec is not penalized for carrying the section the pipeline told it to carry. G2 verifies all five files exist and the back-references match |
| Simplicity: no feature untraceable to a `workflow.md` scenario | **Deferred** | There is no `workflow.md` at G1 |
| Simplicity: standalone-component count | **Deferred** | Components are named in `plan.md`, which does not exist at G1. Any count at G1 is projective |

Read literally without this table, a correctly-drafted spec fails G1 on its own mandatory final section. It should not.

**Gate-failure behavior:** log a PHR with the findings, block, and return the document to the responsible drafting sub-skill. When one root cause spans several documents — a broken tests-first ordering, say, that only shows up in `tasks.md`'s dependency column but must be fixed in `tasks`, `workflow`, and `tests` together — return it to **every** owning sub-skill as one finding, and re-run the gate on the whole set once. Do not split it into separate findings per file; that loses the shared cause and invites three partial fixes. The critique loop may not argue a gate finding away (gates and the Stranger Test are not negotiable).

## Sub-skill dispatch

| Sub-skill | Job |
|---|---|
| `research-ct-scan` | Requirement Category Checklist |
| `specify` | Draft the spec |
| `milestone-builder` | Milestone split, dependency-ordered |
| `clarify-interview` | Ask the compiled needs_clarify items, fold answers |
| `plan-builder` | Technical how (tech stack, architecture, data model, rationale) |
| `task-breakdown` | Ordered executable steps, `[P]` parallel markers, tests-first |
| `workflow-builder` | Scenario-branching tree |
| `scenario-tester` | One test per workflow node + end-to-end walkthrough |
| `critique-loop` | Run the critique engine — invoke, read, triage, stop |
| `stranger-test` | Zero-context verification |
| `history-logger` | PHR/ADR records |

Each sub-skill's input/output/edge-case contract is in its own SKILL.md. The critique engine's automation — the `critique-loop` sub-skill plus the two scripts under `kit/scripts/` — ships with the kit and is invoked from step 6 and step 10.

## Standing rules

- **Sub-skill failure:** log a PHR, retry once (same input, no backoff); second failure → **blocking** escalation to the human with a summary. Never silent, never unbounded.
- **Adjudication:** as drafter+adjudicator, accept or reject each critic issue with a reason; measurement decay and false positives are rejected in writing (PHR), never silently.
- **Retry (critique):** a response invalid (unparseable, or overall_score < 10 with zero issues) is retried ≤1 time; still invalid → that critic yields no signal that round and participates again next round (never excluded across rounds). Transport failure → ≤5 tries with growing backoff; still failing → logged, absent for that round only.
- **Stopping:** Pass 1 stops when every objective issue is resolved and the needs_clarify list is compiled. Pass 2 stops when every currently-valid critic scores perfect. When the panel asymptotes instead — **two consecutive non-progressing rounds** (a round is progressing if the document changed in response to it or it surfaced a genuinely new, actionable issue) — escalate to the human with the full summary: rounds run, issues accepted, issues rejected with reasons, and the evidence that the remaining flags are repeats. You may report that the panel stopped producing new signal; you may not decide on your own that your own draft is finished. Round safety cap defaults to 25 per pass; at the cap, escalate the same way — never stop without telling anyone.
- **Referencing:** `PLAN.md §X` means the project brief; bare `§X` means the current document.