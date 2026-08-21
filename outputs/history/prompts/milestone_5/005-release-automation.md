# PHR 005 (milestone_5) — Release Automation: npm Publishing Driven from GitHub

- **Prompt date:** 2026-08-21
- **Phase:** Post-completion — distribution
- **Trigger:** "Ma cahata ka npm publish aisa hoka github pa koi bhi change ho to wo npm ma bhi ho gaye — npm github sa connect ho"

## What was requested

npm publishing should follow from GitHub automatically: push a change, and the
published package keeps up, without a maintainer running `npm publish`.

## What was found first

The starting state was verified against live APIs rather than assumed:

| Check | Result |
|---|---|
| npm registry `sdd-multiagent-kit` | HTTP 404 — never published, name free |
| GitHub Releases / tags | none / 0 |
| `main` | 4 commits, tip `9192191` (PR #1 merge) |
| `CHANGELOG.md` on `main` vs local | identical |
| `npm pack --dry-run` | clean 28-file / 37.8 kB tarball |

So the code was fully pushed and nothing had ever been released. Those are two
different facts about two different systems, and conflating them was the crux of
the follow-up questions this prompt generated.

**The request as literally stated is impossible,** and saying so was necessary
before building anything. npm versions are immutable, so publishing on every push
would succeed once and then fail forever with 403, marking every later commit red.
The implementable form: every push is *verified*, and a push carrying a *new
version number* is *published*.

**A blocker sat in the way of even that.** `0.1.0` was hand-written in 17 places,
and `verify_milestone_3.py` pinned the literal in two assertions. Bumping the
version therefore turned the suite red — confirmed by doing it, `FAILED
(failures=2)`. Since `publish.yml` runs the suites before publishing, the bump
required to release was the bump that blocked the release. Version-driven
publishing would have deadlocked on first use.

## What was produced

**Single source of truth for the version.** `pkgVersion()` in
`bin/setup-wizard.js` walks up for the package manifest — the same idiom as
`kitDir()` minus the `kit/SKILL.md` requirement, so `--version` works without the
kit tree — and reports an error rather than inventing a number when none is
readable. `scripts/bump-version.js` sets `package.json` and all twelve `SKILL.md`
frontmatters together, with `--check` asserting agreement; it discovers sub-skills
by directory listing, so a new one cannot be silently skipped. It deliberately does
not touch `CHANGELOG.md`.

**`ci.yml`** runs on every push and pull request: both suites, packaging assertions,
version consistency, a no-dependencies check, a wizard smoke test, and a secret
scan. `contents: read`, no secrets.

**`publish.yml`** runs on push to `main` and publishes only when the version is
absent from the registry, otherwise exiting 0 silently. Authentication is npm
Trusted Publishing (OIDC) — no stored token, provenance automatic. It also refuses
to publish a version with no `CHANGELOG.md` section, and refuses to reuse an
existing tag.

**`CHANGELOG.md`** `[Unreleased]` folded into `[0.1.0] — 2026-08-21`, with
"what the package ships" placed first for readers who are installing it and the
completion-pass history after. Verified no content was lost: 26 bullets in, 28 out,
the two additions being this work.

Plus `repository.url` normalized to `git+https://…git` (npm matches it against the
building repo), a `Releasing` and `Verification` section in `CONTRIBUTING.md`, and
`AGENTS.md` updated — including removal of its own hard-coded `version: 0.1.0`,
an 18th copy found while writing the pointer.

## Rationale

**Reading stdout, not the exit code, for the publish decision.** The plan assumed
`npm view <pkg>@<ver>` would exit 0 with empty output for a missing version and
non-zero for a missing package. Tested against the live registry, it exits **1 with
empty output in both cases** (`express@99.99.99` → exit 1; `express@4.18.2` → exit 0
with output). Only non-empty output proves a version is live. Had the workflow
branched on the exit code — the obvious implementation — it would have treated the
first publish as an error. Worth noting that the assumption came from the plan and
survived until it was actually run.

**A test that passes either way proves nothing.** The pre-existing
`assertEqual(out.strip(), "0.1.0")` on `sdd-setup --version` passed both before and
after the refactor, because the fixture wrote `0.1.0` into its own `package.json`.
It could not distinguish a wizard reading the manifest from one carrying a copy —
exactly how the duplicated literal survived. The replacement writes `9.9.9` into the
fixture, and was confirmed to fail against the pre-refactor wizard
(`AssertionError: '0.1.0' != '9.9.9'`) before being accepted. Only two of the three
literal assertions had failed on the version bump; the third was this false
comfort.

**OIDC over a stored token.** A long-lived publish credential in repository settings
is the one place this project would contradict its own posture — `SECURITY.md`, and
`providers.yaml`'s `key_env` indirection, exist so that only env-var *names* travel
in committed content. OIDC needs nothing stored and adds provenance.

**Normalize the changelog rather than generate release notes.** `publish.yml` fails
when a version has no changelog section instead of synthesizing one. Generated notes
would be a plausible-looking record nobody verified — the same failure shape as the
stale "all suites pass" claim corrected in `milestone_5/002`.

## Verification

- M2 **32/32**, M3 **34/34** (was 32; two version tests added).
- The `9.9.9` test proven to fail against the pre-refactor wizard, then pass after.
- `bump-version.js` round-tripped `0.1.0 → 0.2.0 → 0.1.0`: 13 files changed, **0
  non-version lines** touched, idempotent on re-run, and M3 green at `0.2.0` —
  the proof the suite no longer pins a literal.
- Every `ci.yml` step executed locally: packaging check reports 28 files with
  `scripts/` and `.github/` absent; wizard smoke test, dependency check, and secret
  scan all pass.
- All three publish-decision branches exercised against the real registry
  (package absent, version present, version absent).
- Release-note extraction: 90 lines for `0.1.0`, and correctly blocking on a version
  with no section.
- Wizard: `--version` → `0.1.0`, `--help` → `(v0.1.0)`, `--bogus` → exit 2,
  executable bit intact.

## ADR assessment

One warranted and written: **ADR-005**. Two decisions had real alternatives and are
hard to reverse — the publish trigger (version-change-on-`main` vs
release-published vs tag-push) and the auth method (OIDC vs stored token) — and both
affect every future release. The version-sourcing refactor is recorded there too,
since it is what makes the trigger workable.

## Result

Releasing is now: `node scripts/bump-version.js <version>` → changelog entry →
merge to `main`. Nobody runs `npm publish`; the published tree is always one that
passed CI; doc-only pushes are silent no-ops rather than failures; and no publish
credential exists in the repository.

**Two steps remain outside CI, by necessity.** npm's trusted-publisher settings live
on an existing package's page, so the configuration cannot precede the package: the
first `npm publish` must come from a maintainer's machine, followed by the one-time
npmjs.com form. Both are documented in `CONTRIBUTING.md` and ADR-005. The first
publish was left for the maintainer to authorize — it is irreversible, and
unpublishing is limited to 72 hours with the name+version pair never reusable.
