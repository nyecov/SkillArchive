---
name: gemba
version: 1.2.0
level: methodology
description: Use to establish a factual baseline of the codebase. Mandates direct observation before reasoning and enforces a structured discovery report.
category: cognition
tags:
- context
- methodology
- research
- lean
- TPS
references:
- name: rag-strategy
  path: ../rag-strategy/SKILL.md
- name: ontology
  path: ../ontology/SKILL.md
- name: shisa-kanko
  path: ../shisa-kanko/SKILL.md
- name: genchi-genbutsu
  path: ../genchi-genbutsu/SKILL.md
requires:
- rag-strategy
- ontology
---

# Gemba

Gemba is the "Real Place." This skill mandates that the agent establish a verified factual baseline before any reasoning. It orchestrates three modes of discovery and enforces a rigid output reporting structure to avoid assumptions.

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
- **Constraint:** DO NOT rely on cached summaries or previous-turn assumptions. All discovery MUST culminate in a formal Gemba Discovery Report (see Workflow).

## Escalation & Halting

- **Jidoka:** If a file's content contradicts the user's description or the model's prediction, trigger a Jidoka halt and perform a deeper search/read to resolve the discrepancy.
- **Hō-Ren-Sō:** Report any "Hidden Waste" (unused code, broken links, outdated comments) discovered during the observation.

## Implementation Workflow

1. **Trigger:** A new task is received or a context gap is identified.
2. **Execute:** 
   - Choose between Direct, RAG, or Ontology. 
   - Execute the chosen strategy to gather the facts.
   - Cross-reference with the `genchi-genbutsu` mandate to ensure raw proof is captured if necessary.
3. **Verify:** Read the bytes/data to explicitly confirm reality. Ensure no hallucinated paths or logic exist in your working memory.
4. **Output:** A high-signal factual foundation for the **shisa-kanko** plan. You MUST output the following exact template:

```markdown
### Gemba Discovery Report
- **[OBSERVED FILES]:** 
  - `[list of absolute paths read]`
- **[KEY FACTS]:** 
  - `[bulleted list of verifiable data points]`
- **[DISCREPANCIES]:** 
  - `[none / or specifically detail contradictions between expectations and reality]`
```
