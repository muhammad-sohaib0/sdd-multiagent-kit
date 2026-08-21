# ADR-005 — Publish from GitHub on version change, authenticated by OIDC

**Date:** 2026-08-21
**Status:** Accepted
**Affects:** `.github/workflows/{ci,publish}.yml` (new), `scripts/bump-version.js` (new), `bin/setup-wizard.js` (version sourcing), `outputs/milestones/milestone_3/verify_milestone_3.py` (version assertions), `package.json` (`repository.url`), `CHANGELOG.md`, `CONTRIBUTING.md`, `AGENTS.md`

## Context

The kit was fully pushed to GitHub but had never been released: the npm registry
returned 404 for `sdd-multiagent-kit`, and the repository had **0 tags and 0 GitHub
Releases**. The requirement was that npm should stay in sync with GitHub without a
maintainer running `npm publish` by hand.

Two facts constrain any design.

**npm versions are immutable.** A published version can never be replaced or reused.
So "publish on every push" is not merely undesirable, it is impossible: the first push
would succeed and every subsequent push carrying the same version would fail with 403,
painting the whole commit history red. Some property of the commit must decide whether
a publish is due, and the version number is the only honest candidate.

**The version was not a single value.** `0.1.0` was hand-written in 17 places —
`package.json`, two literals in `bin/setup-wizard.js`, twelve `SKILL.md` frontmatters,
and five assertions in `verify_milestone_3.py`. Two of those assertions pinned the
literal, so a *correct* version bump turned the M3 suite red. Verified by doing it:
bumping to `0.2.0` produced `FAILED (failures=2)`. Since the publish workflow runs the
suites before publishing, version-driven release would have deadlocked on its first
use — the bump needed to release is the bump that blocks the release.

A third finding shaped the test design. The pre-existing assertion
`assertEqual(out.strip(), "0.1.0")` on `sdd-setup --version` passed *both* before and
after the refactor, because the fixture wrote `0.1.0` into its own `package.json` too.
It could not distinguish a wizard reading the manifest from one carrying a copy — which
is precisely how the duplicated literal survived unnoticed.

## Alternatives considered

### What triggers a publish

| Option | Verdict | Reason |
|---|---|---|
| Push to `main` where `package.json`'s version is not yet on npm | **Adopted** | Closest honest reading of "GitHub changes → npm changes" within immutability. Merging is the only action; no second ceremony. Doc-only pushes exit 0 silently instead of failing |
| Publish on a GitHub Release being published | Rejected | Requires a manual release-creation step per version, so it is not automated so much as relocated. Also splits the source of truth: the tag and `package.json` can disagree |
| Publish on any push to `main` | Rejected | Fails on the second push forever. Immutability makes this unimplementable, not just noisy |
| Publish on a `v*` tag push | Rejected | Same manual-ceremony objection, plus tags are easy to push from a stale checkout, which would publish content that never passed CI on `main` |

### How it authenticates

