# SDD Multi-Agent Kit — Project Plan

**What this document is:** This is the brief handed to an AI coding tool (with the SDD skill installed) so it can run its own Research → Specify process against this document and produce the real `spec.md`, `plan.md`, `tasks.md`, `workflow.md`, and `tests.md` files. This document itself is the plan, not the formal spec — its job is to make sure every human and every AI tool that reads it understands exactly what is being built and why, in full, with nothing assumed.

**A note on where some of this comes from:** Several patterns below — the plan/tasks split, the constitution-as-governing-articles idea, and the PHR/ADR history system — are adapted from `github/spec-kit` and its enhanced fork `panaversity/spec-kit-plus`, existing open-source Spec-Driven Development toolkits. This project does not depend on either of them or use their code; the patterns are re-implemented here, in this system's own words and its own tool-agnostic, npm-distributed form, credited properly in the repository itself (see §11.2).

---

## 1. What This Project Is

The SDD Multi-Agent Kit is a reusable, open-source framework that brings true Spec-Driven Development to any CLI-based coding agent — Claude Code, Claude Desktop, OpenCode, and Antigravity today, with room to add more later without reworking the core system.

Instead of a single model writing a spec alone — which carries that one model's blind spots straight into the build — this system runs a strict multi-model critique loop: seven independent AI models, from seven different labs, score and challenge every draft with no sugar-coating, round after round, until every one of them is satisfied. A spec only reaches that stage after passing a completeness gate driven by computational thinking, which figures out — for this specific project — exactly what categories of requirements must exist before quality even matters, and a simplicity gate that blocks over-engineering before it takes root. Large projects are broken into ordered, dependency-safe delivery milestones, each producing its own self-contained set of documents — what to build, how to build it technically, the ordered steps to build it, every scenario it must handle, and how each scenario gets verified. Every significant interaction and decision along the way is logged automatically, so nothing about how the system arrived at its output is a mystery later. Before anything is handed off to be built, the finished milestone is stress-tested by handing it to a fresh AI session with zero context, to prove the documents themselves are what's clear — not just that seven models agreed with each other.

The whole system is installed with a single `npm install`, works entirely on free-tier API access, detects which AI tools are already on the user's machine, and installs itself into them directly — no manual configuration.

## 2. Goal — What We Want

- **A milestone this system produces should be trustworthy enough that handing only its own documents to a completely fresh AI session — no other context, no follow-up questions allowed — reliably produces the correct build.**
- No single model's blind spot should ever pass through unchallenged. Every issue in a spec must survive independent scrutiny from more than one model, from more than one lab, before it's considered resolved.
- A spec that is missing something structurally important (for example, no UI requirements for a project that has a UI) must be caught and blocked before the critique loop wastes any effort polishing it. Missing is a different, more serious problem than badly written, and it must be treated that way.
- A design that is more complicated than the problem requires must also be caught and blocked — unjustified complexity is as much a failure as a missing requirement.
- The requirement checklist a spec is measured against must not be static or generic — it must be derived, every time, from what this specific project actually is, using computational thinking to reason about what a build like this genuinely needs.
- What a project needs to do (the spec) and how it will technically be built (the plan) must stay clearly separated, so specs remain stable even when technical choices change.
- The system must be usable by someone with no paid API infrastructure at all — every model in the critique panel must be reachable through a genuinely free tier.
- Every delivery milestone must produce a self-contained set of documents — usable on its own, in the correct dependency order, referencing its own history so nothing upstream needs to be re-read to understand it.
- Every significant AI interaction and every consequential decision must leave a written trace, so the reasoning behind the system's output is never lost.
- The finished project must be a clean, well-documented, open-source repository that a human contributor or an entirely unfamiliar AI tool can pick up cold and understand — what it is, how it works, and how to extend it — without needing anything explained outside the repo itself.

## 3. Grounding

Every mechanism in this system is traceable to a specific concept, not invented loosely:

