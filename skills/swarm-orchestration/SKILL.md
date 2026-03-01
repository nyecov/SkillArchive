---
name: swarm-orchestration
version: 1.1.0
level: methodology
description: 'Protocols for multi-agent coordination and delegation.  Ensures that
  specialized sub-agents are tasked precisely and their outputs are synthesized without
  losing architectural harmony (Wa).\'
category: architecture
tags:
- communication
- design
- kubernetes
references:
- name: Shusa Leadership
  path: ../shusa-leadership/SKILL.md
- name: Nemawashi (Foundation Building)
  path: ../nemawashi/SKILL.md
- name: Kodawari Craftsmanship
  path: ../kodawari-craftsmanship/SKILL.md
---

# Swarm Orchestration

In complex systems, a single agent cannot maintain the necessary focus on all domains simultaneously. Swarm Orchestration provides the "Protocol of Handover" between a Lead Agent (**Shusa**) and specialized **Sub-Agents**. It ensures that delegation does not lead to fragmentation.

## Core Mandates

### 1. Precise Mission Tasking
Every delegation MUST be accompanied by a "Mission Brief" that includes context, constraints, and success criteria.
- **Action:** Define the specific "Value Stream" being delegated and the **Anchors** that must be respected.
- **Constraint:** NEVER task a sub-agent with a "vague" goal. Use the **Shisa Kanko** pointing method to define the task boundary.
- **Integration:** Directly implements the **Shusa Leadership** model of strategic ownership.

### 2. Output Synthesis (Wa Audit)
The Lead Agent is responsible for auditing and synthesizing the sub-agent's output back into the primary codebase.
- **Action:** Perform a **Kodawari (Craftsmanship)** audit on all sub-agent contributions.
- **Constraint:** Do not blindly accept sub-agent code. Ensure it maintains **Architectural Harmony (Wa)** with the rest of the system.
- **Integration:** Uses **Nemawashi** to identify cross-domain side effects of the sub-agent's work.

### 3. State Synchronization
Ensure that all agents in the "Swarm" share a consistent view of the "True North" (the project goal).
- **Action:** Broadcast major state changes or architectural pivots (Renraku) to all active sub-agents.
- **Constraint:** Prevent "State Drift" where sub-agents work against stale or conflicting requirements.
- **Integration:** Aligns with **Hō-Ren-Sō** for continuous reporting and state sharing across the system.

## Escalation & Halting

- **Jidoka:** If a sub-agent produces output that fundamentally contradicts the project's **Anchors**, trigger a Jidoka halt and re-evaluate the delegation brief.
- **Hō-Ren-Sō:** Use the Hōkoku (Report) protocol to summarize sub-agent progress to the user.

## Implementation Workflow

1. **Trigger:** A task is identified as requiring specialized expertise (e.g., Security, Performance, Testing).
2. **Execute:** 
   - Draft the "Mission Brief."
   - Delegate to the specialized Sub-Agent.
   - Monitor for "Muri (Overburden)" in the sub-agent's reasoning.
3. **Verify:** Perform the **Wa (Harmony) Audit** on the returned output.
4. **Output:** A synthesized, high-integrity update to the primary system, documented via the Poka-yoke Output Template.

## Poka-yoke Output Template

When delegating a task to a sub-agent, the Lead Agent MUST output the delegation using the schema defined in the Poka-yoke Output Template.

👉 **[Swarm Mission Brief Template](templates/mission-brief.md)**
