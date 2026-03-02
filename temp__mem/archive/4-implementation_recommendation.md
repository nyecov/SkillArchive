# Context Engine Implementation: Architecture Recommendation

After auditing the `Skill Archive`'s structural guidelines—specifically `skills/tools-management` and `skills/interface-governance`—the optimal implementation path for the Context Engine is clear.

## The Verdict: MCP Server + Skill Wrapper

The Context Engine **MUST be implemented as an MCP Server**, accompanied by a single `skills/context-engine/SKILL.md` instruction file. 

Implementing it as a simple local script (`context_operator.py`) is architecturally insufficient for this specific use case.

## Justification (Based on Archive Rules)

### 1. The "Complex State" Mandate (`tools-management`)
According to `tools-management`, simple filesystem operations can be shell scripts, but **"complex state management... or proprietary data handling [must be delegated] to MCP Servers."**
Because the Context Engine handles the `ontology` capability (which requires mutating a semantic Knowledge Graph and ensuring no circular dependencies in a DAG), it crosses the threshold of "complex state." 

### 2. Built-in Poka-yoke (Schema Enforcement)
Our Lean Analysis identified that the engine needs rigid guardrails to prevent AI hallucinations. 
As defined in `interface-governance`, MCP Servers inherently provide **Rigorous Schema Enforcement**. Every tool exposed by an MCP server (e.g., `ingest_context`, `commit_entity`) requires a strict JSON Schema. If the LLM tries to input unstructured data, the MCP protocol automatically rejects it, providing the exact "Error Prevention" (Poka-yoke) we need without writing custom CLI parsing logic.

### 3. Modularity and Sandboxing
By building the Context Engine as an MCP Server (ideally running in a Docker container), you completely isolate the memory database (JSON files, SQLite, or a Vector DB for RAG) from the agent's immediate workspace. The agent cannot accidentally delete its own brain; it must interact with it through the governed JSON-RPC interface.

## Recommended Architecture

1. **The Tool (The MCP Server):**
   - **Format:** Python or TypeScript MCP Server (Dockerized for drop-in usage across workspaces).
   - **Exposed Tools:** `query_rag`, `log_session_finding`, `commit_ontology_edge`, `read_graph`.
   - **Role:** Handles all read/write logic, token counting, chunking algorithms, and strict schema validation.

2. **The Mindset (The Skill):**
   - **Format:** `skills/context-engine/SKILL.md`
   - **Role:** A concise user manual. It does not explain *how* to parse a file. It only teaches the agent *when* to use the MCP tools (e.g., "If you learn a new domain rule, call `commit_ontology_edge`").

3. **Cleanup:**
   - Deprecate `rag-strategy`, `plan-with-files`, and `ontology`.

## Conclusion
A script is too weak for structural graph memory. A native MCP Server is the exact technology built to solve the Context Window problem.
