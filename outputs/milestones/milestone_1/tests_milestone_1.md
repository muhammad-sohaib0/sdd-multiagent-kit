# SDD Multi-Agent Kit — Milestone 1 Tests

**Document:** `tests_milestone_1.md`
**Milestone:** 1 of 5
**Status:** Draft
> Companion to: `outputs/milestones/milestone_1/spec_milestone_1.md`

## Cumulative History

Same as the spec/plan. This file is both (a) the verification suite the M1 build must pass (Article III: written before the content is implemented) and (b) the mapping of one test to each node in `workflow_milestone_1.md` plus one end-to-end walkthrough. It is the T1 deliverable referenced by `tasks_milestone_1.md`.

## 1. Node Tests (one per workflow node, mapped)

| # | Workflow node | Test | Pass criterion |
|---|---|---|---|
| NT1 | S1a CT scan (non-empty brief) | Provide a non-empty brief; run research-ct-scan logic | Produces a checklist with base + conditional categories |
| NT2 | S1b CT scan (empty brief) | Provide a blank brief | HALT + ask for a brief; nothing fabricated |
| NT3 | S3a multi-milestone | Large brief → milestone-builder | Ordered milestone folders under `outputs/milestones/` |
| NT4 | S3b single-milestone | Small brief → milestone-builder | Five docs at `outputs/` root (`spec.md` etc.), no `_milestone_N` suffix |
| NT5 | M1 / G1 gate pass | spec with all required sections | Gate G1 passes. Required G1 sections = the base checklist categories: Goal, User Scenarios, Functional Requirements, Edge Cases & Rules, Out of Scope, Acceptance Criteria (spec §4.5) |
| NT6 | G1 gate fail | spec missing a section | Gate G1 blocks + returns findings to specify |
| NT7 | M2 Pass 1 objective resolution | issues tagged objective | Loop iterates until none remain (bounded by the 25-round per-pass cap, workflow C2) |
| NT8 | M3a Clarify empty | no needs_clarify items | skip, no questions asked |
| NT9 | M3b Clarify non-empty | items present | questions asked, answers folded into spec |
| NT10 | M3b clarify refusal | human refuses/invalid answer | refusal recorded in PHR (with a reason); item dropped and noted in Out of Scope; not silently defaulted |
| NT11 | M8 G2 gate | all five docs reviewed | G2 passes; on failure returns to drafting sub-skill |
| NT12 | M9 Pass 2 full rigor | all five docs critiqued | passes only when every currently-valid critic scores **perfect** — `overall_score == 10` with zero issues, per the M2 US-2 perfect rule (the M1-era `≥ 9` definition was superseded; the M1 doc is bound by the later M2 contract) |
| NT13 | M10 Stranger pass | fresh session on five-doc set | contract parity achieved — the fresh session independently derives the same 13 file paths, the same seven-model + ordered `critic_slots` panel, and the same seven-article constitution from the five-doc set alone (spec AC-7) |
| NT14 | M10 Stranger fail | fresh session diverges | failure fed back as a loop issue (bounded by round cap) |
| NT15 | F1 sub-skill failure | a sub-skill errors | log PHR, retry once; second failure → blocking escalation |
| NT16 | C1 critique validity | unparseable, or low-score-with-empty-issues | **low-score-with-empty-issues** = `overall_score < 10` with zero issues (the runner's validity rule). Invalid → ≤1 retry (up to 2 attempts); no cross-round exclusion — a failed critic participates again next round |
| NT17 | C2 round cap | cap reached | escalate to human with full summary, never silent |
| NT18 | B4 T16 inventory+frontmatter | check 13 files + frontmatter | 13 exist at spec §4.1 paths; eleven sub-skills — the ten from M1 plus `critique-loop` (shipped since M2 as the 11th sub-skill; M1's "no shipped critique-loop file" assumption was superseded by M2 FR-3); no stub files; the 12 SKILL.md files (11 sub-skills + master) each have name/description/version |
| NT19 | B4 T17 providers validation | parse + validate providers.yaml | seven models (`nemotron-3-ultra-550b-a55b`, `gpt-oss-120b`, `glm-5.2`, `mistral-nemotron`, `muse-glimmer-30b`, `gemini-3.6-flash`, `minimax-m3:cloud`), ordered `critic_slots`, model→provider binding, no duplicates, env-var names only (spec §4.3) |
| NT20 | B4 T18 secret scan | run detection patterns on 13 files | zero matches. Patterns: reject `sk-[A-Za-z0-9]{20,}`, `AIza[0-9A-Za-z_-]{35}`, `Bearer [A-Za-z0-9._-]{20,}`, or a base64/hex blob ≥32 chars that is not an obvious, allowlisted constant (spec §6). The allowlist is **empty by default**; the "allowlisted constant" carve-out is the mechanism by which a future legitimately-long constant would be excluded (per the §4.5 criteria: written reason + PHR). Enforced by the small check helper referenced in spec §6 — this NT20 is that helper's definition and pass criterion |
| NT21 | B4 T19 constitution verbatim | diff against PLAN.md §6 | seven articles rendered verbatim |
| NT22 | Section 3 (end-to-end walkthrough) | the full single-user path from brief → built kit | follows the walkthrough to its expected end state: 13 files exist, NT18–NT21 pass, Stranger Test achieves contract parity (spec AC-1/AC-4/AC-5) |

## 2. Acceptance-Criterion Mapping

| Acceptance | Covered by |
|---|---|
| AC-1 (13 files, no stubs) | NT18 + NT22 walkthrough |
| AC-2 (providers.yaml, ADR-001 panel) | NT19 |
| AC-3 (no secrets) | NT20 |
| AC-4 (eleven sub-skills, contracts, critique-loop as 11th) | NT18 + NT22 |
| AC-5 (pipeline order, deferrals, Clarify timing) | NT22 + NT5–NT8/NT11/NT12 (the pipeline-order nodes) |
| AC-6 (constitution verbatim) | NT21 |
| AC-7 (Stranger Test contract parity) | NT13/NT14 |

## 3. End-to-End Walkthrough (one real-user path through the whole tree)

**Scenario (M1's own build, single run):** Furnish PLAN.md as the brief (this bootstrap).
1. CT scan → checklist (S1a). Pass.
2. Constitution adopted from template (S2).
3. Milestone-builder → multi-milestone (S3a), 5 milestones, ordered (PHR milestone_0/002).
4. Per milestone M1: specify → spec (M1) → G1 passes (NT5).
5. Pass 1 critique (M2) — 11 real seven-model rounds; all objective issues resolved; needs_clarify compiled empty (M3a, NT8). Pass 1 concluded (PHR milestone_1/001).
6. plan/tasks/workflow/tests authored (M4–M7).
7. G2 gate across all five (M8, NT11). Pass.
8. Pass 2 critique — full rigor, all five (M9, NT12). Passed (PHR milestone_1/002; post-ADR-003 confirmation rounds on the seven-model panel).
9. Stranger Test on the five-document set (M10, NT13). Passed — contract parity (PHR milestone_1/003).
10. Build: execute T1→T20 to materialize the 13 kit files (M11). Completed (PHR milestone_1/003, milestone_1/004; re-verified end-to-end, PHR milestone_1/005).
11. Retire the seed; kit becomes self-hosting (BOOTSTRAP.md §3).

**Expected end state:** the 13 kit files exist and pass NT18–NT21; the Stranger Test confirms contract parity; the critique loop's transport/validity/retry machinery was exercised for real (PHR milestone_0/003, PHR milestone_1/001).

## 4. Cross-Reference

| Document | Path |
|---|---|
| Spec | `outputs/milestones/milestone_1/spec_milestone_1.md` |
| Plan | `outputs/milestones/milestone_1/plan_milestone_1.md` |
| Tasks | `outputs/milestones/milestone_1/tasks_milestone_1.md` |
| Workflow | `outputs/milestones/milestone_1/workflow_milestone_1.md` |
| Tests (this file) | `outputs/milestones/milestone_1/tests_milestone_1.md` |