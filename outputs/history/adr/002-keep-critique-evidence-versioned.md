# ADR-002 — Keep critique evidence in version control

- **Status:** Accepted (bootstrap corrective pass)
- **Date:** bootstrap run

## Context

PLAN.md §9's layout shows `outputs/critique-log/` as the raw critique store. The M4 spec's original Edge-Cases rule mandated `.gitignore` exclude it. During the bootstrap's corrective pass the user directed that critique evidence must be visible in version control ("yes do that" — keep critique logs auditable), which contradicts the ignore rule.

## Decision

`outputs/critique-log/` is **not** ignored by the repo-root `.gitignore`. The raw critique JSON for every round (M1–M5) is a versionable deliverable, alongside the PHR narrative records under `outputs/history/`.

## Consequences

- Critique rounds are auditable from the git history: any reader can see exactly what each critic said and what was adopted or rejected.
- The M4 spec's `.gitignore` bullet was revised accordingly (critique-log removed from the mandatory patterns and explicitly called out as deliberately un-ignored).
- Repo cost: one additional directory of small JSON files (~25 files, tens of KB).
