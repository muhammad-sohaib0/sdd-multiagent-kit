# SDD Multi-Agent Kit — Milestone 1 Spec (rev 3)

**Document:** `spec_milestone_1.md`
**Milestone:** 1 of 5
**Status:** Returning from Pass 1 (round 2)

## Cumulative History (inherited context)

This document is the first deliverable of the SDD Multi-Agent Kit build. Everything here is in force and must be honored by every M1 document.

- **Overall goal:** a reusable, open-source, npm-distributed framework (`sdd-multiagent-kit`) that brings genuine Spec-Driven Development to CLI coding agents (Claude Code, Claude Desktop, OpenCode, Antigravity) via a strict multi-model critique loop (seven models), a computational-thinking requirement gate, a simplicity gate, dependency-ordered milestones, five-document milestone sets, and automatic PHR/ADR history logging. Installable with a single `npm install -g`, running entirely on free-tier API access.
- **Trigger command:** `/sdd` (shipped by M3). **License:** MIT.
- **Constitution (adopted, `outputs/constitution.md`):** Standalone-First; Observable Interfaces; Tests Before Implementation; Simplicity by Default; Framework Trust; Real-World Testing; Amendment Process. Immutable for the life of this project.
- **Critic panel (lock incl. ADR-001, revised by ADR-003):** seven models, three provider keys, one free tier — `nvidia/nemotron-3-ultra-550b-a55b`, `openai/gpt-oss-120b`, `z-ai/glm-5.2`, `mistralai/mistral-nemotron`, `meta/muse-glimmer-30b` (all NVIDIA NIM / `NVIDIA_NIM_API_KEY`); `gemini-3.6-flash` (Google AI Studio / `GOOGLE_AISTUDIO_API_KEY`); `minimax-m3:cloud` (Ollama Cloud, id `ollama-cloud` / `OLLAMA_API_KEY`). DeepSeek's V4 flash slot was removed and replaced by the two additional NVIDIA NIM voices per ADR-003.
- **Retry policy (PHR milestone_0/003, which covers the bootstrap Clarify + provider preflight + retry policy):** unparseable response → up to 2 tries; transport failure → up to 5 tries with adaptive backoff (429 → 30s × attempt, other transport failures → 8s × attempt); no cross-round exclusion — a failed critic participates again next round; the loop continues with the remaining valid critics (PLAN.md §4.3–§4.4).
- **Deliverable locations:** milestone sets under `outputs/milestones/`; PHRs under `outputs/history/prompts/`; ADRs under `outputs/history/adr/`; critique JSON under `outputs/critique-log/`. Shipped kit materializes in the `PLAN.md` §11.3 repo layout.

**Cross-reference convention for this project:** all references with an explicit `PLAN.md` prefix point at the brief. Bare references (§3, §4.3, FR-x, AC-x) point at sections of *this* document. No bare number is ever left ambiguous.

---

## 1. Goal

Produce the **core process content** of the kit: the master skill file, the constitution template, the provider/model configuration, and the ten process sub-skills that together encode the SDD workflow — so that this content, installed into a target CLI tool, can run the entire Research → Specify → Clarify → Build pipeline on a project brief. This milestone deliberately excludes the critique engine's automation (the `critique-loop` sub-skill and the orchestration/validation scripts are Milestone 2) and the installer (Milestone 3).

## 2. User Scenarios

**US-1 — First run on a brief.** A user has the M1 content installed in a supported CLI tool (the `/sdd` trigger and installer are M3; until then the content is placed manually into the tool's skills directory per the Agent-Skills standard — `.claude/skills/sdd-multiagent-kit/` for Claude-family and OpenCode, `.agents/skills/...` for Antigravity — and invoked by the skill's name rather than `/sdd`). Invoking the kit's entry point with a project brief must decompose it (CT scan), adopt a constitution, decide milestone splitting, and begin producing the first milestone's documents, logging PHRs throughout.

