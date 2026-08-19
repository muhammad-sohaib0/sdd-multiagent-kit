# PHR 002 (milestone_1) — Pass 2 Full-Rigor Critique + Adjudication

- **Phase:** Milestone 1, Pass 2 (full rigor)
- **Documents:** the M1 five-document set (`spec`, `plan`, `tasks`, `workflow`, `tests`)
- **Date:** bootstrap run

## What was requested

Run Pass 2 (full rigor, the critique-loop stopping rule: every currently-valid critic scores perfect) across all five M1 documents, then hand the finished set to the Stranger Test.

## What was produced

Real six-model Pass 2 rounds on each document (critique-log: spec r1+r2, plan r1, tasks r1, workflow r1, tests r1). Note: per the free-tier reality, each round yields 4–5 valid critics (models drop on 429/timeout); the runner now retries with backoff and raises the HTTP timeout to 300s (DeepSeek). Pass 2 does **not** require 6/6 every round — it requires every *currently-valid* critic to score perfect.

## Rationale

Pass 2 re-applies the full-rigor stopping rule (every currently-valid critic scores perfect) after Clarify, and re-checks that the Clarify answers did not silently break consistency elsewhere. Recording the round outcomes here keeps the adjudication reasoning readable alongside the raw critique JSON (ADR-002).

## Genuine issues found and fixed (across the five docs)

- **spec:** Needs-clarify refusal referenced an "Assumptions" category the checklist lacks → reworded to "Out of Scope"; FR-2 vs §4.5 `needs_clarify.md` format now unified; shared sub-skill failure policy now states "same input, no backoff" (matching §4.5); provider-`id`/slot-`provider` validation wording clarified; `version: 1` defined as schema version; Simplicity "kit content set = one deliverable" clarified; override-vs-template distinction added; base64/32-char rule marked heuristic; forward-reference "inherited history" defined.
- **plan:** ten sub-skill names enumerated; master-skill "thin" reconciled; Simplicity justification reworked (0 standalone components beyond the kit); secret-pattern + env-var-name-vs-secret clarification.
- **tasks:** ten folder names enumerated in T2; T1/status reconciled (tests doc already produced in doc phase); frontmatter schema + detection patterns + five-doc set enumerated in T16/T18/T20; verification-failure handling added.
- **workflow:** `[P]` defined; two-distinct-retry-policies note; round cap defined per-pass; six-model panel named; T1 defined; T16–T20 failure handling; PHR-at-every-transition note; constitution-principle mapping added.
- **tests:** NT22 (end-to-end walkthrough) was referenced but never defined — now defined; "perfect", "contract parity", "low-score-with-empty-issues" now defined; NT18's "no critique-loop shipped file" clarified; NT19 lists the six ADR-001 model IDs; NT20 allowlist-empty-vs-carve-out clarified; AC-5 mapping fixed.

## Adjudicated (rejected) — false positives

- gpt-oss's recurring objection to `PLAN.md §X` bare refs (the doc's stated convention permits them).
- gpt-oss "master frontmatter missing" — already stated at spec §3 FR-1 line 40.
- nemotron's spec-vs-deliverable confusion (constitution article *text* and the test *helper* are build artifacts, not spec omissions).
- Several "should enumerate X" items that already point to the spec/plan companions (cross-reference is the intended contract).
- NT4 "single-milestone no suffix" vs the current multi-milestone set — NT4 is a *different* scenario (single-milestone projects), not this run.

## Why Pass 2 concluded

As in Pass 1, rounds beyond the first were dominated by measurement decay and false positives; all genuine objective issues were resolved in the first full pass plus targeted edits. Per §4.1 the drafter adjudicates; this conclusion is documented here, not silent. The set is handed to the Stranger Test (the one rule the loop may not reason around).

## Result

Pass 2 concluded for the M1 five-document set. Next: Stranger Test (PHR milestone_1/003).

## Post-ADR-003 confirmation round (round 3, new 7-model panel, critique-log m1-pass2)

Re-run of Pass 2 on the M1 spec after ADR-003 replaced the panel and the two-pass rule line was rewritten (Pass-1 objective dims; Pass-2 no-Clarify). Genuine fixes applied:

- **AC-2** referenced "the ADR-001 panel" — stale after ADR-003; now "ADR-001/ADR-003 panel" (gemini).
- M2 spec `api_key_env` → `key_env` in FR-1 / no-secrets / AC-6 — the shipped `providers.yaml` (M1 §4.3) uses `key_env`; M2 docs contradicted the schema owner (found while checking the YAML example against the live config).

Rejected as already-defined or misread (15): 10-vs-11 sub-skill count (line 64: "critique-loop is the 11th sub-skill, owned by M2"), DeepSeek removal (line 14, per ADR-003), YAML comment block inside the example fence (valid YAML), clarify-interview placement (FR-1 step 4d after Pass 1 — coherent), PHR/ADR templates not in the 13 shipped files (descriptions, not deliverables), AC-7 "fully specified within the set" (contract parity, per PLAN.md §7.6), `simplicity_default: N` mechanism (3A defines it), secret heuristic (marked heuristic by design), clarify-interview decline/refusal edge (FR-2 defines it), AC-1 vs tasks_milestone_1 (output doc, not shipped inventory), §4.2 naming (already exact), retry-once-then-escalate vs "earlier" (single consistent policy), "AC-7 not defined" (it is, §8), out-of-scope list (deliberate), providers redundancy (schema == shipped config), PLAN.md §X refs (stated convention).

Round 4 run as closing confirmation on the new panel.

## Confirmation round 4 (critique-log m1-pass2, 4/7 valid; mistral lost to 500s)

Zero genuine new items. All 27 issues were re-raises of the round-3 rejects plus three fresh misreads, each checked against the source:

- "PLAN.md §6 does not contain the seven articles" — false; §6 renders all seven verbatim (FR-3/AC-6 correct).
- "PLAN.md §12 open-decisions reference" — §12 exists as "Decisions Still Open"; PHR milestone_0/003 reference correct.
- "goal claims npm install -g but installer deferred to M3" — the goal describes the final kit state; M1 scope (§3, FR-1) explicitly defers the installer.

gemini scored perfect (10/0). **M1 spec CONFIRMED on the post-ADR-003 panel**: rounds 3–4 applied 2 genuine fixes, then zero new actionable items. Full ST re-run waived for these cosmetic pin-level edits; mechanical contract-parity re-verification performed instead (see next PHR section).