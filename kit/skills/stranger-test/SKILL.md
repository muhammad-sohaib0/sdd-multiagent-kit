---
name: stranger-test
description: >-
  Verification sub-skill. Hands the finished five-document set to a fresh,
  zero-context AI session with a single instruction — implement this, ask no
  questions — and checks contract parity. A failure is fed back as a new loop
  issue. This is the one rule the loop may not reason its way around.
version: 0.1.0
---

# Stranger Test — Prove the Documents, Not the Agreement

Verify the finished milestone's full five-document set against a fresh, zero-context session.

## Input
- The finished five-document set: `spec`, `plan`, `tasks`, `workflow`, `tests` for the milestone (together, never any one file alone).

## Output
- A verification result (pass/fail), or a **new loop issue** on failure.

## Procedure
1. Hand the full set to a fresh, zero-context AI session with a single instruction: implement this, ask no questions.
2. Compare what it independently derives against the contract the documents actually specify — e.g. the exact deliverable file inventory, the exact ordered critic panel, the constitution articles, and the phase order.
3. If it builds the right thing, the documents are genuinely clear → pass.
4. If it diverges, that failure becomes a new issue fed back into the loop.

## Edge cases / rules
- Agreement among critics is **not** proof of correctness (measurement decay) — this test exists precisely because critics can share a blind spot.
- **A failure may not be reasoned away.** It is re-entered into the loop; re-entry is bounded by the same round safety cap, at which the master escalates to the human.
- Runs against the full five-document set together, never a single file alone.