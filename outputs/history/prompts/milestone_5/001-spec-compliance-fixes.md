# PHR 001 (milestone_5) — Spec-Compliance Fixes (post-build strict verification pass)

- **Phase:** Post-build verification (after M5)
- **Date:** 2026-08-19

## What was requested

A strict 100% spec-vs-implementation comparison of all five milestone specs against the shipped kit, followed by fixes for every deviation found. Six deviations (D1–D6) were identified and fixed.

## What was produced

- **D1 — providers.yaml schema alignment (§4.3).** `kit/config/providers.yaml` `models` entries changed from plain scalars to the spec'd `- id: <model>` map form; `kit/scripts/orchestrate_critique_loop.py` now normalizes both forms (map and scalar) for the slot-membership validation, so a §4.3-literal config loads.
- **D2 — PHR template compliance (§4.5).** Added the missing `## Rationale` field to `outputs/history/prompts/milestone_1/002-pass2-critique-and-adjudication.md`.
- **D3 — Frontmatter-scoped trigger checks (M3 FR-2).** All four installers' `confirmEnabled()` now check `name: sdd-multiagent-kit` (and, for Antigravity, the `Invocation: /sdd` phrase) inside the YAML frontmatter block only, not the whole file; the Antigravity invocation re-assertion is likewise scoped to the frontmatter.
- **D4 — Docs-vs-kit registration contract.** `CONTRIBUTING.md` corrected: adapter registration is automatic (file discovery in `installers/`), no `bin/setup-wizard.js` registry edit exists; the model-add walkthrough now shows the `- id: <model>` schema form.
- **D5 — Transient artifacts.** `.gitignore` gained `__pycache__/` and `*.pyc`; the unignored bytecode was removed and confirmed absent from the npm tarball.
- **D6 — Spec staleness.** M4 spec FR-8 corrected ("eleven sub-skill folders"); the `outputs/history/adrs/` typo in its Edge Cases corrected to `adr/`.

Verification performed: JS syntax checks, end-to-end adapter install/confirm/reinstall cycle against a fake HOME (all four tools), config parse + slot validation via the engine's own loader, orchestrator config-path run (halt-on-missing-env, exit 2), secret regex scan (zero matches), `npm pack` dry-run (no `.pyc`, correct file list), wizard `--version`/`--help`/exit codes.

## Rationale

The bootstrap's shipped kit had drifted from its own milestone specs in six places; none were functional breakers, but the specs are the contract, so each was brought into conformance (or, where the spec itself was stale — D6 — the spec was corrected). No ADR is warranted: all fixes are reversible, single-context corrections with no real alternatives.
