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

### 1. Pattern Recognition (The Scan)
When a successful **Kaizen** (improvement) or a critical **Jidoka** (fix) is completed, the agent MUST scan the rest of the workspace for similar patterns.
- **Action:** Use `grep_search` to find other modules, functions, or files that share the same structural flaw or could benefit from the same improvement.
- **Constraint:** NEVER assume an improvement is "local" until a global scan has been performed.

### 2. Horizontal Broadcast (The Proposal)
Propose a multi-file deployment plan for the recognized pattern.
- **Action:** Draft a **Nemawashi (A3)** for the horizontal change.
- **Constraint:** Do not blindly apply the change everywhere at once. Validate the "Wa" (Harmony) for each specific location.
- **Integration:** This is the "Sustain" and "Standardize" phase of the **5S** framework.

## Escalation & Halting

- **Jidoka:** If a Yokoten deployment reveals that other modules are too varied for a standardized fix, trigger a Jidoka halt to re-evaluate the pattern.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to inform the user of the "Horizontal Discovery" and the proposed deployment plan.

## Implementation Workflow

1. **Trigger:** A local improvement or fix is successfully verified.
2. **Scan:** Search the codebase for all other instances where the pattern exists.
3. **Draft:** Create a deployment plan (Nemawashi).
4. **Deploy:** Systematically update all relevant modules using Shisa Kanko.
5. **Verify:** Confirm that the horizontal deployment has stabilized the entire system.
