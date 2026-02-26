---
name: Value Stream Mapping (VSM)
version: 1.0.0
description: A diagnostic visualization tool to map the flow of logic, tokens, and data through an agentic system, used to identify bottlenecks and structural waste.
category: diagnostics
tags: [vsm, mapping, architecture, bottlenecks, flow]
references:
  - name: Lean Principles (Muda Eradication)
    path: ./lean-principles-muda.md
  - name: Kaizen (Continuous Improvement)
    path: ./kaizen-continuous-improvement.md
---

# Value Stream Mapping (VSM) for Agents

Value Stream Mapping (VSM) is an analytical technique used to document, analyze, and improve the flow of information or materials. In AI systems, it maps the flow of context (tokens), reasoning (LLM calls), and execution (tool use) from the user's initial prompt to the final output.

## Core Mandates

### 1. Current State Mapping (The Diagnostic)
When a complex workflow feels slow or frequently hallucinates, the agent MUST map the current state.
- **Action:** Log the exact sequence of events, including:
  - Tool calls made (and their latency).
  - Context size passed to each reasoning step.
  - Number of autonomous loops or retries.
  - Locations of any **Jidoka** halts.

### 2. Identifying the Bottlenecks
Analyze the Current State Map to locate structural waste (Muda).
- **Questions to Ask:**
  - Where is the LLM spending the most tokens?
  - Are there sequential tool calls that could be parallelized?
  - Is there a "Contact Check" (Poka-yoke) that happens too late in the flow, causing wasted processing if it fails?

### 3. Future State Design (The Target)
Design a more efficient, direct path.
- **Action:** Propose an optimized architectural flow. This often involves rearranging the order of operations, summarizing context before passing it to sub-agents, or introducing a fast deterministic script to bypass the LLM entirely for specific steps.

## Implementation Workflow

1. **Observe:** Run a complex task and trace the execution path.
2. **Map:** Output a visual or structured text representation of the steps (e.g., `User -> Prompt -> Agent (20k tokens) -> Tool A -> Agent (22k tokens) -> Output`).
3. **Analyze:** Identify the "Transportation" and "Waiting" wastes.
4. **Improve:** Trigger a **Kaizen** event to restructure the workflow toward the Future State Map.
