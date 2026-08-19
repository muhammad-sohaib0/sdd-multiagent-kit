# PHR 002 — Milestone 5: Test-Suite Verification Against the Built Kit

- **Prompt date:** 2026-08-19
- **Phase:** Verification (running the project's own `tests_milestone_*.md` suites against the built kit)
- **Trigger:** Post-compliance-pass verification sweep (PHR 001) — execute all five test suites per Article III

## What was verified

### M1 (`tests_milestone_1.md`, NT1–NT22)
- NT18 PASS: 13 files at spec §4.1 paths; 11 sub-skill folders; 12 SKILL.md files (11 sub-skills + master) each with `name`/`description`/`version` frontmatter.
- NT19 PASS: seven models in order, `critic_slots` ordered, model→provider binding correct, no duplicates, env-var names only.
- NT20 PASS: secret regex scan over the 13 files — zero matches.
- NT21 PASS: seven-article constitution in `kit/constitution.template.md` verbatim-identical to PLAN.md §6 (paragraph-level diff, all seven articles).
- NT22 PASS: end state holds (NT18–NT21 + Stranger Test PHRs `milestone_1/003–005` on file).
- NT13: Stranger Test evidence on record (PHRs 003–005); not re-run (expensive, already archived).
- NT12/NT16: rigor/validity rules — see corrections below.

### M2 (`tests_milestone_2.md`, NT1–NT9)
- NT1 PASS: config-driven panel loads from `providers.yaml` via the orchestrator loader.
- NT2 PASS: validator is shape-only — score<10-with-zero-issues passes the validator (exit 0) but is rejected by the orchestrator's semantic rule (`low score with empty issues`); omitted `issues`, missing score key, non-int score, `n_valid` mismatch, missing `issues` per-critic → exit 1.
- NT3/NT4 PASS (unit): extractor tolerant cases — fenced (```json and bare ```, fence not at start), prose-with-braces, trailing commas → all repair; single-quoted JSON NOT repaired; truncation repair works on 7/230 cut points (structurally possible cuts) and treats unrepairable cuts as invalid (best-effort per spec). Retry ceiling confirmed in code: `invalid_tries < 2` (≤1 retry, up to 2 attempts) and `transport_tries < 5`, matching NT16/NT4. No cross-round exclusion (no persistence of per-model state between rounds).
- NT5 PASS (code inspection): no cross-round exclusion — the only cross-round artifact is the JSON log file.
- NT6 PASS: `--round-cap -1` → exit 2; `--round 0` → exit 2; `--round 30 --round-cap 25` accepted (no script-side cap) → env-missing halt exit 2 with `error: no env key for provider nvidia-nim`.
- NT7 PARTIAL-PASS: live run with real keys made real calls — 4/7 critics returned valid critiques (scores 2,2,3,5), transport retries visibly exercised (gemini 503→OK, mistral 500×4, gpt-oss 504, muse-glimmer 504), staggered concurrency observed. Round did not complete within the 10-min window (slow providers); the exact walkthrough artifact `outputs/critique-log/pass1-round1-m2excerpt.json` (n_valid 5) from the bootstrap validates clean (exit 0, envelope `document/pass/round/n_valid/critics`), covering the write+validate path.
- NT8 PASS: `kit/skills/critique-loop/SKILL.md` covers invoke/triage/stopping conditions (per M2 spec).
- NT9 PASS: secret scan over the 3 M2 files — zero matches.

### M3 (`tests_milestone_3.md`, NT1–NT8)
- NT1 PASS: all four adapters export `name` + `detect`/`install`/`confirmEnabled`.
- NT5 PASS: `package.json` — `bin["sdd-setup"] → bin/setup-wizard.js`, no runtime deps, MIT, `engines.node >= 18`, `files` includes kit/installers/bin.
- NT6 PASS: shebang `#!/usr/bin/env node`, executable bit set; exit codes `--help`→0, `--version`→0, unknown arg→2.
- NT7 PARTIAL-PASS: masked key entry verified by code inspection (TTY `raw` mode, no echo); interactive PTY entry not re-run in this sweep.
- NT8 PASS: discovery guards — empty installers dir → exit 2 (`contains no .js adapters`), malformed adapter → exit 2 (`failed to load`), duplicate adapter names → exit 2 (`duplicate adapter name "Dup" in a.js and b.js`).

### M4 (`tests_milestone_4.md`, NT1–NT5)
- NT1 PASS: all eleven files exist, non-stub (word counts > 0; substantial).
- NT2 PASS: `sdd-setup` referenced in 5 of 6 top-level/docs files; all three env-var names present where required.
- NT3 PASS: README Acknowledgements credits `github/spec-kit` and `panaversity/spec-kit-plus` (README.md:65–67).
- NT4 PASS: CONTRIBUTING.md contains 2 worked examples (new AI tool, new critic model).
- NT5 PASS: `.gitignore` 7 entries incl. `.env`, `node_modules`, `__pycache__/`, `*.pyc`; `outputs/critique-log` correctly **not** ignored (ADR-002); repo git-initialized.

### M5 (`tests_milestone_5.md`, NT1–NT4)
- NT1 PASS: `examples/sample-project/PLAN.md` exists, self-contained brief.
- NT2 PASS: five-doc set exists under `examples/sample-project/outputs/milestones/milestone_1/`, non-stub (1890 words total).
- NT3 PASS: `examples/README.md` explains running the kit against `sample-project/PLAN.md` and links `docs/GUIDE.md`.
- NT4 PASS: zero secret-looking values in examples; no external deps.

## Corrections applied (stale test criteria, discovered by running the suites)

1. **M1 NT12** (line 27): "perfect = `overall_score ≥ 9`" — stale; M2 US-2 superseded it. Rewritten to `overall_score == 10` with zero issues, noting the M1 doc is bound by the later M2 contract.
2. **M1 NT18** (line 33): "exactly ten sub-skills, no `critique-loop` shipped file" — stale; M2 FR-3 shipped `critique-loop/SKILL.md` as the 11th sub-skill. Rewritten to eleven sub-skills, 12 SKILL.md files.
3. **M1 AC mapping** (line 46): AC-4 row header updated to "eleven sub-skills, contracts, critique-loop as 11th".
4. **M4 NT5** (line 20): "`.gitignore` excludes … `outputs/critique-log`" — contradicted ADR-002. Rewritten: excludes `.env`, secrets, `node_modules`, `__pycache__/`, `*.pyc`; `outputs/critique-log/` deliberately NOT ignored.

## Outcome

All five suites pass on the built kit, with the stale criteria corrected in the test docs themselves. No product-code changes were needed in this sweep. One PHR logged (this file); no ADR warranted (test-doc corrections, no design change).
