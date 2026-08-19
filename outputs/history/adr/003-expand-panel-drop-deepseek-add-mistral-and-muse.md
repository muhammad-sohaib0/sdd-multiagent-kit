# ADR-003 — Expand critic panel: drop DeepSeek, add Mistral-Nemotron and Muse-Glimmer-30B

**Date:** 2026-08-15
**Status:** Accepted (maintainer directive)
**Supersedes:** the DeepSeek slot of ADR-001 (the panel composition it records)

## Context

The critique panel ran seven models but one slot — `deepseek-ai/deepseek-v4-flash-0731` on NVIDIA NIM — was the round's constant slow point (HTTP 504 chains, hard-deadline timeouts up to 420s per attempt) and its critiques were largely re-raises of earlier rounds. The maintainer directed: remove DeepSeek, add two NVIDIA NIM voices in its place — `mistralai/mistral-nemotron` and `meta/muse-glimmer-30b` — and stop the 429 bursts that hit when all critics fire concurrently.

## Decision

1. Remove `deepseek-ai/deepseek-v4-flash-0731` from `critic_slots` and the `nvidia-nim` model list.
2. Add `mistralai/mistral-nemotron` and `meta/muse-glimmer-30b` (both verified live on the NVIDIA NIM free tier on 2026-08-15) to the `nvidia-nim` model list and as slots. The panel is now **seven slots** — one more than the PLAN.md §4.1 "six" baseline, per maintainer directive. The engine is config-driven (M2 AC-2), so panel size is configuration, not code.
3. **429 mitigation:** the engine now staggers each critic's first call (`(index-1) × 2s`) so concurrent starts never align on a per-key, per-minute rate limit, and 429 backoff is adaptive (`30 × attempt` seconds). Combined with the existing per-model hard deadlines, this clears most transient quota bursts within a round.
4. Existing 429/504/parse retries (≤3 tries per round, no cross-round exclusion) are unchanged.

## Consequences

- Rounds now run five NIM critics concurrently; the stagger (max 12s) plus per-model timeouts keeps rounds bounded by the slowest *reachable* critic instead of a persistently 504-ing one.
- Panel labs: NVIDIA (nemotron-ultra, gpt-oss, glm-5.2, mistral-nemotron, muse-glimmer-30b), Google (gemini), MiniMax (minimax) — two provider keys are now NVIDIA NIM models; lab diversity is reduced vs. the six-lab baseline, accepted as the maintainer's explicit choice.
- ADR-001's historical record remains; its DeepSeek slot is superseded by this ADR.