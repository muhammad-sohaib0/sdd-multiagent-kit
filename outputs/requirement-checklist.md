# Requirement Category Checklist — SDD Multi-Agent Kit

**Artifact type:** runtime working artifact (`PLAN.md` §9), produced by `research-ct-scan` from the §5.1 computational-thinking scan
**Input:** `PLAN.md` (the full brief, all 13 sections)
**Consumed by:** `specify` (drafts one section per row) and the Structural Completeness Gate (§5.3, which fails a spec missing any required row)

> Extracted to this fixed path so it is readable without going through the history
> log. The primary record — including the full decomposition and the
> installed-skill awareness check — is PHR `milestone_0/000`, which remains
> authoritative.

## Project category

A CLI-distributed developer tool: an agent-skill framework shipped as an npm
package, with external API integrations (three providers), structured config and
data contracts, API-key secrets handling, and multi-platform installation into
four target tools. Not a UI product; not a backend service with a dashboard.

## The checklist

| Category | Required | Why needed |
|---|---|---|
| Goal | base | Base spec anatomy (§5.1) |
| User Scenarios | base | Base spec anatomy (§5.1) |
| Functional Requirements | base | Base spec anatomy (§5.1) |
| Edge Cases & Rules | base | Base spec anatomy (§5.1) |
| Out of Scope | base | Base spec anatomy (§5.1) |
| Acceptance Criteria | base | Base spec anatomy (§5.1) |
| Command-Line Interface & Arguments | conditional | The setup wizard (`bin/setup-wizard.js`) is an interactive CLI; the `/sdd` trigger is an in-tool CLI surface |
| Data Model | conditional | Concrete structured data: the critique response JSON schema (§4.3), `providers.yaml`, the PHR/ADR file formats, the install-target path mapping, `package.json` manifest fields |
| API / Integration | conditional | Three external provider APIs (NVIDIA NIM, Google AI Studio, Ollama Cloud) with key auth; integration points into four AI tools' config directories |
| Authentication / Security | conditional | API keys are secrets: env-based reading, never logged or committed, plus a security-report surface |
| Deployment / Environment | conditional | npm distribution, cross-platform paths (macOS/Linux/Windows), Node availability, free-tier rate limits, per-tool install locations |
| Performance / Scale & Concurrency | conditional | The panel runs concurrently per round; per-round retry budget; 25-round safety cap; free-tier rate-limit behavior |
| UI/UX Requirements | n/a | No graphical interface anywhere in the product. The wizard is CLI-interactive and fully covered by the CLI category; forcing a UI section would violate the "only what the project needs" rule |
| Accessibility | n/a | No UI surface to make accessible |
| Localization | n/a | Single-language (English) product and docs |

## Installed-skill awareness (§5.2)

Every conditional category was checked against the skills installed in the running
tool. The available skills were design, frontend, and branding oriented; **none
matched** any conditional category of this project (CLI tooling, Node scripts, API
integration, security, packaging). No skill-specific conventions were adopted, so
all sections were drafted from the brief directly.

## Note on per-milestone application

M1's spec §7 records that M1 — a process-content milestone — commits to the base
anatomy plus Data Model, API/Integration, and Authentication/Security, and that
Performance/Scale, Concurrency, UI/UX, Accessibility, Localization, and Deployment
are owned by the milestones that realize those subsystems. The checklist is
project-wide; which rows a given milestone must answer follows from that
milestone's scope.
