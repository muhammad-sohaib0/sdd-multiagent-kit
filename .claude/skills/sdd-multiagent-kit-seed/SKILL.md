---
name: sdd-multiagent-kit-seed
description: Bootstrap seed of the SDD Multi-Agent Kit. Runs one real cycle of the Spec-Driven Development process — computational thinking requirement scan, constitution adoption, dependency-ordered milestone breakdown, five-document milestone sets (spec, plan, tasks, workflow, tests), structural completeness and simplicity gates, a two-pass six-model critique loop, Clarify, a Stranger Test, and PHR/ADR history logging. Invoke it with a project brief (e.g. PLAN.md). Used once to build the real kit, then retired.
version: 0.1.0
---

# SDD Multi-Agent Kit — Seed Skill

## What this is

A hand-built seed containing just enough of the SDD Multi-Agent Kit's process to run one real cycle, created manually per `BOOTSTRAP.md` §3. It is not the polished kit — it is the test harness that builds the kit, and it is retired once the real kit exists. The non-negotiables in `BOOTSTRAP.md` §4 are binding for every run of this seed: the full two-pass loop with all six critics, no skipped rounds, no waived gates, all five documents per milestone, real PHR/ADR logging, and a genuinely fresh Stranger Test session.

## 1. Roles

- **Drafter + Adjudicator:** the invoking agent (Claude-family). Writes drafts, reads every critique every round, accepts or rejects each issue with a reason, produces the next revision. The maker is never the checker.
- **Critic Panel — six models, every model runs every round:**

| # | Model | Provider | Key |
|---|---|---|---|
| 1 | `nvidia/nemotron-3-ultra-550b-a55b` | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 2 | `openai/gpt-oss-120b` | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 3 | `qwen/qwen3-next-80b-a3b-instruct` | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 4 | `z-ai/glm-5.2` | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 5 | `gemini-3.6-flash` | Google AI Studio | `GOOGLE_AISTUDIO_API_KEY` |
| 6 | `minimax-m3:cloud` | Ollama Cloud | `OLLAMA_API_KEY` |

Every document a milestone produces goes through this same panel; none are reviewed by a single model alone.

## 2. The Two-Pass Loop

**Pass 1 — before Clarify (light):** runs on the raw draft. Critics score only objective dimensions — clarity, structure, internal consistency, presence of required sections. Anything genuinely subjective or a business decision is tagged `"category": "needs_clarify"` instead of demanding a fix. Pass 1 stops once every objective issue is resolved and the full `needs_clarify` list is compiled. That compiled list becomes the question set for Clarify — the human is only asked things an AI genuinely could not have answered.

**Pass 2 — after Clarify (full rigor):** runs with the human's answers folded in. Full six-critic rigor, stopping only under §4. Also re-checks that the answers didn't break consistency elsewhere.

## 3. Critique Response Schema

Every critic responds only in this structure — a strict rubric, never free-form praise:

```json
{
  "model": "z-ai/glm-5.2",
  "document": "plan_milestone_2",
  "round": 3,
  "pass": 1,
  "overall_score": 7,
  "scores": {
    "clarity": 8,
    "completeness": 6,
    "edge_case_coverage": 5,
    "internal_consistency": 8,
    "testability": 7
  },
  "issues": [
    {
      "section": "Data Model",
      "category": "objective",
      "problem": "No defined behavior when the user cancels mid-way through scenario B.",
      "why_it_matters": "The agent will guess at build time instead of following the spec.",
      "suggested_fix": "Add an explicit cancel branch under 2.3."
    },
    {
      "section": "Tech Stack",
      "category": "needs_clarify",
      "problem": "Should this use a managed database or an embedded one?",
      "why_it_matters": "This is a product decision, not something inferable from context."
    }
  ],
  "verdict": "needs_revision"
}
```

**Validity rule:** a response is invalid, and that critic is excluded from that round only, if `overall_score` is below 10 while `issues` is empty (a low score with nothing to fix is noise), or if the response cannot be parsed into this shape after one retry. A critic invalid three rounds in a row is flagged non-cooperative for the session; the loop keeps running with the remaining valid critics. The loop never stops silently because scores aren't 10 — only because a voice stopped producing usable signal.

