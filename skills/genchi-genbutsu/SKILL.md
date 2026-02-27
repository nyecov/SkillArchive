---
name: genchi-genbutsu
version: 1.0.0
description: 'Use to "Go and See for Yourself." Mandates empirical verification of
  all hypotheses  and findings through direct execution and testing.

  '
category: methodology
tags:
- methodology
- research
- testing
references:
- name: Gemba (The Real Place)
  path: ../gemba/SKILL.md
- name: Poka-Yoke (Mistake Proofing)
  path: ../poka-yoke/SKILL.md
level: methodology
---

# Genchi Genbutsu (Dynamic Verification)

Genchi Genbutsu means going to the source to find the facts. For an AI agent, this means **Dynamic Verification**. Don't just "think" the code works — run the code and see for yourself.

## Core Mandates

### 1. Dynamic Verification
- **Action:** Before claiming a bug is fixed or a feature is complete, the agent MUST run the code or a test that specifically targets the behavior.
- **Constraint:** NEVER say "the code should now work" without having observed a successful execution or test run.
- **Integration:** Directly supports **Poka-Yoke** by providing the proof of "Proofing." Use **Gemba** to observe the static state of the codebase before and after execution.

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
