---
name: critique-loop
description: >-
  The 11th sub-skill: the agent-facing layer of the critique engine. Instructs
  the agent on how to invoke the orchestration script for a given document and
  pass, how to read the resulting critique JSON, how to triage each issue
  (objective / needs_clarify / false positive), and how to apply the stopping
  conditions. The mechanical scoring lives in the scripts; the judgement lives
  here.
version: 0.1.0
---

# Critique Loop — Invoke, Triage, Stop

The script scores; you adjudicate. Keep maker ≠ checker: never score your own draft; only triage what the panel returns.

## Input
- The document to critique and the pass (1 = light, before Clarify; 2 = full rigor, after Clarify). In Pass 2 you also hold the Clarify answers — the critics never see them.

## Procedure

### 1. Invoke
Run the orchestrator for one pass over the document (one invocation = one pass over one document; `--round` is the round label, starting at 1):
```
python3 kit/scripts/orchestrate_critique_loop.py \
  --doc <path> --name <doc-id> --pass 1|2 --round <N> [--round-cap 25] [--timeout 600]
```
Set `NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY` in the environment first (names only, never logged). The panel and critique order come from `kit/config/providers.yaml` — the ordered `critic_slots` is the critique order and the script never hard-codes models.

### 2. Read
The result JSON lands at `outputs/critique-log/pass{1|2}-round{N}-{doc-id}.json`; the script's stdout log names the critics that failed the round and why. Read each critic's `overall_score`, `scores`, `issues`, and `verdict`, then verify the file's shape with:
```
python3 kit/scripts/validate_critique.py --file outputs/critique-log/pass{1|2}-round{N}-{doc-id}.json
```
There is no minimum quorum — a round completes with whatever valid critics it got and `n_valid` records it (free-tier 429s are normal). A critic that fails a round (invalid or transport) participates again next round — never excluded across rounds. Keep going — never stop because scores aren't 10.

### 3. Triage every issue
- **objective** → resolve it in the draft, then run the next round.
- **needs_clarify** → do not fix it yourself; compile it into the `needs_clarify` list (one entry per item, `- **section**: problem — why_it_matters`) for the Clarify phase.
- **false positive / measurement decay / contradiction** → reject with a written reason and record it in a PHR; do not silently ignore.
- **Pass 2 only — Clarify re-check:** before stopping, verify the Clarify answers were folded in without quietly breaking consistency elsewhere in the document. The re-check is yours — the critics never see the answers (the script embeds document + schema only, no cross-document state).

### 4. Stop
- **Pass 1:** stop once every objective issue is resolved and the full `needs_clarify` list is compiled → advance to Clarify.
- **Pass 2:** stop only when every currently-valid critic scores perfect → advance to the Stranger Test. "Currently-valid" = that round's own `critics` array; perfect = `overall_score` 10 (a 10-with-zero-issues is valid and perfect; only a sub-10 score with zero issues is invalid noise). A critic absent from a round (transport/invalid) neither blocks nor satisfies the condition — it participates next round.
- **Asymptote (the common real-world Pass-2 exit):** free-tier panels re-raise. When two consecutive rounds are non-progressing, stop and **escalate to the human** with the full summary — rounds run, issues accepted and applied, issues rejected with their written reasons, and the evidence that what remains is repeats (e.g. an issue list verbatim-identical to a prior round's). Hand the disposition to the human. Recording "converged" yourself, without that summary, is a silent stop: you are the maker, and the maker does not sign off on its own draft (`PLAN.md` §4.1, §4.4).
- **Round cap** (default 25 per pass, configurable; `0` disables): at the cap, escalate the same way — never stop silently.

## Edge cases / rules
- A response with `overall_score < 10` and an empty `issues` list is **noise** (invalid) — the script retries it once; you should not act on it.
- **Pass-1 `testability` is always 0** in the logged round — "not assessed in this pass". Critics frequently score it anyway, so the script normalizes the value rather than rejecting the critique. Do not read a Pass-1 `testability` as a judgement, and do not raise its being 0 as an issue.
- Transport failures (429/5xx/timeout) are retried by the script ≤5 tries with growing backoff (429 → 30s×attempt; 5xx/timeout → 8s×attempt); if a critic still fails it is excluded for that round and logged. A deterministic client error (4xx other than 429) is not retried.
- **Non-progressing rounds:** a round is *progressing* when the document changed in response to it or it surfaced at least one issue triaged as genuinely new and actionable; otherwise it is non-progressing. Track them at session level (your repeated invocations for a document+pass): on the **second consecutive** non-progressing round (no progressing round between them), escalate to the human with a full summary — never loop silently.
- A round with `n_valid == 0` produces no usable signal (the script records it and exits 3 with the escalation note `escalation: round produced no valid critics`) and **never counts as advancement** — for Pass 2 it is neither a perfect round nor a blocker; log it and run the next round.
- On a sub-skill failure (missing doc, bad config), the script exits with a clear error (exit 2); log a PHR and retry once, then escalate if it recurs.
- Log a PHR after every round with the round's result and your adjudication summary.
