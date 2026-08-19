# SDD Multi-Agent Kit — Milestone 3 Tests

**Document:** `tests_milestone_3.md`
**Milestone:** 3 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_3/spec_milestone_3.md`

## Cumulative History

Same as the spec/plan. Verification suite for the installer. Article III: written before implementation (T1).

## 1. Node Tests (per workflow node)

| # | Node | Test | Pass criterion |
|---|---|---|---|
| NT1 | T8 adapter interface | require each `installers/*.js` | each exports `name`, `detect`, `install`, `confirmEnabled` (discovery validates the interface, exit 2 on a malformed adapter file); `detect()` returns `{installed, location}` with `location: null` when not installed (AC-1) |
| NT2 | T9 keys + slot | run wizard prompt sequence (mock stdin; PTY for the TTY path) | collects all three keys in one pass in order (NVIDIA, Google, Ollama); key entry is masked on a TTY (raw-mode, no echo) with a `[skip]`/`(existing value found)` hint; key prompts require a TTY — off-TTY they are skipped with the env-var names printed (no cleartext echo); Pakistani-guide option appears directly under the NVIDIA key prompt, slot-only (AC-2) |
| NT3 | T10 graceful | adapter `detect()` returns false for an absent tool; a stub `install()` throws | absent tool skipped (no error); failing install reported per-tool and the run continues to others (AC-3) |
| NT4 | T11 locations + trigger | assert destination paths per §10.3 | Claude Code/Desktop → `~/.claude/skills/sdd-multiagent-kit/` (user-level); Claude Desktop `detect()` verifies the desktop app itself (per-platform app config dir); OpenCode → detects the tool itself (config dir/executable on PATH incl. Windows `.exe`/`.cmd`/`.bat`), reads `.claude/skills/` (no-op only when populated *with the kit* — `SKILL.md` carries `name: sdd-multiagent-kit`; otherwise a real copy refreshes); Antigravity → `~/.agents/skills/sdd-multiagent-kit/` with the canonical `Invocation: /sdd` re-asserted into the copied SKILL.md (AC-4) |
| NT5 | T12 package + secrets | `require('package.json')`; scan for secret writes | `bin.sdd-setup` resolves to `bin/setup-wizard.js`; no runtime deps; license MIT; `files` includes `kit/` and `installers/`; no key values written to `kit/` or logs (AC-5) |
| NT6 | T13 runnable | resolve the bin entry and start the wizard | the `sdd-setup` bin path exists, carries the `#!/usr/bin/env node` shebang + executable bit, and the wizard begins; `--help` exits 0; `--version` prints the package version and exits 0; any other argument exits 2 (AC-6) |
| NT7 | T14 key-entry rules | PTY: enter a whitespace-containing key, then a valid one; pipe a non-TTY run | internal-whitespace/control-character keys are rejected and re-prompted (no fixed retry cap); empty/whitespace-only entry = skip; non-ASCII accepted; reminder reports a key entered this session as `entered this session (not persisted)` — never `set in env`; on non-TTY the key prompts **and** the Pakistani-guide prompt are skipped and the env-var names printed (AC-2) |
| NT8 | T15 discovery guards | point `installers/` at a dir with no `.js` files, a malformed adapter, and two adapters sharing a `name` | each configuration error exits 2 with a clear message listing the offending file(s) (AC-1) |

## 2. Acceptance-Criterion Mapping

| Acceptance | Covered by |
|---|---|
| AC-1 (five files + adapter interface) | NT1 + NT8 + build presence |
| AC-2 (keys + guide slot) | NT2 + NT7 |
| AC-3 (graceful detection/failure) | NT3 |
| AC-4 (locations + trigger per §10.3) | NT4 |
| AC-5 (package.json + no secrets) | NT5 |
| AC-6 (sdd-setup runnable) | NT6 |

## 3. End-to-End Walkthrough

Simulate `sdd-setup`: feed the three keys via mock stdin, decline the Pakistani-guide option, and run against an environment where only a mock "installed" tool exists. Expect: keys collected in one pass (masked on a TTY); guide slot offered under the NVIDIA prompt; the absent tools skipped; the chosen tool installed to its §10.3 path; `confirmEnabled()` returns the trigger active; final summary printed; re-running overwrites in place (idempotent). The `kit/` folder and all logs contain no key values. Interrupt (Ctrl-C) aborts cleanly with exit 130 and no partial writes.

## 4. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_3/spec_milestone_3.md` |
| Plan | `outputs/milestones/milestone_3/plan_milestone_3.md` |
| Tasks | `outputs/milestones/milestone_3/tasks_milestone_3.md` |
| Workflow | `outputs/milestones/milestone_3/workflow_milestone_3.md` |
| Tests (this file) | `outputs/milestones/milestone_3/tests_milestone_3.md` |