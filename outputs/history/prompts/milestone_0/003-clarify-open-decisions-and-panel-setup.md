# PHR 003 — Clarify (Open Decisions) + Provider Preflight & Panel Lock

- **Phase:** Clarify (PLAN.md §13, seed §11.4d) + provider preflight
- **Input:** PLAN.md §12 open decisions; actual provider reachability
- **Date:** bootstrap run, session start

## What was requested

1. Resolve the open decisions in PLAN.md §12 before milestone drafting.
2. Verify all six panel models are actually reachable on the free tiers before relying on any critique loop.

## What was produced

### Open decisions — confirmed (human)

| §12 item | Decision |
|---|---|
| npm package / repo name | `sdd-multiagent-kit` (as assumed) |
| In-tool trigger command | `/sdd` (as assumed) |
| License | MIT (as assumed) |
| "Guide for Pakistani users" content | **Reserved slot only**; content supplied by maintainer separately |
| Critic panel keys | User has all three keys (`NVIDIA_NIM_API_KEY`, `GOOGLE_AISTUDIO_API_KEY`, `OLLAMA_API_KEY`); set via `.env` |

### Provider preflight — findings

All three providers reached with the plan's model IDs except one. Full status:
- `nvidia/nemotron-3-ultra-550b-a55b` — reachable (one transient HTTP 503 cold-start observed)
- `openai/gpt-oss-120b` — reachable (earlier blank was transient; confirmed HTTP 200)
- `z-ai/glm-5.2` — reachable (HTTP 200)
- `qwen/qwen3-next-80b-a3b-instruct` — **HTTP 410 Gone, EOL 2026-07-27** → replaced (ADR-001)
- `gemini-3.6-flash` — reachable (Google AI Studio) (HTTP 200)
- `minimax-m3:cloud` — reachable (Ollama Cloud) (HTTP 200)

Account-gated / unusable candidates checked and excluded: `moonshotai/kimi-k2.6`, `mistralai/mistral-large` (404). `nvidia/nemotron-3-ultra-550b-a55b` remains the plan's #1 slot.

### Decision: transport-error retry policy (a plan gap, now explicit)

PLAN.md §4.3 specifies one retry for an unparseable response, but is silent on transport failures (timeout / 5xx / 429). Policy adopted for this run and to be formalized in the M2 orchestration spec:
- Successful HTTP response that fails schema parsing → **2 tries** (initial + one retry per §4.3), then critic excluded for the round.
- Transport failure (timeout / 5xx / 429) → **3 tries** total with short backoff and rate-limit honoring, then the critic is skipped for the round, logged.
- Three consecutive-round failures of any kind → non-cooperative flag (§4.4).

## Rationale

None of the critique loop's claims can be trusted until the six voices are proven reachable on the real free tiers; this preflight makes that explicit rather than assumed. The EOL finding and transport policy are logged because they change what the shipped kit must configure and how it must behave — both are absorbed into M1 (`providers.yaml` carries the corrected model IDs) and M2 (translator + loop spec carries the retry/backoff policy).