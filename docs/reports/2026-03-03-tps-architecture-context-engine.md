# TPS Architecture Review: Context Engine

## 1. Shusa Strategy & Vision
**Vision:** Provide a highly stable, concurrent, and cross-platform Context Engine that serves as the infallible memory and state foundation for all autonomous agent operations.
**Misalignment Target:** The current reliance on full-file JSON serialization (for every mutation) and basic OS file-existence checks for singleton locking is deeply misaligned with the requirement for robust, concurrent stability, particularly on Windows.

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks:** 
  - Over-processing: The entire JSON ontology is read, parsed, mutated, serialized, and written to disk synchronously for every single edge addition.
  - Waiting: 15-second stale-out timeouts on the singleton lock when recovering from unclean shutdowns.
  - Overburden (Muri): Disk I/O strain on large graphs.
- **Future State Architecture:** 
  - Transition the Knowledge Graph (Ontology) to an embedded database (e.g., SQLite via `modernc.org/sqlite` or `bbolt`) to provide true ACID transactions, granular locks, and eliminate full-file rewrites.
  - Implement in-memory `sync.RWMutex` for the Scratchpad to safely handle concurrent MCP tool requests.
  - Replace the flaky file-existence singleton lock with a robust, cross-platform locking library (e.g., `gofrs/flock`) or process-level socket binding.

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** The storage format of `ontology.json` will change. Any external scripts or agents reading this file directly (bypassing the Context Engine MCP tools) will break.
- **Identified Conflicts:** Upgrading the storage layer requires a seamless, automated data migration path for users with existing `ontology.json` files to preserve their knowledge graphs.

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan:**
  1. **Batch 1 (Stabilize Current):** Introduce `sync.RWMutex` to the internal maps. Add `target_path` validation to `ingest_context`.
  2. **Batch 2 (Locking):** Rip out `pokayoke/singleton.go` and replace it with a proven cross-platform mutex library.
  3. **Batch 3 (Storage Interface):** Abstract the storage layer and implement the new DB backend alongside the JSON backend. Write the JSON-to-DB migration utility.
  4. **Batch 4 (Cutover):** Switch the MCP tool handlers (`HandleCommitOntologyEdge`, etc.) to use the new DB backend.
- **Critical Hazards Isolated:** 
  - Data loss during the JSON-to-DB migration (Point of No Return).
  - Deadlocks introduced by new `sync.RWMutex` logic.

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** 
  - If the migration utility encounters unparseable or corrupted JSON, the server MUST halt the boot sequence immediately (fail-safe) rather than starting with empty state.
  - If any MCP tool handler execution exceeds 2000ms, it indicates a potential deadlock or severe DB lock contention; trip the breaker and log a critical error.
- **Poka-yoke Interlocks:** 
  - The migration utility MUST automatically create an immutable `.bak` copy of `ontology.json` before any migration logic executes.
  - Strict interface decoupling between the MCP handlers and the Storage backend to allow easy fallback if the DB implementation fails in testing.
