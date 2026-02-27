---
name: hansei-self-reflection
version: 1.1.0
description: >
  Use when a plan needs critical review, an execution has failed, or a recurring error pattern emerges.
  Handles proactive plan critique, reactive root-cause analysis, and improvement proposals.
category: cognition
tags: [hansei, reflection, iterative-refinement, cognitive-bias, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: KYT (Hazard Prediction)
    path: ../kyt-hazard-prediction/SKILL.md
  - name: Hō-Ren-Sō (Communication)
    path: ../ho-ren-so-communication/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
  - name: Value Stream Mapping (VSM)
    path: ../vsm-value-stream-mapping/SKILL.md
---

# Hansei: Agentic Self-Reflection

Hansei is the practice of looking back at a plan or action with a critical, objective eye to identify flaws, acknowledge mistakes, and develop improvement plans. In an agentic system, it serves as the cognitive engine for both proactive refinement and reactive debugging.

## Core Mandates

### 1. Proactive Reflection (The Plan Critique)
Before finalizing a plan, perform a critical review of the proposed reasoning to identify subtle flaws.
- **Action:** Formulate three distinct ways the current plan could fail or introduce architectural rot.
- **Constraint:** NEVER accept the first draft of a complex plan without a formal Hansei pass.
- **Integration:** The findings feed directly into **KYT (Hazard Prediction)** to establish countermeasures.

### 2. Reactive Root Cause Analysis (RCA)
When an execution fails or a Jidoka halt occurs, analyze the failure rather than just reporting the error.
- **Action:** Trace the error back to its origin (Hallucination, Missing Context, Logic Flaw).
- **Constraint:** Do not attempt to "hide" or "gloss over" logical leaps. State the failure plainly.
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
