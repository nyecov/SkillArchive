---
name: genchi-genbutsu
version: 1.1.0
level: methodology
description: Use to "Go and See for Yourself." Mandates empirical verification of all hypotheses and findings through direct execution and testing.
category: methodology
tags:
- methodology
- research
- testing
- lean
- TPS
references:
- name: Gemba (The Real Place)
  path: ../gemba/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
---

# Genchi Genbutsu

Genchi Genbutsu means going to the source to find the facts. For an AI agent, this means **Dynamic Verification**. Don't just "think" the code works — run the code and see for yourself.

## Core Mandates

### 1. Dynamic Verification
- **Action:** Before claiming a bug is fixed or a feature is complete, the agent MUST run the code or a test that specifically targets the behavior.
- **Constraint:** NEVER say "the code should now work" without having observed a successful execution or test run. Claims of verification MUST be accompanied by raw console logs, screenshots, or code diffs (via `render_diffs`).
- **Integration:** Directly supports **Poka-yoke** by providing the proof of "Proofing." Use **Gemba** to observe the static state of the codebase before and after execution.

### 2. Fact-Based Decision Making
- **Action:** If a tool output is ambiguous, the agent MUST "Go and See" by adding logging, running a debugger, or using more specific search patterns to gather the *facts*.
- **Constraint:** Do not make architectural decisions based on "likely" scenarios. Find the evidence first. Hearsay is treated as a policy violation.
- **Integration:** Feeds into **Hansei** during the validation phase of the lifecycle.

## Escalation & Halting

- **Jidoka:** If empirical evidence contradicts the "Strategy," halt and re-evaluate the plan at the "Gemba."
- **Hō-Ren-Sō:** Share the *raw output* of the validation (logs/screenshots) with the user to support your conclusions.

## Implementation Workflow

1. **Trigger:** A hypothesis is formed, a code change is applied, or a verification step is reached in another skill.
2. **Execute:** 
   - Run reproduction commands (for bugs).
   - Run test suites (for features).
   - Capture raw logs or snapshots of system state.
3. **Verify:** Confirm that the "Real" behavior matches "Expected". Ensure evidence capture is complete and unambiguous.
4. **Output:** A verified status report that MUST include the raw evidence block (logs, screenshots, or `render_diffs`). Do not deliver the report if the evidence is missing.
