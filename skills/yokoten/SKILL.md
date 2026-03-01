---
name: yokoten
version: 1.0.0
level: methodology
description: Horizontal deployment of knowledge and best practices.  Used to "broadcast"
  successful patterns or critical fixes from one module to all other relevant areas
  of the project.\
category: methodology
tags:
- methodology
- lean
- TPS
- kaizen
references:
- name: Kaizen
  path: ../kaizen/SKILL.md
- name: Nemawashi
  path: ../nemawashi/SKILL.md
- name: Shisa Kanko
  path: ../shisa-kanko/SKILL.md
---
# Yokoten

**Yokoten** is the practice of sharing information across the organization. In an agentic workflow, it ensures that a "lesson learned" or a "best practice" discovered in one file or module is systematically applied to every other relevant area of the project, preventing siloed improvements.

## Core Mandates

### 1. Deterministic Enforcement (Python Script)
Yokoten deployments MUST be governed entirely by a deterministic Python script (`manage_yokoten.py`). The agent acts as an operator of the script, not the orchestrator of the deployment.
- **Action:** Execute the Python script to formally log the pattern, track target files, and generate the final diagnostic report.
- **Constraint:** NEVER manually apply multi-file deployments without the script acting as the state-machine and batch-controller.

### 2. Pattern Recognition (The Scan)
When a successful **Kaizen** (improvement) or a critical **Jidoka** (fix) is completed, the agent MUST scan the rest of the workspace for similar patterns.
- **Action:** Use `grep_search` (or semantic search via the python script) to find other modules that share the same structural flaw.
- **Constraint:** NEVER assume an improvement is "local" until a global scan has been performed.

### 3. Horizontal Broadcast (The Proposal)
Propose a multi-file deployment plan for the recognized pattern.
- **Action:** Draft a **Nemawashi (A3)** for the horizontal change.
- **Constraint (Heijunka):** The script mechanically enforces Heijunka batches. NEVER load more than 5 targets into context simultaneously.
- **Integration:** This is the "Sustain" and "Standardize" phase of the **5S** framework.

## Escalation & Halting

- **Jidoka (Boundary Halt):** If a target file requires fundamentally different logic, the Yokoten script MUST halt that specific deployment and invoke the `story-interview` skill to rebuild the logic with the user.
- **Jidoka (Failure Halt):** If local unit tests fail after a Yokoten change, the agent may attempt up to 2 autonomous corrections. After 2 consecutive failures, it MUST halt and require user input.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to inform the user of the "Horizontal Discovery" and present the script's final diagnostic report.

## Implementation Workflow

1. **Trigger:** A local improvement or fix is successfully verified.
2. **Scan:** Search the codebase for all other instances where the pattern exists.
3. **Draft:** Create a deployment plan (Nemawashi).
4. **Deploy:** Systematically update all relevant modules using Shisa Kanko.
5. **Verify:** Confirm that the horizontal deployment has stabilized the entire system.
