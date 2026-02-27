---
name: vsm
version: 1.1.0
description: Use when diagnosing slow workflows, high token consumption, or unexplained
  latency in multi-step tasks. Handles current-state mapping, bottleneck identification,
  and future-state design for optimized flow.\
category: architecture
tags:
- design
- methodology
- optimization
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
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Hō-Ren-Sō (Communication)
  path: ../ho-ren-so/SKILL.md
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
level: technical
---
# Value Stream Mapping

Value Stream Mapping (VSM) is an analytical technique used to document, analyze, and improve the flow of information or materials. In AI systems, it maps the flow of context (tokens), reasoning (LLM calls), and execution (tool use) from the user's initial prompt to the final output.

## Core Mandates

### 1. Current State Mapping (The Diagnostic)
Document the actual flow of context (tokens), reasoning (LLM calls), and execution (tool use) for complex tasks.
- **Action:** Log the sequence of tool calls, context sizes, latencies, and locations of Jidoka halts.
- **Constraint:** NEVER optimize a workflow without first mapping its current state to identify the true bottlenecks.
- **Integration:** Directly uses findings from **Jidoka** and **Poka-yoke** logs.

### 2. Bottleneck & Muda Identification
Analyze the Current State Map to locate structural waste, focusing on Transportation (Context Bloat) and Over-processing.
- **Action:** Identify where the LLM spends the most tokens or where sequential calls could be parallelized.
- **Constraint:** Do not ignore "silent waste"—processes that work but are inefficient.
- **Integration:** Maps to the 7 Muda categories defined in **Lean Foundations**.

### 3. Future State Design
Design and propose an optimized architectural flow that maximizes deterministic output and minimizes waste.
- **Action:** Propose rearrangements, context summaries, or deterministic script bypasses.
- **Constraint:** MUST run a **KYT (Hazard Prediction)** pass on the proposed future state to ensure safety is not compromised for speed.
- **Integration:** Triggers a **Kaizen** event to implement the optimized flow.

## Escalation & Halting

- **Jidoka:** If VSM reveals clustering of Jidoka halts in a specific phase, trigger a mandatory Jidoka halt for that phase until it is redesigned.
- **Hō-Ren-Sō:** Use the Hōkoku (Report) protocol to present the Current and Future State maps to the user as a structured diagnostic.

## Implementation Workflow

1. **Trigger:** A workflow feels slow, expensive (token-wise), or frequently encounters hallucinations.
2. **Execute:** Trace the execution path, identify bottlenecks, and design a future state.
3. **Verify:** Use a Kaizen PDCA cycle to implement and test the optimized flow.
4. **Output:** A leaner, faster, and more reliable agentic process.
