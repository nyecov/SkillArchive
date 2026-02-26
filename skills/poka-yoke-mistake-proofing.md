---
name: Poka-yoke (Mistake-proofing)
version: 1.1.0
description: Design-level error prevention. Uses deterministic guardrails, schema enforcement, and state machines to make agentic errors impossible to execute, acting as the trigger for Jidoka and Hansei.
category: engineering-standards
tags: [poka-yoke, guardrails, validation, deterministic, reliability, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ./shisa-kanko-vibecoding.md
  - name: Jidoka (Autonomation)
    path: ./jidoka-autonomation.md
  - name: Hansei (Self-reflection)
    path: ./hansei-self-reflection.md
  - name: KYT (Hazard Prediction)
    path: ./kyt-hazard-prediction.md
  - name: Hō-Ren-Sō (Communication)
    path: ./ho-ren-so-communication.md
---

# Poka-yoke: Mistake-proofing AI Workflows

Poka-yoke focuses on 'fail-safe' mechanisms that prevent errors from occurring rather than just detecting them after the fact. In an agentic system, Poka-yoke constraints act as the physical "interlocks" that enforce the rules established by other Lean protocols.

## Core Mandates & Interlocks

### 1. Schema Enforcement (The Template)
The agent MUST use rigid, validated schemas for all structured data exchange.
- **Action:** Force all tool parameters through a strict JSON schema validator.
- **Constraint:** If the LLM output does not match the schema, the execution layer MUST reject it.
- **Jidoka Integration:** A schema validation failure is a primary abnormality that triggers a **Jidoka** halt.

### 2. State Machine Constraints (The Track)
Restrict the agent's movement to a pre-defined state machine.
- **Action:** Define 'legal' transitions (e.g., `ISOLATE_TARGET -> DECLARE_LOGIC -> EXECUTE`).
- **Constraint:** The system MUST refuse to execute an action if the agent attempts to skip a mandatory validation state (e.g., trying to execute before performing **Shisa Kanko** pointing).

### 3. Contact Checks (The Prerequisite Interlock)
Ensure all 'prerequisites' are physically present before acting.
- **Action:** Check for the existence of files, environment variables, and active network connections before calling a tool.
- **Constraint:** Fail-fast if any dependency is missing. This is often implemented as a countermeasure derived from a **KYT (Hazard Prediction)** session.

## The Poka-yoke Response Workflow

When a Poka-yoke constraint is triggered (an action is blocked):

1. **Halt (Jidoka):** Immediately freeze the execution state. Do not attempt to bypass the interlock.
2. **Reflect (Hansei):** Perform a root-cause analysis. *Why* did the agent generate an output that violated the constraint? (e.g., Was the schema documentation ambiguous? Was the context window overflowing?)
3. **Escalate (Hō-Ren-Sō):** Use the Sōdan (Consult) protocol to inform the human operator:
   - "Execution blocked by Poka-yoke interlock: [Name of Constraint]."
   - "Hansei analysis suggests: [Root Cause]."
   - "Requesting guidance to resolve."

## Implementation Guidelines
- **Make it Physical:** Where possible, enforce Poka-yoke at the tool level (e.g., setting `required: true` in an OpenAPI spec) rather than relying on prompt instructions.
- **Deterministic Validation:** Poka-yoke checks must be 100% deterministic (e.g., Regex, JSON Schema, file existence), never based on another LLM's subjective evaluation.
