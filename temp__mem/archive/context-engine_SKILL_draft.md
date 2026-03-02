---
name: context-engine
version: 1.0.0
level: methodology
description: 'Sovereign memory management for agents. Replaces isolated RAG, flat-file planning, and manual ontology with a unified, deterministic MCP Server interface to prevent context bloat and hallucination.'
category: cognition
tags:
- memory
- state-management
- methodology
- mcp
references:
- name: MCP Integration Governance
  path: ../interface-governance/SKILL.md
- name: Tools Management
  path: ../tools-management/SKILL.md
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
requires:
- mcp-context-engine-server
---

# Context Engine

Agents suffer from "goldfish memory"—forgetting context as the reasoning window rolls, hallucinating unverified "facts," or drowning in massive, un-chunked file dumps. 

The **Context Engine** solves this by forbidding the agent from managing its own memory through fluid markdown files. Instead, all context ingestion, session scratchpads, and long-term knowledge graphs are aggressively governed by the `mcp-context-engine-server`.

This skill dictates *when* and *how* the agent must invoke the MCP to manage its memory pipeline.

## Core Mandates

### 1. Ingestion via Tool (Never Raw File Dumps)
You are forbidden from pulling massive, un-chunked files directly into your context window if the file exceeds 4k tokens.
- **Action:** When searching for facts or code, trigger the MCP `ingest_context` tool. It natively handles semantic search, structural chunking, and token limit enforcement.
- **Constraint:** If a standard `view_file` operation fails due to length or causes you to lose focus, you MUST immediately switch to the `ingest_context` tool to retrieve a high-signal, de-noised payload.
- **Integration:** Replaces legacy `rag-strategy` by mechanizing the chunking logic.

### 2. The Volatile Scratchpad (Working Memory)
Do not rely on your internal conversational history to remember complex, multi-step tasks, research trails, or errors.
- **Action:** After every 2 major tool executions (or whenever an important decision is made), use the MCP `log_session_finding` tool to write your progress to the engine's deterministic state file.
- **Constraint:** Before making an architectural decision or starting a new phase of work, you MUST read the current session state via the MCP `read_session_state` tool. "Read Before Decide."
- **Integration:** Replaces legacy `plan-with-files` by enforcing strict API schemas for logging rather than allowing freeform markdown sprawl.

### 3. The Knowledge Graph (Long-Term Memory)
Hardened facts, architectural rules, and cross-domain dependencies must survive session resets. They must be stored programmatically, not as flat text.
- **Action:** When you discover a concrete dependency or rule (e.g., "Module A depends on Database B"), use the MCP `commit_ontology_edge` tool. 
- **Constraint:** NEVER store "loose" facts. All long-term knowledge must be strictly typed as Entities (Node) with directional Edges (`DEPENDS_ON`, `OWNED_BY`).
- **Integration:** Replaces legacy `ontology` by forcing the MCP server to validate the Directed Acyclic Graph (DAG) state, rejecting circular logic autonomously.

## Escalation & Halting

- **Jidoka (Schema/Token Halt):** If the MCP server rejects your tool call due to schema validation failures, or if the `ingest_context` tool repeatedly fails to find the required signal, invoke an autonomous halt. Do not attempt to guess or hallucinate the missing data.
- **Hō-Ren-Sō:** Escalate to the human operator if the Ontology Graph reveals conflicting dependencies (e.g., you are about to `commit` a rule that the MCP server rejects as a circular dependency).

## Implementation Workflow

1. **Trigger:** A codebase is too large, a task is too complex for working memory, or a hardened architectural rule is discovered.
2. **Execute:** 
   - **Ingest:** Call `ingest_context` instead of raw file reads.
   - **Process:** Call `log_session_finding` continuously to offload context pressure.
   - **Persist:** Call `commit_ontology_edge` to save the final distilled rules to the global Knowledge Graph.
3. **Verify:** Confirm via `read_session_state` that your findings were actually logged before proceeding to write code.
4. **Output:** A strict separation of concerns—the LLM focuses purely on logic, while the MCP server handles all memory state.

## Required MCP Tools Reference

*Note: The actual implementation logic for these tools lives entirely within the external MCP Server. Use its provided JSON schemas.*

- `ingest_context`: Takes a query and path; returns chunked, high-signal snippets below a strict token threshold.
- `log_session_finding`: Takes a string finding/error; appends to the current volatile session log.
- `read_session_state`: Returns the current serialized session log.
- `commit_ontology_edge`: Takes Entity A, Edge Type, and Entity B; commits to the permanent Knowledge Graph.
- `read_ontology_graph`: Takes an Entity; returns its connected dependencies and rules.
