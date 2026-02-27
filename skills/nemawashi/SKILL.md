---
name: nemawashi
version: 1.0.0
description: >
  Use to lay the groundwork for changes through impact analysis and consensus building. 
  Ensures all dependencies are identified and stakeholders are aligned before a "Directive" is executed.
category: lean-principles
tags: [nemawashi, consensus, alignment, impact-analysis, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Ho-Ren-So (Communication)
    path: ../ho-ren-so-communication/SKILL.md
---

# Nemawashi (Foundation Building)

Nemawashi is the practice of quietly laying the foundation for a change. In agentic engineering, this means performing deep dependency analysis and "socializing" a proposed strategy with the user before touching the codebase, ensuring no surprises or regressions.

## Core Mandates

### 1. Dependency Mapping
- **Action:** Before suggesting a fix, the agent MUST trace the "ripples" of the change across the entire workspace (imports, side effects, downstream tests).
- **Constraint:** NEVER propose a change based solely on the local file context without checking for global usage of the affected symbols.
- **Integration:** Uses **Grep** and **Glob** tools to perform "Digital Nemawashi" (gathering data) before the "Strategy" phase.

### 2. Strategic Consensus
- **Action:** Explicitly state the *impact* of a proposed change and wait for user acknowledgment or directive.
- **Constraint:** Do not proceed with high-risk refactors or deletions until the "Foundation" (user alignment) is solid.
- **Integration:** Feeds directly into **Ho-Ren-So** to provide structured options and observations.

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
4. **Output:** A de-risked Strategy ready for surgical execution.
