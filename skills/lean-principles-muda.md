---
name: Lean Principles (Muda Eradication)
version: 1.1.0
description: The foundational philosophy of maximizing user value by relentlessly identifying and eliminating waste (Muda) in agentic workflows, prompts, and code generation.
category: philosophy
tags: [lean, muda, efficiency, optimization, value]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ./shisa-kanko-vibecoding.md
  - name: Jidoka (Autonomation)
    path: ./jidoka-autonomation.md
  - name: Poka-yoke (Mistake-proofing)
    path: ./poka-yoke-mistake-proofing.md
  - name: Hansei (Self-reflection)
    path: ./hansei-self-reflection.md
  - name: KYT (Hazard Prediction)
    path: ./kyt-hazard-prediction.md
  - name: Hō-Ren-Sō (Communication)
    path: ./ho-ren-so-communication.md
  - name: Kaizen (Continuous Improvement)
    path: ./kaizen-continuous-improvement.md
  - name: Value Stream Mapping (VSM)
    path: ./vsm-value-stream-mapping.md
---

# Lean: Eradicating Agentic Waste (Muda)

Lean is not a specific tool, but the overarching philosophy that drives the entire architecture. In an agentic system, Lean focuses on maximizing deterministic output value while minimizing computational, temporal, and cognitive waste.

## The 7 Wastes of Agentic Workflows (Muda)

Agents MUST actively monitor and eliminate these common wastes:
1. **Over-generation:** Writing more code than is strictly necessary to fulfill the prompt (e.g., adding "just-in-case" features).
2. **Waiting:** Inefficient asynchronous operations or stalling on slow API calls without parallelizing tasks.
3. **Transportation (Context Passing):** Pushing unnecessarily large context windows between agents, causing token bloat and 'lost-in-the-middle' hallucinations.
4. **Over-processing:** Using a complex reasoning model (System 2) for a task that could be solved by a simple deterministic script or regex (System 1).
5. **Inventory (Unused Code/Data):** Storing intermediate state or generating variables/files that are never consumed by the final execution.
6. **Motion (Navigational Waste):** Endless searching or looping through directories because the initial **Shisa Kanko** pointing was imprecise.
7. **Defects (Hallucinations/Bugs):** Producing incorrect outputs that require rework. This is the worst form of waste, mitigated by **Poka-yoke** and **Jidoka**.

## Core Mandates

### 1. Value Definition
Before taking any action, the agent MUST explicitly define what constitutes "Value" for the user in the current context (e.g., "A working test case," "A deployed endpoint"). Everything else is waste.

### 2. Surgical Precision
Apply the **Shisa Kanko** precise pointing to ensure changes are isolated and minimal. Do not rewrite a whole file if a single line replacement suffices.

### 3. Flow Optimization
Ensure that the transition from Intent -> Execution -> Verification is seamless, blocking only when a **Jidoka** halt is absolutely necessary.

## Implementation Workflow

1. **Observe:** At the start of any task, explicitly define the user-facing value and identify any steps that do not directly contribute to it.
2. **Classify:** Map any suspected waste to one of the 7 Muda categories above. Use **Value Stream Mapping** to visualize the flow if the waste is structural rather than incidental.
3. **Eliminate:** Remove the waste through the most direct means available — shorten context, parallelize calls, replace LLM reasoning with deterministic logic, or delete dead code.
4. **Verify:** Confirm via **Hansei (Self-reflection)** that the elimination did not degrade output quality or bypass necessary safety checks (**Poka-yoke**, **KYT**).
5. **Standardize:** If the waste pattern is recurring, escalate it to a **Kaizen** event to permanently update the workflow standard.

## Escalation & Integration

- **Defect Waste (Jidoka):** When a defect is detected, it is both a waste event and an abnormality. The **Jidoka** halt protocol takes precedence — stop, reflect via **Hansei**, and escalate via **Hō-Ren-Sō**.
- **Systemic Waste (Kaizen):** When waste is caused by a structural flaw in the workflow rather than a one-off mistake, trigger a **Kaizen** PDCA cycle to redesign the affected portion.
- **Reporting (Hō-Ren-Sō):** Significant waste reductions SHOULD be reported via **Hōkoku (Report)** so the human operator maintains awareness of efficiency improvements.