| System piece | Source |
|---|---|
| 4-phase loop (Research → Specify → Clarify → Build), spec anatomy | Spec-Driven Development crash course |
| Multi-model critique loop, structured rubric scoring | AI Prompting in 2026 — Concept 13, "Models checking models" |
| Heartbeat / body / spine, maker ≠ checker | Loop Engineering crash course |
| Five verbs (constrain, inform, verify, correct, escalate) | Harness Engineering crash course |
| Anchors, frozen nodes, Perez's four failures (gaming, blindness upward, conflict, measurement decay) | Graph Engineering crash course |
| Plan/tasks separation, constitution-as-governing-articles, PHR/ADR history, simplicity gate | Adapted from `github/spec-kit` and `panaversity/spec-kit-plus` |

---

## 4. The Critique Engine

### 4.1 Roles & Critic Panel

**Drafter + Adjudicator:** Claude, running inside whichever CLI tool invoked the skill. Writes drafts, reads every critique each round, decides what to accept or reject with a reason, and produces the next revision. This is the maker — kept structurally separate from the checkers, so the entity writing a document is never the entity approving it.

**Critic Panel — seven models, three provider keys, one tier, every model runs every round:**

| # | Model | Lab | Provider | Key |
|---|---|---|---|---|
| 1 | `nvidia/nemotron-3-ultra-550b-a55b` | NVIDIA | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 2 | `openai/gpt-oss-120b` | OpenAI (open-weight) | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 3 | `z-ai/glm-5.2` | Zhipu / Z.ai | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 4 | `mistralai/mistral-nemotron` | Mistral AI | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 5 | `meta/muse-glimmer-30b` | Meta | NVIDIA NIM | `NVIDIA_NIM_API_KEY` |
| 6 | `gemini-3.6-flash` | Google DeepMind | Google AI Studio | `GOOGLE_AISTUDIO_API_KEY` |
| 7 | `minimax-m3:cloud` | MiniMax | Ollama Cloud | `OLLAMA_API_KEY` |

The panel is read from `kit/config/providers.yaml` at runtime — the engine is config-driven, so panel composition is configuration, not code (per-model timeouts are set there too). The shipped seven-slot composition evolved during the bootstrap: ADR-001 established the original panel; ADR-003 removed the DeepSeek slot, added Mistral-Nemotron and Muse-Glimmer-30B, and introduced the 429 mitigation (first-call stagger + adaptive backoff).

Total: eight voices in every cycle — Claude plus the seven critics above. Every document a milestone produces (§7.2) goes through this same panel; none of them are reviewed by a single model alone.

### 4.2 The Two-Pass Loop

The loop runs twice around the Clarify phase, not once, because polishing wording and resolving business decisions are different problems that need different handling:

**Pass 1 — before Clarify (light):** Runs on the raw draft. Critics score only the objective dimensions — clarity, completeness, edge_case_coverage, internal_consistency — all checkable against the document alone. Testability is subjective (it needs a runtime) and is out of Pass-1 scope; the response schema still requires the key, so Pass-1 critics emit `testability: 0`, meaning "not assessed in this pass". When a critic hits something that is genuinely a subjective or business decision rather than something an AI could correctly infer, it tags that issue `"category": "needs_clarify"` instead of demanding a fix for it. Pass 1 does not require every score to be 10 — it stops once every objective issue is resolved and the full `needs_clarify` list has been compiled. That compiled list becomes the actual question set for the Clarify phase, so the human is only ever asked things an AI genuinely could not have answered on its own.

**Pass 2 — after Clarify (full rigor):** Runs once the human's answers have been folded into the draft. Full seven-critic rigor applies here, stopping only under the conditions in §4.4. The `needs_clarify` category is pass-independent — Pass-2 critics may still tag genuinely new business/subjective decisions with it. This pass also re-checks that the human's answers didn't quietly break consistency somewhere else in the document.

### 4.3 Critique Response Schema

Every critic responds only in this structure — a strict rubric, never free-form praise. The example below is a **Pass-2** response, so all five dimensions carry real scores:

