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
  path: ../../../skills/shisa-kanko/SKILL.md
- name: Tools Management Strategy
  path: ../../../skills/tools-management/SKILL.md
- name: Agent Querying Guide
  path: ./querying-guide.md
---

# Context Engine

This skill dictates how agents build, access, and maintain context. You **MUST** delegate all context and memory retrieval to the deterministic `Context Engine` MCP server tools.

## Core Mandates

### 1. Mandatory Tool Usage
- **Action:** You must ALWAYS use the `context-engine` MCP tools to observe files, document plans, and record facts.
- **Constraint:** NEVER attempt to write notes directly to raw `.txt` or `.md` files in the `.gemini/mem` directory. Manual edits will be quarantined and reverted by boot-time diagnostics.
- **Provenance:** All memory artifacts possess a unique UUIDv4. The server guarantees persistence across file moves and renames.

### 2. The Scratchpad (Short-Term Memory)
- **Action:** Use `log_session_finding` to record intent, discovered bugs, or phase changes.
- **Action:** Use `read_session_state` to regain situational awareness before initiating `shisa-kanko`.
- **Limits:** The server enforces a Soft Limit (8k chars) and a Hard Limit (10k chars). If blocked, synthesize findings into the Ontology and prune the scratchpad.

### 3. The Knowledge Graph (Long-Term Memory)
- **Action:** Use `commit_ontology_edge` to save architectural rules (e.g., "Module A REQUIRES Module B").
- **Constraint:** Hierarchical edges (`REQUIRES`, `DEPENDS_ON`, `OWNS`) cannot create circular dependencies.
- **Integrity:** The system uses `ontology.json` with atomic `Sync()` writes. If a cycle error occurs, use `delete_ontology_edge` to refactor the broken graph logic.

### 4. Token-Safe Ingestion
- **Action:** Use `ingest_context` to safely retrieve file chunks. It automatically token-caps the return to ~16,000 characters to protect your context window.

## Escalation & Halting

- **Jidoka Halt:** If you hit a Hard Limit or Cycle Error, trigger a Jidoka halt immediately to resolve the block. 
- **Singleton Violation:** If the server fails to boot, ensure no other engine instances are active. The engine enforces a **Structural Singleton** guard to prevent state corruption.

## Implementation Workflow

1. **Awareness:** Run `read_session_state` and `ingest_context` to regain context.
2. **Mutation:** Save thoughts via `log_session_finding`.
3. **Synthesis:** Harden architectural facts into `commit_ontology_edge`.
