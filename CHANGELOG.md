# Changelog

All notable changes to the SDD Multi-Agent Kit are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- **`publish.yml`'s packaging check crashed under npm 12.** `npm pack --json` has two
  output shapes — `[{files: […]}]` up to npm 11, and `{"<pkg-name>": {files: […]}}` from
  npm 12 — so reading `[0].files` throws `TypeError: Cannot read properties of
  undefined`. It surfaced only after merging, because `ci.yml` ran Node 22's bundled npm
  10 while `publish.yml` upgrades to npm ≥ 11.5.1 for trusted publishing: **CI green did
  not imply publish green.** Two fixes, not one — the shape is now normalized in
  `scripts/check-package-contents.js`, shared by both workflows so they cannot drift
  again, and `ci.yml` upgrades npm to match `publish.yml` so a change like this fails on
  a branch instead of on `main`. The script carries a `--selftest` that exercises both
  shapes without either npm installed.
- **Both workflows installed a *floating* `npm@latest`,** which is the root cause the
  fix above only treated the symptom of: a silent major bump to npm 12 changed
  `npm pack --json`'s shape mid-flight. Both are now pinned to `npm@12`, and
  `scripts/check-workflows.js` fails the build if the two files disagree on the version
  or if either drifts back to `latest`.

### Documented

- **Bootstrapping the trusted publisher**, now that it has actually been done.
  `CONTRIBUTING.md` records the working CLI route (`npm trust github … --allow-publish`)
  and the three traps found by hitting them: `--allow-publish` is mandatory but **npm 11
  cannot send it** (the registry answers a bare `400` with no body), the package must
  already exist (`POST …/trust` is **404** while unpublished — npm has no pending
  publisher, so the first release is necessarily manual), and publishing demands 2FA even
  when the account reports it disabled. See ADR-005 addendum 2.

