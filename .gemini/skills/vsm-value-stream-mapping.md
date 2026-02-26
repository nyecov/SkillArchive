---
name: vsm-value-stream-mapping
version: 1.1.0
description: >
  Use when diagnosing slow workflows, high token consumption, or unexplained latency in multi-step tasks.
  Handles current-state mapping, bottleneck identification, and future-state design for optimized flow.
category: diagnostics
tags: [vsm, mapping, architecture, bottlenecks, flow, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: Hansei (Self-reflection)
    path: ../hansei-self-reflection/SKILL.md
  - name: KYT (Hazard Prediction)
    path: ../kyt-hazard-prediction/SKILL.md
  - name: Hō-Ren-Sō (Communication)
    path: ../ho-ren-so-communication/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
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
  - Points where **Poka-yoke** interlocks were checked (and whether they passed or failed).

### 2. Identifying the Bottlenecks
Analyze the Current State Map to locate structural waste (Muda).
- **Questions to Ask:**
  - Where is the LLM spending the most tokens?
  - Are there sequential tool calls that could be parallelized?
  - Is there a "Contact Check" (**Poka-yoke**) that happens too late in the flow, causing wasted processing if it fails?
  - Are there unnecessary **Hansei** reflection loops that add latency without improving output quality?

### 3. Future State Design (The Target)
Design a more efficient, direct path.
- **Action:** Propose an optimized architectural flow. This often involves rearranging the order of operations, summarizing context before passing it to sub-agents, or introducing a fast deterministic script to bypass the LLM entirely for specific steps.
- **KYT Integration:** Run a lightweight **KYT** pass on the proposed Future State to ensure the optimization does not remove a critical safety check.

## Escalation & Reporting

- **Hō-Ren-Sō (Hōkoku):** The completed VSM map (Current State + Future State) SHOULD be reported to the human operator as a structured diagnostic. This gives the operator visibility into where the system spends its resources and what improvements are proposed.
- **Jidoka Correlation:** If the map reveals that **Jidoka** halts are clustering around a specific workflow phase, this is a strong signal that the phase needs a **Kaizen** redesign rather than individual fixes.

## Implementation Workflow

1. **Observe:** Run a complex task and trace the execution path.
2. **Map:** Output a visual or structured text representation of the steps (e.g., `User -> Prompt -> Agent (20k tokens) -> Tool A -> Agent (22k tokens) -> Output`).
3. **Analyze:** Classify the identified waste using the **Lean Principles** 7 Muda categories — focus on "Transportation," "Waiting," and "Over-processing."
4. **Improve:** Trigger a **Kaizen** event to restructure the workflow toward the Future State Map.
5. **Verify:** After the Kaizen change is applied, re-run the map to confirm the bottleneck has been resolved.
