# SDD Multi-Agent Kit — Milestone 3 Tasks

**Document:** `tasks_milestone_3.md`
**Milestone:** 3 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_3/spec_milestone_3.md`

## Cumulative History

Same as the spec/plan. Ordered build plan for the installer. Tests first (Article III).

## Build Order

### Group A — Verification contract (before implementation)

- **T1 — Define the M3 verification suite** (`tests_milestone_3.md`). Contract the build must pass (AC-1..AC-6).

### Group B — Adapters `[P]` (independent of each other)

- **T2 — Write `installers/claude-code.js`** — detect/install/confirmEnabled per §10.3 (`.claude/skills/sdd-multiagent-kit/`).
- **T3 — Write `installers/claude-desktop.js`** — same location as Claude Code (shared config).
- **T4 — Write `installers/opencode.js`** — reads `.claude/skills/` directly; no separate copy; confirm `/sdd` works.
- **T5 — Write `installers/antigravity.js`** — `.agents/skills/sdd-multiagent-kit/`, separate copy, trigger embedded in description.

### Group C — Wizard + package

- **T6 — Write `bin/setup-wizard.js`** — orchestrates: keys in one pass, Pakistani-guide slot under the NVIDIA key prompt, detect → choose → install → confirm → report. Depends on T2–T5 (registers and calls them).
- **T7 — Write `package.json`** — `name`, `bin: { "sdd-setup": "bin/setup-wizard.js" }`, `files` (kit/, bin/, installers/), MIT license, no runtime deps. Depends on T6.

### Group E — Verification

- **T8 — Adapter interface check** — each adapter exports `detect`/`install`/`confirmEnabled` (AC-1).
- **T9 — Wizard key+slot check** — the wizard prompts for all three keys and offers the Pakistani-guide slot directly under the NVIDIA prompt (AC-2).
- **T10 — Graceful behavior** — detect skips an absent tool; a failing `install()` is reported per-tool and the run continues (AC-3).
- **T11 — Location + trigger check** — install destinations and Antigravity's description-embedded trigger match §10.3 (AC-4).
- **T12 — package.json + secrets** — `bin` resolves, no runtime deps, MIT; no secret-value writes into `kit/` or logs (AC-5).
- **T13 — Runnable** — `sdd-setup` bin entry resolves and the wizard starts (AC-6).
- **T14 — Key-entry rules** — masked entry, whitespace/control rejection, skip semantics, entered-this-session reminder status (NT7).
- **T15 — Discovery guards** — `installers/` missing/empty, malformed adapter, `require()` throw, duplicate `name` → each exits 2 with the offending file(s) named (NT8).

**Verification failure handling:** T8–T15 failure → fix and re-run (internal). Never aborts silently.

## Status

| Task | Status |
|---|---|
| T1 | **done** (`tests_milestone_3.md` — NT1–NT8, E2E walkthrough) |
| T2 | **done** (`installers/claude-code.js`) |
| T3 | **done** (`installers/claude-desktop.js`; shared `.claude/skills/` folder) |
| T4 | **done** (`installers/opencode.js`; no-op only when the shared folder is kit-marked, else real copy refreshes) |
| T5 | **done** (`installers/antigravity.js`; canonical `Invocation: /sdd` re-asserted idempotently) |
| T6 | **done** (`bin/setup-wizard.js`) |
| T7 | **done** (`package.json` — `name`, `bin: {"sdd-setup": "bin/setup-wizard.js"}`, `files`, MIT, zero deps) |
| T8 | **done** (NT1: all four adapters export `name`/`detect`/`install`/`confirmEnabled`; `{installed, location}` shapes; non-stub) |
| T9 | **done** (NT2/NT7: keys in one pass, masked on a TTY, guide slot under the NVIDIA prompt, key-entry rules) |
| T10 | **done** (NT3: absent tools skipped; failing install reported per-tool, run continues, exit 1) |
| T11 | **done** (NT4: §10.3 destinations + trigger semantics for all four tools) |
| T12 | **done** (NT5: `package.json` contract; secret scan 0 matches on `bin/`, `installers/`, `kit/`, milestone docs) |
| T13 | **done** (NT6: bin shebang + exec bit; `--help`/`-h` exit 0; `--version` prints the version read from `package.json` and exits 0, proven by a fixture writing a version the wizard has never seen; bad arg exit 2) |
| T14 | **done** (NT7: PTY — whitespace/control rejection + re-prompt, empty = skip, non-ASCII accepted, masked no-echo, entered-this-session status, non-TTY skips key + guide prompts) |
| T15 | **done** (NT8: all four discovery guards exit 2 with the offending file(s) named) |

Verification suite: `outputs/milestones/milestone_3/verify_milestone_3.py` — 32 tests, all PASS (NT1–NT8 + E2E walkthrough; PTY-driven; see PHR 000 addendum).