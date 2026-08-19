# BOOTSTRAP.md §5 — The Real Bar

**Artifact type:** whole-system verification record (`BOOTSTRAP.md` §5)
**Date:** 2026-08-20
**Result: PASS, with 13 defects found and fixed in the kit**

> `BOOTSTRAP.md` §5 is explicit that building the kit is not proof the kit works:
> *"a system can build one specific thing correctly by coincidence, or because
> whoever ran it already knew the right answer."* This is the record of the test it
> names instead — the kit's own Stranger Test, run against the whole system rather
> than a single milestone.

## The criterion, verbatim

> **Once the kit is finished and installed through its own installer, give it a
> brief for a completely unrelated project — something with no connection to this
> plan or this conversation — and it must produce a correct, properly-ordered
> milestone breakdown, with real plan and task documents, without any leftover
> context from having built itself.**

## How each clause was satisfied

| Clause | How |
|---|---|
| "installed through its own installer" | `sdd-setup` was run and reported `[OK] ... trigger active` for all four detected tools. Before this the installed copies were three days stale and still carried the plain-scalar `providers.yaml`; the reinstall brought them current, verified by `diff -rq` against the repo `kit/` (identical for the shared copy; the Antigravity copy differs only by the adapter-owned `Invocation: /sdd` line, as designed) |
| "a completely unrelated project" | A **Shelf Audit Reconciler** — a grocery-chain CLI that reconciles hand-counted stock against a warehouse CSV export. No connection to SDD, agent skills, npm packaging, or critique loops. Written fresh for this test |
| "without any leftover context" | The run was dispatched to **fresh zero-context sessions**. The session that had built the kit (this one) deliberately did not run it: knowing the intended answer is precisely the contamination §5 warns about. The brief was placed in an isolated directory (`/tmp/sdd-realbar/inventory-reconciler/`) with instructions not to read the kit's own repository |
| "correct, properly-ordered milestone breakdown" | Produced — assessed below |
| "with real plan and task documents" | Produced — a full five-document set for milestone 1 |

## What the kit produced

Nineteen files, unaided: the Requirement Category Checklist, an adopted
constitution, a four-milestone breakdown, the complete five-document set for
milestone 1 (976 lines), and ten PHRs.

**The breakdown it chose** — `ingest → reconcile → present → prove`:

| # | Milestone | Depends on |
|---|---|---|
| 1 | **Input Trust** — validated streaming of both CSV shapes, every rejection carrying an explicit reason | — |
| 2 | **Reconciliation Core** — per-SKU accumulation, exact-to-the-cent variance, the five-way classification | 1 |
| 3 | **Actionable Report** — ranking, threshold suppression, report CSV, terminal summary, exit codes | 2 |
| 4 | **Scale Proof & Offline Delivery** — the 50,000-SKU / 8 GB budget and offline posture, verified | 1–3 |

## Assessment: is the breakdown actually correct?

Yes, and the reasoning is not superficial. Three things stand out as genuine
engineering judgment rather than restated headings:

1. **It found the load-bearing invariant and put it first.** The brief's "never
   silently drops a row" is listed as one non-negotiable among five. The kit
   identified it as a property *of the boundary where rows enter the system* and
   ordered ingestion first on that basis — "if it is not established there, every
   later stage has to re-establish it and the invariant becomes a habit instead of
   a structure."

2. **It derived the ordering constraint from the data, not from convention.**
   Requirement 5 ranks by absolute dollar variance, so ranking is *defined in terms
   of* a quantity milestone 2 produces. Sorting before that sort key exists to the
   cent would mean building against a placeholder — which it correctly named a
   forward-reference violation.

3. **It refused a plausible wrong answer.** It explicitly declined to make
   milestone 4 the place where memory-bounded design gets *added*, arguing
   streaming is a constraint on milestones 1–3 from the start and that milestone 4
   only *proves* the assembled budget: "No defect found in Milestones 1–3 may be
   deferred to Milestone 4." That is the distinction between hardening-as-a-phase
   (wrong) and verification-as-a-phase (right), and nothing in the brief spelled it
   out.

It also applied the Simplicity gate correctly — projecting one standalone component
across all four milestones against the default limit of 3, concluding no
justification or amendment was needed.

**Independently verified, not taken on trust:** all 14 acceptance criteria appear
in the tests mapping; all 13 required checklist categories have matching spec
sections; the spec carries its Cross-Reference section.

