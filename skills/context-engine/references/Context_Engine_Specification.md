# Context Engine: Master Specification

This document synthesizes and supersedes all prior analysis, requirements, schematics, and strategy documents regarding the **Context Engine MCP Server**. Those documents and all iterations leading up to this point have been moved to the `/archive` folder.

This is the singular, authoritative blueprint for building and deploying the deterministic AI memory platform.

---

## 1. Core Architectural Vision

The Context Engine replaces fluid, unstructured markdown-based memory skills (`rag-strategy`, `plan-with-files`, `ontology`) with a sovereign, strictly-typed local server. 
It removes the cognitive load of memory management from the LLM, offloading it to a deterministic **Model Context Protocol (MCP)** server built in **Go**.

### 1.1 Deployment & Containerization
- **Runtime:** Go 1.22+ (chosen for its robust standard library, native concurrency, and ability to compile to tiny static binaries without a heavy runtime engine like Node or Python).
- **Container Strategy:** A minimal `<15MB` image generated via a multi-stage Dockerfile utilizing a `scratch` base image.
- **Protocol:** MCP `stdio` JSON-RPC over Docker standard pipes (with `tty: false` strictly enforced).
- **Latency Control:** The server's operations are bounded by a user-configurable timeout injected via the `docker-compose.yml` environment variable `CONTEXT_TIMEOUT_MS`.
- **Storage Strategy:** Stateless inside the container. All data read/writes are mapped to the host's `.gemini/mem` directory via a `volumes:` mount in `docker-compose.yml`.

---

### 1.3 Memory Provenance (Identity & Tracking)
To ensure memories can iterate, move seamlessly, and be renamed without losing their identity, all memory files generated or managed by the engine must adhere to strict Provenance tracking:
- **UUIDv4 Identity:** Every single memory artifact (Scratchpad note, Ontology Node, Interview Pattern) MUST receive an immutable, unique identifier.
- **Fast Collision Check (The Registry Heuristic):** Even though UUIDv4 collisions are astronomically rare, the Go server must physically guarantee uniqueness. It maintains a lightweight, in-memory `map[string]filepath` of all active UUIDs loaded during engine boot (by scanning `.gemini/mem`). When generating a *new* UUID, the server performs a fast `O(1)` map lookup. If a collision is magically detected, it loops to generate a new one until absolute uniqueness is confirmed before writing to disk.
- **Version Counter:** Every file must maintain a `version` integer that increments atomically upon any mutation by the server.
- **Atomic Residency (TPS Reliability):** All state mutations MUST utilize SQLite WAL mode combined with robust connection pooling to guarantee data persistence during power failure and support Swarm concurrency.
- **Persistence Mechanism:** For all memory tiers (Short/Middle/Long), records are persisted in localized tables within `engine.db`.

---

## 2. Poka-yoke & Edge Case Handling

The engine acts as the final guardrail against agent hallucination and system context bloat. It handles errors natively:

1. **State Corruption (Drive Failure/Human Error):**
   - If the server detects a corrupt SQLite database file (`engine.db`), it will instantly fail `PRAGMA integrity_check` and quarantine the database.
   - It will return an explicit `ToolError` warning the agent of the corruption.
2. **Type/Enum Hallucinations & Query Feedback:**
   - LLM errors (like inventing random Edge Types) are inherently blocked by the MCP JSON Schema. The server returns standard `InvalidParams`, forcing the agent to retry with the correct Enum.
   - For malformed queries, the server MUST return a rich, instructional `ToolError` message exactly outlining *why* the query failed and *how* the agent should correct it. Do not return empty strings or raw stack traces.
3. **Automated Boot Diagnostics (Self-Check):**
   - Upon container boot or reboot, the Go server MUST execute a complete schema verification sequence across the SQLite database `engine.db` in `.gemini/mem`. 
   - It validates structural constraints via `PRAGMA integrity_check`. If a corruption or unauthorized circumvention is detected at boot, the server halts loading and outputs a detailed forensic log to `engine_diagnostics.log`.
