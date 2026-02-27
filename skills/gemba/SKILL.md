---
name: gemba
version: 1.1.0
level: methodology
description: Use to establish a factual baseline of the codebase. Mandates direct
  observation before reasoning.
category: cognition
tags:
- context
- methodology
- research
- lean
- TPS
references:
- name: RAG Strategy
  path: ../rag-strategy/SKILL.md
- name: Ontology
  path: ../ontology/SKILL.md
- name: Shisa Kanko
  path: ../shisa-kanko/SKILL.md
requires:
- rag-strategy
- ontology
---
# Gemba

Gemba is the "Real Place." This skill mandates that the agent establish a verified factual baseline before any reasoning. It orchestrates three modes of discovery:

## Core Mandates

### 1. Discovery Mode Selection
Determine the optimal tool to satisfy an information need based on the scope of the project.
- **Action:**
  - **Local/Direct (Gemba):** Reading known files (`read_file`).
  - **Global/Sparse (RAG):** Searching the workspace for keywords/semantics (`rag-strategy`).
  - **Structural/Relational (Ontology):** Querying the knowledge graph for dependencies (`ontology`).
- **Constraint:** NEVER guess a file path or a symbol's usage. 

### 2. Fact Verification
Every discovery MUST be verified as a "Current Reality" (Genchi Genbutsu).
- **Action:** Read the actual content of the discovered file or record the tool's raw output.
- **Constraint:** DO NOT rely on cached summaries or previous-turn assumptions.

## Escalation & Halting

- **Jidoka:** If a file's content contradicts the user's description or the model's prediction, trigger a Jidoka halt and perform a deeper search/read to resolve the discrepancy.
- **Hō-Ren-Sō:** Report any "Hidden Waste" (unused code, broken links, outdated comments) discovered during the observation.

## Implementation Workflow

1. **Trigger:** A new task is received or a context gap is identified.
2. **Select Mode:** Choose between Direct, RAG, or Ontology based on the information need.
3. **Discover:** Execute the chosen strategy to gather the facts.
4. **Verify:** Read the bytes/data to confirm reality.
5. **Output:** A high-signal factual foundation for the **Shisa Kanko** plan.
