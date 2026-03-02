# Context Engine: Agent Querying Guide

This guide defines the explicit technical constraints and error-handling protocols for interacting with the Context Engine MCP Server.

## 1. Interaction Constraints (Latency)
The server executes with a strict host-defined `CONTEXT_TIMEOUT_MS` (typically 5000ms).
- **Protocol:** If a tool call times out, do not retry immediately with the exact same payload. Reduce your `query` scope, ensure the target file is not locked by another process, and retry.

## 2. Ingestion & File Formats
You must use `ingest_context` for reading files. It naturally understands JSON and standard Code.
- **TOON Decoding:** The engine parses TOON (Token-Oriented Object Notation). If you receive an error stating `ToolError: Malformed Query`, it means your target TOON file or JSON request violates the strict schema.
- **Action:** Read the specific instructional payload returned by the error. Do not hallucinate the missing data. Re-format your request to match the schema referenced in the error and re-fire.

## 3. The Tiered Memory Guardrail (Scratchpad Limits)
The `current_session.json` state cannot grow infinitely.
- **The Soft Limit:** Handled by the engine at 8,000 characters. If your `log_session_finding` call returns a payload ending with `[WARNING: SCRATCHPAD SOFT LIMIT REACHED]`, you are entering the danger zone.
- **Action:** Immediately read the session state, distill the core findings into the Ontology graph, and cull the unneeded scratchpad entries using `delete_session_finding` or `clear_session_state`.
- **The Hard Limit (Jidoka Halt):** Handled by the engine at 10,000 characters. Any attempt to write to the scratchpad will be hard-rejected with a block error. You MUST prune the session memory before you are permitted to continue.

## 4. Ontology Resolution
- **Hierarchical Edges:** `REQUIRES`, `DEPENDS_ON`, `OWNS`. These will fail if they create a cyclic loop (A -> B -> A).
- **Non-Hierarchical Edges:** `REFERENCES`, `CONFLICTS_WITH`. Use these for bidirectional documentation loops or API cross-talk.
- **Resolution:** If you trigger a Cycle Error legitimately, use `delete_ontology_edge` to destroy the outdated hierarchy rule creating the blockage before committing the new correct edge. The system utilizes `ontology.json` for high-integrity storage with atomic `Sync()` writes.