| Option | Verdict | Reason |
|---|---|---|
| npm Trusted Publishing (OIDC) | **Adopted** | No stored credential to leak or rotate. Provenance is automatic, so the npm page proves which commit built the tarball. Consistent with the kit's own rule that only env-var *names* live in committed content |
| `NPM_TOKEN` in GitHub Secrets | Rejected | A long-lived publish credential in repository settings is the one place this project would contradict its own security posture (`SECURITY.md`, `providers.yaml`'s `key_env` indirection). Also needs rotation and an explicit `--provenance` |
| Keep publishing manually from a laptop | Rejected | The status quo being replaced. No provenance, no guarantee the published tree matches `main`, and it does not survive the maintainer being unavailable |

### How the version stops being duplicated

| Option | Verdict | Reason |
|---|---|---|
| `package.json` is the sole source; wizard reads it; a script bumps the twelve SKILL.md copies; tests assert agreement | **Adopted** | The SKILL.md frontmatter version is required by the Agent-Skills standard and cannot simply be deleted, so the duplication must be *managed* rather than removed. One command changes them together, `--check` proves agreement, CI enforces it |
| Generate SKILL.md frontmatter at install time | Rejected | Makes shipped skill files derived artifacts, so a user reading `.claude/skills/.../SKILL.md` no longer sees what the repo contains. Large change, small gain |
| Decouple skill versions from the package version | Rejected | Defensible in principle — they are different things — but they ship in one tarball and nothing would keep the mapping discoverable. Lockstep is the simpler true statement |
| Leave the literals and bump by hand | Rejected | 15 files per release with a test that fails when you get it right. This is the defect being fixed |

## Decision

1. **`ci.yml` runs on every push and pull request:** both milestone suites, the
   packaging assertions (`docs/` present, no `.pyc`, no `scripts/` or `.github/` in the
   tarball), version consistency, a no-dependencies assertion, a wizard smoke test, and
   a secret scan. `contents: read`, no secrets. This is the part that truly means
   "every GitHub change is checked."
2. **`publish.yml` runs on push to `main`:** it publishes only when `package.json`'s
   version is absent from the registry, and otherwise **exits 0 without publishing**.
   That silent-skip path is the load-bearing behavior; without it the automation is
   unsafe to leave running.
3. **The publish decision reads stdout, not the exit code.** Verified against the live
   registry: `npm view <pkg>@<ver> version` exits 1 with empty output both when the
   package does not exist (first publish) and when the package exists but the version
   does not. Only non-empty output proves a version is live. A registry error also
   yields empty output and thus an attempted publish, which npm rejects with 403 — a
   loud failure rather than a silent duplicate, the safe direction.
4. **Authentication is OIDC**, with `id-token: write`. No `NODE_AUTH_TOKEN` and no repo
   secret; provenance is automatic. The maintainer configures the trusted publisher once
   on npmjs.com. `repository.url` is normalized to the canonical `git+https://…git` form
   that npm matches against the building repository.
5. **Release-note extraction is a gate.** A version with no `## [<version>]` section in
   `CHANGELOG.md`, or an empty one, fails the run. The GitHub Release body is built from
   that section, and generating it would produce release notes nobody verified.
6. **The version has one source.** `pkgVersion()` in `bin/setup-wizard.js` walks up for
   the package manifest — the same idiom as `kitDir()`, minus the `kit/SKILL.md`
   requirement so `--version` works without the kit tree. When no manifest is readable
   it reports an error and exits 2 rather than inventing a number.
7. **M3 asserts the property, not the value.** The literal assertions are replaced by
   (a) a fixture writing `9.9.9`, so a wizard carrying its own copy cannot pass, and
   (b) a check that all twelve frontmatters match `package.json`. Confirmed that (a)
   fails against the pre-refactor wizard — `AssertionError: '0.1.0' != '9.9.9'` — because
   a test that passes either way proves nothing. M3 goes 32 → 34 tests.
8. **The first publish is manual, once.** npm's trusted-publisher settings live on an
   existing package's page, so the configuration cannot precede the package. This is
   recorded as a known one-time exception, not a gap.

## Consequences

- Releasing is `node scripts/bump-version.js <version>` → changelog entry → merge.
  Nobody runs `npm publish`, and the published tree is always one that passed CI.
- Doc-only pushes to `main` are no-ops that exit 0, so the automation can be left
  unattended without producing false failures.
- No publish credential exists in this repository, and users get provenance linking each
  tarball to its commit.
- A half-finished bump cannot ship: `--check` fails in CI and again in `publish.yml`.
- Cost: version bumps must go through the script, and a new sub-skill must carry a
  `version:` frontmatter key or `--check` fails — deliberate, since a skill without one
  is malformed under the Agent-Skills standard anyway.
- Accepted limitation: the trusted-publisher configuration is state on npmjs.com that
  this repository cannot verify. A mismatch surfaces only as an authentication failure at
  publish time, so `CONTRIBUTING.md` names it as the first thing to check.
- The retired path is not merely deprecated but removed: no token, no manual publish
  step, and `AGENTS.md` says so, so a future agent does not reintroduce one.

## Addendum — CI and publish must run the same npm

**Found by the first real run on `main`.** The merge triggered `publish.yml`, which
failed — not on authentication, as expected, but on the **packaging check**, with
`TypeError: Cannot read properties of undefined (reading 'files')`.

`npm pack --json` has two output shapes, and the change is silent:

```
npm <= 11:  [ { id, name, files: [{path, size}, …] } ]
npm >= 12:  { "<pkg-name>": { id, name, files: […] } }
```

Reading `[0].files` works on the first and throws on the second. Verified by installing
npm 12.0.2 to a temp prefix and comparing: `Object.keys()` is `["sdd-multiagent-kit"]`
and `[0]` is `undefined`.

**Why CI did not catch it.** `ci.yml` used Node 22's bundled npm (10.9.8); `publish.yml`
runs `npm install -g npm@latest` because trusted publishing requires ≥ 11.5.1. The two
workflows therefore exercised different CLIs, and **"CI is green" stopped implying
"publish will work"** — the one guarantee the two-workflow split is supposed to provide.
That gap, not the shape change, is the actual defect: npm was always free to change its
own output format.

**Two corrections, because one would have left the gap open:**

1. `scripts/check-package-contents.js` normalizes both shapes and is called by *both*
   workflows, replacing two inline copies that had already diverged. It carries a
   `--selftest` exercising both shapes with no npm installed, since the failure mode was
   precisely a shape CI could not see.
2. `ci.yml` now upgrades npm to match `publish.yml`, so a future npm change fails on a
   branch rather than on `main`.

**Same defect class as the version duplication this ADR already records:** one rule
written down twice, in two files, drifting apart with nothing asserting they agree. The
first instance was `0.1.0` in 17 places; this was the packaging contract in two. The
lesson generalizes — a shared, executable definition beats two copies and a convention.

Also verified while investigating: `npm view <pkg>@<ver> version` behaves identically on
npm 11 and 12 across all three decision cases, so the publish decision itself was never
at risk.
