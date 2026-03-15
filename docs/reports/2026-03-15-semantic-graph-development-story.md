# Semantic Graph Upgrade (SQLite FTS5)
## The Goal
Enhance the Context Engine Ontology Graph with semantic search capabilities (via SQLite FTS5) to allow agents to find target entities using fuzzy matching instead of requiring exact node names.

## The Problem
Agents currently fail to traverse the DAG if they forget the exact string literal of a target node created previously, leading to orphaned memories.

## The Acceptance Criteria
- FTS5 virtual table (`ontology_fts`) is linked to `ontology_edges`.
- SQLite Triggers auto-sync the FTS table on INSERT, UPDATE, DELETE.
- A new MCP Tool `mcp_context-engine_search_ontology_semantic` is implemented.
- The tool returns structured JSON of matching edges.
- BDD Tests confirm that fuzzy keyword queries return the correct edges despite exact string mismatch.
- Malformed FTS queries return empty arrays without crashing.