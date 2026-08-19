# SDD Multi-Agent Kit — Milestone 4 Tests

**Document:** `tests_milestone_4.md`
**Milestone:** 4 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_4/spec_milestone_4.md`

## Cumulative History

Same as the spec/plan. Verification suite for the documentation layer. Article III: written before content (T1).

## 1. Node Tests (per build/reader node)

| # | Node | Test | Pass criterion |
|---|---|---|---|
| NT1 | T14 presence+non-stub | assert the eleven files exist and are substantive | `README`, `CLAUDE`, `AGENTS`, `CONTRIBUTING`, `SECURITY`, `SUPPORT`, `LICENSE`, `CHANGELOG`, `docs/GUIDE`, `docs/ARCHITECTURE`, `docs/BOOTSTRAP` exist, non-stub (AC-1) |
| NT2 | T15 consistency | cross-check docs' key strings vs the built kit | docs use `sdd-setup`, `/sdd`, the three env-var names, and the real `kit/` paths (AC-4) |
| NT3 | T16 credit | search README | acknowledges `github/spec-kit` and `panaversity/spec-kit-plus`, clearly marked (AC-2) |
| NT4 | T17 contributing | read CONTRIBUTING | contains a full worked example for adding a new AI tool and a new critic model (AC-3) |
| NT5 | T18 secret scan + git | scan staged docs; check `.gitignore` | no secret values; `.gitignore` excludes `.env`, secrets, `node_modules`, `__pycache__/`, `*.pyc`; `outputs/critique-log/` is deliberately **NOT** ignored (ADR-002 — raw critique evidence stays versioned); repo is git-initialized (AC-5) |

## 2. Acceptance-Criterion Mapping

| Acceptance | Covered by |
|---|---|
| AC-1 (eleven files non-stub) | NT1 |
| AC-2 (README credit) | NT3 |
| AC-3 (CONTRIBUTING examples) | NT4 |
| AC-4 (consistency) | NT2 |
| AC-5 (git + .gitignore) | NT5 |

## 3. End-to-End Walkthrough

A contributor cloning the repo: README explains what/why and links to GUIDE; GUIDE walks the setup wizard; CONTRIBUTING shows how to add a new tool and model; ARCHITECTURE explains the design; AGENTS/CLAUDE give an agent everything to work in the repo; SECURITY/SUPPORT cover reporting and questions; LICENSE and CHANGELOG present. The repo is git-initialized and `.gitignore` keeps `.env`/secrets/artifacts out.

## 4. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_4/spec_milestone_4.md` |
| Plan | `outputs/milestones/milestone_4/plan_milestone_4.md` |
| Tasks | `outputs/milestones/milestone_4/tasks_milestone_4.md` |
| Workflow | `outputs/milestones/milestone_4/workflow_milestone_4.md` |
| Tests (this file) | `outputs/milestones/milestone_4/tests_milestone_4.md` |