```json
{
  "model": "z-ai/glm-5.2",
  "document": "plan_milestone_2",
  "round": 3,
  "pass": 2,
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

**The one Pass-1 difference.** In a `"pass": 1` response every field above is identical except `testability`, which is **always `0`** — "not assessed in this pass", per §4.2. The key is required by the schema, so it cannot be omitted; scoring it would mean judging a runtime that does not exist yet. Because free-tier critics do not reliably follow that instruction, the engine **normalizes `testability` to 0 on every Pass-1 response** rather than rejecting the critic over it: the rule is a scoping convention, not a correctness test, and losing a whole critique to it would trade real signal for tidiness. Nothing in §4.4's stopping conditions reads `testability`, so the normalization changes no decision — it only keeps the logged data honest about what was actually assessed.

**Validity rule:** A response is invalid, and that critic is excluded from that round only, if `overall_score` is below 10 while `issues` is empty — a low score with nothing to fix is not a critique, it's noise — or if the response can't be parsed into this shape after at most one retry (≤2 attempts). A failed critic is excluded from that round only and participates again next round — no critic is ever excluded across rounds — and a round with zero valid critics never counts as advancement (the round is logged and escalated; see §4.4). The loop never stops silently just because scores aren't 10 — only because a specific voice stopped producing usable signal.

### 4.4 Stopping Conditions

| Condition | What happens |
|---|---|
| Pass 1: every objective issue resolved, `needs_clarify` list compiled | Advance to the Clarify phase |
| Pass 2: every currently-valid critic returns a perfect score | Advance to the Stranger Test |
| A round with `n_valid == 0` (no usable signal) | Never counts as advancement — the round is logged and the escalation note `escalation: round produced no valid critics` is printed |
| A failed or invalid critic | Excluded from that round only; participates again next round — no cross-round exclusion |
| **Two consecutive non-progressing rounds** | Escalate to the human with a full summary — the loop has asymptoted and must not spin silently |
| Round count reaches the safety cap (default 25, configurable, can be disabled) | Escalate to the human with a full summary — never stop without telling anyone |

**Why a non-progression condition is necessary.** A perfect-score round is the
*ideal* Pass-2 exit, not a guaranteed one. Free-tier critics re-raise: past a
certain point a round returns the same objections it returned before — often
verbatim — while the scores sit in the 6–8 band and never climb. Waiting for
all-10s in that state is not rigor, it is an unbounded loop, and the round cap
alone would burn 25 rounds before admitting it. So the loop watches for
*progress*, not just for scores.

**Definition.** A round is **progressing** when either the document changed in
response to it, or it surfaced at least one issue the adjudicator triaged as
genuinely new and actionable. Otherwise it is **non-progressing**. Two are
**consecutive** when no progressing round falls between them. Progression is
tracked at the **session** level — the adjudicator's repeated invocations for one
document and pass — because a single invocation is one round and cannot see its
own predecessor.

**What escalation means here.** Escalation is a message to the human containing
the full summary: the rounds run, the issues accepted and applied, the issues
rejected *with their written reasons*, and the evidence that the remaining flags
are repeats rather than new findings. The human disposes of it. This is the point
of the maker/checker separation in §4.1: the drafter may report that the panel has
stopped producing new signal, but it may not quietly decide on its own that its
own document is finished. A conclusion recorded without that summary is a silent
stop, and silent stops are what every rule in this section exists to prevent.

Non-progression never overrides a gate or the Stranger Test (§4.5). Those are
frozen nodes; only the *quality-scoring* loop can exit this way.

### 4.5 Grounding Anchor — the Stranger Test

Agreement between seven critics is not proof of correctness — models agreeing with each other can still share the same blind spot, and Graph Engineering's warning about measurement decay applies directly here. Once Pass 2 succeeds, the finished milestone's full document set (§7.2 — spec, plan, tasks, workflow, and tests together, not any one file alone) is handed to a fresh, zero-context AI session with a single instruction: implement this, ask no questions. If it builds the right thing, the documents are genuinely clear. If it goes wrong, that failure becomes a new issue fed straight back into the loop, even though every critic already scored it perfectly. This is the one rule the loop is never allowed to reason its way around.

---

## 5. Spec Completeness — the Gates

### 5.1 Computational Thinking Requirement Scan

The first concrete output of the Research phase. Before any document gets written, the stated goal is decomposed using computational thinking — breaking the build down into its fundamental parts, and recognizing what category of project this is — to produce a Requirement Category Checklist specific to this exact project.

Some categories are always required, taken directly from the base anatomy of a spec: Goal, User Scenarios, Functional Requirements, Edge Cases & Rules, Out of Scope, Acceptance Criteria.

Other categories are added only when this specific project needs them: UI/UX Requirements, Data Model, API/Integration, Authentication/Security, Command-Line Interface & Arguments, Performance/Scale, Deployment/Environment, Accessibility, Concurrency, and anything else the project genuinely calls for. A backend script with no user interface never gets a UI section forced onto it; a project with a real user interface must have one written in full, or it fails the gate below.

Every category on this checklist is answered twice, in two different places, on purpose: `spec.md` states *what* is needed and *why* it matters to the user; `plan.md` (§7.2) states *how* it will actually be built, technically. Keeping these separate is deliberate — it's what lets the technical approach change later without the spec itself becoming unstable.

### 5.2 Installed-Skill Awareness

For every conditional category the scan adds, check whether the person already has a relevant skill or plugin installed — a UI design-system skill, for example. If one exists, that section is drafted using that skill's own conventions instead of generic boilerplate, so the output matches how this person actually builds.

### 5.3 Structural Completeness Gate

This runs before any quality scoring begins — Pass 1 of the critique loop cannot start until this gate passes:

- **Missing-section check:** every category on the checklist has a real, substantive section — not a stub, not a placeholder. A missing section is not something the critique loop is allowed to "improve" — it has to be written first.
- **Forward-reference check:** nothing in the draft refers to something that doesn't exist yet, either within the document itself or within the history it inherited from earlier milestones. This same check is reused across milestones — see §7.5.

### 5.4 Simplicity Gate

Runs alongside §5.3, checking for the opposite failure — a design that is more complicated than the problem calls for:

- Does `plan.md` introduce more standalone projects, services, or libraries than the milestone actually needs? Each one beyond a small, justified number requires a documented reason, not a default.
- Does anything in the plan wrap a framework or tool in a custom abstraction where using it directly would have worked?
- Does `spec.md` or `plan.md` contain a feature that isn't traceable to a concrete scenario in `workflow.md` — a "might need this later" addition with no present justification?

Anything this gate catches gets sent back for simplification before quality-scoring starts, the same way a missing section does. An unjustified layer of complexity is treated as seriously as a missing requirement, not as a style preference.

---

## 6. Constitution — Governing Principles

Every project built with this kit gets a `constitution.md` — a short set of principles that stay fixed for the life of the project and that every milestone's documents must be consistent with. Where the spec answers "what does this milestone need," the constitution answers "what does this project never compromise on, regardless of milestone."

`constitution.template.md` (§10.3) ships with a starter set of articles, meant to be adopted as-is or edited once at project start, not rewritten per milestone:

**Article I — Standalone-First:** Every capability starts as an independently testable unit before it's wired into the larger system. Nothing is built directly inside application glue code that couldn't be pulled out and tested on its own.

**Article II — Observable Interfaces:** Every unit exposes its behavior through an interface that can be inspected and scripted from the outside — command-line, API, or equivalent. Behavior that can only be observed by reading source code is a defect, not a design choice.

**Article III — Tests Before Implementation:** No implementation code is written before its tests exist, have been reviewed, and are confirmed to fail first. This is enforced through the task ordering in each milestone's `tasks.md`, not left to discipline alone.

**Article IV — Simplicity by Default:** Start with the smallest structure that could work. Anything more requires a documented justification in the milestone's `plan.md`, not a default assumption that more structure is safer.

**Article V — Framework Trust:** Use the tools and frameworks already in play directly. A wrapper around them needs a specific, stated reason to exist.

**Article VI — Real-World Testing:** Prefer real dependencies over mocks wherever practical. Contract tests are written before the implementation they're testing.

**Article VII — Amendment Process:** Changing this constitution requires a written reason for the change and a note on what it might affect downstream. Amendments are logged as ADRs under `outputs/history/adr/`, never made silently.

These are immutable within a project once adopted — no milestone's critique loop is allowed to argue its way around them; they're a frozen node in the sense §4.5 uses that term. They can only change through the amendment process in Article VII, which is itself deliberately slower and more visible than any single milestone's revision cycle.

**A note on the article wording.** The seven articles above are what `constitution.template.md` ships to every project, so they are written to stand alone: they refer to a milestone's own `tasks.md` / `plan.md` and to `outputs/history/adr/`, never to a section number of *this* brief. A user who installs the kit never receives this document, so an article citing "§5.4" would be a dangling reference in their repository. The rest of this brief may cross-reference itself freely; these seven paragraphs may not.

---

## 7. Build Milestones

### 7.1 Why Milestones Exist

Large projects are split into ordered delivery milestones instead of one single spec file. The computational thinking scan in §5.1 is also what decides whether a given project is large enough to need this — small, single-purpose projects stay as one milestone.

### 7.2 The Milestone Document Set

Every milestone produces five documents together, each with a distinct job:

```
spec_milestone_N.md      — what this milestone needs to do, and why (never the how)
plan_milestone_N.md      — the technical how: tech stack, architecture, data model,
                            API/integration contracts, with rationale for each choice