## The 13 defects this test found

The Stranger Test's purpose is to surface what authors are blind to, and it did.
Every finding below is a real gap in the shipped kit, found by sessions that had
only the kit's own instructions to work from. All are now fixed.

**Contradictions — the instructions could not be followed as written:**

1. **G1 was literally unsatisfiable.** `specify` step 4 *requires* the spec to end
   with a Cross-Reference section naming four files that do not exist until step 8,
   while G1's forward-reference check rejects references to things that do not
   exist. A correctly-drafted spec failed G1 on its own mandatory final section.
   Fixed: `kit/SKILL.md` now carries a table of exactly what each gate can check,
   with three sub-checks explicitly deferred to G2.
2. **`plan-builder` carried an obligation it cannot meet.** It required every
   feature to trace to a `workflow.md` scenario, but the pipeline runs it *before*
   `workflow-builder`. Fixed: the check is now stated as discharged at G2.
3. **Gate-failure routing assumed a single owner.** The master said return "the
   document to the responsible drafting sub-skill" (singular). The run hit one root
   cause spanning `tasks`, `workflow`, and `tests`. Fixed: fan-out is now specified.

**Missing paths — three artifacts the pipeline writes had no documented location:**

4. **Pre-milestone PHRs.** The master logs PHRs after the CT scan, constitution,
   and breakdown — all before milestone 1 exists — but `history-logger` documented
   only `milestone_N/` and `single-milestone/`. The stranger invented `project/`;
   the bootstrap had used `milestone_0/`. Divergence on the first artifact written.
5. **The Requirement Category Checklist** had no path. Fixed: `outputs/requirement-checklist.md`.
6. **The milestone breakdown** had no path. Fixed: `outputs/milestone-breakdown.md`.
   Both are now in `PLAN.md` §9's layout, with the working-artifact distinction
   spelled out. The bootstrap's own two artifacts were extracted to those paths.

**Missing rules — things three documents must agree on, that nothing defined:**

7. **PHR numbering.** Nothing said whether `NNN` restarts per milestone or runs
   project-wide. The stranger noted this "will bite at Milestone 2, where 011 and
   001 are both defensible."
8. **No ID scheme** for tasks, workflow nodes, or tests — yet the traceability
   tables the gates depend on cannot be written without stable ids.
9. **`[P]` referenced an undefined "group".**
10. **Task status vocabulary** was required but its allowed values never listed.
11. **"One test per workflow node" was undefined over a nested tree** — is a
    grouping parent a node? Is `START`? Fixed: leaf nodes, stated explicitly.

**Weak enforcement:**

12. **Article III's "confirmed to fail first" had no task-level representation.**
    `task-breakdown` only said order tests before implementation, which permits
    tests written and never run. The stranger invented explicit confirm-failure
    gate tasks; the kit now requires them.
13. **`task-breakdown` never instructed the back-reference** that `PLAN.md` §7.4
    requires on all four companions — so the produced `tasks` and `tests` documents
    lacked it. My own check caught this one; the agent's did not.

**Also fixed:** the constitution template shipped articles citing `§7.2`, `§5.4`,
and `§8.2` — dangling references, since users never receive `PLAN.md`. Corrected at
the source in `PLAN.md` §6 so template and brief stay verbatim-identical (AC-6
holds at 7/7), with a note that those seven paragraphs may not cite this brief's
section numbers.

## Verdict

**The criterion is met.** The kit, installed through its own installer and handed
an unrelated brief with no leftover context, produced a correct and well-argued
dependency-ordered milestone breakdown plus real plan and task documents.

And the test did the job `BOOTSTRAP.md` §1 claims for it: *"If the kit is used to
build itself and the result is wrong, that is not a special case to explain away —
it means the design itself has a real gap, found before a single outside user ever
saw it."* Thirteen such gaps surfaced. Every one was invisible from inside the
bootstrap, because the bootstrap's author knew the conventions the documents never
stated — which is exactly the blind spot §4.5 exists to catch.

## Cross-reference

| Record | Path |
|---|---|
| PHR | `outputs/history/prompts/milestone_5/004-completion-pass.md` |
| The brief used | `/tmp/sdd-realbar/inventory-reconciler/PLAN.md` (outside the repo, deliberately) |
| Per-milestone Stranger Tests | `outputs/critique-log/stranger-test-milestone-{1..5}.md` |
