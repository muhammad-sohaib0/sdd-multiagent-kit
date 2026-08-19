# PHR 000 (milestone_3) — Installer: Pass 2, Stranger Test, Build, Verify

- **Phase:** Milestone 3 (npm installer)
- **Date:** bootstrap run

## Pass 2 (full rigor) on the M3 spec

Ran one real six-model Pass-2 round (critique-log pass2-round1-spec_milestone_3; all 6 valid). Genuine issues fixed: the OpenCode "reads .claude/skills/ directly" vs `install()` contradiction (OpenCode install is a no-op verification of the shared folder); "README input" typo → readline; non-stub defined in AC-1; `engines.node >=18` added; `detect()` (filesystem-only) and `confirmEnabled()` (Antigravity = description phrase) semantics specified; Pakistani-guide slot as a "Learn more" link to the reserved docs location; the three env-var names named; edge cases added (skipped key warning, config-dir-created, confirmEnabled-failure continues, re-run overwrite, exit codes 0/1/2); `/sdd`-from-folder and Desktop-shared-config referenced to PLAN.md §10.3. False positives rejected with reason (e.g. Ollama Cloud vs Ollama naming — consistent; Desktop-shared-config — per §10.3). Pass 2 concluded by adjudication.

## Build

Delivered `bin/setup-wizard.js` (bin: `sdd-setup`), the four adapters (`claude-code`, `claude-desktop`, `opencode`, `antigravity`), and `package.json`. Adapters export detect/install/confirmEnabled; locations per §10.3; Antigravity embeds an `Invocation: ... /sdd` line into the copied master SKILL.md. Wizard collects the three keys in one pass, offers the guide slot under the NVIDIA prompt, detects → choose → install → confirm → report, with exit codes 0/1/2.

## Verification

- T8: all four adapters export detect/install/confirmEnabled — PASS.
- T11: Claude/Claude Desktop → `.claude/skills/sdd-multiagent-kit/`; Antigravity → `.agents/skills/sdd-multiagent-kit/`; OpenCode shares `.claude/skills/` — PASS.
- T12: `package.json` bin resolves, no runtime deps, MIT — PASS.
- T13: wizard starts and prompts keys + guide slot — PASS (non-TTY pipe mode is out of scope; the interactive flow is the target).
- Direct adapter install into a temp HOME: Claude copy + confirm true; Antigravity copy + embedded Invocation trigger + confirm true (after fixing the annotation to be added regardless of a pre-existing `/sdd` mention in kit/SKILL.md) — PASS.
- No secret values written to kit/, bin/, or installers/ — PASS.

## Stranger Test

Fresh zero-context session, given only the five M3 docs, independently derived: all six artifact paths; the three-function adapter interface and its per-tool meaning; the four §10.3 install locations and the Antigravity-vs-native trigger handling; the wizard flow order; the three env-var names + exit codes; and the package.json requirements. All matched the built artifacts. **PASS.**

**Result: Milestone 3 complete and verified.**

## Corrective convergence round

A later Pass-2 round 2 (critique-log m3-pass2 pass2-round2-spec_milestone_3; 2/6 valid — heavy free-tier saturation) added genuine micro-clarifications: `install(paths)`/`detect().location` semantics defined (single absolute `kit/` dir path; absolute `location`), `package.json` declared zero dev-dependencies too (stdlib-only wizard), and edge cases added for Ctrl-C/abort (no partial writes) and invalid tool selection (re-prompt). Rejected with reason: the "non-stub is subjective" and "OpenCode install must do file ops" objections (both already specified in FR-3 line 40 and AC-1/M4 definition), the "guide placeholder URL" objection (it points at the real reserved `docs/GUIDE.md#guide-for-pakistani-users` path), and the "package name/version conflict" objection (pinned in FR-5). The build already matched all revised items; no rebuild required.

## Post-PHR convergence (engine hardening, panel change, rounds 6–9)

A second corrective phase, driven by live critique rounds on the seven-model panel (see ADR-003 for the panel change; engine fixes recorded here as they are installer-adjacent design input). Rounds 6–9 (critique-log m3-pass2) applied genuine pins and aligned the build at each step; PTY end-to-end re-verified after each build change (rc=0, all four tools installed+confirmed, no key leaks). Notable converged items:

