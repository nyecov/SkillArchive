---
name: deglaze-tactics
version: 1.1.0
description: Use when reviewing AI-generated solutions, validating user comprehension, or stress-testing proposals. Handles 5 constraint-pressure techniques to generate a formal Deglaze Pressure Report.
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

Deglaze provides the **Tactical Toolkit** for combating "glaze" — the false sense of understanding that forms when AI-generated solutions look clean but the substrate is weak. This skill provides specific **constraint pressure** techniques to force ideas into hard, verifiable edges, culminating in a formal reporting artifact.

## Core Mandates

### 1. Constraint Pressure (The 5 Techniques)
Combats "glaze" by applying five standardized pressure tests to generate the mandatory `Deglaze Pressure Report`.
- **Action:** Before accepting an AI-generated solution, challenge the user/system to populate the 5 tests: Compression, Deletion, Adversary, Explain-to-Junior, and Rollback.
- **Constraint:** NEVER accept a solution that is "too polished" to explain or defend. The report MUST be written to code.
- **Integration:** This is a tactical **Poka-yoke** designed to expose **Muda (Waste)** in reasoning. It fulfills the formal verification requirements of the **CC — Comprehend** policy gate.

### 2. Socratic Verification
Shift the burden of proof to the user by asking questions that force the externalization of their mental model.
- **Action:** Ask "What happens if we remove X?" or "How would an adversary break this?".
- **Constraint:** Do not provide the answers. The goal is to verify the *user's* understanding, not the model's.

### 3. Gap Identification
Identify "glaze" by watching for red flags like jargon, vague gestures, or "The AI handled it" responses.
- **Action:** If the user cannot populate the `Deglaze Pressure Report` with concrete answers, flag it as a critical risk.
- **Constraint:** Do not proceed with implementation if the solution cannot survive the Deglaze protocol.

## Escalation & Halting

- **Jidoka:** If a solution fails to produce coherent answers for the Deglaze tests, trigger a Jidoka halt to perform a deep-dive review.
- **Hō-Ren-Sō:** Use Sōdan (Consult) to report the specific gaps revealed by the pressure tests and propose a simpler alternative.

## Implementation Workflow

1. **Trigger:** A new solution is proposed, or AI-generated code is accepted, requiring formal comprehension verification.
2. **Execute:** Apply the five constraint pressure techniques (Compression, Deletion, Adversary, Explain-to-Junior, Rollback).
3. **Verify:** Confirm the user or the AI explicitly defends the solution against all five tests with concrete reasoning.
4. **Output:** The agent MUST output the following `Deglaze Pressure Report` markdown template to formally clear the verification gate.

```markdown
### Deglaze Pressure Report
- **[COMPRESSION TEST]:**
  - `[Can the core mechanism be explained in one clear sentence?]`
- **[DELETION TEST]:**
  - `[What 20% of the code/logic can be removed without breaking the core value?]`
- **[ADVERSARY TEST]:**
  - `[How would a malicious actor or severe edge case break this?]`
- **[EXPLAIN-TO-JUNIOR TEST]:**
  - `[Explain the most complex part using only common terminology.]`
- **[ROLLBACK TEST]:**
  - `[What is the exact, step-by-step procedure to undo this implementation?]`
```
