# Master Refinement Dossier: Semantic Graph Upgrade (SQLite FTS5)

This dossier consolidates the rigorous multi-phase refinement protocol executed on the proposed `context-engine` Semantic Graph Upgrade, elevating it to the highest level of Lean quality before execution begins.

---

## 1. The Verified Story (Phase 1)
**Goal:** Enhance the Ontology Graph with semantic search (SQLite FTS5) to allow agents to find target entities using fuzzy matching, solving the memory orphaning problem caused by exact-match failures.
**Acceptance Criteria:**
- FTS5 virtual table (`ontology_fts`) linked to `ontology_edges`.
- SQLite Triggers auto-sync the FTS table on INSERT, UPDATE, DELETE.
- New MCP Tool `mcp_context-engine_search_ontology_semantic` implemented and mapped to a `SearchOntologyFTS` Go handler.
- BDD Tests confirm fuzzy keyword queries return correct edges.
- Malformed FTS queries return empty arrays without crashing (Jidoka).

---

## 2. The Lean Audit (Phase 2)
**Verdict:** The use of native SQLite FTS5 over an external vector database is highly aligned with Lean principles by eliminating Muri (Overburden).
**Critical Discoveries:**
- **KYT Hazard:** SQL Injection via the MCP tool's `query` parameter.
- **Poka-yoke Missing:** Explicit input validation must be added for the `query` string before hitting the database.
- **Yokoten Pattern:** Preferring native SQLite capabilities over microservices is a strong pattern to broadcast to other data-layer skills.

---

## 3. The Strategic Architecture (Phase 3)
**Shusa Strategy:** Maintain a lightweight, zero-dependency engine while improving agent UX.
**Value Stream:** Agent fails DAG read -> Context lost -> Agent halts (Current). Agent fails DAG read -> Calls semantic search -> Gets exact node name -> DAG read succeeds (Future).
**Dependency Ripple:** Isolated to `sqlite.go` (schema), `ontology.go` (data access), and `main.go` (MCP tool).
**Heijunka Rollout Plan:**
  1. Migrate Schema (`sqlite.go` virtual table + triggers).
  2. Implement Go Data Access (`ontology.go` FTS query).
  3. Register MCP Tool (`main.go`).
  4. Write BDD Tests (`test_ontology.py`).
**Jidoka Andon Cord:** Any failure in `test_ontology.py` related to basic inserts or reads must immediately trip the Andon cord and halt the rollout, reverting the FTS schema migration to prevent corruption of the core Graph inserts.

---

## 4. Pilot & Kaizen Optimization (Phases 4 & 5)
*To be executed concurrently with the Heijunka Rollout Plan:*
- **Pilot Module:** Target `sqlite.go` first in isolation. Execute the FTS5 virtual table and trigger logic on a local instance and verify using `sqlite3` CLI before wiring up the Go backend.
- **Kaizen Targets:** Track the latency of the FTS query vs the exact DAG read. If FTS introduces unacceptable overhead, optimize the `MATCH` ranking algorithm in subsequent sprints.