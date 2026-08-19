# SDD Multi-Agent Kit — Milestone 5 Spec

**Document:** `spec_milestone_5.md`
**Milestone:** 5 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_5/spec_milestone_5.md`

## Cumulative History

Inherited from M1 (kit content), M2 (critique engine), M3 (installer), M4 (distribution docs), all verified. This milestone ships the worked example promised by M4 (README/GUIDE point to `examples/`).

## Goal

Provide at least one complete example project under `examples/` that demonstrates the kit end-to-end: a brief the user can run the kit (`/sdd`, or the critique engine) against, showing the milestone workflow, the five-document set, and the build that follows from it. "The build that follows" means the example's `tasks` document outlines the build steps the way the kit does — the example ships the *output shape* (spec/plan/tasks/workflow/tests), not a compiled artifact or source code, per Out-of-Scope.

## User Scenario

**US-1 — A user wants to see the kit in action.** They clone the repo, open `examples/sample-project/PLAN.md`, and either run the kit against it or study the supplied example milestone set to learn the workflow by imitation. Note: the shipped example set is a **hand-crafted representative** demonstrating the kit's output shape; running the kit against the brief generates *your own* set, so run it in a fresh copy/directory to avoid overwriting the shipped example — the kit itself has no overwrite protection, so running in place will replace the example files.

**US-2 — A user wants a starting template.** The example serves as a copyable template: a realistic-but-small brief plus a completed example milestone set they can model their own project on.

## Functional Requirements

**FR-1 — `examples/sample-project/PLAN.md`.** A realistic, self-contained brief for a small project, written so the kit can be invoked against it directly. Its concrete subject is a small, dependency-free Python 3 command-line tool (a "quote" CLI that prints programming quotes and manages a plain-text store) — small enough to demo, non-trivial enough to exercise the loop. The brief is **sufficient to implement the tool without any shipped source**: it specifies the CLI contract, the store, the exit codes, and the constraints. `PLAN.md` is the kit's designated brief format (the kit is invoked against any folder containing a `PLAN.md`, per `AGENTS.md`); the critique engine is a *later-stage* tool for critiquing produced documents, so `/sdd` on the brief and the engine on a produced spec are complementary, not alternatives. The brief must carry the **required brief headings** — `## Brief`, `## Requirements`, `## Non-negotiable`, `## Out of scope`, `## Success criteria` (the set AC-1 checks; additional headings are permitted) — and **any additional metadata (front-matter, version, project name) is permitted but not required**: the kit's scan reads the brief's content, and its behavior is defined in `kit/skills/research-ct-scan/SKILL.md`.

