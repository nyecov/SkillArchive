# TPS Architecture Review: Semantic Graph Upgrade (SQLite FTS5)

## 1. Shusa Strategy & Vision
The core vision of the `context-engine` is to provide lightweight, dependency-free, and deterministic memory to agent swarms. The current exact-match graph traversal creates a bottleneck for LLMs trying to recall historical UUIDs or node strings. The strategy is to introduce a fuzzy/semantic search fallback using native SQLite FTS5, maintaining the zero-dependency vision while drastically improving agent UX and context retention.

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks:** Agent reads graph -> Exact string mismatch -> Graph returns empty -> Agent hallucinates or halts. This is Transportation Waste (Context Lost).
- **Future State Architecture:** Agent reads graph -> Mismatch -> Falls back to `search_ontology_semantic` -> Retrieves ranked matches -> Agent uses correct target entity string for precise DAG traversal.

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** Only affects `sqlite.go` (schema), `ontology.go` (data access layer), and `main.go` (MCP tool registration).
- **Identified Conflicts:** The primary conflict is ensuring that the new `AFTER INSERT/UPDATE/DELETE` triggers do not lock the `ontology_edges` table during Swarm concurrent writes (WAL mode handles this).

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan:**
  1. Migrate Schema (`sqlite.go` virtual table + triggers).
  2. Implement Go Data Access (`ontology.go` FTS query).
  3. Register MCP Tool (`main.go`).
  4. Write BDD Tests (`test_ontology.py`).
- **Critical Hazards Isolated:** If the SQLite triggers are malformed, they could crash the main `commit_ontology_edge` inserts, completely breaking the Context Engine's core functionality.

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** Any failure in `test_ontology.py` related to basic inserts or reads must immediately trip the Andon cord and halt the deployment.
- **Poka-yoke Interlocks:** The schema migration MUST be wrapped in a transaction, and the MCP `query` MUST be sanitized to prevent SQL injection.