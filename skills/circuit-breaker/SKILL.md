---
name: circuit-breaker
version: 1.0.0
description: >
  Use when the same bug persists after 3+ attempts, regressions match fixes, or time spent exceeds the iteration budget.
  Handles circuit breaker triggers, Stop/Revert/Restart decisions, and iteration budgets.
category: safety
tags: [circuit, iteration-breaker, halt, budget, sunk-cost, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ../deglaze-tactics/SKILL.md
  - name: CC — Comprehend (Understanding Gate)
    path: ../comprehend-understanding/SKILL.md
  - name: CC — Anchor (Architectural Coherence)
    path: ../anchor-coherence/SKILL.md
  - name: CC — Isolate (Systematic Debugging)
    path: ../isolate-debugging/SKILL.md
  - name: CC — Secure (Security)
    path: ../secure-security/SKILL.md
  - name: CC — Ship (Production Readiness)
    path: ../ship-production/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka/SKILL.md
---

# Circuit: The Iteration Breaker

*Stopping feels like failure. It's not. It's the only way to avoid actual failure.*

The user is caught in a dopamine loop: prompt, hope, disappointment, prompt again. Using AI to fix AI-introduced bugs is "paying off credit card debt with another credit card." The debt compounds. This skill breaks the loop before the codebase becomes unsalvageable.

## Core Mandates

### 1. Threshold Monitoring
Track and enforce strict iteration thresholds to prevent the "Dopamine-Sunk-Cost Spiral."
- **Action:** Before starting a task, set an iteration budget (e.g., 3-5 prompts for a bug fix).
- **Constraint:** NEVER exceed the budget without a formal "Strategic Re-Pivot" and user consultation.
- **Integration:** Acts as a higher-level workflow monitor for **Shisa Kanko** execution loops.

### 2. Standardized Responses
When a threshold is hit, the circuit MUST trip, and only three responses are permitted: Stop, Revert, or Restart.
- **Action:** Present the user with the three options (Stop, Revert, Restart) and the rationale for the trip.
- **Constraint:** Do not suggest "just one more fix" once the circuit has tripped.
- **Integration:** Connects to **Hansei** to identify why the iteration budget was exhausted.

### 3. Regression Enforcement
Stop work if the rate of new bugs introduced equals or exceeds the rate of fixes.
- **Action:** Audit the workspace for new linting errors or test failures after every 3 iterations.
- **Constraint:** If the debt is compounding, trigger an immediate halt.
- **Integration:** Uses **Jidoka** for the technical halt and **Circuit** for the workflow halt.

## Escalation & Halting

- **Jidoka:** This skill triggers a Jidoka halt when iteration budgets are exhausted or regression rates spike.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to present the Stop/Revert/Restart options to the user.

## Implementation Workflow

1. **Trigger:** An iteration budget is set or a repeated failure is detected.
2. **Execute:** Track attempts, regressions, and time against thresholds.
3. **Verify:** When a threshold is hit, stop and signal the "Red Light" status.
4. **Output:** A user-selected decision (Stop, Revert, or Restart) and a clean state.

## Quick Reference

```
CIRCUIT BREAKER TRIGGERS:
□ 3+ failed attempts at same bug?
□ New bugs ≥ fixed bugs?
□ User can't explain recent changes?
□ 2+ hours on single issue?
□ Fix requires 5+ file changes?

IF TRIGGERED:
1. STOP  - Walk away, return fresh
2. REVERT - Go back to last good state
3. RESTART - Burn it down, apply lessons

ITERATION BUDGET:
- Bug fix: 3-5 prompts
- Simple feature: 5-10 prompts
- Complex feature: 15-25 prompts
- Over budget = wrong approach
```