Bump the version with `node scripts/bump-version.js <version>`, move the entries above
into a new `## [<version>]` section, and merging to `main` publishes it — see
[CONTRIBUTING.md](CONTRIBUTING.md#releasing).

## [0.1.0] — 2026-08-21

First release. **Added — what the package ships** is the section to read if you are
installing this; the rest records the pre-release completion pass, in which the
whole-system verification `BOOTSTRAP.md` §5 requires was run for the first time and the
13 kit defects it exposed were fixed. Those fixes landed before this version was ever
published, so no user received the broken behavior — the entries are kept because the
defects are instructive, not because anyone needs to upgrade past them.

### Added — what the package ships

- Master skill (`kit/SKILL.md`) with the `/sdd` trigger and eleven sub-skills (`kit/skills/*`).
- Adopted constitution (`kit/constitution.template.md`).
- Locked seven-model critic panel (`kit/config/providers.yaml`): `nvidia/nemotron-3-ultra-550b-a55b`, `openai/gpt-oss-120b`, `z-ai/glm-5.2`, `mistralai/mistral-nemotron`, `meta/muse-glimmer-30b` on NVIDIA NIM, `gemini-3.6-flash` on Google AI Studio, `minimax-m3:cloud` on Ollama Cloud (ADR-001, ADR-003).
- Critique engine (`kit/scripts/orchestrate_critique_loop.py`) and validator (`kit/scripts/validate_critique.py`), zero runtime dependencies.
- Engine hardening: per-model `timeout` keys in `providers.yaml`; transport retry ≤5 tries with adaptive backoff (429 → 30s × attempt, others → 8s × attempt); deterministic non-429 4xx break immediately; 200-with-non-JSON treated as transport failure; first-call stagger `(slot_index-1) × 4s`; CLI validation of `--round`, `--round-cap`, `--timeout` (exit 2); no cross-round critic exclusion — a failed critic participates again next round and `n_valid == 0` never counts as advancement; `providers.yaml` read fresh per invocation.
- Installer (`bin/setup-wizard.js`, bin `sdd-setup`) with adapters for Claude Code, Claude Desktop, OpenCode, and Antigravity.
- Distribution docs: `README`, `CLAUDE`, `AGENTS`, `CONTRIBUTING`, `SECURITY`, `SUPPORT`, and `docs/` (GUIDE, ARCHITECTURE, BOOTSTRAP).
- Example project under `examples/`.
- Bootstrap history under `outputs/` (specs, critique logs, PHRs, ADRs), with the raw critique evidence kept versioned (ADR-002).

### Fixed

- **`PLAN.md` §4.3's schema example contradicted §4.2** — it showed `"pass": 1`
  with `"testability": 7`, while §4.2 requires Pass-1 critics to emit `0`
  ("not assessed in this pass"). Investigating it found the rule was *unenforced*:
  only 5 of 69 Pass-1 critiques in the bootstrap's own logs honored it, so the
  logged evidence claimed a runtime had been judged when none existed. The example
  is now a Pass-2 response (where all five dimensions legitimately score), and the
  engine normalizes `testability` to 0 on every Pass-1 response — correcting the
  value rather than rejecting the critique, since the rule is a scoping convention
  and no stopping condition reads the field. Verified against a live provider.
- **`CONTRIBUTING.md`'s new-tool worked example produced a non-working adapter** — it
  omitted the mandatory `name` export and returned a bare boolean from
  `confirmEnabled()`, so an adapter built by following it made `sdd-setup` exit 2 at
  startup and blocked *every* tool. Rewritten as a complete, verified adapter.
- **G1 was unsatisfiable as specified.** `specify` requires the spec to end with a
  Cross-Reference section naming four documents that do not exist yet, while G1
  rejects references to things that do not exist. `kit/SKILL.md` now states exactly
  which sub-checks each gate can run and which defer to G2.
- **`plan-builder`** required workflow traceability it runs too early to verify; now
  discharged at G2.
- **Gate-failure routing** assumed a single owning sub-skill; fan-out across several
  documents from one root cause is now specified.
- **Undocumented artifact paths** — pre-milestone PHRs (`milestone_0/`), the
  Requirement Category Checklist, and the milestone breakdown all now have fixed
  locations in `PLAN.md` §9 and their sub-skills.
- **Undefined rules that three documents must agree on** — PHR numbering, stable ID
  schemes for tasks/workflow nodes/tests, `[P]`'s group boundary, task-status
  vocabulary, and "one test per node" over a nested tree (now: leaf nodes).
- **Article III enforcement** — `task-breakdown` now requires an explicit
  confirm-tests-fail task, not just tests-before-code ordering.
- **`task-breakdown`** never instructed the back-reference `PLAN.md` §7.4 requires on
  all four companion documents.
- **The constitution template** shipped articles citing `§7.2`/`§5.4`/`§8.2` —
  dangling references, since users never receive `PLAN.md`. Fixed at the source; the
  template remains verbatim-identical to the brief.
- **`kit/SKILL.md`** told users the installer "ships in a later milestone (M3); until
  then, place this content manually" — in the file the installer had just placed.
- **`docs/` was absent from `package.json` `files`**, so README's guide link and the
  wizard's guide pointer dangled in a global install. Python bytecode is now excluded
  from the tarball.
- **Two verification suites had drifted** and were failing (M2 24/26, M3 30/32) —
  stale fixtures, not product defects. Now M2 29/29 and M3 32/32, with regression
  guards pinning the `providers.yaml` dual-form contract that nothing had covered.

### Added — process and records

- **`PLAN.md` §4.4: non-progression stopping condition** (ADR-004). Pass 2 never
  reached perfect scores on any milestone during the bootstrap; it exited when rounds
  stopped producing new findings. That route is now specified, with progression
  defined and the escalation summary's contents required — so the drafter can report
  that the panel is spent but cannot sign off on its own draft.
- **Stranger Test records** for all five milestones plus the whole system, at the
  `PLAN.md` §9 paths that mandated them.
- Retrospective Pass-2 escalation summaries for M1–M5 (PHR `milestone_5/003`).
- **Release automation** (ADR-005). `.github/workflows/ci.yml` verifies every push and
  pull request — both milestone suites, packaging contents, version consistency, and a
  secret scan. `.github/workflows/publish.yml` publishes to npm when, and only when,
  `package.json` carries a version the registry does not have yet; every other push to
  `main` exits cleanly without publishing. Authentication is npm Trusted Publishing
  (OIDC), so no token is stored anywhere and provenance is attached automatically.
- **`scripts/bump-version.js`** — sets the version across `package.json` and all twelve
  SKILL.md frontmatters in one command, with `--check` to assert they agree. The version
  now has a single source of truth: `bin/setup-wizard.js` reads it from `package.json`
  instead of carrying a copy, and M3 asserts that agreement rather than a literal, so a
  release bump can no longer leave the wizard reporting a stale number.

### Removed

- The bootstrap seed skill and the `.bootstrap/` scratch harness, per `BOOTSTRAP.md`
  §3.6. Both still described the pre-ADR-003 six-model panel.
