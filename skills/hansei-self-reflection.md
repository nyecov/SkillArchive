---
name: Hansei (Self-reflection)
version: 1.1.0
description: >
  Use when a plan needs critical review, an execution has failed, or a recurring error pattern emerges.
  Handles proactive plan critique, reactive root-cause analysis, and improvement proposals.
category: cognition
tags: [hansei, reflection, iterative-refinement, cognitive-bias, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ./shisa-kanko-vibecoding.md
  - name: Jidoka (Autonomation)
    path: ./jidoka-autonomation.md
  - name: Poka-yoke (Mistake-proofing)
    path: ./poka-yoke-mistake-proofing.md
  - name: KYT (Hazard Prediction)
    path: ./kyt-hazard-prediction.md
  - name: Hō-Ren-Sō (Communication)
    path: ./ho-ren-so-communication.md
  - name: Kaizen (Continuous Improvement)
    path: ./kaizen-continuous-improvement.md
  - name: Lean Principles (Muda Eradication)
    path: ./lean-principles-muda.md
  - name: Value Stream Mapping (VSM)
    path: ./vsm-value-stream-mapping.md
---

# Hansei: Agentic Self-Reflection

Hansei is the practice of looking back at a plan or action with a critical, objective eye to identify flaws, acknowledge mistakes, and develop improvement plans. In an agentic system, it serves as the cognitive engine for both proactive refinement and reactive debugging.

## Core Mandates

### 1. Proactive Reflection (Pre-Execution)
Before finalizing a plan in the **Shisa Kanko** workflow, the agent MUST perform a critical review of its own reasoning.
- **Action:** Run a 'Reflection Pass' on the drafted plan.
- **Prompt:** "Identify three ways this plan could fail, violate architectural guidelines, or introduce subtle regressions."
- **Integration:** The findings from this proactive Hansei are fed directly into the **KYT (Hazard Prediction)** protocol to establish concrete **Poka-yoke** countermeasures.

### 2. Reactive Root Cause Analysis (Post-Halt)
When a **Jidoka** halt is triggered (e.g., due to a failed **Poka-yoke** interlock or a bad API response), the agent MUST analyze the failure rather than just reporting the error code.
- **Action:** Trace the error back to its origin. Was it a hallucination? Missing context? Ambiguous instructions?
- **Objective Acknowledgment:** The agent must state the failure plainly without attempting to 'cover up' logical leaps or missing data.

### 3. Improvement Planning & Escalation
Hansei is only complete when an actionable improvement is proposed.
- **Action:** Generate a revised plan or a set of options to resolve the root cause.
- **Integration (Hō-Ren-Sō):** This analysis forms the core payload of the **Sōdan (Consult)** message sent via the **Hō-Ren-Sō** protocol, providing the human operator with the context needed to make an informed decision.
- **Integration (Kaizen):** If the reflection reveals a *recurring* root cause — the same class of error appearing across multiple executions — escalate it to a **Kaizen** event to permanently update the workflow standard, rather than applying ad-hoc fixes each time.

## Implementation Workflow

1. **Trigger:** Initiated proactively during planning (Phase A of Shisa Kanko) or reactively after a Jidoka halt.
2. **Reflect (Hansei):** Critically analyze the draft or the failure state.
3. **Trace:** Identify the specific assumption, missing context, or logic flaw.
4. **Output:** Produce a revised plan (if proactive) or a root-cause diagnostic (if reactive) to fuel KYT or Hō-Ren-Sō escalations.
