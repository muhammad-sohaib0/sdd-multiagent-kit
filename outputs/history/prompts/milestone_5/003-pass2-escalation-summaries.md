# PHR 003 (milestone_5) — Pass-2 Non-Progression Escalations (retrospective, M1–M5)

- **Prompt date:** 2026-08-20
- **Phase:** Completion pass — discharging the `PLAN.md` §4.4 escalation duty for every Pass 2 the bootstrap ran
- **Trigger:** The completion pass added the two-consecutive-non-progressing-rounds stopping condition to `PLAN.md` §4.4. Every milestone's Pass 2 actually terminated by that route, so each owes the summary the condition requires.

## What was requested

Audit how Pass 2 terminated for each of the five milestones against the stopping
conditions, and produce the escalation summary `PLAN.md` §4.4 requires wherever
the loop exited by asymptote rather than by perfect scores.

## What was produced

This record. Five escalation summaries, below, one per milestone, each built from
the round evidence already on file (`outputs/critique-log/`) and the adjudication
narratives in the milestone PHRs.

## The finding that prompted this

Pass 2's documented ideal exit is *every currently-valid critic scores perfect*.
The raw evidence shows that never happened, on any milestone:

| Milestone | Pass-2 rounds | Final round scores | Perfect? |
|---|---|---|---|
| M1 | 4 | `[4, 6, 8, 10]` | No |
| M2 | 24 (cap 25) | `[6, 7, 7, 8, 6]` | No |
| M3 | 15 | `[7, 7, 9, 5]` | No |
| M4 | 12 | `[7, 7]` | No |
| M5 | 13 | `[6, 7]` | No |

Each milestone's PHR states the real reason plainly — "**Loop concluded by
adjudication at convergence**" — and documents the asymptote with specifics: for
M5, one critic re-submitted an issue list "verbatim identical to rounds 11–12
(provable asymptote: same eight items re-submitted word-for-word)"; for M4, "no
new genuine defect appeared after r11".

So the *observation* was correct and recorded. Two things were not:

1. **`PLAN.md` §4.4 had no such condition.** The shipped `critique-loop`
   sub-skill did (two consecutive non-progressing rounds → escalate), but the
   brief that governs it listed only perfect-scores, `n_valid == 0`, and the round
   cap. The implementation was ahead of the spec, so the real exit route was
   undocumented at the top level. Now closed.
2. **The exit was recorded as a conclusion, not raised as an escalation.** The
   difference matters and is not cosmetic. §4.1 keeps the drafter structurally
   separate from the checkers; §4.4's escalation is the mechanism that keeps the
   drafter from being the one who declares its own draft done. Writing
   "concluded by adjudication" in a PHR is the drafter closing the loop on itself.
   The corrective is not to re-run the rounds — the evidence that they asymptoted
   is solid — but to hand the human what the rule entitles them to: the summary,
   with the rejections and their reasons, for their disposition.

The maintainer was in fact in the loop throughout the bootstrap (ADR-003 and
ADR-002 both record direct maintainer directives mid-run), so this is a
record-keeping and specification gap, not an unsupervised loop. Discharged below.

---

## Escalation summary — M1 (core process content)