tasks_milestone_N.md     — the ordered, executable steps derived from the plan: exact
                            file paths, dependency order, [P] markers for tasks that
                            can run in parallel, tests ordered before the code they test
workflow_milestone_N.md  — the scenario-branching tree: every path the milestone must handle
tests_milestone_N.md     — one test per node in the workflow tree, plus one end-to-end
                            real-user walkthrough of the whole tree
```

`spec.md` and `plan.md` are deliberately kept separate for the same reason stated in §5.1 and §2 — what a milestone must accomplish should stay stable even if the technical approach behind it changes later.

### 7.3 Cumulative History

Each of the five documents carries a condensed history of everything decided in every prior milestone — the overall goal, the key decisions already made, what already exists, and any constraints already in force — so that an AI tool given only that one file, with nothing else, can still build correctly on top of everything that came before it. The Out of Scope section of each milestone's spec explicitly notes what has been deliberately deferred to a later milestone, so nothing reads as accidentally forgotten.

### 7.4 Cross-Referencing

Every `spec_milestone_N.md` has a fixed section pointing directly to its own `plan_milestone_N.md`, `tasks_milestone_N.md`, `workflow_milestone_N.md`, and `tests_milestone_N.md`. Every one of those four companion files carries a back-reference at the top pointing to their spec. All five files always stay traceable to each other from any starting point.

### 7.5 Dependency Ordering

The computational thinking pass maps exactly what each milestone actually needs from the milestones before it, and orders the milestones so that nothing ever depends on something that hasn't been established yet. `tasks_milestone_N.md` applies this same ordering logic one level down, inside a single milestone — individual tasks are sequenced so nothing runs before what it depends on, with independent tasks explicitly marked so they can run in parallel. The Structural Completeness Gate from §5.3 checks every milestone file for references to anything from a future milestone — finding one means the milestones are in the wrong order and must be reordered before work continues.

### 7.6 Stranger Test Scope

The Stranger Test from §4.5 always runs against the full five-document set together, never against any single file alone.

---

## 8. History & Traceability

### 8.1 Prompt History Records (PHR)

Every significant interaction with the system — a computational thinking scan, a Clarify session, a critique-loop round, a plan or task generation — is logged automatically, without needing to be asked for. Each record captures what was requested, what was produced, and a short rationale, stored at:

```
history/prompts/milestone_N/NNN-phase-name.md
```

This is distinct from `critique-log/` (§9), which holds only the raw critique JSON from §4.3. PHRs are the readable narrative of how a milestone came to be — useful to a future contributor, or to an AI tool picking up the project later, who needs to understand why something is the way it is without re-deriving it from scratch.

### 8.2 Architecture Decision Records (ADR)

Not every decision needs an ADR — most are routine and already traceable through the PHR log. An ADR is warranted when a decision meets a significance test: real alternatives existed, the choice is hard to reverse later, or it affects more than one milestone. When that test is met, the system produces an ADR suggestion and waits for the human's confirmation before writing it — ADRs are never created silently. Stored at:

```
history/adr/NNN-decision-title.md
```

Constitution amendments (§6, Article VII) always produce an ADR; there is no significance test to pass for those, they're automatic.

---

## 9. Deliverables Produced For Every Project

```
outputs/
├── constitution.md
├── requirement-checklist.md          working artifact — the §5.1 Requirement Category Checklist
├── milestone-breakdown.md            working artifact — the §7.5 split, order, and dependencies
├── milestones/
│   ├── milestone_1/
│   │   ├── spec_milestone_1.md
│   │   ├── plan_milestone_1.md
│   │   ├── tasks_milestone_1.md
│   │   ├── workflow_milestone_1.md
│   │   ├── tests_milestone_1.md
│   │   └── needs_clarify.md          working artifact — the compiled §4.2 Clarify question set
│   ├── milestone_2/
│   │   └── (same five-document set)
│   └── ...
├── history/
│   ├── prompts/
│   │   ├── milestone_0/...           pre-milestone phases: CT scan, constitution, breakdown
│   │   └── milestone_N/...           (single-milestone projects: single-milestone/)
│   └── adr/
│       └── NNN-decision-title.md
└── critique-log/
    ├── pass1-round-N-{document}.json / pass2-round-N-{document}.json  (kept per milestone, per document)
    └── stranger-test-milestone-N.md
