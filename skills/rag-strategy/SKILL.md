---
name: rag-strategy
version: 1.1.0
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
- name: Context Heijunka Tool
  path: ../../tools/context-heijunka/description.md
---

# RAG Strategy

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
- **Integration:** Aligns with **Shisa Kanko** by empirically verifying the retrieved context before execution.

### 4. Multi-Modal Ingestion (Tool Utilization)
Do not limit context retrieval to just code or text files; utilize custom tooling to ingest rich context formats when required.
- **Action:** Utilize the project's specific python tools (e.g., `youtube_transcript.py`, `pdf_tools.py`, `docx_tools.py`) to scrape, parse, and ingest non-text data formats into the reasoning window.
- **Constraint:** ALWAYS pipe the output of these tools through the **Context Heijunka Chunker** (`context_chunker.py`) if the resulting raw text exceeds the 4k token limit.
- **Integration:** Aligns with **Tools Management** to prioritize deterministic python scripts over hallucinated manual parsing.

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
4. **Output:** A high-signal, de-noised context payload ready for **Shisa Kanko** processing, documented via the Poka-yoke Output Template.

## Poka-yoke Output Template

When retrieving external knowledge, the agent MUST output the completed manifest using the exact schema defined in the Poka-yoke Output Template to prevent context bloat and hallucination.

[RAG Context Manifest Template](templates/rag-context-manifest.md)
