---
name: poka-yoke
version: 1.1.0
description: 'Use when designing validation gates, enforcing schemas, or preventing
  invalid tool calls. Handles deterministic guardrails, prerequisite interlocks, and
  state machine constraints.

  '
category: safety
tags:
- methodology
- safety
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Jidoka (Autonomation)
  path: ../jidoka/SKILL.md
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
level: safety
---

# Poka-yoke: Mistake-proofing AI Workflows

Poka-yoke focuses on 'fail-safe' mechanisms that prevent errors from occurring rather than just detecting them after the fact. In an agentic system, Poka-yoke constraints act as the physical "interlocks" that enforce the rules established by other Lean protocols.

## Core Mandates

### 1. Schema Enforcement (The Template)
The agent MUST use rigid, validated schemas for all structured data exchange.
- **Action:** Force all tool parameters through a strict JSON schema validator.
- **Constraint:** If the LLM output does not match the schema, the execution layer MUST reject it.
- **Integration:** A schema validation failure is a primary abnormality that triggers a **Jidoka** halt.

### 2. State Machine Constraints (The Track)
Restrict the agent's movement to a pre-defined state machine.
- **Action:** Define 'legal' transitions (e.g., `ISOLATE_TARGET -> DECLARE_LOGIC -> EXECUTE`).
- **Constraint:** The system MUST refuse to execute an action if the agent attempts to skip a mandatory validation state (e.g., trying to execute before performing **Shisa Kanko** pointing).
- **Integration:** Directly enforces the lifecycle phases defined in **Shisa Kanko**.

### 3. Prerequisite Interlocks
Ensure all 'prerequisites' are physically present before acting.
- **Action:** Check for the existence of files, environment variables, and active network connections before calling a tool.
- **Constraint:** Fail-fast if any dependency is missing. 
- **Integration:** This is often implemented as a countermeasure derived from a **KYT (Hazard Prediction)** session.

## Escalation & Halting

- **Jidoka:** Any breach of a Poka-yoke interlock (e.g., failed schema validation, missing prerequisite) MUST trigger an immediate Jidoka halt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to report the specific interlock that was tripped and the Hansei root-cause analysis.

## Implementation Workflow

1. **Trigger:** A tool call is initiated or a state transition is requested.
2. **Execute:** Run all deterministic checks (Schema, State, Prerequisites).
3. **Verify:** Confirm all checks passed with 100% confidence.
4. **Output:** Allow the action to proceed or trigger the Jidoka halt.
