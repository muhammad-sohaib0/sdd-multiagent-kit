# ADR-004 — Add non-progression as an explicit Pass-2 stopping condition

**Date:** 2026-08-20
**Status:** Accepted (completion pass)
**Affects:** `PLAN.md` §4.4 (stopping conditions), `kit/SKILL.md` (standing rules), `kit/skills/critique-loop/SKILL.md` (step 4), and the interpretation of every Pass 2 the bootstrap ran

## Context

`PLAN.md` §4.4 listed three ways a critique pass could end: Pass 1 resolving every
objective issue, Pass 2 reaching perfect scores from every currently-valid critic,
and the round safety cap (default 25) escalating to the human. The shipped
`critique-loop` sub-skill carried a fourth that the brief did not: on the second
consecutive non-progressing round, escalate.

Auditing the bootstrap's own critique evidence showed the omission was not
academic. **No milestone's Pass 2 ever reached perfect scores.** Final rounds
landed at `[4,6,8,10]` (M1), `[6,7,7,8,6]` (M2), `[7,7,9,5]` (M3), `[7,7]` (M4),
and `[6,7]` (M5). Scores plateaued in the 6–8 band, and `n_valid` degraded to 2–5
of 7 as free-tier providers failed. Each milestone's PHR recorded the real exit as
"loop concluded by adjudication at convergence" — a route with no entry in §4.4.

The asymptote itself is well-evidenced, not asserted: M5's round 13 issue list was
verbatim identical to its rounds 11 and 12, the same eight items word-for-word;
M4's PHR records "no new genuine defect appeared after r11".

Two problems followed. The spec did not describe how the system actually
terminated, so the top-level brief and the shipped kit disagreed. And the exit was
recorded as a *conclusion by the drafter* rather than raised as an *escalation to
the human* — which erodes the maker/checker separation §4.1 is built on, since the
drafter ends up signing off on its own document.

## Alternatives considered

| Option | Verdict | Reason |
|---|---|---|
| Add the non-progression condition to §4.4, define it, and require the escalation summary | **Adopted** | Documents what the system genuinely does; keeps a bounded exit; preserves maker ≠ checker by handing disposition to the human |
| Leave §4.4 as-is and keep the rule only in the sub-skill | Rejected | The brief governs; a stopping condition living only in an implementation file is exactly the drift this ADR corrects |
| Require literal all-10s, re-running until reached | Rejected | Not achievable against a re-raising free-tier panel — the observed behavior is plateau-then-degrade, not convergence. Would spin to the round cap on every document while adding no signal, which is the failure mode the condition prevents |
| Lower "perfect" from 10 to ≥8 so the recorded rounds qualify | Rejected | Moves the goalposts to fit the evidence. `PLAN.md` §4.3's validity rule is built on 10 meaning "requires no revision"; redefining it would weaken the rubric to manufacture a pass |
| Treat "concluded by adjudication" as sufficient and change nothing | Rejected | Lets the maker approve its own work — the one structural guarantee the design exists to hold |

## Decision

1. `PLAN.md` §4.4 gains the condition: **two consecutive non-progressing rounds →
   escalate to the human with a full summary.**
2. **Progression is defined** in the brief: a round is progressing when the
   document changed in response to it, or it surfaced at least one issue triaged as
   genuinely new and actionable. Consecutive means no progressing round between
   them. Progression is tracked at session level, since one invocation is one round
   and cannot observe its predecessor.
3. **The escalation's contents are specified:** rounds run, issues accepted and
   applied, issues rejected *with their written reasons*, and the evidence that
   remaining flags are repeats. The human disposes of it.
4. **Explicit limit:** non-progression may never exit a gate or the Stranger Test.
   Those stay frozen nodes; only the quality-scoring loop can end this way.
5. The five Pass-2 exits already taken are documented retrospectively as
   escalations in PHR `milestone_5/003`, each with its own summary. The rounds are
   **not** re-run — the asymptote evidence stands on its own.

## Consequences

- The brief now describes the loop's real behavior; `PLAN.md`, `kit/SKILL.md`, and
  the `critique-loop` sub-skill agree on all four exits.
- Pass 2 has a bounded, honest exit that does not depend on free-tier critics
  behaving ideally, and does not require pretending they did.
- The drafter can report that the panel stopped producing signal, but cannot close
  the loop on its own document — the summary goes to the human either way.
- The bootstrap's own record is accurate rather than flattering: Pass 2 exited on
  asymptote, not on perfect scores, and says so.
- Cost: one more stopping condition to reason about, and an escalation summary owed
  per document that ends this way.
