---
name: deglaze-tactics
version: 1.0.0
description: 'Use when reviewing AI-generated solutions, validating user comprehension,
  or stress-testing proposals. Handles 5 constraint-pressure techniques: Compression,
  Deletion, Adversary, Explain-to-Junior, and Rollback tests.\'
category: cognition
tags:
- cognition
- safety
- methodology
references:
- name: Crowd Control (Source Repo)
  url: https://github.com/newsbubbles/crowd_control
- name: CC — Comprehend (Understanding Gate)
  path: ../comprehend-understanding/SKILL.md
- name: CC — Anchor (Architectural Coherence)
  path: ../anchor-coherence/SKILL.md
- name: CC — Circuit (Iteration Breaker)
  path: ../jidoka/SKILL.md
- name: CC — Isolate (Systematic Debugging)
  path: ../isolate-debugging/SKILL.md
- name: CC — Secure (Security)
  path: ../secure-security/SKILL.md
- name: CC — Ship (Production Readiness)
  path: ../ship-production/SKILL.md
- name: Hansei (Self-reflection)
  path: ../hansei/SKILL.md
level: tactical
---

# Deglaze

*Strip the polish. Reveal the substrate.*

Deglaze provides the **Tactical Toolkit** for combating "glaze" — the false sense of understanding that forms when AI-generated solutions look clean but the substrate is weak. This skill provides specific **constraint pressure** techniques to force ideas into hard, verifiable edges.

## Core Mandates

### 1. Constraint Pressure (The 5 Techniques)
Combats "glaze" (the false sense of understanding) by applying five standardized pressure techniques: Compression, Deletion, Adversary, Explain-to-Junior, and Rollback.
- **Action:** Before accepting an AI-generated solution, challenge it with at least two pressure techniques.
- **Constraint:** NEVER accept a solution that is "too polished" to explain or defend.
- **Integration:** This is a tactical **Poka-yoke** designed to expose **Muda (Waste)** in reasoning. It fulfills the verification requirements of the **CC — Comprehend** policy gate.

### 2. Socratic Verification
Shift the burden of proof to the user by asking questions that force the externalization of their mental model.
- **Action:** Ask "What happens if we remove X?" or "How would an adversary break this?".
- **Constraint:** Do not provide the answers. The goal is to verify the *user's* understanding, not the model's.
- **Integration:** Directly supports the **Comprehend** understanding gate.

### 3. Gap Identification
Identify "glaze" by watching for red flags like jargon, vague gestures, or "The AI handled it" responses.
- **Action:** Flag any 3+ unchecked boxes in the Deglaze checklist as a critical risk.
- **Constraint:** Do not proceed with implementation if the solution cannot survive the Deglaze protocol.
- **Integration:** Feeds into **Hansei** to reflect on why a solution was accepted without deep understanding.

## Escalation & Halting

- **Jidoka:** If a solution fails 3+ Deglaze tests, trigger a Jidoka halt to perform a deep-dive review.
- **Hō-Ren-Sō:** Use Sōdan (Consult) to report the specific gaps revealed by the pressure tests and propose a simpler alternative.

## Implementation Workflow

1. **Trigger:** A new solution is proposed or AI-generated code is accepted.
2. **Execute:** Apply the five pressure techniques in sequence.
3. **Verify:** Confirm the user can defend the solution against all five tests.
4. **Output:** A de-glazed, robust implementation plan and a user with a verified mental model.

## Quick Reference

```
DEGLAZE CHECKLIST:
□ Can user explain it in one sentence?
□ Can user identify what to delete?
□ Can user describe how to break it?
□ Can user explain it to a newcomer?
□ Can user describe the rollback plan?

If 3+ boxes are unchecked → deeper review needed
```