- Key handling: onboarding-only (keys never written/echoed/used); empty/whitespace-only entry = skip; **internal-whitespace/control-character keys rejected + re-prompted** (format sanity, no provider validation); non-ASCII accepted; non-TTY skips key **and** guide prompts (TTY-only), prints env-var names; reminder prints fixed-order status + skipped marking.
- Discovery guards (all exit 2 with clear messages): `installers/` missing/empty, malformed adapter (missing exports), **duplicate adapter `name`**; kit source found by walking parents for `package.json` with `name: sdd-multiagent-kit` **and** sibling `kit/SKILL.md` (monorepo-safe); `os.homedir()` failure → exit 2 before install.
- OpenCode install no-op **only when the shared folder is populated with the kit** (kit-marked `SKILL.md`); otherwise a real copy refreshes — stale-copy refresh; OpenCode-only re-runs intentionally do not refresh an existing kit-marked copy. PATH check stdlib-only with Windows `.exe`/`.cmd`/`.bat` variants.
- Claude Desktop per-platform app-config paths (macOS/Windows/Linux); Claude Code + Desktop share one folder, idempotent.
- `detect()` `{installed, location}` independent fields (`location` null when kit not installed even if tool present); `confirmEnabled()` takes no args, returns `{installed, location}`, called only after successful install (build aligned to this shape).
- Install errors: one-line message printed verbatim per-tool; tool-id prefix is a convention the wizard does not enforce; per-tool failure → exit 1, never aborts. Copy semantics: writes each source file at its relative path, never deletes other destination files.
- Exit codes + flags: `--version` added (exits 0). `files` wording clarified (npm always includes package.json/README regardless).
- T8–T13 suite re-run green after each build change; T14 (key-entry rules) and T15 (discovery guards) added to tests_milestone_3.md; the corresponding PTY and temp-tree guard checks pass.

Convergence status at round 9: 5/7 valid critics (all NVIDIA/Google/Ollama models; glm-5.2 and minimax-m3:cloud absent that round under hard provider quota 429s — see ADR-003/engine hardening for the retry/backoff/stagger/deadline machinery). Rounds 10–15 confirmed convergence: the panel's remaining flags were re-raises of settled decisions (OpenCode's deliberate no-op exception, the guide-slot reservation, stdlib raw-mode masked entry, exit-code/reminder semantics, non-stub/§10.3 cross-references), each already answered by an explicit sentence in the spec. Genuine micro-pins added across rounds 10–14: the "populated" loose-vs-strict distinction, per-tool prefix-as-convention wording, nearest-ancestor kitPath walk, XDG_CONFIG_HOME + Windows exec variants for OpenCode PATH detection, `--version`, adapter `require()`-throw guard, case-sensitive duplicate-`name` comparison, default-No guide prompt parsing, Antigravity stale-`Invocation:`-line replacement mechanism, reminder's `entered this session (not persisted)` status, `detect()` `location`-vs-`installed` independence (incl. orphaned-install case), and the opaque-string/hygiene-guard rationale. Rounds 13–15 returned no new actionable items (gpt-oss 9/10 at r15), so the spec is **converged**. Build re-verified (PTY + T8–T15) after each change; see critique-log for the record.
---

## Post-convergence strict 100% completion pass (2026-08-18)

Mechanical re-audit of the M3 build against `spec_milestone_3.md` (FR-1..FR-5, edge cases, AC-1..AC-6) and `tests_milestone_3.md` (NT1–NT8), run end to end with a new hermetic verification suite. Conformance gaps found and fixed:

