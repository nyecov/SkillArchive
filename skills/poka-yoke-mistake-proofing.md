---
name: Poka-yoke (Mistake-proofing)
version: 1.0.0
description: Design-level error prevention. Uses deterministic guardrails and strict validation to make errors impossible to execute.
category: engineering-standards
tags: [poka-yoke, guardrails, validation, deterministic, reliability]
---

# Poka-yoke: Mistake-proofing AI Workflows

Poka-yoke focuses on 'fail-safe' mechanisms that prevent errors from occurring rather than just detecting them after the fact.

## Core Mandates

### 1. Schema Enforcement (The Template)
The agent MUST use rigid, validated schemas for all structured data exchange.
- **Action:** Force all tool parameters through a strict JSON schema validator.
- **Constraint:** If the LLM output does not match the schema, the execution layer MUST reject it before it reaches the external API.

### 2. State Machine Constraints (The Track)
Restrict the agent's movement to a pre-defined state machine.
- **Action:** Define 'legal' transitions between states (e.g., REACHED_TARGET -> VALIDATED -> EXECUTED).
- **Constraint:** The system MUST refuse to execute an action if the agent attempts to skip a mandatory validation state.

### 3. Contact Checks (The Interlock)
Ensure all 'prerequisites' are physically present before acting.
- **Action:** Check for the existence of files, environment variables, and active network connections before calling a tool.
- **Constraint:** Fail-fast if any dependency is missing.

## Implementation Workflow

1. **Define Constraints:** Set rigid schemas and state transitions.
2. **Validate:** Check every LLM proposal against these constraints.
3. **Prevent:** Block execution if any constraint is violated.
