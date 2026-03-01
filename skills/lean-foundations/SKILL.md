---
name: lean-foundations
version: 1.2.0
description: Foundational Lean principles for stabilizing workflows through the 3
  Ms (Mura, Muri, Muda) and the 5S framework. Focuses on maximizing value by surgically
  eliminating 7 types of agentic waste.
category: methodology
tags:
- methodology
- optimization
- lean
- TPS
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Jidoka (Autonomation)
  path: ../jidoka/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
- name: Lean Glossary
  path: ./references/lean-glossary.md
- name: 5S Validation Report Template
  path: ./templates/lean-5s-output.md
level: methodology
---
# Lean Foundations

Lean focuses on maximizing deterministic output value while minimizing computational, temporal, and cognitive waste. This is achieved through identifying the **3 Ms** (Mura, Muri, Muda) and maintaining a disciplined workspace with the **5S** framework.

## Core Mandates

### 1. Value-First Orientation
Explicitly define the user-facing value before execution and eliminate any activity that does not contribute to it.
- **Action:** Identify "Value" (e.g., a passing test, a deployed fix) before starting tool calls.
- **Constraint:** Do not perform exploratory changes or unverified refactoring that lacks a direct link to the stated Value.
- **Integration:** Directly informs the **VSM (Value Stream Mapping)** process.

### 2. Surgical Muda Eradication
Actively monitor and eliminate the 7 agentic wastes. Use the most direct means (e.g., regex instead of LLM) to achieve the goal.
- **Action:** Identify and eliminate inconsistencies (**Mura**) and overburden (**Muri**).
- **Constraint:** Do not rewrite entire files if a single-line replacement suffices.
- **Integration:** Aligns with **Kodawari** to ensure changes are exact and deliberate.

### 3. Capacity Respect (Muri Prevention)
Recognize and respect the limits of the context window and reasoning capabilities.
- **Action:** Decompose monolithic tasks that threaten to overburden the model.
- **Constraint:** NEVER process more than 3 distinct architectural layers or independent domains in a single execution phase.
- **Integration:** Triggers **Heijunka** to level the workload.

### 4. Workplace Discipline (5S)
Maintain a high-signal, low-noise environment through constant sorting, ordering, and cleaning.
- **Action:** Perform Seiri (Sort) and Seiso (Shine) operations to remove "dead code" and redundant context.
- **Constraint:** Every tool call MUST leave the workspace in a state of Seiketsu (Standardization).
- **Integration:** Provides the baseline environment required for **Shisa Kanko** to operate without distraction.

## Escalation & Halting

- **Jidoka:** If **Muri** leads to repeated hallucinations or a "Defect" is detected, trigger an immediate Jidoka halt.
- **Hō-Ren-Sō:** Escalate to the user before deleting *any* code or file during a 'Seiso' (Shine) operation if that file is located outside of a designated temporary workspace (e.g., `.gemini/tmp/`) and lacks verified redundancy.

## Implementation Workflow

1. **Trigger:** Start of a new session, major context bloat is detected, or a core architectural change requires workspace stabilization.
2. **Execute:** Execute the 3M diagnostic (identify Unevenness, Overburden, Waste) and sequentially process the workspace through the 5S steps (Sort, Set in Order, Shine, Standardize, Sustain).
3. **Verify:** Confirm the workspace is organized, confirm context tokens are reduced, and verify no critical files outside temporary boundaries were illegally altered/deleted.
4. **Output:** Render the validation state using the Poka-yoke Output Template.

## Poka-yoke Output Template

For the exact diagnostic output schema to use post-validation, read:
[5S Validation Report Template](templates/lean-5s-output.md)

## Progressive Resources

For detailed definitions of the 3 Ms, the 7 Wastes, and the 5S Framework, read:
[Lean Glossary](references/lean-glossary.md)