4. **Concurrency (Swarm Parallelism):**
   - The Go server utilizes an embedded SQLite database in WAL (Write-Ahead-Log) mode.
   - **Multi-Agent Orchestration:** Replacing the legacy single-file Lock, WAL mode native driver locks allow multiple Context Engines initiated by different LLM threads to safely coordinate against the single persistent `engine.db` concurrently.
5. **The "Zip-Bomb" Guardrail:**
   - `ingest_context` executes a pre-read byte-stat. If a file exceeds a safe threshold (e.g., 5MB), it rejects the payload entirely.
6. **Tiered Context Limits (The Infinite Growth Guardrail):**
   - The volatile scratchpad state cannot grow infinitely without exceeding LLM context windows.
   - **Soft Limit:** If the file exceeds 8,000 characters, the server appends a system warning instructing the agent to prune unused memory.
   - **Hard Limit (Jidoka Halt):** If the file exceeds 10,000 characters, the server actively rejects new write requests with a strict error, forcing the agent to prune state before proceeding.
7. **Token Count Heuristic (Go Limitation Pivot):**
   - Go lacks native LLM tokenizer libraries (like `tiktoken`). Importing a heavy third-party dictionary would violate the `<15MB` binary footprint rule.
   - **Solution:** The server implements a fast String Length heuristic. It hard-caps `ingest_context` returns at roughly **16,000 characters** rather than specific tokens. This $O(1)$ byte-calculation natively secures the context window with zero overhead.
6. **Ontology Cycle Detection & Resolution:**
   - Committing a strict hierarchical edge (`REQUIRES`, `DEPENDS_ON`, `OWNS`) to the Knowledge Graph triggers a Depth-First-Search cycle-check. Circular reasoning (`A -> B -> A`) is actively rejected via an MCP error.
   - **Resolution Strategy:** If an agent discovers a legitimate cycle (e.g., refactoring logic where two modules mutually depend on each other, or cyclic document references), it must use the newly provided `delete_ontology_edge` tool to break the existing incorrect hierarchy before committing the newly discovered ground truth, or it must use non-hierarchical edge types (like `REFERENCES` or `CONFLICTS_WITH`) which bypass the DAG cycle block.

---

## 3. Skill Enforcement Strategy

If the agent is not forced to use the engine, it will revert to standard file-reading. We enforce its usage at three layers:

1. **The Orchestration Layer:** The engine is permanently bolted to the agent's core `system_instructions.txt` or `skills-config.json` configuration as a global, non-negotiable dependency.
2. **The Methodology Layer (Shisa Kanko):** The master workflow `skills/shisa-kanko/SKILL.md` is updated to include a hard block: *"You MUST execute `read_session_state` and `log_session_finding` before engaging the pointing protocol."*
3. **The Poka-yoke Layer (Obfuscation):** The legacy `rag-strategy`, `plan-with-files`, and `ontology` skills are **deleted**. The agent is left with NO alternative documentation on how to perform memory tasks except via the Context Engine MCP tools.
4. **The Physical Guardrail (Circumvention Prevention):** Because `.gemini/mem` is a physical directory, an agent could theoretically use raw bash or python scripts to read/write the databases directly. To prevent this:
   - **Environment Blacklisting:** The `.gemini/mem` directory MUST be added to the workspace's `.gitignore` and any agent-specific ignore files (e.g., `.cursorignore`, `.aiderignore`).
   - **Procedural Hard-Block:** The `context-engine` skill explicitly declares native file manipulation on `.gemini/mem` as a Jidoka Violation.
   - **SQLite Corruption Guard:** If the agent *does* attempt to manually edit SQLite binaries directly, it will likely corrupt the WAL. The server's start-up audit will detect this via PRAGMA assertions, quarantine the DB, and restart the swarm, rendering LLM circumvention futile.