## 4. Stopping Conditions

| Condition | What happens |
|---|---|
| Pass 1: every objective issue resolved, `needs_clarify` list compiled | Advance to Clarify |
| Pass 2: every currently-valid critic returns a perfect score | Advance to the Stranger Test |
| A critic invalid three rounds running | Exclude from the count, keep looping, log it |
| Round count reaches the safety cap (default 25; configurable; can be disabled) | Escalate to the human with a full summary — never stop silently |

## 5. Grounding Anchor — the Stranger Test

Agreement between six critics is not proof of correctness — models agreeing can share one blind spot. Once Pass 2 succeeds, the finished milestone's full document set (all five files together, never one alone) is handed to a fresh, zero-context AI session with a single instruction: *implement this, ask no questions.* If it builds the right thing, the documents are genuinely clear. If it goes wrong, the failure becomes a new issue fed straight back into the loop. This is the one rule the loop is never allowed to reason its way around.

## 6. Computational Thinking Requirement Scan

The first concrete output of Research. Before any document is written, decompose the stated goal using computational thinking — break the build into its fundamental parts, recognize what category of project this is — to produce a Requirement Category Checklist specific to this exact project.

Always required (base anatomy): Goal, User Scenarios, Functional Requirements, Edge Cases & Rules, Out of Scope, Acceptance Criteria.

Conditional, added only when the project needs them: UI/UX Requirements, Data Model, API/Integration, Authentication/Security, Command-Line Interface & Arguments, Performance/Scale, Deployment/Environment, Accessibility, Concurrency, or anything else the build genuinely calls for. A backend script with no UI never gets a UI section forced on it; a project with a real UI must have its UI section written in full or it fails the gate.

Every category is answered twice, deliberately: `spec.md` states *what* and *why*; `plan.md` states *how* — technically. The separation keeps specs stable when technical choices change.

Also: for every conditional category the scan adds, check whether the person already has a relevant skill or plugin installed (e.g. a UI design-system skill). If one exists, draft that section using that skill's conventions instead of generic boilerplate.

## 7. The Two Gates

**Structural Completeness Gate** — runs before any quality scoring (Pass 1 cannot start until it passes):

- **Missing-section check:** every category on the checklist has a real, substantive section — not a stub, not a placeholder. A missing section must be written first; the critique loop is not allowed to "improve" it.
- **Forward-reference check:** nothing refers to something that doesn't exist yet, within the document itself or within the history inherited from earlier milestones.

**Simplicity Gate** — runs alongside, checking the opposite failure (over-engineering):

- Does `plan.md` introduce more standalone projects, services, or libraries than the milestone needs? Each one beyond a small, justified number requires a documented reason.
- Does anything wrap a framework or tool in a custom abstraction where using it directly would have worked?
- Does `spec.md` or `plan.md` contain a feature not traceable to a concrete scenario in `workflow.md` — a "might need this later" addition with no present justification?

Anything caught is sent back for simplification before quality-scoring starts. An unjustified layer of complexity is treated as seriously as a missing requirement.

## 8. Constitution

Every project gets a `constitution.md` — principles fixed for the life of the project, consistent with every milestone's documents. Where the spec answers "what does this milestone need," the constitution answers "what does this project never compromise on, regardless of milestone." It is adopted once at project start, not rewritten per milestone, and cannot be argued around by any milestone's critique loop. Starter articles:

- **Article I — Standalone-First:** Every capability starts as an independently testable unit before it's wired into the larger system.
- **Article II — Observable Interfaces:** Every unit exposes behavior through an interface that can be inspected and scripted from the outside. Behavior observable only by reading source code is a defect.
- **Article III — Tests Before Implementation:** No implementation code is written before its tests exist, have been reviewed, and are confirmed to fail first — enforced through task ordering in `tasks.md`, not discipline.
- **Article IV — Simplicity by Default:** Start with the smallest structure that could work; anything more needs documented justification.
- **Article V — Framework Trust:** Use the tools and frameworks already in play directly; a wrapper needs a specific, stated reason.
- **Article VI — Real-World Testing:** Prefer real dependencies over mocks wherever practical; contract tests are written before the implementation they test.
- **Article VII — Amendment Process:** Changing the constitution requires a written reason and a note on downstream effects, logged as an ADR, never made silently.

