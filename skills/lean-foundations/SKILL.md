---
name: lean-foundations
version: 1.1.0
description: Foundational Lean principles for stabilizing workflows through the 3 Ms (Mura, Muri, Muda) and the 5S framework. Focuses on maximizing value by surgically eliminating 7 types of agentic waste.
category: methodology
tags:
- methodology
- optimization
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Jidoka (Autonomation)
  path: ../jidoka/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
level: methodology
---

# Lean Foundations: Stability through 3M & 5S

Lean focuses on maximizing deterministic output value while minimizing computational, temporal, and cognitive waste. This is achieved through identifying the **3 Ms** (Mura, Muri, Muda) and maintaining a disciplined workspace with the **5S** framework.

## The 3 Ms: The Trio of Inefficiency

1.  **Mura (Unevenness):** Inconsistency in workflow, logic, or output.
2.  **Muri (Overburden):** Pushing the model or context window beyond its optimal limits.
3.  **Muda (Waste):** Activities that consume resources without adding value.

## The 7 Wastes of Agentic Workflows (Muda)

Agents MUST actively monitor and eliminate these common wastes:
1. **Over-generation:** Writing more code than is strictly necessary (e.g., adding "just-in-case" features).
2. **Waiting:** Stalling on slow API calls without parallelizing tasks.
3. **Transportation (Context Bloat):** Pushing unnecessarily large context windows, causing hallucinations.
4. **Over-processing:** Using complex reasoning for tasks that simple deterministic scripts or regex could solve.
5. **Inventory (Unused Data):** Storing intermediate state or variables never consumed by the final execution.
6. **Motion (Navigational Waste):** Endless searching through directories due to imprecise initial pointing.
7. **Defects (Hallucinations):** Producing incorrect outputs that require rework. This is the worst form of waste.

## The 5S Framework for Agentic Workspaces

1.  **Seiri (Sort):** Distinguish between necessary and unnecessary files/context. Delete logs and trial scripts.
2.  **Seiton (Set in Order):** A place for everything. Follow established project structures.
3.  **Seiso (Shine):** Clean the workspace. Remove "dead code" and outdated comments.
4.  **Seiketsu (Standardize):** Use templates (`skill-template.md`) and consistent naming.
5.  **Shitsuke (Sustain):** Perform regular **Hansei** to ensure the standards are maintained.

## Core Mandates

### 1. Value-First Orientation
Explicitly define the user-facing value before execution and eliminate any activity that does not contribute to it.
- **Action:** Identify "Value" (e.g., a passing test, a deployed fix) before starting tool calls.
- **Integration:** Directly informs the **VSM (Value Stream Mapping)** process.

### 2. Surgical Muda Eradication
Actively monitor and eliminate the 7 agentic wastes. Use the most direct means (e.g., regex instead of LLM) to achieve the goal.
- **Action:** Identify and eliminate inconsistencies (**Mura**) and overburden (**Muri**).
- **Constraint:** Do not rewrite entire files if a single-line replacement suffices.

### 3. Capacity Respect (Muri Prevention)
Recognize and respect the limits of the context window and reasoning capabilities.
- **Action:** Decompose monolithic tasks that threaten to overburden the model.
- **Integration:** Triggers **Heijunka** to level the workload.

### 4. Workplace Discipline (5S)
Maintain a high-signal, low-noise environment through constant sorting, ordering, and cleaning.
- **Action:** Perform Seiri (Sort) and Seiso (Shine) operations to remove "dead code" and redundant context.
- **Constraint:** Every tool call MUST leave the workspace in a state of Seiketsu (Standardization).

## Escalation & Halting

- **Jidoka:** If **Muri** leads to repeated hallucinations or a "Defect" is detected, trigger an immediate Jidoka halt.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to inform the user when major 5S operations are performed.

## Implementation Workflow

1. **Trigger:** Start of a new session or a major task.
2. **Execute:** Run the 3M check (Unevenness, Overburden, Waste) and apply the 5S steps.
3. **Verify:** Confirm the workspace is organized, lean, and within model limits.
4. **Output:** A stabilized, high-signal workspace ready for precise engineering.
