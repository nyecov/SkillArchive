---
name: context-engine
version: 1.0.0
description: Use when required to retrieve information, learn codebase rules, read files over 4,000 tokens, or record short-term plans. This skill governs all agent memory operations via the MCP Server.
category: memory
level: technical
tags:
- memory
- mcp
- rag
- state
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Tools Management Strategy
  path: ../tools-management/SKILL.md
- name: Agent Querying Guide
  path: ./querying-guide.md
---

# Context Engine

This skill dictates how agents build, access, and maintain context. You do not store working memory or complex long-term dependencies in the chat history or unstructured flat files. You **MUST** delegate all context and memory retrieval to the deterministic `Context Engine` MCP server tools.
*Note: All memory artifacts handled by the server possess a permanent UUIDv4 and automatic version counter. You do not need to manage versioning yourself; simply use the tools and the server guarantees persistence across file moves and renames.*

## Core Mandates

### 1. Mandatory Tool Usage (The Orchestration Hook)
You are functionally blind to the broader workspace without the Context Engine.
- **Action:** You must ALWAYS use the `context-engine` MCP tools to observe files, document plans, and record facts.
- **Constraint:** NEVER attempt to write scratchpad-style notes or architectural summaries to raw `.txt` or `.md` files on disk manually.
- **Constraint (The Forbidden Zone):** It is a strict violation to use native file commands (e.g., `read_file`, `write_file`, `sed`, `cat`) on the `.gemini/mem` directory. You will corrupt the UUID/Version tracking, and the server will instantly quarantine and delete your manual edits.

### 2. The Scratchpad (Short-Term Memory)
The scratchpad prevents working-memory drift during multi-step tasks.
- **Action:** Use `log_session_finding` to record your current intent, any discovered bug, or phase change.
- **Action:** Use `read_session_state` to immediately regain situational awareness if you return from an error, or before initiating `shisa-kanko` pointing.
- **Constraint:** Do not clutter the scratchpad with irrelevant data. Log terse, actionable intelligence.
- **Integration (Tiered Limits):** The server enforces a Soft Limit (warning at 8k chars) and a Hard Limit (block at 10k chars). If you receive a Soft Limit Warning, you MUST immediately synthesize your findings into the long-term Ontology and prune the scratchpad.

### 3. The Knowledge Graph (Long-Term Memory)
The ontology acts as the permanent hard drive for agentic knowledge.
- **Action:** Use `commit_ontology_edge` to save permanent architectural rules (e.g., "Module A REQUIRES Module B").
- **Action:** Use `read_ontology_graph` when modifying a system to discover hidden upstream/downstream impacts before executing code.
- **Action:** Use `delete_ontology_edge` to remove outdated rules or break invalid circular dependencies.
- **Integration:** The ontology leverages DAG validation for hierarchical edges (`REQUIRES`, `DEPENDS_ON`, `OWNS`). It will automatically reject cyclic dependencies to prevent logical paradoxes. 
- **Constraint:** If you receive a Cycle Error, do not force it. You must either map it as a non-hierarchical edge (`REFERENCES`) or use `delete_ontology_edge` to refactor the broken graph logic first.

### 4. Token-Safe File Reading (Ingestion)
Standard file reading can destroy the LLM context window with minified data.
- **Action:** Use `ingest_context` to safely retrieve file chunks. It automatically token-caps the return to ~16,000 characters.
- **Integration:** The engine natively understands TOON, JSON, and standard code. Use the `query` parameter to force the engine to extract only the text relevant to your search.

## Escalation & Halting

- **Jidoka (Hard Limit/Cycle Block):** If `log_session_finding` throws a Hard Limit error, or `commit_ontology_edge` throws a Cycle Error, trigger a Jidoka halt automatically to resolve the architectural block.
- **Malformed Query Correction:** If the server returns an instructional `ToolError` regarding a malformed TOON/JSON parsing request, DO NOT GUESS. Follow the exact instructions provided by the server payload to format your next query correctly.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if the session scratchpad returns a corrupted history warning indicating a sudden OS or container crash.

## Implementation Workflow

1. **Trigger:** You are asked to perform a complex task, debug a problem, or map an architecture.
2. **Execute (Awareness):** Immediately run `read_session_state` to grab existing context. Use `ingest_context` on target files to safely retrieve chunks.
3. **Execute (Mutation):** Save your findings via `log_session_finding`.
4. **Output:** Complete your objective, ensuring any new system dependencies learned are hardened into the database via `commit_ontology_edge`.
