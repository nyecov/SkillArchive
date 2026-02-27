---
name: hansei
version: 1.1.0
description: Use when a plan fails, a bug is found, or a post-mortem is needed. Mandates
  5-Whys root-cause analysis.
category: cognition
tags:
- cognition
- methodology
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Jidoka (Autonomation)
  path: ../jidoka/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Hō-Ren-Sō (Communication)
  path: ../ho-ren-so/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
level: methodology
---

# Hansei: Agentic Self-Reflection

Hansei is the practice of looking back at a plan or action with a critical, objective eye to identify flaws, acknowledge mistakes, and develop improvement plans. In an agentic system, it serves as the cognitive engine for both proactive refinement and reactive debugging.

## Core Mandates

### 1. Proactive Reflection (The Plan Critique)
Before finalizing a plan, perform a critical review of the proposed reasoning to identify subtle flaws.
- **Action:** Formulate three distinct ways the current plan could fail or introduce architectural rot.
- **Constraint:** NEVER accept the first draft of a complex plan without a formal Hansei pass.
- **Integration:** The findings feed directly into **KYT (Hazard Prediction)** to establish countermeasures.

### 2. Reactive Root Cause Analysis (The 5-Whys)
When an execution fails or a Jidoka halt occurs, the agent MUST use the **5-Whys Protocol** to drill down to the fundamental cause.
- **Action:** Ask "Why?" sequentially at least 5 times (or until the bedrock cause is reached).
- **Format:**
  1. Why did X happen? (Direct cause)
  2. Why did [1] happen? (Indirect cause)
  3. Why did [2] happen? (Systemic cause)
  4. Why did [3] happen? (Architectural cause)
  5. Why did [4] happen? (Root cause)
- **Constraint:** DO NOT settle for "User error" or "AI hallucination" as a root cause. Find the missing context, ambiguous prompt, or structural flaw that allowed the error.
- **Integration:** Directly supports the **Jidoka** halt protocol.

### 3. Improvement Synthesis
Translate every reflection into an actionable improvement for the current or future tasks.
- **Action:** Propose a revised plan or a permanent change to the workflow standard.
- **Constraint:** Hansei is incomplete without a concrete "Next Action" to prevent recurrence.
- **Integration:** Feeds into **Kaizen** for long-term optimization.

## Escalation & Halting

- **Jidoka:** If Hansei reveals that the root cause is a fundamental misunderstanding of the task, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to share the root-cause analysis and proposed improvements with the user.

## Implementation Workflow

1. **Trigger:** Initiated during planning (Shisa Kanko Phase A) or after an execution failure.
2. **Execute:** Critically analyze the draft or failure to identify assumptions and logic flaws.
3. **Verify:** Confirm the reflection identifies specific, actionable root causes.
4. **Output:** A refined plan, a diagnostic report, or a Kaizen proposal.
