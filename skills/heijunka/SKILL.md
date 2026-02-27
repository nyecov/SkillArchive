---
name: heijunka
version: 1.0.0
description: 'Use to level the workload and prevent token/context spikes (Muri).  Handles
  the decomposition of massive tasks into manageable, consistent batches.

  '
category: methodology
tags:
- methodology
- optimization
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: VSM (Value Stream Mapping)
  path: ../vsm/SKILL.md
level: methodology
---

# Heijunka (Production Leveling)

Heijunka ensures a stable flow of work by leveling the volume and variety of tasks. In an agentic context, it prevents "Context Exhaustion" and "Reasoning Drift" by breaking down large, complex directives into a series of uniform, high-signal iterations.

## Core Mandates

### 1. Workload Leveling (Muri Prevention)
- **Action:** Before execution, the agent MUST assess the total scope of the task and decompose it into sub-tasks that fit comfortably within the optimal context window (typically < 4k tokens of active reasoning).
- **Constraint:** NEVER attempt to solve a multi-layered architectural problem in a single monolithic tool call or reasoning block.
- **Integration:** Connects to **Value Stream Mapping (VSM)** to identify where the "flow" of reasoning might be blocked by excessive complexity.

### 2. Batch Consistency
- **Action:** Group similar operations (e.g., multiple file reads, multiple search queries) into consistent batches to maximize tool efficiency.
- **Constraint:** Avoid "thrashing" between high-level architectural design and low-level syntax fixes. Finish a "level" of abstraction before moving to the next.
- **Integration:** Works with **Shisa Kanko** to ensure each leveled batch is verified before the next begins.

## Escalation & Halting

- **Jidoka:** If a sub-task exceeds the estimated complexity or token budget by 50%, halt and re-level the remaining work.
- **Hō-Ren-Sō:** Inform the user if a request requires more iterations than initially estimated due to the leveling process.

## Implementation Workflow

1. **Trigger:** A complex, multi-file, or high-level architectural request is received.
2. **Execute:** 
   - Analyze the total "Mass" of the request.
   - Divide into "Leveled Batches" (e.g., Research Batch -> Strategy Batch -> Implementation Batch 1 -> Implementation Batch 2).
   - Sequence the batches to maintain a steady flow.
3. **Verify:** Confirm each batch is complete and the context remains "lean" before starting the next.
4. **Output:** A series of successful, verified increments rather than one high-risk leap.
