# PHR 000 — Computational Thinking Requirement Scan

- **Phase:** Research — CT scan (PLAN.md §5.1)
- **Input:** PLAN.md (the full brief, all 13 sections)
- **Date:** bootstrap run, session start

## What was requested

Decompose the SDD Multi-Agent Kit into its fundamental parts using computational thinking, and produce the Requirement Category Checklist this specific project must satisfy — base anatomy categories always, conditional categories only where this project genuinely calls for them.

## What was produced

### Project decomposition (fundamental parts)

1. **The process itself** — the knowledge content that encodes the SDD workflow: the main `SKILL.md` plus eleven sub-skills (research-ct-scan, specify, plan-builder, task-breakdown, critique-loop, clarify-interview, milestone-builder, workflow-builder, scenario-tester, stranger-test, history-logger) and the constitution template.
2. **The critique automation** — scripts that call six models across three free-tier providers in parallel and validate their structured responses.
3. **The installer & distribution** — npm package, interactive setup wizard, four tool adapters, the Shared Agent-Skills Standard install locations.
4. **The open-source repository surface** — root docs, contribution/security/support surfaces, the full usage and architecture guides.

### Category of project

A CLI-distributed developer tool: an agent-skill framework shipped as an npm package, with external API integrations (three providers), structured config/data contracts, API-key secrets handling, and multi-platform installation into four target tools. Not a UI product; not a backend service with a dashboard.

### Requirement Category Checklist

**Always required (base anatomy):**
- Goal
- User Scenarios
- Functional Requirements
- Edge Cases & Rules
- Out of Scope
- Acceptance Criteria

**Conditional — added, with reason:**

| Category | Why it is required here |
|---|---|
| Command-Line Interface & Arguments | The setup wizard (`bin/setup-wizard.js`) is an interactive CLI; the `/sdd` trigger is an in-tool CLI surface. |
| Data Model | Concrete structured data: critique response JSON schema (§4.3), `providers.yaml` config, PHR/ADR file formats, install-target path mapping, `package.json` manifest fields. |
| API/Integration | Three external provider APIs (NVIDIA NIM, Google AI Studio, Ollama Cloud) with key auth; integration points into four AI tools' config directories. |
| Authentication/Security | API keys are secrets: env-based reading, never logged or committed, key validation, file-permission hygiene, security-report surface. |
| Deployment/Environment | npm install/distribution, cross-platform paths (macOS/Linux/Windows), Node.js availability, free-tier rate limits, per-tool install locations. |
| Performance/Scale & Concurrency | Six critics run per round in parallel; per-round retry budget; 25-round safety cap; free-tier rate-limit behavior. |

**Evaluated and rejected, with reason:**
- UI/UX Requirements — no graphical user interface anywhere in the product; the wizard is CLI-interactive and is fully covered by the CLI category. Forcing a UI section would violate the "only what the project needs" rule.
- Accessibility — no UI surface to make accessible; no category created.
- Localization — single-language (English) product and docs; no category created.

### Installed-skill awareness (PLAN.md §5.2)

Checked installed skills against every conditional category. The machine's installed skills are design/frontend/branding oriented (brandkit, design-taste-frontend, high-end-visual-design, imagegen variants, etc.) and opencode-config oriented (customize-opencode). **None match** any conditional category of this project (CLI tooling, Node scripts, API integration, security, packaging). No skill-specific conventions to adopt; all sections will be drafted from the brief directly.

## Rationale

The scan stays honest to §5.1: it recognizes this as a CLI + integration + security project and adds exactly those categories — nothing more. The rejected rows document the computation rather than silently omitting it, so a later reviewer can see the scan ran and why those categories are absent.