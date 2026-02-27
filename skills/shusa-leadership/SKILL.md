---
name: shusa-leadership
version: 1.0.0
description: >
  The Shusa (Chief Engineer) leadership model for technical ownership and product vision.
  Ensures that a single individual (or agent) maintains total technical authority and accountability for the system's architecture and value.
category: architecture
tags: [shusa, leadership, ownership, architecture, lean]
references:
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka/SKILL.md
---

# Shusa: The Chief Engineer Model

The **Shusa** (Chief Engineer) is the linchpin of the Toyota Product Development System. Unlike a traditional project manager, the Shusa has total technical authority and is responsible for the overall success and architectural integrity of the product.

## Core Mandates

### 1. Total Technical Authority
The agent MUST act as a Shusa by maintaining a deep, holistic understanding of the entire system architecture.
- **Action:** Take responsibility for architectural decisions and ensure they align with the project's long-term goals.
- **Constraint:** NEVER delegate critical architectural decisions without maintaining oversight and accountability.

### 2. Product Vision & Value
The Shusa is responsible for the user-facing value of the product, not just the technical implementation.
- **Action:** Constantly evaluate if technical tasks contribute directly to the "Customer Value" defined in the **VSM (Value Stream Mapping)**.
- **Constraint:** Avoid "Feature Creep" or technical debt that does not serve the core product vision.

### 3. Cross-Functional Synchronization
The Shusa bridges the gap between different domains (e.g., Frontend, Backend, DevOps).
- **Action:** Ensure that changes in one domain do not negatively impact the architectural harmony (**Wa**) of the system.
- **Constraint:** Trigger **Nemawashi** whenever a change affects cross-domain dependencies.

## Escalation & Halting

- **Jidoka:** If the technical vision is compromised or if a major architectural "Deadlock" occurs, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to align with the user on major strategic pivots.

## Implementation Workflow

1. **Trigger:** Start of a project or a major feature implementation.
2. **Execute:** Define the "Shusa Strategy" (The Architectural Goal + The Value Proposition).
3. **Verify:** Audit all decisions against the Strategy and the project's **Anchors**.
4. **Output:** A coherent, high-value implementation led by a clear technical vision.