```

**Five documents vs. working artifacts.** The five-document set (§7.2) is the milestone's
deliverable — what the Stranger Test receives and what a build is derived from. The four
files marked *working artifact* are not part of that set; they are process state the pipeline
writes so a later phase, or a later session, can read what an earlier phase decided instead
of re-deriving it. They still have fixed paths, because a working artifact nobody can find is
process state that lives only in one session's memory.

**Pre-milestone PHRs.** The CT scan, constitution adoption, and milestone breakdown all run
before milestone 1 exists, so their PHRs go in `milestone_0/`. PHR numbering restarts inside
each folder; ADR numbering is global across the project and never resets.

For a project small enough that the computational thinking scan decides against splitting into milestones, the same five documents sit at the root of `outputs/` instead (`spec.md`, `plan.md`, `tasks.md`, `workflow.md`, `tests.md` — no `_milestone_N` suffix), with `needs_clarify.md` beside them and milestone PHRs under `history/prompts/single-milestone/`, following every other rule exactly the same way.

---

## 10. Distribution — the npm Package and Installer

### 10.1 Setup Wizard Flow

Installed with a single `npm install -g` of the package, and run from the command line afterward. Running it starts an interactive wizard that:

1. Asks for all three API keys together in one setup pass — NVIDIA NIM, Google AI Studio, and Ollama Cloud.
2. Directly beneath the NVIDIA key prompt only, offers a "Guide for Pakistani users" option, since NVIDIA's signup has a regional gap that the other two providers don't share. The guide's actual content is supplied by the maintainer separately — this document only reserves the slot for it.
3. Detects which supported AI tools are already installed on the machine.
4. Lets the person choose which detected tool or tools to install into.
5. Copies the kit's files into the correct location for each chosen tool.
6. Confirms the trigger is active and ready to use.

### 10.2 Target AI Tools

Claude Code, Claude Desktop, OpenCode, and Antigravity. The installer is built around an adapter pattern (see §11.4) specifically so that support for additional tools can be added later without touching the core kit at all.

### 10.3 The Shared Agent-Skills Standard

All four target tools read the same open Agent Skills format — a folder containing `SKILL.md` with YAML frontmatter, plus optional `scripts/`, `references/`, and `assets/` subfolders. The kit's actual skill content is therefore identical across every tool; only the install location differs:

| Tool | Where the files land | How it gets triggered |
|---|---|---|
| Claude Code | `.claude/skills/sdd-multiagent-kit/` (project) or `~/.claude/skills/...` (personal) | A native slash command is created automatically from the folder name — no separate registration step |
| Claude Desktop | The same location as Claude Code, since Desktop shares Claude Code's configuration | Same, automatic |
| OpenCode | Reads `.claude/skills/` directly, so no separate copy is needed once that location is populated | Same slash command works automatically |
| Antigravity | `.agents/skills/sdd-multiagent-kit/` — a separate copy is required here | There is no native slash-command registry in this tool, so the exact trigger phrase is written directly into the skill's own description and instructions, making it reliably recognized as an explicit invocation the same way a slash command would be |

In practice, one copy into `.claude/skills/` covers three of the four tools; one additional copy into `.agents/skills/` covers Antigravity.

---

## 11. The Open-Source Repository

### 11.1 Who This Repository Needs to Work For

Any human contributor, and any AI coding tool encountering this repository for the first time with no other context — including tools not in the currently-supported list — needs to be able to understand what this project is, how it works, and how to extend it, entirely from what's inside the repository.

### 11.2 Required Root Files

- `README.md` — what this project is, why it exists, a quickstart install, and a link to the full guide. Includes a short, clearly marked acknowledgement that the plan/tasks split, the constitution-as-articles pattern, and the PHR/ADR history system are adapted from `github/spec-kit` and `panaversity/spec-kit-plus`.
- `CLAUDE.md` — project instructions for Claude-family tools working inside this repository
- `AGENTS.md` — project instructions written in the cross-tool AGENTS.md convention, for any other agent working in this repository
- `CONTRIBUTING.md` — how to contribute, including a full walkthrough of how to add support for a new AI tool or a new critic model
- `SECURITY.md` — how to report a security issue privately, and what's in scope
- `SUPPORT.md` — where to ask questions and file issues, separate from security reports
- `LICENSE`
- `CHANGELOG.md`
- `docs/GUIDE.md` — the complete usage guide: the setup wizard walkthrough, how the critique loop actually works, how milestones work
- `docs/ARCHITECTURE.md` — a readable explanation of this system's architecture, for anyone who wants to understand it deeply without reading source code
- `docs/BOOTSTRAP.md` — a historical record of how the kit was built the first time, using its own process on itself before any of its automation existed; not part of the kit's ongoing operation, kept for anyone who wants to understand how the project came to exist

### 11.3 Repository Structure

```
sdd-multiagent-kit/
├── README.md
├── CLAUDE.md
├── AGENTS.md
├── CONTRIBUTING.md
├── SECURITY.md
├── SUPPORT.md
├── LICENSE
├── CHANGELOG.md
├── package.json
├── bin/
│   └── setup-wizard.js
├── installers/
│   ├── claude-code.js
│   ├── claude-desktop.js
│   ├── opencode.js
│   └── antigravity.js
├── kit/
│   ├── SKILL.md
│   ├── constitution.template.md
│   ├── config/
│   │   └── providers.yaml
│   ├── skills/
│   │   ├── research-ct-scan/SKILL.md
│   │   ├── specify/SKILL.md
│   │   ├── plan-builder/SKILL.md
│   │   ├── task-breakdown/SKILL.md
│   │   ├── critique-loop/SKILL.md
│   │   ├── clarify-interview/SKILL.md
│   │   ├── milestone-builder/SKILL.md
│   │   ├── workflow-builder/SKILL.md
│   │   ├── scenario-tester/SKILL.md
│   │   ├── stranger-test/SKILL.md
│   │   └── history-logger/SKILL.md
│   └── scripts/
│       ├── orchestrate_critique_loop.py
│       └── validate_critique.py
├── docs/
│   ├── GUIDE.md
│   ├── ARCHITECTURE.md
│   └── BOOTSTRAP.md
└── examples/
    └── sample-project/
