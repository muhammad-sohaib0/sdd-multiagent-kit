# SDD Multi-Agent Kit — Milestone 3 Workflow

**Document:** `workflow_milestone_3.md`
**Milestone:** 3 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_3/spec_milestone_3.md`

## Cumulative History

Same as the spec/plan. Scenario tree for the installer's runtime + M3 build/verification.

## 1. Installer Runtime States

```
I0 run `sdd-setup`
 ├─ [TTY] read three API keys (one pass)
 │   ├─ NVIDIA key prompt → offer "Guide for Pakistani users" option (slot only, default-No, every interactive run)
 │   │   ├─ chose guide → link to reserved content (never fabricate) → continue
 │   │   └─ skipped → continue
 │   ├─ empty/whitespace-only entry → skip; internal whitespace/control → reject + re-prompt
 │   └─ keys held in-memory only (never written/echoed/used; discarded on exit)
 ├─ [non-TTY] key prompts + guide prompt skipped → env-var names printed
 ├─ discovery guards: installers/ missing/empty, malformed adapter, require() throw, duplicate name → exit 2
 ├─ for each registered adapter: detect() → {installed, location} (tool present ≠ kit installed)
 │   ├─ tool installed → add to available list
 │   └─ not installed → skip gracefully (not an error)
 ├─ user picks which detected tools to install into (readline on non-TTY; no "none")
 │   └─ (nothing detected → report, exit cleanly)
 ├─ for each chosen tool: install(kitPath)
 │   ├─ OpenCode: no-op only when shared folder kit-marked; else real copy (refreshes)
 │   ├─ Claude Code/Desktop: copy if shared folder not kit-populated (idempotent pair)
 │   ├─ Antigravity: copy + re-assert canonical Invocation: /sdd
 │   ├─ success → confirmEnabled() → {installed, location} (called only after install)
 │   │   ├─ native tools: SKILL.md frontmatter name: sdd-multiagent-kit
 │   │   └─ Antigravity: description carries Invocation: /sdd
 │   │       └─ confirmed → report "trigger active"
 │   └─ failure → report per-tool, continue with others (never abort silently)
 └─ print final summary: installed tools + triggers + env-var reminder (fixed order,
    set-in-env / entered-this-session / not-set status)
```

## 2. Adapter Extension State (adding a new tool)

```
E1 add installers/<tool>.js implementing detect()/install()/confirmEnabled()
 → auto-discovered (no central registry; no change inside kit/)
```

## 3. M3 Build/Verification States

```
B0 start (T1 tests first)
 B1 adapters T2–T5  [P]
 B2 wizard T6 + package.json T7
 B3 verify: T8 interface | T9 keys+slot | T10 graceful | T11 locations+trigger | T12 package+secrets | T13 runnable | T14 key-entry rules | T15 discovery guards
   └─ failure → fix + re-run (internal)
```

## 4. Feature-to-Node Traceability

Keys-in-one-pass → I0; Pakistani-guide slot → I0; key-entry rules → I0; discovery guards → I0; detection → I0; per-tool failure → I0; Antigravity trigger → I0; OpenCode refresh semantics → I0; extension pattern → §2; idempotent re-run → I0 (overwrite in place; OpenCode exception). Every feature maps here; every node is backed by a task (T2–T15) and a test (NT1–NT8 in `tests_milestone_3.md`). No orphan features; no untested nodes.

## 5. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_3/spec_milestone_3.md` |
| Plan | `outputs/milestones/milestone_3/plan_milestone_3.md` |
| Tasks | `outputs/milestones/milestone_3/tasks_milestone_3.md` |
| Workflow (this file) | `outputs/milestones/milestone_3/workflow_milestone_3.md` |
| Tests | `outputs/milestones/milestone_3/tests_milestone_3.md` |