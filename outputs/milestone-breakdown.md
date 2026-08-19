# Milestone Breakdown — SDD Multi-Agent Kit

**Artifact type:** runtime working artifact (`PLAN.md` §9), produced by `milestone-builder`
**Input:** the PHR `milestone_0/000` decomposition and `PLAN.md` §11.3
**Decision: ordered multi-milestone — 5 milestones**

> Extracted to this fixed path so the split and its ordering are readable without
> going through the history log. The primary record is PHR `milestone_0/002`,
> which remains authoritative.

## Why it splits

The kit is a multi-part framework — process content, then automation, then
installer, then distribution, then examples — where each part is a separate
deliverable with distinct dependencies. It is not a single-purpose project, so the
§7.1 "small, single-purpose projects stay as one milestone" default does not apply.

## The milestones, in dependency order

| # | Milestone | Scope | Depends on |
|---|---|---|---|
| 1 | **Core process content** | `kit/SKILL.md`, `kit/constitution.template.md`, `kit/config/providers.yaml`, and ten pure-process sub-skills | — |
| 2 | **Critique engine** | `kit/scripts/orchestrate_critique_loop.py`, `kit/scripts/validate_critique.py`, and the `critique-loop` sub-skill (the 11th) | M1 |
| 3 | **Installer system** | `bin/setup-wizard.js` and the four `installers/*.js` adapters | M1, M2 |
| 4 | **Distribution & repository** | `package.json` plus the eight root docs, the three `docs/` files, and `.gitignore` | M1–M3 |
| 5 | **Examples** | `examples/sample-project/` and `examples/README.md` | M1–M4 |

## Why this order

- **M1 first.** The definition of the process is load-bearing: the scripts automate
  it, the installer copies it, the docs describe it. Nothing meaningful exists
  until it does.
- **M1/M2 split is forced by the forward-reference gate.** The `critique-loop`
  sub-skill must reference its automation scripts, and those scripts implement
  contracts M1 defines (`providers.yaml`, the critique schema). So the skill ships
  in M2 *with* the scripts rather than in M1 pointing at files that do not exist.
  Every other sub-skill is pure process instruction with no script dependency and
  belongs in M1.
- **M3 after M1–M2.** The installer copies the kit, so the kit must be complete.
- **M3 before M4.** `docs/GUIDE.md` documents the setup-wizard walkthrough; the
  wizard has to be real before the walkthrough can be written honestly.
- **M5 last.** An example that demonstrates the finished system requires the
  finished system, and it exercises everything before it.

## Forward-reference check (§7.5)

| Milestone | Reads from | Forward reference? |
|---|---|---|
| 1 | The constitution and the Requirement Category Checklist | No — its Out of Scope *names* M2–M5 deferrals, which is what `specify` requires; naming a deferral is not consuming an artifact |
| 2 | M1's `providers.yaml` and critique schema | No |
| 3 | M1's `kit/` tree, M2's scripts | No |
| 4 | M1–M3, as the subject being documented | No |
| 5 | M1–M4, as the system being demonstrated | No |

Order verified: nothing depends on a future milestone's artifact.

## Layout

Multi-milestone layout: `outputs/milestones/milestone_N/` holding the five
`_milestone_N` documents. PHRs at `outputs/history/prompts/milestone_N/`;
pre-milestone PHRs (CT scan, constitution, this breakdown) at
`outputs/history/prompts/milestone_0/`.