```

### 11.4 The Extension Pattern

Every file inside `installers/` implements the same small interface — `detect()`, `install(paths)`, `confirmEnabled()`. Adding a new AI tool later means writing one new file in `installers/` and registering it in `bin/setup-wizard.js`; nothing inside `kit/` needs to change. `CONTRIBUTING.md` documents this pattern with a full worked example, alongside a matching walkthrough for adding a new critic model to `kit/config/providers.yaml`.

---

## 12. Decisions Still Open

These are stated as working assumptions in this document but are not yet confirmed, and should not be treated as final by anyone building from this plan:

| Item | Status |
|---|---|
| npm package and repository name | Decided during bootstrap: `sdd-multiagent-kit` (package.json) |
| In-tool trigger command | Decided during bootstrap: `/sdd` (kit/SKILL.md frontmatter, `name: sdd-multiagent-kit`) |
| License | Decided during bootstrap: MIT |
| Content of the "Guide for Pakistani users" | Still open — only the slot exists (§10.1); content supplied by the maintainer |

---

## 13. Handoff Instructions

When this plan is given to an AI tool running the SDD skill: run the computational thinking Requirement Scan from §5.1 against this plan itself first. This project is large enough to need milestone splitting per §7.1. Produce the milestone breakdown in dependency order, then for each milestone: draft `spec.md`, run Pass 1 of the critique loop, draft `plan.md` from the accepted spec, draft `tasks.md` from the accepted plan, draft `workflow.md` and `tests.md`, run the Structural Completeness and Simplicity Gates across all five documents together, run Clarify against the compiled `needs_clarify` list — starting with the items in §12 — then run Pass 2 on all five documents, then run the Stranger Test on the finished set, then build. Log a PHR at every phase transition automatically; suggest an ADR whenever a decision meets the significance test in §8.2.
