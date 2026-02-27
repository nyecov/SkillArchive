---
name: lean-foundations
version: 1.0.0
description: >
  Foundational Lean principles for stabilizing workflows through the 3 Ms (Mura, Muri, Muda) 
  and the 5S workplace organization framework. Focuses on eliminating inconsistency and 
  overburden while maintaining a disciplined agentic environment.
category: methodology
tags: [lean, 3m, 5s, mura, muri, stability, organization]
references:
  - name: Lean Principles (Muda)
    path: ../muda/SKILL.md
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen/SKILL.md
---

# Lean Foundations: Stability through 3M & 5S

While **Muda** (Waste) is the most visible enemy of efficiency, it is often caused by deeper structural issues: **Mura** (Unevenness) and **Muri** (Overburden). The **5S** framework provides the tactical discipline needed to maintain a clean, high-signal workspace.

## The 3 Ms: The Trio of Inefficiency

Agents MUST identify and address all three forms of inefficiency:

1.  **Muda (Waste):** Activities that consume resources without adding value. Refer to **Lean Principles — Muda** for the 7-waste taxonomy.
2.  **Mura (Unevenness):** Inconsistency in workflow, logic, or output.

## The 5S Framework for Agentic Workspaces

Apply these five steps to maintain a high-signal, low-noise environment:

1.  **Seiri (Sort):** Distinguish between necessary and unnecessary information/files.
    *   *Action:* Delete or move temporary logs, trial scripts, and redundant context that don't serve the final goal.
2.  **Seiton (Set in Order):** A place for everything, and everything in its place.
    *   *Action:* Follow established project structures (e.g., `src/`, `tests/`, `.gemini/`). Ensure every file and tool call has a clear, logical purpose.
3.  **Seiso (Shine):** Clean the workspace and tools.
    *   *Action:* Remove "dead code," comments that no longer apply, and outdated documentation. Ensure the "state" of the agent's memory is clear.
4.  **Seiketsu (Standardize):** Create rules to maintain the first three Ss.
    *   *Action:* Use templates (`skill-template.md`) and consistent naming conventions. Establish "best practices" for tool usage.
5.  **Shitsuke (Sustain):** Build the discipline to keep the standards.
    *   *Action:* Perform regular **Hansei** (Self-reflection) to ensure the workspace hasn't drifted into chaos.

## Core Mandates

### 1. Stability Before Speed (Mura Prevention)
Prioritize a stable, consistent workflow over erratic bursts of high-speed activity.
- **Action:** Identify and eliminate inconsistencies (**Mura**) in reasoning, code style, and task handling.
- **Constraint:** NEVER sacrifice structural integrity for the sake of finishing a task faster.
- **Integration:** Directly supports **Shisa Kanko** by ensuring each "Calling" is based on a stable "Pointing."

### 2. Capacity Respect (Muri Prevention)
Recognize and respect the limits of the context window and reasoning capabilities.
- **Action:** Decompose tasks that threaten to "Overburden" (**Muri**) the model's performance.
- **Constraint:** MUST NOT attempt monolithic reasoning on tasks that exceed the optimal context window.
- **Integration:** Triggers **Heijunka** to level the workload.

### 3. Workplace Discipline (5S)
Maintain a high-signal, low-noise environment through constant sorting, ordering, and cleaning.
- **Action:** Perform Seiri (Sort) and Seiso (Shine) operations to remove "dead code" and redundant context.
- **Constraint:** Every tool call MUST leave the workspace in a state of Seiketsu (Standardization).
- **Integration:** Works with **Poka-yoke** to ensure that "Set in Order" (Seiton) constraints are maintained.

## Escalation & Halting

- **Jidoka:** If **Muri** (Overburden) leads to repeated hallucinations or tool failures, trigger a Jidoka halt to re-level the task.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to inform the user when major 5S operations (e.g., refactoring for clarity) are performed.

## Implementation Workflow

1. **Trigger:** Start of a new session or a major task.
2. **Execute:** Run the 3M check (Unevenness, Overburden, Waste) and apply the 5S steps.
3. **Verify:** Confirm the workspace is organized, consistent, and within model limits.
4. **Output:** A stabilized, high-signal workspace ready for precise engineering.
