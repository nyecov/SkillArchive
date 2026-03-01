---
name: nemawashi
version: 1.1.0
description: Use before suggesting major refactors or architectural changes. Mandates
  impact analysis and A3 proposals.
category: methodology
tags:
- methodology
- lean
- TPS
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Ho-Ren-So (Communication)
  path: ../ho-ren-so/SKILL.md
level: methodology
requires:
- ho-ren-so
---
# Nemawashi

Nemawashi is the practice of quietly laying the foundation for a change. In agentic engineering, this means performing deep dependency analysis and "socializing" a proposed strategy with the user before touching the codebase, ensuring no surprises or regressions.

## Core Mandates

### 1. Dependency Mapping
- **Action:** Before suggesting a fix, the agent MUST trace the "ripples" of the change across the entire workspace (imports, side effects, downstream tests).
- **Constraint:** NEVER propose a change based solely on the local file context without checking for global usage of the affected symbols.
- **Integration:** Uses **Grep** and **Glob** tools to perform "Digital Nemawashi" (gathering data) before the "Strategy" phase.

### 2. Strategic Consensus (The A3 Proposal)
- **Action:** Present findings to the user using the **A3 Proposal format** to secure alignment.
- **Constraint:** Do not proceed with high-risk refactors until the A3 "Foundation" is acknowledged by the user.
- **Integration:** Feeds directly into **Ho-Ren-So** (Sōdan) for structured decision-making.

## Escalation & Halting

- **Jidoka:** If the impact analysis reveals a "Breaking Change" or a conflict with a project **Anchor**, halt and request specific guidance.
- **Hō-Ren-Sō:** Report identified risks early in the Research/Strategy phase, not during Execution.

## Implementation Workflow

1. **Trigger:** A request for a significant modification or refactor is identified.
2. **Execute:** 
   - Identify all files that import or depend on the target code.
   - Evaluate potential side effects on state or performance.
   - Formulate a "Foundation Report" (Proposed Strategy + Impact Analysis).
3. **Verify:** User confirms the approach (Consensus).
4. **Output:** A de-risked Strategy ready for surgical execution, documented via the Poka-yoke Output Template.

## Poka-yoke Output Template

When proposing a major refactor or architectural change, the agent MUST format the proposal using the exact schema defined in the Poka-yoke Output Template.

[A3 Proposal Template](templates/a3-proposal.md)