- **Rounds:** Pass 2 rounds 1–2 (root critique-log), then post-ADR-003 confirmation rounds 3–4 (`m1-pass2/`).
- **Terminal state:** round 4, 4/7 valid, scores `[4, 6, 8, 10]`. `gemini-3.6-flash` scored a perfect 10 with zero issues.
- **Non-progression evidence:** round 4 produced **zero genuinely new items**. All 27 issues were re-raises of round-3 rejections plus three fresh misreads, each checked against the source and refuted individually (that PLAN.md §6 lacks the seven articles — it renders all seven; that §12 does not exist — it does, as "Decisions Still Open"; that the goal's `npm install -g` contradicts the M3 deferral — the goal describes the finished kit, and §3/FR-1 defer the installer explicitly).
- **Accepted and applied across Pass 2:** AC-2's stale "ADR-001 panel" → "ADR-001/ADR-003 panel"; `api_key_env` → `key_env` reconciled against the shipped `providers.yaml`; needs-clarify refusal path rerouted to Out of Scope; the FR-2 vs §4.5 `needs_clarify.md` format unified; sub-skill failure policy pinned to "same input, no backoff"; `version: 1` defined as schema version; the base64/32-char secret rule marked a heuristic; forward-reference "inherited history" defined.
- **Rejected, with reasons:** 15 items, enumerated in PHR `milestone_1/002` — chiefly the 10-vs-11 sub-skill count (line 64 states `critique-loop` is the 11th, owned by M2), the DeepSeek-removal objection (ADR-003), and the recurring `PLAN.md §X` bare-reference complaint (the document's stated convention permits it).
- **Disposition for the human:** the panel stopped producing new signal after round 3. Remaining flags are repeats or refuted misreads. Contract parity was independently confirmed by the Stranger Test (`stranger-test-milestone-1.md`) and re-verified mechanically in PHRs `milestone_1/004` and `milestone_1/005`.

## Escalation summary — M2 (critique engine)

- **Rounds:** 24 of a 25 round cap — the only milestone to effectively reach the safety cap.
- **Terminal state:** round 24, 5/7 valid, scores `[6, 7, 7, 8, 6]`.
- **Non-progression evidence:** rounds 12–24 produced no new engine-vs-spec mismatch. The last genuine mechanical catches were rounds 6 and 11 (see below); everything after was re-raises the PHR enumerates as "rejected re-raises across 4–6" recurring.
- **Accepted and applied — this loop earned its length:** round 6 caught the engine *contradicting its own spec* (stagger implemented at 2s where the spec said 4s) and forced exit code 3 on `n_valid == 0`; round 11 made the output `critics` array deterministic slot order instead of completion order, and pinned an omitted `issues` field as invalid. These are real defects a single model would plausibly have missed, and they are the strongest evidence in the bootstrap that the multi-lab panel does work.
- **Rejected, with reasons:** prompt-template over-specification; `PLAN.md` cross-reference style; document-mutation-mid-round (out of scope); `providers.yaml` validation rules (M1's spec owns them); "no automated suite" (`tests_milestone_2.md` exists); AC-1 non-stub subjectivity (defined in the spec).
- **Disposition for the human:** the round cap was the effective bound here, which is itself the §4.4 escalation trigger. The engine's behavior is now pinned by an executable suite (`verify_milestone_2.py`, 29 tests, green).

## Escalation summary — M3 (installer)

- **Rounds:** 15.
- **Terminal state:** round 15, 4/7 valid, scores `[7, 7, 9, 5]`.
- **Non-progression evidence:** `n_valid` degraded to 2–5 per round on free-tier failures, and the surviving critics recycled objections about the OpenCode no-op semantics that rounds 3–6 had already resolved and documented.
- **Accepted and applied:** the OpenCode "reads `.claude/skills/` directly" vs `install()` contradiction resolved (no-op only when the shared folder is kit-marked); `detect()` fixed as filesystem-only; `confirmEnabled()`'s Antigravity phrase check specified; `engines.node >=18` added; the full exit-code set (0/1/2/130) pinned; the Pakistani-guide slot specified as a Learn-more link to a reserved location.
- **Rejected, with reasons:** the Ollama-Cloud-vs-Ollama naming objection (consistent as written); the Desktop-shared-config objection (mandated by `PLAN.md` §10.3).
- **Disposition for the human:** behavior is pinned by `verify_milestone_3.py` (32 tests, green, hermetic — temp HOME and temp package tree, with PTY-driven masked key entry).

## Escalation summary — M4 (repository documentation)

- **Rounds:** 12.
- **Terminal state:** round 12, 2/7 valid, scores `[7, 7]`.
- **Non-progression evidence:** PHR `milestone_4/001` states it directly — "no new genuine defect appeared after r11" — and characterizes the panel's steady state: "gemini oscillates pass/trivial-items, deepseek re-raises verbatim, gpt-oss alternates genuine catches with score-5 noise".
- **Accepted and applied:** the env-var names were referenced but never enumerated, so FR-8 (Kit identity constants) was added to pin them. Notably the critics *guessed wrong* names (`SDD_API_KEY`, `SDD_MODEL`); adjudication rejected the guesses and used the real M3 names — a case where deferring to the panel would have introduced the defect.
- **Rejected, with reasons:** a demand for a `tests/docs_test.md` outline (the M4 test contract already lives in `tests_milestone_4.md`, which the critic could not see); `/sdd` "example command" suggestions that misread the trigger as an npm script.
- **Disposition for the human:** documentation coverage was independently confirmed by the Stranger Test (`stranger-test-milestone-4.md`). That test checked coverage, not correctness of the examples — and the completion pass later found a real defect in `CONTRIBUTING.md`'s adapter example that neither the panel nor the stranger caught. Recorded there.

## Escalation summary — M5 (examples)

- **Rounds:** 1 Pass-1 round + 13 Pass-2 rounds = 14 real rounds.
- **Terminal state:** round 13, 2/7 valid, scores `[6, 7]`.
- **Non-progression evidence:** the strongest in the bootstrap and provable from the artifacts — one critic's round-13 issue list was **verbatim identical** to its rounds 11 and 12 lists, the same eight items re-submitted word-for-word.
- **Accepted and applied:** workflow-node and test-row definitions; the private-URL definition; the exact `FR-<n>→C<m>` / `AC-<n>→NT<m>` entry formats with the Unicode arrow pinned; a decisive word-count rule (tables, bullets and inline code count; markers stripped; fenced blocks excluded); env-vars restricted to prose only, keeping command examples shell-agnostic; case-sensitive exact heading strings in AC-1.
- **Rejected, with reasons:** the "blockquote content" and "interleaved-order trivial" objections (both already explicitly specified, and answered twice); remaining items were semantic quibbles or over-specification.
- **Disposition for the human:** the example set verifies mechanically — every `FR-<n>` appears in the workflow traceability section and every `AC-<n>` in the tests mapping, all required headings present in relative order, all files clearing the non-stub threshold.

---

## Rationale

`PLAN.md` §4.4 now documents the exit route every milestone actually took, so the
spec and the implementation agree. These five summaries discharge the duty that
route carries. Re-running the rounds was considered and rejected: the asymptote
evidence is concrete (verbatim-identical issue lists, enumerated refutations), the
free-tier panel degrades rather than converges as rounds accumulate, and burning
further rounds would add cost without adding signal — which is the exact failure
mode the non-progression condition exists to stop.

What the record now shows honestly: the bootstrap's Pass 2 never reached all-10s,
it exited on asymptote, that exit is legitimate and specified, and the human has
the summary the rule entitles them to.

## ADR assessment

Warranted. Adding a stopping condition to §4.4 meets the significance test on all
three counts — real alternatives existed (require perfect scores and accept
unbounded loops; leave the rule only in the sub-skill), it is hard to reverse once
downstream documents depend on it, and it affects every milestone. Logged as
ADR-004.