---

## 4. MCP Tool JSON Schemas

The server exposes 5 precise tools to the LLM Client.

### 4.1. `ingest_context`
Ingests a file, safely chunking it using the 16,000-character heuristic. Natively splits and parses **TOON (Token-Oriented Object Notation)**, JSON, and Markdown.
```json
{
  "properties": {
    "target_path": { "type": "string", "description": "Absolute/relative path to the file to ingest." },
    "query": { "type": "string", "description": "(Optional) Specific keyword query to extract relevant chunks." }
  },
  "required": ["target_path"]
}
```

### 4.2. `log_session_finding`
Appends a single thought or decision to the volatile short-term scratchpad database table. Enforces a sliding-window array size limit.
```json
{
  "properties": {
    "finding_text": { "type": "string" },
    "phase": { "type": "string", "enum": ["planning", "execution", "verification", "blocked"] }
  },
  "required": ["finding_text", "phase"]
}
```

### 4.3. `read_session_state`
Quickly retrieves the latest short-term memory array to regain situational awareness and the active phase.
```json
{
  "properties": {},
  "required": []
}
```

### 4.4. `delete_session_finding`
Removes a specific finding from the volatile scratchpad by its `index`. Essential for pruning distilled thoughts or managing the 10,000-character Hard Limit.
```json
{
  "properties": {
    "index": { "type": "number", "description": "The 0-based index of the finding to delete." }
  },
  "required": ["index"]
}
```

### 4.5. `clear_session_state`
Resets the volatile scratchpad, permanently deleting all short-term session findings in a single atomic action. Highly efficient for bulk cleanup after a phase completes.
```json
{
  "properties": {},
  "required": []
}
```

### 4.6. `commit_ontology_edge`
Mutates the permanent `.gemini/mem/engine.db` Directed Graph. Hierarchical edges fail if a cycle is created.
```json
{
  "properties": {
    "source_entity": { "type": "string" },
    "edge_type": { "type": "string", "enum": ["REQUIRES", "IMPLEMENTS", "DEPENDS_ON", "OWNS", "REFERENCES", "CONFLICTS_WITH"] },
    "target_entity": { "type": "string" }
  },
  "required": ["source_entity", "edge_type", "target_entity"]
}
```

### 4.7. `delete_ontology_edge`
Removes an existing edge from the Knowledge Graph. Critical for resolving DAG cycle errors and refactoring outdated architectural rules (Downgrading memory).
```json
{
  "properties": {
    "source_entity": { "type": "string" },
    "edge_type": { "type": "string" },
    "target_entity": { "type": "string" }
  },
  "required": ["source_entity", "edge_type", "target_entity"]
}
```

### 4.8. `read_ontology_graph`
Given a target entity, traverses the graph to return all established upstream and downstream architectural dependencies.
```json
{
  "properties": {
    "target_entity": { "type": "string" }
  },
  "required": ["target_entity"]
}
```



## 6. Persistent Operations (Daemon Mode)

To eliminate "Cold Start" latency associated with ephemeral Docker container instantiation, the system supports a **Persistent Daemon Mode**. 

### 6.1. Architectural Pattern
- **Persistence Layer**: A long-running container named `context-engine-daemon` remains resident in memory.
- **Connection Proxy**: MCP Clients invoke a lightweight `connect.ps1` or `connect.sh` script instead of `docker run`.
- **Latency Reduction**: This bypasses the Docker Engine's container lifecycle management, reducing tool-call latency from `~1.5s` to `~0.1s` (native execution speed).

### 6.2. Reliability & Wa
- **Jidoka Monitoring**: The daemon preserves the same Poka-yoke boot diagnostics and file-locking logic.
- **Lifecycle**: If the container crashes or is killed, the connection script automatically detects the absence and re-triggers `docker-compose up -d`.

---

## 7. Next Steps for Implementation
The system is now fully verified for both ephemeral and persistent residency.
