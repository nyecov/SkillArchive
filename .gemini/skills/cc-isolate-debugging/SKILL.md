---
name: cc-isolate-debugging
version: 1.0.0
description: >
  Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed.
  Handles 5-step hypothesis-driven debugging, binary search isolation, minimal reproduction, and single-variable testing.
category: engineering-standards
tags: [isolate, debugging, systematic, hypothesis, single-variable, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ../cc-deglaze-anti-sycophancy/SKILL.md
  - name: CC — Comprehend (Understanding Gate)
    path: ../cc-comprehend-understanding/SKILL.md
  - name: CC — Anchor (Architectural Coherence)
    path: ../cc-anchor-coherence/SKILL.md
  - name: CC — Circuit (Iteration Breaker)
    path: ../cc-circuit-iteration-breaker/SKILL.md
  - name: CC — Secure (Security)
    path: ../cc-secure-security/SKILL.md
  - name: CC — Ship (Production Readiness)
    path: ../cc-ship-production/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: KYT (Hazard Prediction)
    path: ../kyt-hazard-prediction/SKILL.md
---

# Isolate: Systematic Debugging

*You are a scientist, not a gambler.*

Gamblers try random things hoping something works. Scientists form hypotheses, test them, and learn from results. Debugging is not about luck — it's about systematically eliminating possibilities until only the truth remains.

## Core Mandates

### 1. Symptom Definition
Before attempting a fix, precisely define the abnormality and establish a deterministic reproduction path.
- **Action:** Output a "Symptom Report" (Expectation vs. Reality) and a minimal reproduction command.
- **Constraint:** NEVER start "guessing" at a fix before the bug is reproduced.
- **Integration:** Directly supports **Genchi Genbutsu** (Go and See).

### 2. Hypothesis-Driven Isolation
Systematically eliminate possibilities using the "Single Variable Rule" and binary search.
- **Action:** Form a single, testable hypothesis and change only one variable at a time.
- **Constraint:** Do not apply multiple changes simultaneously. One change, one observation.
- **Integration:** This is a diagnostic **Poka-yoke** — it prevents the "Gambler's Fallacy" in debugging.

### 3. Evidence-Based Conclusion
Verify the fix with empirical evidence that specifically addresses the reproduction path.
- **Action:** Run the reproduction script to confirm the fix and run the full test suite to ensure no regressions.
- **Constraint:** "It works now" is not an acceptable status. You MUST explain *why* it now works and *how* the fix addressed the root cause.
- **Integration:** Feeds into **Hansei** to reflect on why the bug was introduced.

## Escalation & Halting

- **Jidoka:** If 3+ hypotheses fail or if a fix attempt introduces a regression, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if the bug is rooted in an architectural contradiction (an Anchor conflict) that requires a strategic decision.

## Implementation Workflow

1. **Trigger:** A bug is reported or a test fails.
2. **Execute:** Follow the 5-step protocol (Define -> Locate -> Hypothesize -> Test -> Interpret).
3. **Verify:** Confirm the reproduction script passes and no regressions exist.
4. **Output:** A verified fix and a root-cause analysis report.

## The Isolation Toolkit

### Automated Binary Search
For complex isolations (e.g., finding a breaking line in a large file or a breaking commit), use the provided deterministic runner:
- **Tool**: `./scripts/binary_search_runner.py`
- **Usage**: `python ./scripts/binary_search_runner.py "test_command {item}" item1 item2 ...`

## Quick Reference

```
ISOLATE PROTOCOL:
1. DEFINE symptom precisely
2. LOCATE boundary (working → broken)
3. HYPOTHESIZE one cause
4. TEST with minimal change
5. INTERPRET with evidence

SINGLE VARIABLE RULE:
- Change ONE thing
- Test
- Then change the next thing
- Never change multiple things

QUESTIONS BEFORE FIXING:
□ Can you reproduce it?
□ Where is the boundary?
□ What's your hypothesis?
□ How will you test it?
□ What evidence will confirm/reject?
```
