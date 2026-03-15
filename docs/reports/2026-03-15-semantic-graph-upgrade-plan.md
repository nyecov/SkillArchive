# Context Engine Upgrade Plan: Semantic Graph Traversal (Hybrid RAG)

## Objective
Enhance the existing `context-engine` Middle-Term memory (Ontology Graph) with semantic search capabilities. Currently, agents must recall exact `target_entity` node names to use `read_ontology_graph`. This upgrade will allow agents to perform fuzzy/semantic searches across the ontology, merging deterministic DAG logic with forgiving RAG retrieval.

## Strategy: SQLite FTS5 (Full-Text Search)
Instead of introducing a heavy vector embedding dependency (like a local vector DB or an external API) to a lightweight Go server, we will implement **SQLite FTS5** as the first iteration. FTS5 provides excellent semantic-like fuzzy search (BM25 ranking) over the graph's nodes and relationships without architectural bloat. If true vector embeddings are required later, we can migrate to `sqlite-vec`.

## Phase 1: Database Schema Migration
**Target:** `skills/context-engine/server/internal/storage/sqlite.go`

1. **Enable FTS5:** Ensure the `modernc.org/sqlite` driver supports FTS5 (it does by default).
2. **Create Virtual Table:** Add a migration step in `InitDB()` to create an FTS5 virtual table linked to the `ontology_edges` table.
   ```sql
   CREATE VIRTUAL TABLE IF NOT EXISTS ontology_fts USING fts5(
       source_entity, 
       target_entity, 
       edge_type, 
       content=ontology_edges, 
       content_rowid=id
   );
   ```
3. **Database Triggers:** Create SQLite triggers to automatically keep the FTS index in sync when `commit_ontology_edge` or `delete_ontology_edge` is called.
   ```sql
   CREATE TRIGGER IF NOT EXISTS ontology_ai AFTER INSERT ON ontology_edges BEGIN
       INSERT INTO ontology_fts(rowid, source_entity, target_entity, edge_type) 
       VALUES (new.id, new.source_entity, new.target_entity, new.edge_type);
   END;
   -- (Add similar triggers for DELETE and UPDATE)
   ```

## Phase 2: Go Server Implementation
**Target:** `skills/context-engine/server/internal/ontology/ontology.go`

1. **New Backend Function:** Add `SearchOntologyFTS(query string) ([]Edge, error)` to query the FTS table using the `MATCH` operator and rank results.
   ```sql
   SELECT source_entity, target_entity, edge_type 
   FROM ontology_fts 
   WHERE ontology_fts MATCH ? ORDER BY rank LIMIT 10;
   ```

## Phase 3: MCP Interface Extension
**Target:** `skills/context-engine/server/cmd/server/main.go`

1. **Define New Tool:** Register a new MCP tool: `mcp_context-engine_search_ontology_semantic`.
   - **Description:** "Searches the Knowledge Graph for entities and relationships using fuzzy/semantic keyword matching. Use this when you forget the exact node name."
   - **Parameters:**
     - `query` (string): The search query (e.g., "Redis cache", "authentication").
2. **Implement Tool Handler:** Map the MCP tool execution to the `SearchOntologyFTS` function. Return a structured JSON array of matching edges so the agent can discover the exact `target_entity` names for subsequent DAG traversal.

## Phase 4: Validation & Testing
**Target:** `skills/context-engine/testing/test_ontology.py`

1. **Unit Tests:** Add a new BDD test `test_semantic_search` to verify:
   - Inserting a complex edge (e.g., `source: "OAuth2_Service", target: "Postgres_DB"`).
   - Querying the FTS endpoint with a fuzzy term like `"auth database"`.
   - Ensuring the correct edge is returned despite exact string mismatch.
2. **Jidoka Safeguards:** Ensure malformed FTS queries gracefully return empty lists rather than crashing the SQL driver.

## Phase 5: Documentation & Maturation
**Target:** `skills/context-engine/SKILL.md` & Web UI

1. **SKILL.md Update:** Document the new tool and the workflow change (e.g., "If `read_ontology_graph` fails due to exact match failure, fallback to `search_ontology_semantic` to discover the node").
2. **Web UI Extension:** (Optional) Add a search bar to the Graph view in `webui/index.html` calling a new `/api/graph/search` endpoint to visually highlight matching nodes.

---
**Next Steps:** If approved, we will begin execution with Phase 1 by updating `sqlite.go` with the FTS schema.