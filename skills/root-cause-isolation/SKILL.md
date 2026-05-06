---
id: 21733901-f490-4f5d-b9d3-7dc79b68d697
name: root-cause-isolation
version: 1.2.0
level: tactical
description: 'Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed. Handles 5-step hypothesis-driven debugging, binary search isolation, minimal reproduction, and tactical grep-powered discovery.'
category: engineering
tags:
- debugging
- search
- testing
- engineering
references:
- name: Crowd Control (Source Repo)
  url: https://github.com/newsbubbles/crowd_control
- name: CC — Deglaze (Anti-Sycophancy)
  path: ../logic-deglazing/SKILL.md
- name: CC — Comprehend (Understanding Gate)
  path: ../comprehension-gate/SKILL.md
- name: CC — Anchor (Architectural Coherence)
  path: ../architectural-anchoring/SKILL.md
- name: CC — Circuit (Iteration Breaker)
  path: ../jidoka/SKILL.md
- name: CC — Secure (Security)
  path: ../security-enforcement/SKILL.md
- name: CC — Ship (Production Readiness)
  path: ../release-management/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Test-Driven Development
  path: ../test-driven-development/SKILL.md
---
# Isolate (Root Cause Isolation)

*You are a scientist, not a gambler.*

Gamblers try random things hoping something works. Scientists form hypotheses, test them, and learn from results. Debugging is not about luck — it's about systematically eliminating possibilities until only the truth remains. This skill combines scientific hypothesis-driven isolation with tactical grep-powered discovery.

## Core Mandates

### 1. Reproduce Before Investigating
Before attempting a fix, precisely define the abnormality and establish a deterministic reproduction path.
- **Action:** Output a "Symptom Report" (Expectation vs. Reality) and a minimal reproduction command (e.g., a failing test).
- **Constraint:** NEVER start "guessing" at a fix before the bug is reproduced. The bug reproduction IS the `[Red]` TDD phase.
- **Integration:** Implements **Genchi Genbutsu** (Go and See).

### 2. Grep-First Discovery
- **Action:** Start with the error message or symptom string. Grep for the exact string to find where it's emitted. Then grep for all callers and callees of the suspected code path.
- **Constraint:** Do not read entire files. Use grep to find the relevant sections first, then read only those sections with line bounds.
- **Integration:** Ensures you go to the actual source of the problem, not a guess.

### 3. Surgical Inspection
- **Action:** Read only the relevant sections of files using start and end line numbers. Never open a large file without first identifying the target section via grep.
- **Constraint:** If a file needs to be read entirely to understand the bug, it is a sign the code needs better decomposition — note it as a Kaizen finding.
- **Integration:** Supports **Heijunka** token efficiency.

### 4. Hypothesis-Driven Isolation
Systematically eliminate possibilities using the "Single Variable Rule" and binary search.
- **Action:** Form a single, testable hypothesis and change only one variable at a time.
- **Constraint:** Do not apply multiple changes simultaneously. One change, one observation.
- **Integration:** This is a diagnostic **Poka-yoke** — it prevents the "Gambler's Fallacy."

### 5. Evidence-Based Conclusion
Verify the fix with empirical evidence that specifically addresses the reproduction path.
- **Action:** Run the reproduction script to confirm the fix and run the full test suite to ensure no regressions.
- **Constraint:** "It works now" is not an acceptable status. You MUST explain *why* it now works and *how* the fix addressed the root cause.
- **Integration:** Feeds into **Hansei** to reflect on why the bug was introduced.

### 6. Automated Binary Isolation
For complex isolations (e.g., finding a breaking line in a large file), leverage deterministic binary search tools if available.
- **Action:** Execute binary search over the symptom space (commits or lines).
- **Constraint:** Use only when a clear binary working/broken boundary can be evaluated.

## Escalation & Halting

- **Jidoka:** If 3+ hypotheses fail or if a fix attempt introduces a regression, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if the bug is rooted in an architectural contradiction (an Anchor conflict) that requires a strategic decision.

## Implementation Workflow (The 5-Step Protocol)

1. **Define** — Precisely define the symptom (Expectation vs. Reality).
2. **Locate** — Grep for error strings and trace call paths to locate the boundary (working → broken).
3. **Hypothesize** — Form one testable hypothesis about the root cause.
4. **Test** — Create a minimal reproduction (Failing Test) and test the hypothesis with a minimal change.
5. **Interpret** — Verify with evidence. Confirm the reproducing test passes and no regressions exist.

## Quick Reference

```
ISOLATE PROTOCOL:
1. DEFINE symptom precisely
2. LOCATE boundary (Grep + Trace)
3. HYPOTHESIZE one cause
4. TEST with minimal change (Red/Green)
5. INTERPRET with evidence

SINGLE VARIABLE RULE:
- Change ONE thing -> Test -> Repeat
```


