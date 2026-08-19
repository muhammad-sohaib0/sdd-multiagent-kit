# PHR 004 (milestone_5) — Completion Pass: PLAN.md and BOOTSTRAP.md to 100% Implemented

- **Prompt date:** 2026-08-20
- **Phase:** Completion pass across the whole project
- **Trigger:** Directive to complete, fix, and improve the project so that `PLAN.md` and `BOOTSTRAP.md` are fully implemented

## What was requested

Audit every clause of `PLAN.md` and `BOOTSTRAP.md` against what the repository
actually contains and actually does, fix everything that fell short, and close the
two documents out as genuinely implemented rather than nominally complete.

## What was produced

Eighteen fixes across four categories, plus the whole-system verification
`BOOTSTRAP.md` §5 requires. Nothing was declared done without being executed.

### 1. `BOOTSTRAP.md` §5 — the real bar (the largest gap)

The criterion `BOOTSTRAP.md` calls "the actual bar" had never been run. It now has:
`sdd-setup` installed the kit, and fresh zero-context sessions were handed an
unrelated brief (a grocery stock-reconciliation CLI). They produced a correct
four-milestone dependency-ordered breakdown and a full five-document set.
**PASS**, recorded in `outputs/critique-log/stranger-test-whole-system.md`.

This test found **13 real defects in the shipped kit** — the single most valuable
result of the pass, and precisely what §4.5 predicts a zero-context run will surface
that authors cannot:

- **Contradictions:** G1 was literally unsatisfiable (`specify` mandates a
  Cross-Reference section to four files that do not exist yet; G1 rejects references
  to things that do not exist); `plan-builder` carried a workflow-traceability
  obligation it runs too early to meet; gate-failure routing assumed one owning
  sub-skill where one root cause spanned three documents.
- **Undocumented paths:** pre-milestone PHRs (the stranger invented `project/`, the
  bootstrap had used `milestone_0/`), the Requirement Category Checklist, and the
  milestone breakdown.
- **Undefined rules:** PHR numbering, ID schemes for tasks/nodes/tests, `[P]`'s
  group boundary, task-status vocabulary, and whether "one test per node" covers
  grouping parents.
- **Weak enforcement:** Article III's "confirmed to fail first" had no task-level
  representation; `task-breakdown` never instructed the §7.4 back-reference, so
  produced `tasks`/`tests` documents lacked it.

All 13 fixed in `kit/`, and the corrected kit re-installed to every tool.

### 2. `BOOTSTRAP.md` §3.6 and §6 — seed retired

`.claude/skills/sdd-multiagent-kit-seed/` and `.bootstrap/` deleted. Both still
described the pre-ADR-003 six-model panel, so they were two stale copies of the
process. §6's lifecycle clause is now satisfied, and the recipe-vs-record
relationship between `BOOTSTRAP.md` and `docs/BOOTSTRAP.md` is stated in both.

### 3. `PLAN.md` gaps closed

- **§4.4** gained the non-progression stopping condition, with progression defined
  and the escalation's required contents specified. Every milestone's Pass 2
  actually exited this way; the brief did not describe it. See ADR-004 and PHR
  `milestone_5/003`, which discharges the escalation summaries for all five.
- **§9** gained the four working artifacts (`requirement-checklist.md`,
  `milestone-breakdown.md`, per-milestone `needs_clarify.md`, `milestone_0/` PHRs),
  with the five-documents-vs-working-artifacts distinction spelled out. The
  bootstrap's own checklist and breakdown were extracted from PHRs to those paths.
- **§9's `stranger-test-milestone-N.md`** files were mandated by the layout and did
  not exist. Written for all five from the PHR evidence, without fabricating
  results.
- **§6** article wording no longer cites this brief's section numbers, since the
  seven articles ship to users who never receive `PLAN.md`. Fixed at the source so
  the template stays verbatim-identical — AC-6 verified 7/7.
- **§4.2's** six-critics-era text and ADR-003's stale stagger/retry figures
  reconciled with the shipped engine via an errata table.

### 4. Correctness and packaging

- **`CONTRIBUTING.md` worked example A was broken.** It omitted the mandatory `name`
  export and returned a bare boolean from `confirmEnabled()`. Verified empirically:
  an adapter built from it made the wizard **exit 2 at startup**, blocking every
  tool. Rewritten as a complete working adapter and re-verified end to end —
  `[OK] ... trigger active`, rc 0.
- **Four failing tests fixed** (M2 24/26, M3 30/32 at audit). Both were stale
  fixtures, not product defects: `providers.yaml` had moved to the §4.3 `- id:` map
  form while the M2 helper still emitted Python reprs, and the M3 fixtures wrote a
  bare `name:` line after the adapters were correctly tightened to read inside the
  frontmatter block. Suites now **M2 29/29, M3 32/32**, with three regression guards
  added because the root cause was that *nothing pinned the dual-form contract*.
- **`docs/` was missing from `package.json` `files`**, so README's GUIDE link and
  the wizard's printed guide pointer both dangled in a global install. Added, plus
  negated entries to keep Python bytecode out of the tarball (a `.npmignore` cannot
  override an allowlist; verified with `npm pack --dry-run`). M3 spec FR-5 and its
  test updated to match.
