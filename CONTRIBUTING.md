# Contributing to the SDD Multi-Agent Kit

Thanks for contributing! This project values small, disciplined, well-documented changes. Everything here follows the same Spec-Driven Development loop the kit teaches.

## Ground rules

- **Tests before implementation.** Every change starts from a clear spec; write the verification first.
- **Simplicity by default.** No new runtime dependencies without a strong reason. The kit runs on plain Markdown + Python 3 + Node.
- **Standalone-first.** New skills and scripts must work alone, not only when driven by the master skill.
- **No secrets.** Never commit `.env`, keys, or tokens. `.gitignore` already excludes them.
- **Credit and history.** Log a PHR (and an ADR for design decisions) alongside your change.

## How to contribute

1. Fork and create a branch.
2. Write a short spec (what and why).
3. Implement the change with its tests.
4. Run the verification (see `tests_milestone_*.md` per area) and confirm it passes.
5. Open a pull request describing the change, its spec, and its tests.

## Worked example A — add a new AI tool (adapter)

The installer supports tools through one adapter each, in `installers/<tool>.js`.

1. **Create the adapter** `installers/mytool.js` exporting one string and three functions. All four exports are mandatory — the wizard validates them at startup and exits `2` if any is missing, so an incomplete adapter blocks *every* tool, not just yours:
   - `name` — the display name string (e.g. `My Tool`). This is the tool's identifier throughout the wizard UI: the detected list, the selection prompt, and the per-tool result line. Two adapters exporting the same `name` is a configuration error.
   - `detect()` — filesystem-only check (no network) → `{ installed: bool, location: string|null }`. The two fields are **independent**: `installed` means the *tool* is present (its config directory or its executable on PATH), while `location` is the absolute path of the kit folder and is non-null **only** when that folder is already populated. Catch every filesystem error and return `installed: false` rather than throwing — detection must never abort the wizard.
   - `install(kitDir)` — copy the whole `kit/` tree to the tool's location (creating the directory if absent) → the absolute destination path. On failure throw an `Error` whose one-line message is prefixed with your tool id (e.g. `mytool: permission denied /path`); the wizard prints it, marks that tool failed, and continues with the others.
   - `confirmEnabled()` — takes no arguments and re-checks the filesystem itself → `{ installed: bool, location: string|null }`, the **same shape as `detect()`**. Returning a bare boolean here is the most common mistake: the wizard tests `result.installed === true`, so a `true` return reports WARN. Confirm registration by checking that the copied `SKILL.md` carries `name: sdd-multiagent-kit` **inside its `---` frontmatter block**, not merely somewhere in the file.
2. **Registration is automatic** — there is no central registry to edit. The wizard discovers every `.js` file directly under `installers/` at startup (`bin/setup-wizard.js`), validates the four exports, and errors on a duplicate display `name`. Dropping the file in is the whole registration.
3. **Document it** in `docs/ARCHITECTURE.md` (§5 install locations) and the README table.
4. **Add tests** mirroring the existing per-adapter tests (interface, location, trigger, graceful failure).

### Example

Resolve install paths from `os.homedir()`, not `process.cwd()` — the kit installs per user, not per working directory. This example is a complete, working adapter; copy it and change `FOLDER`'s parent path to your tool's convention.

```js
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");

const FOLDER = "sdd-multiagent-kit";

exports.name = "My Tool";

function destDir() {
  return path.join(os.homedir(), ".mytool", "skills", FOLDER);
}

function toolPresent() {
  try {
    return fs.existsSync(path.join(os.homedir(), ".mytool"));
  } catch {
    return false;
  }
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const ent of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, ent.name);
    const d = path.join(dest, ent.name);
    if (ent.isDirectory()) copyDir(s, d);
    else fs.copyFileSync(s, d);
  }
}

// The registration marker lives in the '---'-delimited block at the top of
// SKILL.md, so the check must look inside that block, not anywhere in the file.
function frontmatter(text) {
  const m = text.match(/^---\s*\n([\s\S]*?)\n---/);
  return m ? m[1] : "";
}

function kitMarked(dest) {
  const master = path.join(dest, "SKILL.md");
  try {
    return fs.existsSync(master) &&
      /name:\s*sdd-multiagent-kit/.test(frontmatter(fs.readFileSync(master, "utf8")));
  } catch {
    return false;
  }
}

exports.detect = function () {
  try {
    const dest = destDir();
    const populated = fs.existsSync(dest) && fs.readdirSync(dest).length > 0;
    return { installed: toolPresent(), location: populated ? dest : null };
  } catch (e) {
    console.warn(`mytool: detect() error (${e.message}) — treated as not installed`);
    return { installed: false, location: null };
  }
};

exports.install = function (kitDir) {
  try {
    const dest = destDir();
    copyDir(kitDir, dest);
    return dest;
  } catch (e) {
    throw new Error(`mytool: ${e.message}`);
  }
};

exports.confirmEnabled = function () {
  const dest = destDir();
  const installed = kitMarked(dest);
  return { installed, location: installed ? dest : null };
};
```

Verify your adapter end to end before opening a pull request — drop it into `installers/` and run `sdd-setup`. It must appear in the detected list under its `name` and report `[OK]`, not `[WARN]`.

## Worked example B — add a new critic model

The critique panel is pure configuration in `kit/config/providers.yaml`:

1. **Add the model id** to the `models:` list of the provider it belongs to (e.g. `nvidia-nim`) as a new `- id: <model>` entry (the schema form in `spec_milestone_1` §4.3). If the provider doesn't exist yet, create a `providers:` entry with an `id`, a `key_env` (the env-var name for its key — names only, never values), and a `tier`.
2. **Add a `critic_slots:` entry** with `model`, `provider`, and an optional per-model `timeout` (seconds; the engine's default applies if omitted). Slot order = critique order. The engine validates that each slot's model exists in its provider's `models` list, that the provider has a `key_env`, and that the timeout is a positive number.
3. **A new provider needs engine support.** Endpoints are hardcoded per provider id: add a `call_*` function in `kit/scripts/orchestrate_critique_loop.py` and wire it into `call()`. If you want the wizard to collect the provider's key, add the env-var name to `KEY_NAMES` in `bin/setup-wizard.js`.
4. **Lock it with an ADR.** The panel is deliberately stable; changing it is a design decision that must be recorded in `outputs/history/adr/`.
5. Run one critique round (`python3 kit/scripts/orchestrate_critique_loop.py --doc <doc> --name <name> --pass 2 --round 1`) and confirm the new model parses and returns a valid verdict.

> Note: the panel's stability is intentional. Add a model because it improves coverage or cost, not to chase every new release.

## Documentation changes

Doc changes (README, `docs/`) are welcomed and expected to stay consistent with the built kit — commands, `/sdd`, env-var names, and paths must match. See `outputs/milestones/milestone_4/` for the doc-layer verification contract.

## Verification

Two executable suites are the contract; both are self-contained (M2 mocks the network, M3 builds a temp package tree under a temp `HOME`), so neither needs provider keys:

```bash
python3 outputs/milestones/milestone_2/verify_milestone_2.py   # critique engine
python3 outputs/milestones/milestone_3/verify_milestone_3.py   # installer wizard
node scripts/check-package-contents.js                         # tarball contents
node scripts/bump-version.js --check                           # version agreement
```

`.github/workflows/ci.yml` runs all four on every push and pull request, along with a secret scan. Run them locally before opening a PR — CI will not tell you anything you could not have learned in under 20 seconds.

Both workflows upgrade npm to the same version before running these checks. Keep it that way: when they ran different npm majors, `npm pack --json` changed shape between them and a green CI shipped a broken publish step to `main` (ADR-005).

## Releasing

Publishing is automated. **You never run `npm publish`** — the workflow does it, and the version number is the trigger.

```bash
node scripts/bump-version.js 0.1.1   # or 0.2.0 for features
```

That sets the version in `package.json` and in all twelve `SKILL.md` frontmatters at once. Never edit a version by hand: `bin/setup-wizard.js` reads it from `package.json`, `scripts/bump-version.js --check` asserts every copy agrees, and CI fails the build if they do not.

Then:

1. Move your entries from `## [Unreleased]` in `CHANGELOG.md` into a new `## [<version>] — <date>` section. This is not optional — `publish.yml` refuses to release a version with no changelog section, because the GitHub Release body is built from it and nobody should ship release notes they did not write.
2. Open a PR, let CI go green, and merge to `main`.
3. `publish.yml` then checks whether that version is already on npm. If it is not, it re-runs both suites, publishes, tags `v<version>`, and creates the GitHub Release. If it is, the run exits cleanly without publishing — so ordinary doc-only pushes to `main` are no-ops, not failures.

**npm versions are immutable.** A published version can never be replaced or reused, so a mistake is fixed by releasing the next patch, never by re-publishing. Check the diff before merging.

### How it authenticates

npm [Trusted Publishing](https://docs.npmjs.com/trusted-publishers) (OIDC). GitHub proves its identity at publish time with a short-lived token; **no npm token is stored in this repository**, which keeps the rule that only env-var *names* ever live in committed content. Provenance is attached automatically, so the npm page links back to the exact commit and workflow run that built the tarball.

Maintainer setup, done once per package. The CLI route is the reliable one:

```bash
npx -y npm@12 trust github sdd-multiagent-kit \
  --file publish.yml \
  --repository muhammad-sohaib0/sdd-multiagent-kit \
  --allow-publish
```

It opens a browser for the 2FA challenge and prints the created config with an id. Three things that are easy to get wrong, all learned the hard way:

- **`--allow-publish` is required, and npm 11 cannot send it.** The registry expects a `permissions` field that only npm ≥ 12 includes; npm 11's `npm trust` posts the older body and the registry answers a bare `400 Bad Request` with no explanation. Hence `npx -y npm@12` rather than whatever npm you have installed.
- **The package must already exist.** `POST /-/package/<name>/trust` returns 404 for an unpublished package — npm has no pre-publication ("pending") publisher, so the very first release is necessarily a manual `npm publish`. Only that first version lacks provenance.
- **`repository.url` in `package.json` must match the repo exactly**, in `git+https://…​.git` form. A mismatch is the most common authentication failure.

The equivalent web form is *Settings → Trusted Publisher → GitHub Actions* on npmjs.com, with workflow filename `publish.yml` (filename only, no path) and allowed action `npm publish`. Values there are case-sensitive and npm does not validate them on save, so a typo stays silent until a publish fails.

Publishing also requires 2FA on the account (`auth-and-writes`); the browser flow above enables it if it is not already on. This does **not** affect OIDC — CI keeps publishing without a second factor.

If a publish fails with an authentication error, check the trusted-publisher config and `repository.url` before anything else.