**US-2 — Multi-milestone project.** A large brief produces several ordered milestones. Each milestone's documents carry cumulative history so a later milestone (or a later fresh session) builds on earlier ones without re-reading them all.

**US-3 — Small single-milestone project.** A small brief correctly stays a single milestone (the CT scan detects this). Its five documents land **directly in `outputs/`** (named `spec.md`, `plan.md`, `tasks.md`, `workflow.md`, `tests.md` — no `_milestone_N` suffix), while `outputs/history/prompts/single-milestone/` and `outputs/history/adr/` still hold its history. Every rule (gates, critique, Stranger Test, logging) applies identically.

**US-4 — Extensibility.** A contributor adds a new critic model: a **data-only change to `kit/config/providers.yaml`**; the process-instruction SKILL.md files must not contain model IDs needing edits. A new target tool is added later, in M3's installer.

## 3. Functional Requirements

### FR-1 — Master skill orchestration (`kit/SKILL.md`)

The master skill defines the whole pipeline, runs the gates (below), and dispatches to sub-skills. Like every SKILL.md, it carries the mandatory frontmatter (`name`, `description`, `version` — §4.2). Stated order:

1. Run `research-ct-scan` → produce the Requirement Category Checklist (base + conditional), with installed-skill awareness (PLAN.md §5.2).
2. Adopt/create the project's `constitution.md` (written to `outputs/constitution.md` per PLAN.md §9) from `constitution.template.md`, **once at project start** — adopted as-is or edited then; it is reused for every subsequent milestone and changed only through amendments (PLAN.md §6).
3. Run `milestone-builder` → using the CT scan output, decide single- vs. multi-milestone and order the split. Output = an ordered milestone list recorded as a PHR (`outputs/history/prompts/milestone_0/NNN-milestone-breakdown.md` — the phase-zero folder, see §4.5) plus creation of `outputs/milestones/milestone_N/` folders.
4. Per milestone, in order:
   a. `specify` → draft `spec.md` from the checklist
   b. **Gate checkpoint G1** — the Structural Completeness and Simplicity gates (defined in §3A) on the spec
   c. **Critique phase, Pass 1** *(automation arrives in M2)* — light pass; objective dimensions only; compile the `needs_clarify` list (PLAN.md §4.2)
   d. `clarify-interview` → fold the compiled `needs_clarify` list into concise questions, ask only what an AI could not infer, and fold the answers into the spec (the authoritative *what*); the plan is drafted afterwards, so it reflects the answers by construction
   e. From the accepted spec: `plan-builder` → `task-breakdown` → `workflow-builder` → `scenario-tester` (this 4e order is the canonical document-generation sequence; the FR-2 table is an inventory of the ten sub-skills, not a pipeline sequence)
   f. **Gate checkpoint G2** — both gates, across all five documents together
   g. **Critique phase, Pass 2** *(automation arrives in M2)* — full rigor on all five; re-checks the Clarify answers did not break consistency elsewhere
   h. `stranger-test` on the finished five-document set
   i. **Build the milestone** (defined below)
5. Run `history-logger` at every phase transition — the enumerated transitions in §4.5 — (PHR), and on any decision meeting the ADR significance test (PLAN.md §8.2; the test is defined in §4.5). ADR suggestions are a **blocking** human-confirmation step, never async.

**About "build the milestone" (step 4i).** "Build" means *execute the milestone's ordered tasks to materialize that milestone's artifacts* — the deliverables whose paths are defined in its `tasks_milestone_N.md`. For the kit's own bootstrap build (this project), the process running now authors the 13 files at the §4.1 paths; those files then become the running kit (the authored `kit/SKILL.md` is the orchestrator for *user* projects afterwards). "Build" does **not** mean installing or distributing the kit (that is M3).

**About the critique phase and gates — M1's exact scope.**

