---
name: rag-strategy
version: 1.0.0
level: tactical
description: 'Optimization of Retrieval-Augmented Generation.  Focuses on minimizing
  "Search Waste" (Motion Muda) by ensuring high-signal context retrieval and efficient
  chunking.\'
category: cognition
tags:
- context
- optimization
references:
- name: Gemba (Static Observation)
  path: ../gemba/SKILL.md
- name: Ontology (Structured Memory)
  path: ../ontology/SKILL.md
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
---

# RAG Strategy: Context Optimization

RAG (Retrieval-Augmented Generation) is the bridge between the agent's internal weights and the project's external facts. This skill optimizes that bridge, ensuring the agent doesn't drown in "Context Noise" or starve from "Information Gaps."

## Core Mandates

### 1. High-Signal Retrieval (Muda Reduction)
Minimize "Transportation Waste" (Context Bloat) by retrieving only the most relevant snippets.
- **Action:** Use semantic search, keyword filtering, and structural navigation (e.g., file trees) to isolate the target context.
- **Constraint:** NEVER pull more than 4k tokens of "Search Result" noise into the active reasoning window.
- **Integration:** Directly reduces **Motion Muda** (Navigational Waste).

### 2. Semantic Chunking & Relevance
Ensure that retrieved context includes enough surrounding structure to be meaningful.
- **Action:** Use "Context-Aware Chunking"—ensure that a retrieved line includes its parent function/class signature.
- **Constraint:** Avoid "Fragment Hallucinations" caused by snippets that lack structural context.
- **Integration:** Supports **Gemba (Static Observation)** by providing a "Walking the Floor" view of the code.

### 3. Retrieval Verification
Verify that the retrieved data actually answers the prompt before proceeding to implementation.
- **Action:** Perform a "Relevance Check" on the retrieved context. Does it contain the symbols, logic, or docs needed for the task?
- **Constraint:** If retrieval fails to provide the facts, do not "hallucinate" the missing data. Re-run the search with refined parameters.

## Escalation & Halting

- **Jidoka:** If 3+ search attempts fail to retrieve the necessary context, trigger a Jidoka halt to ask the user for the specific file or documentation path.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to report any "Missing Documentation" gaps discovered during the RAG process.

## Implementation Workflow

1. **Trigger:** A request requires knowledge outside the immediate context window.
2. **Execute:** 
   - Define the search target (The Information Need).
   - Execute the RAG query (Search/Retrieval).
   - Filter and rank the results for relevance.
3. **Verify:** Confirm the retrieved snippets provide the "True North" for the implementation.
4. **Output:** A high-signal, de-noised context payload ready for **Shisa Kanko** processing.
