---
name: genchi-genbutsu
version: 1.0.0
description: >
  Use to "Go and See for Yourself." Mandates empirical verification of all hypotheses 
  and findings through direct execution and testing.
category: lean-principles
tags: [genchi-genbutsu, verification, facts, testing, lean]
references:
  - name: Gemba (The Real Place)
    path: ../gemba/SKILL.md
  - name: Poka-Yoke (Mistake Proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
---

# Genchi Genbutsu (Go and See)

Genchi Genbutsu means going to the source to find the facts to make correct decisions. For an AI agent, this means **empirical validation**. Don't just "think" the code works or "think" a bug exists—run the code and see for yourself.

## Core Mandates

### 1. Empirical Validation
- **Action:** Before claiming a bug is fixed, the agent MUST run a reproduction script or an automated test that specifically targeted the failure.
- **Constraint:** NEVER say "the code should now work" without having observed a successful execution or test run.
- **Integration:** Directly supports **Poka-Yoke** by providing the proof of "Proofing."

### 2. Fact-Based Decision Making
- **Action:** If a tool output is ambiguous, the agent MUST "Go and See" by adding logging, running a debugger, or using more specific search patterns to gather the *facts*.
- **Constraint:** Do not make architectural decisions based on "likely" scenarios. Find the evidence first.
- **Integration:** Feeds into **Hansei** during the validation phase of the lifecycle.

## Escalation & Halting

- **Jidoka:** If empirical evidence contradicts the "Strategy," halt and re-evaluate the plan at the "Gemba."
- **Hō-Ren-Sō:** Share the *raw output* of the validation (the "See" part) with the user to support your conclusions.

## Implementation Workflow

1. **Trigger:** A hypothesis is formed or a change is applied.
2. **Execute:** 
   - Run a reproduction command (for bugs).
   - Run a test suite (for features).
   - Check logs/output for specific "Fact" markers.
3. **Verify:** The "Real" behavior matches the "Expected" behavior.
4. **Output:** A verified status report backed by empirical evidence.
