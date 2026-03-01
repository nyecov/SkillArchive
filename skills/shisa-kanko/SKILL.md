---
name: shisa-kanko
version: 2.1.0
level: methodology
description: Use when executing code changes, tool calls, or multi-step tasks. Mandates
  pointing, calling, and verification.
category: methodology
tags:
- cognition
- communication
- methodology
- safety
- lean
- TPS
references:
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
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
requires:
- kyt
- genchi-genbutsu
- jidoka
---
# Shisa Kanko

This master skill synthesizes the **Shisa Kanko (Pointing and Calling)** architecture with core Lean manufacturing principles. It transforms 'vibecoding' from intuitive execution into a rigorously safe, deterministic engineering discipline.

## Core Mandates

### 1. Precise Pointing (Context Isolation)
Before any modification, 'point' to the target with absolute precision.
- **Action:** Output a `[TARGET_ISOLATION]` block containing the file path, line ranges, and the **Exact Code Snippet**.
- **Constraint:** If the snippet cannot be perfectly matched via a `read_file` check, you MUST NOT proceed to execution.
- **Integration:** Acts as a **Poka-yoke** interlock.

### 2. Risk Gating (Delegate to KYT)
Every plan involving high-risk or irreversible changes MUST be gated by a formal risk assessment.
- **Action:** Activate the **KYT** skill to identify hazards and establish countermeasures.
- **Constraint:** NEVER execute a plan identified as "High Risk" without a verified Action Target from the KYT pass.
- **Integration:** Delegates the "Risk Assessment" phase of the workflow to the **KYT** protocol.

### 3. Explicit Calling (Logic & TDD)
Never execute a tool call without 'calling out' the expected outcome and the TDD verification path.
- **Action:** Output a strictly formatted `[LOGIC_DECLARATION]` block:
  - **Intent:** Specific code change.
  - **Success Criteria:** What defines success.
  - **Verification Method (TDD):** The exact command/test that MUST pass.
- **Constraint:** All execution MUST be preceded by this declaration. **Prefer writing the test or verification script BEFORE the implementation (TDD).**
- **Integration:** Bridges to **Test-Driven Development (TDD)** ensuring that tests are prioritized before writing logic.

### 4. Empirical Validation (Delegate to Genchi Genbutsu)
Confirm that the results of the execution match the logic declaration through direct observation.
- **Action:** Use the **Genchi Genbutsu** skill to run tests and verify the "Real" behavior.
- **Constraint:** A task is not complete until it has been empirically verified.
- **Integration:** Delegates the "Verification" phase of the workflow to the **Genchi Genbutsu** protocol.

## Escalation & Halting

- **Jidoka:** Any pointing mismatch or abnormal tool response MUST trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if pointing reveals severe drift from the mental model or if KYT identifies unrecoverable risk.

## Implementation Workflow

1. **Trigger:** A Directive is received from the user.
2. **Execute:** Follow the Phases A-C (Reflect -> Risk Assessment -> Deterministic Execution).
3. **Verify:** Phase D (Validation + Vibe Audit).
4. **Output:** A verified, high-integrity update and a Hōkoku (Report) to the user, strictly adopting the format defined in the Poka-yoke Output Template.

## Poka-yoke Output Template

When performing the Pointing and Calling procedure, agents MUST output their isolation and logic statements using the schema defined in the Poka-yoke Output Template.

[Shisa Kanko Declaration Template](templates/shisa-kanko-declaration.md)
