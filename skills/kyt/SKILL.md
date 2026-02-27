---
name: kyt
version: 1.1.0
description: >
  Use before executing high-risk operations, destructive commands, or irreversible changes.
  Handles 4-round hazard identification, countermeasure design, and Go/No-Go gating.
category: safety
tags: [kyt, hazard-prediction, safety, critic-agent, pre-mortem, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke/SKILL.md
  - name: Hansei (Self-reflection)
    path: ../hansei/SKILL.md
  - name: Hō-Ren-Sō (Communication)
    path: ../ho-ren-so/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../muda/SKILL.md
  - name: Value Stream Mapping (VSM)
    path: ../vsm/SKILL.md
---

# KYT: Hazard Prediction Training for Agents

KYT (Kiken Yochi Training) is a systematic, multi-round protocol for identifying dangers before they occur. In an agentic architecture, it serves as the pre-mortem analysis layer, bridging the gap between an Execution Agent's proposed plan and the actual execution of tools.

## Core Mandates

### 1. Multi-Round Hazard Identification
Perform a systematic, 4-round pre-mortem analysis on any plan involving high-risk or irreversible changes.
- **Action:** Identify the Hazard, Determine Critical Danger Points, Establish Countermeasures, and Set Action Targets.
- **Constraint:** NEVER skip the KYT protocol for destructive commands (e.g., `rm`, `drop`, `reset`).
- **Integration:** Directly informs the **Poka-yoke** design for the specific task.

### 2. Critical Point Isolation
Precisely identify the "Point of No Return" where a change becomes irreversible.
- **Action:** Isolate the specific tool call or command that represents the core danger.
- **Constraint:** Do not proceed with execution until a specific countermeasure is established for every identified critical point.
- **Integration:** Feeds into **Shisa Kanko** "Precise Pointing" to ensure the danger zone is well-defined.

### 3. Countermeasure Synthesis (Poka-yoke)
Design deterministic interlocks that make the identified hazard physically or logically impossible to trigger accidentally.
- **Action:** Create "Pre-flight" checks (e.g., backup verification, environment validation) as mandatory interlocks.
- **Constraint:** Avoid "soft" countermeasures like "be careful"; only use deterministic, verifiable interlocks.
- **Integration:** This is the primary design engine for task-specific **Poka-yoke** constraints.

## Escalation & Halting

- **Jidoka:** If Round 3 fails to produce a reliable, deterministic countermeasure for a high-risk hazard, trigger an immediate Jidoka halt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to present the KYT findings (Hansei, Critical Point, Countermeasures) to the user for final approval.

## Implementation Workflow

1. **Plan Generation:** Execution Agent drafts a plan.
2. **KYT Pass:** Critic Agent executes the 4 rounds.
3. **Refinement:** Execution Agent integrates the Poka-yoke countermeasures.
4. **Verification:** System checks Action Targets; if cleared, proceed to Shisa Kanko pointing and calling.
