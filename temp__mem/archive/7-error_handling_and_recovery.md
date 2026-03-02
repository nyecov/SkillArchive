# Context Engine: Error Handling, Memory Corruption, and Edge Cases

Because this server serves as the sole arbiter of agent memory, it must be exceptionally robust. Given the selection of **Go**, we can leverage its strict typing and fast concurrency to deploy severe Poka-yoke validation and graceful Jidoka failure modes.

Here is how the Context Engine will handle failure scenarios natively:

## 1. Handling Memory Corruption on Disk
*The Scenario: The Docker container crashes mid-write, the host machine restarts, or a human manually edits the `session_state.json` file and breaks the syntax.*
- **Detection:** Go's `encoding/json` or custom TOON parser will immediately throw a syntax or unmarshalling error upon reading the `current_session.json` or `ontology.yaml` at the start of any tool invocation.
- **Recovery Strategy (The Quarantine Protocol):** The Go server will NOT crash. Instead, it will:
  1. Rename the corrupted file (e.g., `current_session.json` -> `current_session.corrupted_171012.json`).
  2. Initialize a fresh, empty state file.
  3. Return a highly descriptive `ToolError` to the agent via MCP: `"ERROR: Your memory file was corrupted. It has been backed up to [path]. A fresh session has been started. Please review the backup file via standard file reading if you need to recover old context."`
- **Result:** The agent is explicitly aware that memory was lost, without the server daemon crashing.

## 2. Handling "Wrong Data" (Hallucinations)
*The Scenario: The LLM tries to commit a rule to the Ontology using a non-existent edge type, or tries to log a string disguised as a JSON object into a TOON file.*
- **Detection:** The MCP JSON Schema inherently prevents invalid arguments from even reaching the tool logic. If the LLM sends `"edge_type": "MIGHT_NEED"`, the MCP protocol rejects it because it is not in the strict `["REQUIRES", "IMPLEMENTS", ...]` enumeration.
- **Recovery Strategy:** The server returns `InvalidParams` according to the MCP spec. The LLM immediately sees: *"Must be one of: REQUIRES, IMPLEMENTS..."* and corrects itself on the very next inference step.

## 3. Handling Concurrent Memory Writes (Race Conditions)
*The Scenario: Two agents (or two tool calls in rapid parallel succession) try to execute `log_session_finding` at the exact same millisecond.*
- **Detection:** Standard filesystem read/writes will clobber each other.
- **Recovery Strategy:** The Go server will employ strict **OS-level File Locking** (e.g., using a library like `gofrs/flock`).
  - When tool A triggers, it locks `current_session.json`.
  - Tool B waits securely (blocking) for the lock to release.
  - Because Go handles concurrency phenomenally well, the delay is unnoticeable to the LLM, but state collisions are mathematically prevented.

## 4. Handling Logical Edge Cases (The Circular Graph)
*The Scenario: The agent learns a fact: `Database -> DEPENDS_ON -> Network`. Later, it hallucinates or misreads a file and tries to commit `Network -> DEPENDS_ON -> Database`.*
- **Detection:** The `ontology` module will load the YAML graph into memory as a Directed Graph. It will run a fast Cycle Detection algorithm (like Depth-First Search) inserting the *proposed* edge.
- **Recovery Strategy:** If a cycle is detected, the commit is actively denied, and the database is not written. The tool returns: `"ERROR: Committing this edge creates a circular dependency in the graph. State reverted."`
- **Result:** The agent cannot poison its own permanent long-term memory with logical paradoxes.

## 5. Handling Massive Files (The "Zip Bomb" Scenario)
*The Scenario: The agent uses `ingest_context` on a massive 500MB log file or minified JS bundle.*
- **Detection:** Go can easily stat the file size before opening the entire byte stream.
- **Recovery Strategy:** If the file exceeds a sane threshold (e.g., >5MB), the server refuses to read the whole object into RAM. It either falls back to reading just the first 4k tokens sequentially, or rejects it with an error: `"File too large for standard ingestion. Use a specialized log-parsing tool."`
