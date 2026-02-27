---
name: cc-circuit-iteration-breaker
version: 1.0.0
description: >
  Use when the same bug persists after 3+ attempts, regressions match fixes, or time spent exceeds the iteration budget.
  Handles circuit breaker triggers, Stop/Revert/Restart decisions, and iteration budgets.
category: agent-safety
tags: [circuit, iteration-breaker, halt, budget, sunk-cost, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ../cc-deglaze-anti-sycophancy/SKILL.md
  - name: CC — Comprehend (Understanding Gate)
    path: ../cc-comprehend-understanding/SKILL.md
  - name: CC — Anchor (Architectural Coherence)
    path: ../cc-anchor-coherence/SKILL.md
  - name: CC — Isolate (Systematic Debugging)
    path: ../cc-isolate-debugging/SKILL.md
  - name: CC — Secure (Security)
    path: ../cc-secure-security/SKILL.md
  - name: CC — Ship (Production Readiness)
    path: ../cc-ship-production/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
---

# Circuit: The Iteration Breaker

*Stopping feels like failure. It's not. It's the only way to avoid actual failure.*

The user is caught in a dopamine loop: prompt, hope, disappointment, prompt again. Using AI to fix AI-introduced bugs is "paying off credit card debt with another credit card." The debt compounds. This skill breaks the loop before the codebase becomes unsalvageable.

## Core Mandates

### 1. Trigger Conditions
The circuit breaker trips when any of these thresholds are met:

| Condition | Threshold |
|-----------|----------|
| Consecutive failed fixes | 3+ attempts at same bug |
| Regression rate | New bugs equal or exceed fixes |
| Comprehension loss | User can't explain recent changes |
| Time spiral | 2+ hours on single issue |
| Scope explosion | Fix requires touching 5+ files |

- **Integration:** This is a user-facing complement to the **Jidoka** autonomous halt — while Jidoka halts on system abnormalities, Circuit halts on human-workflow abnormalities.

### 2. The Three Options
When the circuit trips, there are only three valid responses:

**Option 1: STOP** — Walk away, return with fresh eyes. Use when fatigue is the problem, not the code.

**Option 2: REVERT** — Go back to last known good state. The approach is wrong, but the goal is clear.

**Option 3: RESTART** — Start fresh with lessons learned. The codebase is beyond repair. More common than you'd think.

### 3. Iteration Budgets
Before starting any task, set an explicit budget:

| Task Type | Budget |
|-----------|--------|
| Bug fix | 3–5 prompts |
| Simple feature | 5–10 prompts |
| Complex feature | 15–25 prompts |

Over budget = wrong approach. Reassess.

## The Restart Calculation

| Scenario | Time to Fix | Time to Restart |
|----------|-------------|----------------|
| 50 prompts of accumulated bugs | 50+ more prompts | 20 prompts (with lessons learned) |
| Tangled auth system | Days of debugging | Hours of clean implementation |
| Mixed architectural patterns | Endless refactoring | Fresh start with anchors |

**The rule:** If you can't explain the current state, restart is probably faster.

## Anti-Patterns to Watch

- **"Just One More Fix"** — The most dangerous phrase. If you've said it three times, the circuit should trip.
- **"The AI Will Figure It Out"** — The debt compounds.
- **"I'm So Close"** — You're probably not. The feeling of being close is often the spiral tightening.
- **"I Can't Lose This Progress"** — The progress was learning what doesn't work. The code is not the progress.

## Implementation Workflow

1. **Budget:** Set an iteration budget before starting the task.
2. **Monitor:** Track attempts, regressions, and time against thresholds.
3. **Trip:** When a threshold is hit, stop all work and present the three options.
4. **Decide:** User chooses Stop, Revert, or Restart.
5. **Act:** Execute the chosen path cleanly — no hybrid "partial revert."

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
