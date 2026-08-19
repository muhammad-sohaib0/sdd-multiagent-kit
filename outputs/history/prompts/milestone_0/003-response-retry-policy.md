# PHR 003 — Response-Retry Policy (DECISION)

- **Phase:** Research — critique engine mechanism (PLAN.md §4.3–4.4)
- **Input:** provider preflight results (nemotron cold-start 503; gpt-oss transient HTTP 000)
- **Date:** bootstrap run, pre-milestone

## What was requested

Determine how many attempts each critic model gets per round, given that providers on the free tier demonstrably cold-start or fail transiently (observed: one 503, one dropped connection during preflight).

## What was decided

| Failure class | Policy |
|---|---|
| Transport errors (HTTP 5xx, 000/timeout, connection drop, DNS) | Up to **3 total attempts** per model per round (initial + 2 retries), exponential backoff between attempts |
| Rate limiting (HTTP 429) | Treated as transport; same 3-attempt budget, longer backoff |
| Unparseable critique response (§4.3) | **1 retry** with the schema error shown to the model |
| Still failing after the full budget | Critic excluded from that round only, logged in `critique-log/` and the round PHR |
| Invalid 3 rounds in a row | Flagged non-cooperative for the session (§4.4); loop continues with remaining valid critics |

## Rationale

The one-retry rule in PLAN.md §4.3 exists for a different purpose — it is about models not producing the schema shape, which is the model's fault. Free-tier infrastructure failures are not the model's fault and deserve a separate, more generous budget so a cold start does not silently shrink the panel. The cap stays bounded (3 attempts) so a permanently broken model costs at most 3 wasted calls per round, then is excluded without stalling anyone. This policy will be encoded in `kit/scripts/orchestrate_critique_loop.py` (M2) as the retry contract.