- **`kit/SKILL.md` told users the installer "ships in a later milestone (M3); until
  then, place this content manually"** — in the file the installer had just placed.
  Rewritten, along with other bootstrap-milestone leakage into shipped content.
- **Installed copies were three days stale**, still carrying the old
  `providers.yaml` form. Refreshed via `sdd-setup`; verified identical to `kit/`.

### 5. History corrected

PHR `milestone_5/002` claimed "All five suites pass on the built kit." True when
written, false by audit time. Corrected in place with the reason it went stale —
`providers.yaml` and the adapters changed underneath it and nothing re-checked — and
the two code-inspection-only PASSes labelled honestly.

## Rationale

The distinction driving this pass: a clause is implemented when the repository
*does* what it says, not when a file with the right name exists. Three kinds of gap
turned up — deliverables that were specified and absent (§9's stranger-test files),
behavior that diverged from the spec and was recorded as compliant (Pass 2's exit),
and shipped content that was correct-looking but broken (the CONTRIBUTING example,
which no reviewer had executed).

The 13 defects from the real bar are the pass's most useful output, and they are all
of one shape: **conventions the bootstrap's author knew but never wrote down.** Every
one was invisible from inside — the documents read as complete to someone already
holding the missing context. That is the exact failure mode §4.5 exists to catch, and
it took an actual zero-context run to catch it. Running that test was the single
highest-value item in the whole pass.

## ADR assessment

One ADR warranted and written: **ADR-004** (non-progression stopping condition) —
real alternatives existed, hard to reverse, affects every milestone. The remaining
fixes are corrections and specification completions, not design changes, so no
further ADR.

## Result

`PLAN.md` and `BOOTSTRAP.md` are implemented end to end: every §11.3 structural item
present (34/34), every §9 output present, all four `BOOTSTRAP.md` §4 non-negotiables
accounted for honestly, and §5 and §6 — the two clauses that had never been
discharged — both closed with evidence.

---

## Addendum — §4.3 example contradicted §4.2 (user-reported)

**The defect.** §4.3's schema example carried `"pass": 1` alongside
`"testability": 7`, while §4.2 states that Pass-1 critics emit `testability: 0`
("not assessed in this pass"). The brief's normative rule and its illustrative
example disagreed, in the one place a reader looks to learn the response format.

Reported by the user, not found by any of my sweeps — my checks had verified that
files exist, that references resolve, and that suites pass, but nothing compared a
worked example against the rule it illustrates. Worth noting as a gap in how I was
auditing, not just in the document.

**Investigating it exposed the larger problem.** Checking what real critics actually
emitted across every Pass-1 log on file:

```
testability values observed in Pass-1 rounds: {10: 10, 9: 23, 8: 20, 7: 9, 6: 2, 0: 5}
```

Only **5 of 69** Pass-1 critiques honored the rule. The other 64 scored a dimension
the pass explicitly does not assess. So §4.2's rule was not merely mis-illustrated —
it was **unenforced in practice**. Nothing rejected a non-conforming value, nothing
corrected it, and the logged evidence therefore claimed a runtime had been judged
when none existed. The engine's own prompt constant instructs critics correctly; the
critics simply ignore it, which is exactly the free-tier behavior the rest of the
engine is built to absorb.

**Fixes applied:**

1. **§4.3's example is now a `"pass": 2` response**, where all five dimensions
   legitimately carry scores — the better illustration anyway, since Pass 2 is the
   full-rubric pass. A short note states the single Pass-1 difference explicitly.
2. **The engine now normalizes `testability` to 0 on every Pass-1 response**
   (`validate_shape(o, ps)`), after numeric coercion and before the shape check.
3. **Normalize, not reject.** A non-conforming value is corrected rather than
   invalidating the critique. The rule is a scoping convention, not a correctness
   test; discarding a critique with real findings in clarity and completeness — as
   the live check below produced — to punish one out-of-scope field would trade
   signal for tidiness. Nothing in §4.4 reads `testability`, so no control flow
   changes.
4. **Three regression tests** pin the behavior: Pass-1 normalization across emitted
   values 7/9/10/0 with the other four dimensions asserted intact, Pass-2
   preservation, and an end-to-end check that a written Pass-1 log carries 0 and
   still validates.
5. **Contract propagated** to the M2 spec (a new normalization paragraph) and to the
   `critique-loop` sub-skill (do not read a Pass-1 `testability` as a judgement, and
   do not raise its being 0 as an issue).

**Verified against a live provider,** since the defect was about real critic
behavior rather than schema shape. A real Pass-1 round against `gemini-3.6-flash`
returned `clarity: 6, completeness: 2, edge_case_coverage: 2, internal_consistency: 8`
— genuine findings — with `testability` stored as **0**. Suites: M2 32/32, M3 32/32.
Installed copies re-synced.

**Lesson:** an unenforced rule in a brief decays into a rule that is contradicted by
its own example and ignored by its own implementation. The 64-of-69 violation rate
had been sitting in committed evidence the whole time; nobody compared the rule to
the data. This is the same failure shape as the stale "all suites pass" claim
corrected in PHR `milestone_5/002` — a statement nothing re-checked.
