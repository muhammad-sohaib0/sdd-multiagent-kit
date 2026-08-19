# ADR 001 — Critique Panel: Replace Retired Qwen Model with DeepSeek

- **Status:** Accepted (human-confirmed)
- **Date:** bootstrap run, pre-milestone
- **Affects:** `kit/config/providers.yaml` (M1), critique-loop automation defaults (M2), all docs and CONTRIBUTING examples (M4)

## Context

`PLAN.md` §4.1 fixes the critic panel at six models from six labs. Provider preflight on 2026-08-15 found `qwen/qwen3-next-80b-a3b-instruct` returns HTTP 410 **Gone** — NVIDIA retired it on 2026-07-27 (end of life). The slot for "Alibaba / Qwen" must be filled by a model that keeps the panel's properties: six distinct labs, all reachable on genuinely free tiers through the same three provider keys, open-weight class.

## Alternatives considered

| Option | Verdict | Reason |
|---|---|---|
| `deepseek-ai/deepseek-v4-flash-0731` (DeepSeek) | **Adopted** | Distinct lab, open-weight, verified reachable and functioning under `NVIDIA_NIM_API_KEY` (HTTP 200) |
| `moonshotai/kimi-k2.6` (Moonshot) | Rejected | Appears in the public model list but returns HTTP 404 "Not found for account" — account-gated, not usable on an ordinary free account |
| `mistralai/mistral-large` (Mistral) | Rejected | Same account-gating 404 |
| `deepseek-ai/deepseek-coder-6.7b-instruct` | Rejected | Code-specialist; unsuitable as a general-purpose critic |
| "Pro"/larger DeepSeek variant | Rejected | No such model exists on NVIDIA NIM under this key — only the two above |
| `stepfun-ai/step-3.7-flash` (StepFun) | Not adopted | Not probed before the decision; set forth here as a possible future contender if DeepSeek develops availability issues |

## Decision

Replace `qwen/qwen3-next-80b-a3b-instruct` with `deepseek-ai/deepseek-v4-flash-0731` in the critic panel. The DeepSeek slot runs on NVIDIA NIM under `NVIDIA_NIM_API_KEY` — the same provider and key as the model it replaces. The panel remains six models, six labs (NVIDIA, OpenAI-grafted via NIM, DeepSeek, Z.ai, Google, MiniMax), three provider keys, one free tier.

## Consequences

- `providers.yaml` (M1) will list the DeepSeek model ID; the kit's documentation (M4) will carry the corrected panel table and this rationale.
- `PLAN.md` §4.1's table is now known-stale for this one row; the shipped kit and its docs carry the correction, and a note is appended to the repo's history trail via this ADR.
- No API-key or tier changes; no change to the retry policy (PHR 003).