## 9. Milestones

- Large projects are split into ordered, dependency-safe delivery milestones; small single-purpose projects stay as one. The CT scan decides which.
- **The five-document set** — every milestone produces all five, each with a distinct job:
  - `spec.md` — what this milestone needs to do, and why (never the how)
  - `plan.md` — the technical how: tech stack, architecture, data model, API/integration contracts, with rationale for each choice
  - `tasks.md` — the ordered, executable steps derived from the plan: exact file paths, dependency order, `[P]` markers for parallel tasks, tests ordered before the code they test
  - `workflow.md` — the scenario-branching tree: every path the milestone must handle
  - `tests.md` — one test per node in the workflow tree, plus one end-to-end real-user walkthrough of the whole tree
- **Cumulative history:** each of the five documents carries a condensed history of everything decided in prior milestones — overall goal, key decisions, what exists, constraints in force — so an AI tool given only that one file, with nothing else, can still build correctly on top of everything that came before. The Out of Scope section explicitly notes what was deliberately deferred to a later milestone.
- **Cross-referencing:** every `spec.md` has a fixed section pointing to its own plan/tasks/workflow/tests; each of those carries a back-reference to the spec. All five stay traceable to each other from any starting point.
- **Dependency ordering:** the CT pass maps exactly what each milestone needs from earlier ones and orders them so nothing depends on something not yet established. `tasks.md` applies the same logic one level down inside a milestone. The Structural Completeness Gate checks every milestone file for references to anything from a future milestone — finding one means the milestones are in the wrong order.
- **Stranger Test scope:** always runs against the full five-document set together.

## 10. History & Traceability

**PHR — Prompt History Records:** every significant interaction — a CT scan, a Clarify session, a critique-loop round, a plan or task generation — is logged automatically, without being asked for. Each record captures what was requested, what was produced, and a short rationale, at:

```
history/prompts/milestone_N/NNN-phase-name.md
```

**ADR — Architecture Decision Records:** not every decision needs one; most are routine and traceable through PHRs. An ADR is warranted when real alternatives existed, the choice is hard to reverse, or it affects more than one milestone. When that test is met, produce an ADR suggestion and wait for the human's confirmation before writing it — ADRs are never created silently. Stored at `history/adr/NNN-decision-title.md`. Constitution amendments always produce an ADR; no significance test for those.

## 11. Run Order

For a given brief, in this exact order, no steps skipped:

1. CT Requirement Scan → Requirement Category Checklist (log a PHR)
2. Adopt constitution (log a PHR; produce ADR if amendments are made)
3. CT milestone breakdown in dependency order (if the project is large enough) (log a PHR)
4. Per milestone, in order:
   a. Draft `spec.md`
   b. Structural Completeness Gate + Simplicity Gate
   c. Pass 1 critique loop (log a PHR per round; save raw critique JSON)
   d. Clarify: ask the human only the compiled `needs_clarify` list; fold answers in (log a PHR)
   e. Draft `plan.md`, `tasks.md`, `workflow.md`, `tests.md` — from the accepted spec
   f. Gates again, across all five documents together
   g. Pass 2 critique loop (full rigor) (log PHRs)
   h. Stranger Test: fresh zero-context session, full five-document set, instruction: *implement this, ask no questions* (log the result)
   i. Build the milestone from the finished documents
5. Update cumulative history at the start of every subsequent milestone
6. When process guidance in this seed differs from the brief (PLAN.md), the brief governs; flag the difference rather than resolving it silently

## 12. Output Layout

```
outputs/
├── constitution.md
├── milestones/
│   └── milestone_N/
│       ├── spec_milestone_N.md
│       ├── plan_milestone_N.md
│       ├── tasks_milestone_N.md
│       ├── workflow_milestone_N.md
│       └── tests_milestone_N.md
├── history/
│   ├── prompts/milestone_N/NNN-phase-name.md
│   └── adr/NNN-decision-title.md
└── critique-log/
    ├── pass1-round-*.json / pass2-round-*.json
    └── stranger-test-milestone-N.md
```

For a project small enough that the scan decides against milestones, the five documents sit at the root of `outputs/` instead, following every other rule identically.