- **The critique phase is a fixed pipeline invariant:** seven models, two passes, the critique schema and validity rule (PLAN.md §4.3), and the stopping conditions (PLAN.md §4.4).
- **Its automation is Milestone 2:** the `critique-loop` sub-skill and the orchestration/validation scripts are delivered in M2. In M1 the master skill states the invariant and marks the executable step as "(automation arrives in M2)".
- **The `/sdd` trigger, installer, and live script wiring are M3.**
- **`critique-loop` is the 11th sub-skill, owned by M2.** The ten M1 sub-skills below are the M1 deliverable inventory.
- **The gates are master-skill orchestration checkpoints, not sub-skills** — invariants the master enforces before Pass 1 (G1 on the spec) and before Pass 2 (G2 on all five).

### FR-2 — Sub-skill contract (the ten M1 sub-skills)

Every sub-skill is an Agent-Skills-format folder `kit/skills/<name>/SKILL.md` (YAML frontmatter `name`, `description`, `version`; body = instructions). **Every** `SKILL.md` MUST carry those three frontmatter fields (name is kebab-case). Each sub-skill has a defined input, output, and at least one edge-case rule:

| Sub-skill | Input → Output | Edge-case rule |
|---|---|---|
| `research-ct-scan` | project brief → Requirement Category Checklist (base + conditional, with installed-skill awareness) | Empty/blank brief → halt and ask the user for a brief; never fabricate one. *Installed-skill awareness* means: the sub-skill directs the invoking agent to list the skill/plugin directories of the tool it is running in (independent of the M3 installer — it inspects the agent's own runtime, not a deployment). If the agent cannot enumerate them, treat installed-skill awareness as "none detected" and use generic boilerplate. If a skill matches a conditional category, draft that category with that skill's conventions (PLAN.md §5.2). If several match, use the one whose description most closely matches the category; if none clearly matches, use generic boilerplate |
| `specify` | approved checklist + milestone scope → draft `spec.md` | A checklist category with no substantive content → write it in full first; a missing category is a defect to write, not a quality issue to critique |
| `plan-builder` | accepted `spec.md` → draft `plan.md` (stack, architecture, data model, integrations, rationale) | A planned standalone project/service/library with no documented justification → flag it (Simplicity gate), don't ship silently |
| `task-breakdown` | accepted `plan.md` → ordered `tasks.md` (exact paths, dependency order, `[P]` parallel, tests-first) | A task depending on an unlisted prior task → reorder; never leave an orphan dependency |
| `clarify-interview` | Input: the compiled `needs_clarify` list — a set of `{section, problem, why_it_matters}` items compiled by Pass 1 from critics' `needs_clarify`-tagged issues (schema per PLAN.md §4.3), persisted as a Markdown bullet list at `outputs/milestones/milestone_N/needs_clarify.md` — each entry written `- **section**: problem — why_it_matters` (single-milestone projects: `outputs/needs_clarify.md`) → Output: human answers folded into the spec | Empty list → skip gracefully, ask nothing (PLAN.md §4.2); a folded answer that breaks consistency elsewhere → surfaced again in Pass 2 (a consistency edit, not a second Clarify round — Clarify itself runs once per milestone, AC-5). If the human declines or gives an invalid answer → record the refusal in the PHR, drop that question, and note it in the milestone's Out of Scope rather than silently defaulting |
| `milestone-builder` | CT scan output → milestone breakdown (dependency order + cumulative history) | A milestone referencing a future milestone's artifact → signals wrong order; reorder (PLAN.md §7.5) |
| `workflow-builder` | accepted spec + plan → `workflow.md` scenario-branching tree | A feature in spec/plan with no scenario in the tree → unjustified complexity; send back (Simplicity gate) |
| `scenario-tester` | `workflow.md` → `tests.md` (one test per node + one e2e walkthrough) | A branch with no test node → add the test; never leave a path untested |
| `stranger-test` | finished five-document set → verification result, or **new loop issue(s)** | A failure becomes a new issue fed back into the loop — the one rule the loop may not reason its way around (PLAN.md §4.5). Re-entry is bounded by the same round safety cap as the critique loop (PLAN.md §4.4, default 25); at the cap the master escalates to the human |
| `history-logger` | any phase transition / significant decision → PHR; ADR suggestion when the significance test (PLAN.md §8.2) is met | A transition with no produced artifact → record it anyway (requested, produced, rationale); never create an ADR silently — always block for human confirmation |

**Shared sub-skill failure policy.** A "failure" is a sub-skill being unable to produce its required output — an exception, a timeout, or output that fails validation. On failure the master skill logs a PHR, then retries once **with the same input and no backoff**; if it fails again, escalation is **blocking**: the master reports to the human with a summary and stops. Never silent, never an unbounded retry loop.

### FR-3 — Constitution template (`kit/constitution.template.md`)
Ships the seven starter articles from PLAN.md §6 **verbatim** (Standalone-First; Observable Interfaces; Tests Before Implementation; Simplicity by Default; Framework Trust; Real-World Testing; Amendment Process) as a template to adopt as-is or edit once at project start. The seven titles and governing one-liners above are the *contract*; the template renders each article's full PLAN.md §6 wording. AC-6 verifies verbatim rendering against PLAN.md §6, which the bootstrap verifier holds (during normal kit use the template ships pre-verified). Must be valid Markdown suitable to become a project's `constitution.md`.

### FR-4 — Provider configuration (`kit/config/providers.yaml`)
The single source of truth for the critic panel: the seven model IDs (post ADR-001/ADR-003), their provider, the env-var each provider reads, and an ordered `critic_slots` map that **binds each slot to both a model and its provider** — so the panel composition and critique order are fully data-driven with no inference. Adding a model is a data-only edit. No literal secrets — only variable names. `critic_slots` order is significant (critique order) and must be preserved.

**Validation rule:** every model ID listed in a `critic_slots` slot must appear in the `models` list of the provider whose `id` equals that slot's `provider` value (i.e., the string values match exactly). No duplicate model IDs within a provider's `models` list, and no duplicate model across `critic_slots`. A slot whose model is retired or gated (as happened to the Qwen slot, ADR-001) is a config defect resolved by a data-only swap through an ADR; at runtime, transient/provider failures are absorbed by the retry machinery (PLAN.md §4.3–§4.4). The top-level `version` field is the config's **schema version** (`1` = current); on a breaking schema change it increments and the M2 loader migrates or rejects accordingly.

## 3A. The Two Gates (orchestration checkpoints)

- **Structural Completeness Gate:** every category on the checklist has a real, substantive section (no stub, no placeholder); and nothing references something that doesn't exist within the document set or its inherited cumulative history. *Forward-reference check criteria:* a reference is flagged if its target (a file, section, artifact, or earlier-milestone item) is not present in the set or the inherited history. **Inherited cumulative history** = the adopted constitution (`outputs/constitution.md`), the PHR records under `outputs/history/`, and any accepted ADRs. The check is performed at G1 and G2, and is reused across milestones (PLAN.md §5.3, §7.5).
- **Simplicity Gate:** no more standalone projects/services/libraries than the milestone needs. A **standalone component** is a separately installed/deployed unit the milestone *adds* — a new package, service, or executable — not an internal module or a dependency already in play, and **not** the kit deliverable itself (the kit's shipped content set — all 13 M1 files — counts as the single kit deliverable, not as thirteen components). The default limit is **3** standalone components **per milestone** (a constant in the master skill, overridable project-wide once, in `constitution.md` — the override changes the default for all subsequent milestones); each component beyond the limit requires a written justification, recorded in `plan.md` under a "Simplicity Justifications" subsection and logged as a PHR. No wrapping of a framework/tool in a custom abstraction where using it directly would work. No feature that isn't traceable to a scenario in `workflow.md` (PLAN.md §5.4).
- Both gates treat unjustified complexity as seriously as a missing requirement. G1 applies them to the spec alone (the only document that exists at that stage — a deliberately partial application); G2 re-applies them to all five together. They are **master-skill orchestration checkpoints, not sub-skills**, and the master skill re-applies them in **every** milestone: G1 on each spec before that milestone's Pass 1, G2 on each five-document set before that milestone's Pass 2. **Gate-failure behavior:** when a gate fails, the master skill logs a PHR with the findings, blocks the pipeline, and returns the document to the responsible drafting sub-skill with the findings; the critique loop may not argue a gate finding away (gates, like the Stranger Test, are not negotiable).

## 4. Data Model

### 4.1 The M1 content inventory (exact paths — the 13 shipped files)

| # | Exact path | Content |
|---|---|---|
| 1 | `kit/SKILL.md` | master skill |
| 2 | `kit/constitution.template.md` | seven-article template |
| 3 | `kit/config/providers.yaml` | critic panel config |
| 4 | `kit/skills/research-ct-scan/SKILL.md` | sub-skill |
| 5 | `kit/skills/specify/SKILL.md` | sub-skill |
| 6 | `kit/skills/plan-builder/SKILL.md` | sub-skill |
| 7 | `kit/skills/task-breakdown/SKILL.md` | sub-skill |
| 8 | `kit/skills/clarify-interview/SKILL.md` | sub-skill |
| 9 | `kit/skills/milestone-builder/SKILL.md` | sub-skill |
| 10 | `kit/skills/workflow-builder/SKILL.md` | sub-skill |
| 11 | `kit/skills/scenario-tester/SKILL.md` | sub-skill |
| 12 | `kit/skills/stranger-test/SKILL.md` | sub-skill |
| 13 | `kit/skills/history-logger/SKILL.md` | sub-skill |

`critique-loop` (the 11th sub-skill) is **not** in this inventory; it is owned by M2 (§3, FR-1).

### 4.2 Patterns and naming
- A sub-skill is `kit/skills/<name>/SKILL.md`, optionally with `scripts/`, `references/`, `assets/`.
- SKILL.md frontmatter: YAML `name` (kebab-case), `description` (one paragraph on what the sub-skill does and when to use it), `version` (semantic versioning, e.g. `0.1.0`).
- Milestone files: `spec|plan|tasks|workflow|tests_milestone_N.md` under `outputs/milestones/milestone_N/`, i.e. `spec_milestone_1.md`, `plan_milestone_1.md`, `tasks_milestone_1.md`, `workflow_milestone_1.md`, `tests_milestone_1.md`.
- Single-milestone files: `spec.md`, `plan.md`, `tasks.md`, `workflow.md`, `tests.md` directly under `outputs/`.

### 4.3 providers.yaml schema
```yaml
version: 1

providers:
  - id: nvidia-nim
    key_env: NVIDIA_NIM_API_KEY
    tier: free
    models:
      - id: nvidia/nemotron-3-ultra-550b-a55b
      - id: openai/gpt-oss-120b
      - id: z-ai/glm-5.2
      - id: mistralai/mistral-nemotron
      - id: meta/muse-glimmer-30b
  - id: google-ai-studio
    key_env: GOOGLE_AISTUDIO_API_KEY
    tier: free
    models:
      - id: gemini-3.6-flash
  - id: ollama-cloud
    key_env: OLLAMA_API_KEY
    tier: free
    models:
      - id: minimax-m3:cloud

# Ordered critique panel; index is critique order. Each slot binds a model to its provider (no inference).
# VALIDATION: every slot.model must exist under providers[<slot.provider>].models (see FR-4).
critic_slots:
  - model: nvidia/nemotron-3-ultra-550b-a55b
    provider: nvidia-nim
  - model: openai/gpt-oss-120b
    provider: nvidia-nim
  - model: z-ai/glm-5.2
    provider: nvidia-nim
  - model: mistralai/mistral-nemotron
    provider: nvidia-nim
  - model: meta/muse-glimmer-30b
    provider: nvidia-nim
  - model: gemini-3.6-flash
    provider: google-ai-studio
  - model: minimax-m3:cloud
    provider: ollama-cloud
```
`critic_slots` order is the critique order; the engine iterates it in order and resolves each slot's provider explicitly. Each model ID in `critic_slots` must also exist under a `providers[].models` entry of the same `provider` id. **Note on model-id prefixes:** NVIDIA NIM hosts open-weight third-party models (e.g., OpenAI's open-weight GPT-OSS, Mistral's Nemotron, and Meta's Muse-Glimmer); the org prefix in a model id reflects the *origin lab*, not the hosting provider. The seven slots remain seven distinct models across three providers.

### 4.4 PHR / ADR records
- **PHR** — narrative (what was requested, what was produced, short rationale) at `outputs/history/prompts/milestone_N/NNN-phase-name.md`. **Numbering resets per milestone** within each milestone's folder (001, 002, …). Single-milestone projects use `outputs/history/prompts/single-milestone/`.
- **ADR** — (status, date, applies-to, context, decision, why-not-alternatives, consequences) at `outputs/history/adr/NNN-decision-title.md`. **Numbering is global across the project** (001, 002, …), never resetting.
- PHRs are the readable narrative; `outputs/critique-log/` holds only raw critique JSON.

### 4.5 Supporting artifacts and formats (used by the process content)

- **Requirement Category Checklist format:** a Markdown table with columns `category | required (base|conditional) | why needed` (or `n/a` for a rejected conditional category, with the reason). Row order: base categories first (in the fixed order Goal, User Scenarios, Functional Requirements, Edge Cases & Rules, Out of Scope, Acceptance Criteria), then conditional categories (in the order they were derived). Produced by `research-ct-scan`, consumed by `specify`.
- **`needs_clarify.md` format and status:** a **runtime working artifact** of a run (not one of the 13 shipped kit files), at `outputs/milestones/milestone_N/needs_clarify.md` (single-milestone: `outputs/needs_clarify.md`). Format: a Markdown bullet list, each entry `- **section**: problem — why_it_matters` (matching the FR-2 contract). **Lifecycle:** created by Pass 1's critique compile; `clarify-interview` appends the human's answers to it and folds them into the spec; it is then retained as a record of the Clarify round. It is not part of the five-document set or the shipped content.
- **Enumerated phase transitions (the master skill logs a PHR at each):** after the CT scan; after constitution adoption; after milestone breakdown; and per milestone — after `specify`, after G1, after Pass 1, after `clarify-interview`, after each of plan/tasks/workflow/tests generation, after G2, after Pass 2, after `stranger-test`, and after build. This is the full list of transitions the master skill walks.
- **PHR template** (at `outputs/history/prompts/milestone_N/NNN-phase-name.md`): a `# PHR NNN — <phase>` heading, then three short fields — *What was requested / What was produced / Rationale*. `What was produced` is the literal string `none` for a transition that produced no artifact.
- **ADR template** (at `outputs/history/adr/NNN-decision-title.md`): `# ADR-NNN — <title>` then `Status`, `Date`, `Applies to`, and four sections — *Context, Decision, Why not alternatives, Consequences*. (Matches the format already used for ADR-001.)
- **Milestone-zero phase folder:** `outputs/history/prompts/milestone_0/` holds the pre-milestone PHRs (CT scan, constitution, milestone breakdown, and the Clarify of PLAN.md §12 open decisions, PHR milestone_0/003). Normal kit projects that are single-milestone use `outputs/history/prompts/single-milestone/` instead.
- **Sub-skill failure retry semantics:** as specified in FR-2's shared sub-skill failure policy — a single retry re-runs the sub-skill with the same input and no backoff; if it fails again, escalation is blocking. This restates FR-2 for completeness; FR-2 is authoritative.
- **`tier` semantics:** metadata for the provider's access class; currently `free` for all three. Reserved for future non-free tiers; the engine uses it for logging/expectations, not behavior.
- **Simplicity default (3) and override:** the default of 3 standalone components is a **per-milestone** heuristic (each milestone's `plan.md` is evaluated against it independently) in the spirit of Simplicity by Default; it is not a scientifically-derived constant. The default number itself lives in the master skill's gate instructions. It is overridable once — a single change to the default, after which the new value applies to all subsequent milestones — by editing the project's **adopted** `constitution.md` (the copy created from the shipped template at project start; the shipped `constitution.template.md` itself is never edited) and appending a plain-text line `simplicity_default: N` (a convention line inside the Markdown document, not a YAML file); any override is a constitution change and so requires an ADR (PLAN.md §6, Article VII).
- **Secret allowlist:** an explicit, enumerated list in §6 — **by default empty**, i.e.:
  ```
  allowlist: []
  ```
  A token may be added to the allowlist only with a written reason (a PHR) stating why it is not a credential; additions are never silent.
- **Back-reference format:** each companion (plan/tasks/workflow/tests) opens with `> Companion to: outputs/milestones/milestone_1/spec_milestone_1.md` for multi-milestone projects, or `> Companion to: outputs/spec.md` for single-milestone projects.
- **ADR significance test (PLAN.md §8.2):** an ADR is warranted when *real alternatives existed*, *the choice is hard to reverse*, or *it affects more than one milestone*. Constitution amendments always produce an ADR (no significance test for those).
- **AC-7 "consistent with its FR-2 contract":** this means the SKILL.md must name the sub-skill's input, output, and at least the edge-case rule from its FR-2 row — any wording is acceptable as long as those three are present and not contradicted.
- **Gate name convention:** always written as **Structural Completeness Gate** and **Simplicity Gate** (never hyphenated, e.g. not "Structural-Completeness").

## 5. API / Integration

- Configuration-only expression, on the free tier, of the three provider integrations the critique engine will call (the calls themselves are M2).
- Each provider reads exactly one documented env var; no hard-coded credentials; no shipped secrets (§6).
- Free-tier-compatible by construction: the seven models are verified reachable on the free tiers (preflight, the kit's own bootstrap preflight PHR milestone_0/003; incl. the ADR-001 correction). Preflight verification is a documented claim + acceptance-criterion check, **not** a shipped M1 script (scripts are M2).

## 6. Authentication / Security

- **No secrets in content:** `providers.yaml` and every `SKILL.md` reference only env-var *names*, never values. The shipped kit never contains an API key.
- **Secret-handling doctrine:** keys live in the user's environment only (`.env` or shell); nothing in M1 content reads, logs, or commits a key value; PHR/critique logs never embed key material.
- **Concrete detection rule:** reject any token matching `sk-[A-Za-z0-9]{20,}`, `AIza[0-9A-Za-z_-]{35}`, `Bearer [A-Za-z0-9._-]{20,}`, or a base64/hex blob ≥ 32 chars that is not an obvious, allowlisted constant. A "secret value" is text assignable to one of the three documented key env-vars or a key-bearing credential string. The scan operates on the 13 shipped files only (§4.1). The first three patterns above are regex-expressible; the ≥32-char blob rule is a **heuristic** (not fully regex-expressible, because "obvious/allowlisted constant" is qualitative) enforced by a small check helper in `tests_milestone_1.md`. Secret-shaped tokens that are *not* secrets are excluded via an **explicit allowlist enumerated inline here**:
```
allowlist: []
```
By default there are no allowlisted secret-shaped tokens in the 13 shipped files; additions follow the §4.5 criteria (written reason + PHR, never silent). The ≥32-char blob rule targets secret-like randomness; known long non-secrets that legitimately appear (e.g., a UUID) are covered by the allowlist if any ever ships. The allowlist's contract location is inline in this §6; executable enforcement lives in `tests_milestone_1.md`.

## 7. Out of Scope (deferred — named, not forgotten)

- **Critique engine automation** — `orchestrate_critique_loop.py` / `validate_critique.py` **and** the `critique-loop` sub-skill → **M2**.
- **Installer & setup wizard** — four tool adapters, the wizard, the `/sdd` trigger, npm packaging mechanics → **M3**.
- **Repository documentation & distribution surface** — README, CLAUDE.md, AGENTS.md, CONTRIBUTING.md, SECURITY.md, SUPPORT.md, LICENSE, CHANGELOG.md, docs/GUIDE.md, docs/ARCHITECTURE.md, docs/BOOTSTRAP.md → **M4**.
- **Examples** — `examples/sample-project` → **M5**.
- Performance/Scale, Concurrency, UI/UX, Accessibility, Localization, and Deployment are **not** requirement categories for this milestone (a process-content milestone); the milestones that realize those subsystems own them. M1 commits to: base anatomy + Data Model + API/Integration + Authentication/Security.

## 8. Acceptance Criteria

**AC-1.** All 13 files at the §4.1 paths render as valid, substantive content — no stubs, no placeholders. **Enforcement:** the milestone's build step must complete them at the §4.1 paths (verified against `tasks_milestone_1.md`), the Stranger Test (AC-7) verifies contract parity, and the multi-model panel reviews the documents. (The G1/G2 gates operate on the milestone *documents*, not on the built kit files.)

**AC-2.** `providers.yaml` matches §4.3; reflects the ADR-001/ADR-003 panel; encodes ordered `critic_slots` with explicit model→provider binding; references env-var names only; seven models verified on free tiers (the kit's own bootstrap preflight PHR milestone_0/003).

**AC-3.** No secret value (per §6's concrete rule) appears in the 13 shipped files. **Pass criterion:** the scan reports **zero matches** of the four detection patterns against all 13 files (allowlist respected; the allowlist is empty by default) — the regex scan passes.

**AC-4.** Each of the ten sub-skills has a defined input/output and ≥1 edge-case rule (per the FR-2 table), is reachable from the master skill's pipeline, and `critique-loop` is not silently counted as an M1 deliverable.

**AC-5.** The master skill's pipeline expresses the full phase order (incl. the critique invariant and the G1/G2 checkpoints), names the M2 deferral and /sdd/M3 deferral explicitly, and states Clarify runs **once per milestone** after the spec's Pass 1.

**AC-6.** The constitution template renders the seven articles verbatim from PLAN.md §6.

**AC-7.** **Stranger Test.** The completed five-document set (spec + plan + tasks + workflow + tests — these five together form the input brief, per PLAN.md §7.6; never any single file alone) is handed to a genuinely fresh zero-context session with the single instruction *implement this, ask no questions*. "Reproduce" = **contract parity, not byte parity** — the three enumerated checks below are necessary and sufficient, and are **fully specified within this five-document set, so the stranger needs no external PLAN.md** (PLAN.md references in these documents are context pointers for the verifier, not inputs the stranger needs): (1) the produced inventory matches the 13 §4.1 paths with all ten sub-skills present and **no `critique-loop` sub-skill among them**; (2) `providers.yaml` carries the seven panel model IDs (ADR-001/003) in ordered `critic_slots` each bound to a provider; (3) the constitution template renders the seven articles verbatim, and each sub-skill's SKILL.md is consistent with its FR-2 input/output/edge-case ("consistent with" is defined in §4.5; exact prose need not match).

---

## 9. Cross-Reference

The five-document set is the Stranger Test input. This spec governs, and is governed by:

| Document | Path |
|---|---|
| Spec (this file) | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests | `outputs/milestones/milestone_1/tests_milestone_1.md` |

Each companion carries a back-reference to this spec at its top.