---
name: muda
version: 1.1.0
description: 'Use when a workflow feels slow, bloated, or produces unnecessary output.
  Handles classification of 7 waste types (Muda), value definition, surgical elimination,
  and standardization of improvements.

  '
category: methodology
tags:
- methodology
- optimization
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Jidoka (Autonomation)
  path: ../jidoka/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: Hansei (Self-reflection)
  path: ../hansei/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Hō-Ren-Sō (Communication)
  path: ../ho-ren-so/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
level: methodology
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

### 1. Value-First Orientation
Explicitly define the user-facing value for every task and eliminate any activity that does not contribute to it.
- **Action:** Identify "Value" (e.g., a passing test, a deployed fix) before execution.
- **Constraint:** NEVER perform "just-in-case" coding or over-processing.
- **Integration:** Directly informs the **VSM (Value Stream Mapping)** process.

### 2. Surgical Muda Eradication
Actively monitor and eliminate the 7 agentic wastes: Over-generation, Waiting, Context Bloat, Over-processing, Inventory, Motion, and Defects.
- **Action:** Use the most direct means (e.g., regex instead of LLM, parallel calls) to achieve the goal.
- **Constraint:** Do not rewrite entire files if a single-line replacement suffices.
- **Integration:** Supports **Shisa Kanko** by ensuring "Precise Pointing" minimizes waste.

### 3. Continuous Flow (Pull System)
Ensure the transition from Intent -> Execution -> Verification is seamless and "pulled" by the user's requirements.
- **Action:** Minimize the time between a directive and its verified output.
- **Constraint:** Do not introduce artificial bottlenecks or "Wait-states."
- **Integration:** Works with **Heijunka** to maintain a consistent flow without spikes.

## Escalation & Halting

- **Jidoka:** If a "Defect" (Hallucination/Bug) waste is detected, trigger an immediate Jidoka halt.
- **Hō-Ren-Sō:** Use the Hōkoku (Report) protocol to communicate significant waste reductions and efficiency gains to the user.

## Implementation Workflow

1. **Trigger:** A new task is received.
2. **Execute:** Define the value, identify Muda in the plan, and surgically eliminate it.
3. **Verify:** Confirm the waste reduction did not compromise safety or quality (Hansei).
4. **Output:** A high-value, lean result with minimal resource consumption.
