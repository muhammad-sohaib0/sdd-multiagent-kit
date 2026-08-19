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

1. **Create the adapter** `installers/mytool.js` exporting three functions:
   - `detect()` — filesystem-only check that the tool is present → `{ installed: bool, location: string }`.
   - `install(kitDir)` — copy `kit/` to the tool's config location (create if absent) → the destination path.
   - `confirmEnabled()` — verify the trigger is active → `bool`.
2. **Registration is automatic** — there is no central registry to edit. The wizard discovers every `.js` file directly under `installers/` at startup (`bin/setup-wizard.js`), validates that it exports `name`, `detect`, `install`, and `confirmEnabled`, and errors on a duplicate display `name`. Dropping the file in is the whole registration.
3. **Document it** in `docs/ARCHITECTURE.md` (§5 install locations) and the README table.
4. **Add tests** mirroring the existing per-adapter tests (interface, location, trigger, graceful failure).

### Example

```js
"use strict";
const fs = require("fs"), path = require("path");
const FOLDER = "sdd-multiagent-kit";
function destDir() { return path.join(process.cwd(), ".mytool", "skills", FOLDER); }
exports.detect = () => ({ installed: fs.existsSync(destDir()), location: destDir() });
exports.install = (kitDir) => {
  fs.mkdirSync(destDir(), { recursive: true });
  for (const e of fs.readdirSync(kitDir, { withFileTypes: true }))
    if (e.isDirectory()) fs.cpSync(path.join(kitDir, e.name), path.join(destDir(), e.name), { recursive: true });
    else fs.copyFileSync(path.join(kitDir, e.name), path.join(destDir(), e.name));
  return destDir();
};
exports.confirmEnabled = () => fs.existsSync(path.join(destDir(), "SKILL.md"));
```

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