- **`bin/setup-wizard.js`**
  - **Masked-entry echo leak (real bug).** The wizard created a terminal-mode `readline` interface at load and ran its own raw-mode reader on the same TTY; readline's line editor echoed every keypress, so masked API keys appeared in terminal scrollback — violating FR-1's "masked entry, no echo". Fixed: `readline` is now created lazily and only for piped/non-TTY input; on a TTY the raw-mode reader is the only reader. PTY-verified: typed keys never appear in captured output.
  - **UTF-8 key entry was mangled.** The raw-mode reader appended `String.fromCharCode(byte)` per byte, so multibyte (non-ASCII) keys were corrupted. Fixed: bytes are buffered and decoded as UTF-8 at line end (backspace re-encodes after dropping the last code point). PTY-verified: `ключ-🔑` accepted intact.
  - **EOF at a prompt exited 0 instead of 130.** readline never invokes a pending question callback on EOF; the event loop drained and node exited 0 (spec: EOF with no pending input = user abort, 130). Fixed: `q()` races the question against the `close` event; empty resolution + `stdinClosed` → exit 130. Ctrl-D on a TTY also aborts 130.
  - **Reminder missing on early exit.** The final env-var reminder (spec: "both TTY and non-TTY runs") was skipped when nothing was detected. Fixed: `printReminder()` runs on every completion path.
  - Control-character rejection widened to `/[\s\x00-\x1f\x7f]/` (defensive; raw mode already strips most control bytes); "Collected … (stored in your environment only)" reworded — keys are never stored (onboarding-only).
- **`installers/antigravity.js`** — the appended trigger line carried a trailing explanation (`Invocation: /sdd — invoke this skill with the trigger phrase \`/sdd\`.`); the canonical line is now exactly `Invocation: /sdd`, and `replace()` is global (`/gm`) so every stale `Invocation:` line converges on re-runs (FR-2 mechanism, deterministic check).
- **All four adapters** — `detect()` bodies now wrap the filesystem checks in try/catch: any fs error (EACCES, ENOTDIR, ELOOP, EMFILE) logs a warning and returns `{installed: false, location: null}` — detection never aborts the wizard (FR-2).
- **`outputs/milestones/milestone_3/tasks_milestone_3.md`** — status table completed (T1–T15) and the missing T14/T15 rows added (the tests/workflow documents already referenced them).

**Mechanical verification (scripted, all PASS):** new suite `outputs/milestones/milestone_3/verify_milestone_3.py` — 32 tests covering NT1–NT8 + the §3 E2E walkthrough, fully hermetic (temp package tree + temp HOME; PTY harness drives the real wizard):
- NT1: adapter interface (exports, `{installed, location}` shapes, `location: null` when the kit is absent, orphaned-install case), non-stub check.
- NT2/NT7: PTY — three keys in one pass in fixed order, masked (key text never in captured output), guide slot directly under the NVIDIA prompt (slot-only link, default-No), `(existing value found)` hint, whitespace/control rejection + re-prompt, empty = skip with warning, non-ASCII accepted, `entered this session (not persisted)` reminder status, non-TTY skips key + guide prompts and prints the reminder.
- NT3: absent tools skipped; a throwing `install()` reported per-tool (`[FAIL] Bad Tool: bad-tool: boom`) with the run continuing and exit 1; a throwing `detect()` logged and skipped.
- NT4: §10.3 destinations for all four tools; Claude Desktop per-platform app-config detection + copy-if-not-kit-populated; OpenCode config-dir/PATH/XDG detection, Windows exec variants, no-op only on a kit-marked shared folder, real copy refreshes stale content; Antigravity canonical `Invocation: /sdd` under `version:`, stale-line replacement, confirm true; in-place overwrite + idempotent re-runs (marker-preserved/no-op vs marker-replaced/copy).
- NT5: `package.json` contract (name/version/license/bin/files/engines, zero deps) + secret scan 0 matches across `bin/`, `installers/`, `kit/`, milestone docs.
- NT6: shebang + exec bit; `--help`/`-h` exit 0; `--version` prints `0.1.0` exit 0; bad argument exit 2; Node < 18 guard present.
- NT8: all four discovery guards exit 2 naming the offending file(s) (missing `installers/`, no `.js`, malformed exports, `require()` throw, duplicate `name`); missing kit source exits 2.
- E2E walkthrough: PTY full run — fake tool dirs, all four detected, keys masked, guide declined, `all` selected, all four installed+confirmed to §10.3 paths, exit 0, no key values anywhere (session output, temp HOME tree, package tree); re-run idempotent in place; OpenCode-only re-run no-ops; Ctrl-C at a prompt → exit 130 with no partial state; piped EOF → 130; piped `all\n` → 0.

**Result: Milestone 3 complete and verified — 100%.**
