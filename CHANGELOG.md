# Changelog

All notable changes to the SDD Multi-Agent Kit are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] — 2026-08-18

Initial release.

### Added

- Master skill (`kit/SKILL.md`) with the `/sdd` trigger and eleven sub-skills (`kit/skills/*`).
- Adopted constitution (`kit/constitution.template.md`).
- Locked seven-model critic panel (`kit/config/providers.yaml`): `nvidia/nemotron-3-ultra-550b-a55b`, `openai/gpt-oss-120b`, `z-ai/glm-5.2`, `mistralai/mistral-nemotron`, `meta/muse-glimmer-30b` on NVIDIA NIM, `gemini-3.6-flash` on Google AI Studio, `minimax-m3:cloud` on Ollama Cloud (ADR-001, ADR-003).
- Critique engine (`kit/scripts/orchestrate_critique_loop.py`) and validator (`kit/scripts/validate_critique.py`), zero runtime dependencies.
- Engine hardening: per-model `timeout` keys in `providers.yaml`; transport retry ≤5 tries with adaptive backoff (429 → 30s × attempt, others → 8s × attempt); deterministic non-429 4xx break immediately; 200-with-non-JSON treated as transport failure; first-call stagger `(slot_index-1) × 4s`; CLI validation of `--round`, `--round-cap`, `--timeout` (exit 2); no cross-round critic exclusion — a failed critic participates again next round and `n_valid == 0` never counts as advancement; `providers.yaml` read fresh per invocation.
- Installer (`bin/setup-wizard.js`, bin `sdd-setup`) with adapters for Claude Code, Claude Desktop, OpenCode, and Antigravity.
- Distribution docs: `README`, `CLAUDE`, `AGENTS`, `CONTRIBUTING`, `SECURITY`, `SUPPORT`, and `docs/` (GUIDE, ARCHITECTURE, BOOTSTRAP).
- Example project under `examples/`.
- Bootstrap history under `outputs/` (specs, critique logs, PHRs, ADRs), with the raw critique evidence kept versioned (ADR-002).