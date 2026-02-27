---
name: lean-foundations-3m-5s
version: 1.0.0
description: >
  Foundational Lean principles for stabilizing workflows through the 3 Ms (Mura, Muri, Muda) 
  and the 5S workplace organization framework. Focuses on eliminating inconsistency and 
  overburden while maintaining a disciplined agentic environment.
category: philosophy
tags: [lean, 3m, 5s, mura, muri, stability, organization]
references:
  - name: Lean Principles (Muda)
    path: ../lean-principles-muda/SKILL.md
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
---

# Lean Foundations: Stability through 3M & 5S

While **Muda** (Waste) is the most visible enemy of efficiency, it is often caused by deeper structural issues: **Mura** (Unevenness) and **Muri** (Overburden). The **5S** framework provides the tactical discipline needed to maintain a clean, high-signal workspace.

## The 3 Ms: The Trio of Inefficiency

Agents MUST identify and address all three forms of inefficiency:

1.  **Muda (Waste):** Activities that consume resources without adding value (Refer to `lean-principles-muda`).
2.  **Mura (Unevenness):** Inconsistency in workflow, logic, or output. 
    *   *Agentic Example:* Fluctuating between over-explaining and under-explaining, or inconsistent code style across files.
    *   *Fix:* Standardize via **5S** and **Shisa Kanko**.
3.  **Muri (Overburden):** Pushing the system or agent beyond its natural limits.
    *   *Agentic Example:* Attempting to process too much context in a single prompt (causing hallucinations) or running too many parallel tasks that exhaust rate limits.
    *   *Fix:* Decompose tasks into smaller, stable units.

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

### 1. Stability Before Speed
The agent MUST prioritize a stable, consistent workflow (**Heijunka**) over bursts of high-speed but erratic activity. Eliminate **Mura** to prevent the creation of **Muda**.

### 2. Respect the Limits (No Muri)
The agent MUST NOT attempt tasks that exceed the context window or reliable reasoning capabilities of the underlying model. Break complex logic into verifiable sub-tasks.

### 3. Workplace Hygiene
Every tool call or file modification MUST leave the workspace in a state of **Seiketsu** (Standardization). No "messy" intermediate states should persist into the final delivery.

## Implementation Workflow

1.  **Audit (Sort/Shine):** Before starting a complex task, review the current file tree and context. Isolate what is truly needed.
2.  **Stabilize (3M Check):** Check for **Mura** (Are my instructions consistent?) and **Muri** (Is this task too big for one go?).
3.  **Execute (Set in Order):** Perform the work while maintaining structural integrity.
4.  **Cleanse (Standardize):** Refactor, format, and document as you go.
5.  **Audit (Sustain):** Final check of the workspace before concluding the session.

## Escalation & Integration

- **Muri Detection (Jidoka):** If a task is so large it causes repeated failures or extreme latency, trigger a **Jidoka** halt. Decompose the task and restart.
- **Mura Correction (Kaizen):** If inconsistencies are found in existing code or documentation, treat it as a **Kaizen** opportunity to standardize the pattern.
- **Reporting (Hō-Ren-Sō):** Significant "Sort" or "Shine" operations (e.g., major refactors for clarity) should be reported to the user.
