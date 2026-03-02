---
id: 4c9f8b4b-61d8-4d73-b873-be450287362c
name: kyt
version: 1.3.0
level: methodology
description: Use before executing high-risk, destructive, or irreversible commands
  (rm, drop, reset). Mandates hazard prediction.
category: safety
tags:
- methodology
- safety
- lean
- TPS
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
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
- name: KYT Hazard Matrix Template
  path: ./templates/kyt-hazard-matrix.md
requires:
- poka-yoke
---
# KYT

KYT (Kiken Yochi Training) is a systematic, multi-round protocol for identifying dangers before they occur. In an agentic architecture, it serves as the pre-mortem analysis layer, bridging the gap between an Execution Agent's proposed plan and the actual execution of tools.

## Core Mandates

### 1. Multi-Round Hazard Identification
Perform a systematic, 4-round pre-mortem analysis on any plan involving high-risk or irreversible changes.
- **Action:** Identify Hazard, Determine Critical Points, Establish Countermeasures, Set Action Targets.
- **Constraint:** NEVER skip the KYT protocol for destructive commands (e.g., `rm`, `drop`, `reset`).
- **Integration:** Directly informs the **Poka-yoke** design for the task.

### 2. Critical Point Isolation
Precisely identify the "Point of No Return" where a change becomes irreversible.
- **Action:** Isolate the specific tool call or command that represents the core danger.
- **Constraint:** Do not proceed with execution until a specific countermeasure is established for every identified critical point.
- **Integration:** Mandates the input for **Shisa Kanko** "Precise Pointing".

### 3. Deterministic Countermeasure Synthesis
Design safeguards that make the identified hazard logically or physically impossible.
- **Action:** Create "Pre-flight" checks or setup commands (e.g., automated backups, environment locks).
- **Constraint:** ONLY use deterministic, verifiable interlocks. "Human care" or "soft" warnings are strictly forbidden as countermeasures.
- **Constraint:** Round 4 **Action Targets** MUST be manifested as explicit tool calls or executable commands.
- **Integration:** Primary design engine for **Poka-yoke** interlocks.

## Escalation & Halting

- **Jidoka:** If Round 3 fails to produce a reliable, deterministic countermeasure for a high-risk hazard, trigger an immediate Jidoka halt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to present the KYT findings (Hansei, Critical Point, Countermeasures) to the user for final approval.

## Implementation Workflow

1. **Plan Generation:** Execution Agent drafts a plan.
2. **KYT Pass:** Critic Agent executes the 4 rounds.
3. **Refinement:** Execution Agent integrates the Poka-yoke countermeasures.
4. **Verification:** System checks Action Targets; if cleared, proceed to Shisa Kanko pointing and calling, using the Poka-yoke Output Template.

## Poka-yoke Output Template

When the KYT pre-mortem is complete, the agent MUST format its findings using the exact schema defined in the Poka-yoke Output Template.

[KYT Hazard Matrix Template](templates/kyt-hazard-matrix.md)