**FR-2 — Example milestone set.** One completed five-document milestone set **for `milestone_1`** (the example project is a separate single-milestone project; its own milestone numbering starts at 1, independent of this bootstrap's milestone numbers) with the exact filenames `spec_milestone_1.md`, `plan_milestone_1.md`, `tasks_milestone_1.md`, `workflow_milestone_1.md`, `tests_milestone_1.md`, under `examples/sample-project/outputs/milestones/milestone_1/`. **"Faithful to the kit's shape" is defined as:** each file contains **at least** the kit's required section headings — spec → `## Goal`, `## Functional Requirements`, `## Edge Cases & Rules`, `## Acceptance Criteria`; plan → `## Tech Stack / Format`, `## Architecture / Structure`, `## Rationale`, `## Acceptance Mapping`; tasks → `## Build Order`, `## Status`; workflow → `## Build States`, `## Feature-to-Node Traceability`; tests → `## Node Tests`, `## Acceptance-Criterion Mapping` — each required heading present with substantive content beneath it, in their **relative** order (required headings appear in the listed order; additional headings may be interleaved anywhere; the example files' own internal numbering of sections is their formatting, not part of the required heading names). See the Non-stub rule, which applies **per file individually**. **Additional headings are permitted**; the required set is a minimum, not an exhaustive list. The five documents cross-reference each other consistently: **every FR has a corresponding workflow node, and every AC has a test row** — verified by string match: identifiers are exactly `FR-<n>` and `AC-<n>` (hyphenated, case-sensitive), each spec identifier must appear in the workflow's traceability section and the tests' mapping section, in the entry formats `FR-<n>→C<m>` (workflow, where `C<m>` is the command-state node) and `AC-<n>→NT<m>` (tests, where `NT<m>` is the node-test number), using the Unicode arrow `→`. No minimum count is imposed beyond the spec's own FR/AC list, and multiple FRs may map to a single workflow node.

**FR-3 — `examples/README.md`.** Explains what the examples are, how to run the kit against `sample-project/PLAN.md`, and how the sample milestone set was produced (as a hand-crafted representative). Links back to `docs/GUIDE.md`.

## Edge Cases & Rules

- **Non-stub** (inherited from the M4 Edge-Cases definition, applied to all prose deliverables — the brief, the README, and the example spec/plan/workflow files): substantive (**≥200 words per file, individually; count all words in the file including table and bullet content and inline-code text; strip markdown marker characters (`#`, `*`, backticks) before counting; exclude fenced code blocks, i.e. triple-backtick blocks — a rough threshold, not a lint**), no placeholder text (any placeholder marker or phrase such as `TODO`, `TODO:`, `TBD`, "to be decided", `lorem ipsum`), no empty/one-line bodies. **Structured files** (`tasks_milestone_1.md`, `tests_milestone_1.md`) are exempt from the word count; they must be non-empty and contain their required section headings (tasks → `## Build Order` and `## Status`; tests → `## Node Tests` and `## Acceptance-Criterion Mapping`, with at least one row per table), and their content must be substantive (real steps and test rows, not placeholder rows). The illustrative blockquote note in `tasks_milestone_1.md` is a content requirement (a blockquote before the build order that states the build steps are illustrative), not a heading — it is separate from the heading set.
- **Simplicity rule** (inherited from the constitution's Article IV, Simplicity by Default — `outputs/constitution.md`: *"Do not add dependencies, frameworks, or servers without strong reason."*). The example is a small, dependency-free project. For the example's purpose, the kit itself is not counted as a dependency — the kit is the tool being demonstrated, not a dependency of the example project.
- **"Secrets" (AC-4):** API keys, tokens, passwords, or private URLs — where a "private URL" is a URL containing embedded credentials (e.g., `https://user:pass@host/`) or a non-public endpoint. The example contains none.
- **"External dependencies" (AC-4):** any third-party package or library. Python's standard library is not an external dependency and is permitted (the example uses stdlib only).
- The example brief must be self-contained: it must not depend on anything outside `examples/sample-project/` (standalone-first).
- **Internal consistency:** the five example documents must read as if generated by the kit — they reference each other (cross-reference tables) and their task/build steps are consistent with the brief, even though they are hand-crafted representatives. Any `tasks` build steps are illustrative and reference files that need not exist in the repo; `tasks_milestone_1.md` carries a blockquote note **at the top of the file** (before the build order) marking its build steps as illustrative. Illustrative references to unshipped files are documentation, not dependencies — "self-contained" means the example needs nothing outside its folder to be *read* and understood.
- The sample milestone set must reflect the same five-document standard the kit enforces (it is a teaching artifact — consistency matters).
- **Platform-agnostic:** the example is plain text/Markdown; the tasks document must not include platform-specific steps (e.g., `chmod +x`, OS-specific paths, per-OS package-install commands, shell keywords like `export`/`set`, env-var assignment or `$VAR` expansion inside command examples, venv activation commands). Env variables are described **in prose only** (as the plan's store-path description does); command examples contain neither assignment nor expansion. Mentioning the runtime (`python3`) is permitted. Line-ending and file-permission concerns do not arise because the example ships no executable files. Tasks build steps may reference source filenames (e.g., `quote.py`) illustratively; only the files themselves are not shipped — references to files that **do** ship (e.g., the brief) must use their real repo-relative paths.

## Out of Scope

- Examples for every sub-skill or a full multi-milestone demo — one representative project suffices for `0.1.0`.
- A freshly kit-generated build for the example, and **any example source code** (e.g., `quote.py`). The shipped example set is a **hand-crafted representative** of the kit's output shape, and it **is committed as part of the repository** (it is a stable, readable teaching artifact, not a build artifact). A user running the kit against the brief generates their own live set, which is structurally identical (both follow the kit's shape); the shipped representative is a static copy and is not meant to be regenerated in place.
- Localized guide content (e.g., the reserved "Guide for Pakistani users" slot, the kit's own PLAN.md §12) — not an examples concern.

## Acceptance Criteria

**AC-1.** `examples/sample-project/PLAN.md` exists, is self-contained, and is directly invokable by the kit. Testable check: the file exists, contains the brief's required headings as **exact, case-sensitive strings** — `## Brief`, `## Requirements`, `## Non-negotiable`, `## Out of scope`, `## Success criteria` — the minimum set the kit's scan expects; additional headings are permitted; heading-case variations (e.g., `## Out of Scope`) do not satisfy the requirement — and is non-stub. Invocation is `/sdd` run against the folder containing the brief, with the kit installed in a supported tool (Claude Code, Claude Desktop, OpenCode, or Antigravity, per `docs/GUIDE.md` §2; no additional configuration or prerequisites beyond the kit); the critique engine (`python3 kit/scripts/orchestrate_critique_loop.py ...`) is the later-stage tool for critiquing produced documents.

**AC-2.** A completed five-document example milestone set exists under `examples/sample-project/outputs/milestones/milestone_1/` with the exact filenames in FR-2, each file containing **at least** the FR-2 required heading set (in relative order, with substantive content; additional headings permitted), non-stub per the per-file rule, and with the workflow/tests traceability consistent with the spec's FRs and ACs (identifier string-match per FR-2).

**AC-3.** `examples/README.md` exists, explains how to run the kit against the sample brief, and links to `docs/GUIDE.md`.

**AC-4.** The example contains no secrets (API keys, tokens, passwords, private URLs) and no external dependencies beyond the kit.

## Cross-Reference

**Milestone-5 documents (this milestone's own five-document set):**

| Document | Path |
|---|---|
| Spec (this file) | `outputs/milestones/milestone_5/spec_milestone_5.md` |
| Plan | `outputs/milestones/milestone_5/plan_milestone_5.md` |
| Tasks | `outputs/milestones/milestone_5/tasks_milestone_5.md` |
| Workflow | `outputs/milestones/milestone_5/workflow_milestone_5.md` |
| Tests | `outputs/milestones/milestone_5/tests_milestone_5.md` |

**Example deliverables (produced by this milestone):**

| Deliverable | Path |
|---|---|
| Examples README | `examples/README.md` |
| Example brief | `examples/sample-project/PLAN.md` |
| Example set spec | `examples/sample-project/outputs/milestones/milestone_1/spec_milestone_1.md` |
| Example set plan | `examples/sample-project/outputs/milestones/milestone_1/plan_milestone_1.md` |
| Example set tasks | `examples/sample-project/outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Example set workflow | `examples/sample-project/outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Example set tests | `examples/sample-project/outputs/milestones/milestone_1/tests_milestone_1.md` |