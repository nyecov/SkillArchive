---
name: plan-with-files
version: 1.1.0
level: methodology
description: 'Implements file-based planning to organize and track progress on complex tasks using persistent markdown files located in a dedicated temporary workspace directory (e.g. .gemini/tmp) to avoid root bloat.'
category: cognition
tags: [methodology, context, cognition]
references:
  - name: Ontology (Knowledge Graph)
    path: ../ontology/SKILL.md
  - name: Lean Foundations (Waste Elimination)
    path: ../lean-foundations/SKILL.md
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
---

# Plan with Files

Use persistent markdown files as your "working memory on disk." Context windows are volatile and limited; the filesystem is persistent and unlimited. This skill dictates how to externalize state to survive session resets, prevent context drift, and manage complex, multi-step tasks.

## Core Mandates

### 1. The Planning Triad
- **Action:** Before starting ANY complex task, create three files in a dedicated temporary workspace directory (e.g., `.gemini/tmp/` or the IDE Artifacts directory): `task_plan.md` (phases, progress), `findings.md` (research, decisions), and `progress.md` (session log, test results).
- **Constraint:** Never start a complex task (3+ steps) without a `task_plan.md`. Never drop these files in the project root directory; if accidentally created there, relocate them immediately.
- **Integration:** Aligns with **Ontology** by structuring memory, and **Lean Foundations** by eliminating the waste of forgetting while maintaining a clean 5S workspace.

### 2. The 2-Action Rule (Findings)
- **Action:** After every 2 view, browser, or search operations, IMMEDIATELY save key findings to `findings.md`.
- **Constraint:** Do not rely on your internal context window to remember multimodal information (images, complex browser output) or long research trails.
- **Integration:** Acts as a **Poka-yoke** against context loss.

### 3. Read Before Decide
- **Action:** Before major decisions or starting a new phase, read the plan files to refresh your goals.
- **Constraint:** Do not make architectural or phase decisions from stale context.
- **Integration:** Supports **Shisa Kanko** by forcing you to point to the plan and confirm the current state before acting.

### 4. Update After Act
- **Action:** After completing any phase, update `task_plan.md` (status: pending → in_progress → complete) and log actions/errors in `progress.md`.
- **Constraint:** Never leave the file state out-of-sync with the actual project state.
- **Integration:** Directly implements **Hansei** (Reflection) to continuously evaluate progress against the baseline plan.

## Escalation & Halting

- **Jidoka:** If you enter an error loop or fail repeatedly while using `plan-with-files`, immediately halt and delegate the error handling to the **Jidoka** skill. Do not rely on locally tracked retries.
- **Hō-Ren-Sō:** Escalate to the human operator if the 5-Question Reboot Test fails (meaning you've lost track of the plan).

## Implementation Workflow

1. **Trigger:** User requests a complex, multi-step task, research project, or architecture design.
2. **Execute:** 
   - Create the triad in a temporary directory (e.g., `.gemini/tmp/`): `task_plan.md`, `findings.md`, `progress.md`.
   - Populate initial phases and goals.
   - Execute phase 1, applying the 2-Action Rule for research.
3. **Verify:** Use the 5-Question Reboot Test: 
   - Where am I? (Current phase in task_plan)
   - Where am I going? (Remaining phases)
   - What's the goal? (Goal statement)
   - What have I learned? (findings.md)
   - What have I done? (progress.md)
4. **Output:** Updated planning files and progress on the actual codebase, structured via the Poka-yoke Output Template.

## Poka-yoke Output Template

When initiating a complex task, the agent MUST structure the planning files using the exact schema defined in the Poka-yoke Output Template to prevent context drift and ensure standardization.

[Planning Triad Template](templates/planning-triad.md)
