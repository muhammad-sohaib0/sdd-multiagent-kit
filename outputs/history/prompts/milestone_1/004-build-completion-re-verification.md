# PHR 004 (milestone_1) — Build Completion Re-Verification

- **Phase:** Milestone 1, Build → Verification (post-bootstrap completion pass)
- **Date:** 2026-08-18

## What was requested

Re-verify the M1 build (the 13 kit files) 100% strictly against `spec_milestone_1.md` and `tests_milestone_1.md`, fix any strict-conformance gaps found, and re-run the verification suite end to end (NT18–NT22).

## What was produced

**Gap fixes (3 files edited):**

- `kit/constitution.template.md` — Articles III, IV, and VII now render PLAN.md §6 wording verbatim (Article III: "§7.2's `tasks.md`"; Article IV: "§5.4"; Article VII: "ADRs (§8.2)"). Fixes NT21/AC-6.
- `kit/SKILL.md` — (a) the `/sdd` trigger and installer are now named as an explicit M3 deferral with the manual-install fallback (AC-5); (b) ADR suggestions stated as a blocking human-confirmation step (FR-1 step 5); (c) the Simplicity default is now stated as overridable once via `simplicity_default: N` in the adopted constitution with an ADR (spec §4.5).
- `kit/skills/history-logger/SKILL.md` — added the FR-2 edge-case rule: a transition that produced no artifact is still recorded, with `What was produced` = `none`.

**End-to-end verification (all PASS):**

- NT18 — 13/13 files at spec §4.1 paths; all 11 SKILL.md carry `name`/`description`/`version` (`0.1.0`); exactly the ten M1 sub-skill folders (the `critique-loop` folder is M2's shipped deliverable, correctly not part of M1's 13-file inventory).
- NT19 — providers.yaml: `version: 1`, three providers, seven ordered `critic_slots` (ADR-001/ADR-003 panel) each bound to its provider, no duplicates, env-var names only — validated with the M2 engine's own `load_yaml`.
- NT20 — secret scan on the 13 files: zero matches of `sk-…`, `AIza…`, `Bearer …`, or secret-like ≥32-char blobs (the one candidate, the readable path `outputs/history/prompts/single-milestone/`, is the spec §6 "obvious" carve-out — a directory path, not secret-like randomness; the allowlist remains empty).
- NT21 — constitution template: seven articles word-identical to PLAN.md §6.
- AC-7/NT13 parity — each of the ten sub-skills names its FR-2 input, output, and edge-case rule; inventory and panel parity confirmed.

## Rationale

The M1 build was verified complete at bootstrap (PHR 003), but three content files carried small strict-conformance deviations (two non-verbatim articles, an unnamed M3 deferral, a missing ADR-blocking statement, one unstated edge-case rule). This pass closed those gaps and re-ran the full M1 verification suite; every node test and acceptance criterion now passes. No ADR warranted (routine fixes, no alternatives, no cross-milestone impact — except the constitution template, which is a shipped template not the adopted constitution, so no amendment needed).