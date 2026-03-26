# Lean Analysis Report: Semantic Graph Upgrade (SQLite FTS5)

## Executive Summary
A comprehensive Lean audit of the Semantic Graph Upgrade plan. The approach of using native SQLite FTS5 over an external vector database is highly aligned with Lean principles (eliminating Muri/Overburden). The primary areas for improvement are around Poka-yoke (input validation) and KYT (SQL injection prevention).

## Phase Results
### Phase 1: Lean Foundations — 3M + 5S
- **Muri (Overburden):** Successfully avoided by not introducing vector DB dependencies.
- **5S (Sort/Standardize):** The plan is well-sorted, leveraging existing SQLite patterns.

### Phase 2: Story Interview — Value & Assumptions
- **Core Goal:** Allow agents to find target entities using fuzzy matching instead of requiring exact node names.
- **Assumption:** BM25 text ranking is sufficient for semantic meaning in an architectural graph compared to true vector embeddings.

### Phase 3: Value Stream Mapping — Flow Analysis
- **Current State:** Agent fails DAG read -> Context lost -> Agent halts.
- **Future State:** Agent fails DAG read -> Calls semantic search -> Gets exact node name -> DAG read succeeds.

### Phase 4: KYT — Hazard Prediction
- **Hazard:** FTS index drifting from the main table. (Countermeasure: SQLite Triggers included in plan).
- **Hazard:** SQL Injection via the MCP tool's `query` parameter. (Countermeasure: MUST use parameterized `?` queries).

### Phase 5: Poka-yoke — Guardrails Audit
- **Missing Guardrail:** The `query` parameter must be validated to ensure it's not empty, null, or excessively long before hitting the database.

### Phase 6: Shisa Kanko — Precision Audit
- **Point:** `SearchOntologyFTS` function.
- **Call:** Intent: Return top 10 ranked edges. Verification: BDD test asserting fuzzy match success.

### Phase 7: Nemawashi — Impact Analysis
- **Ripple Effects:** Minimal. This is an additive feature (virtual table + new tool) that doesn't break existing `read_ontology_graph` paths.

### Phase 8: Shusa Leadership — Strategic Alignment
- **Verdict:** Aligned. It solves a major pain point for agent autonomy while keeping the Go binary dependency-free.

### Phase 9: Yokoten — Horizontal Deployment
- **Pattern:** Preferring native SQLite capabilities (FTS5) over introducing external microservices for initial implementations. This pattern should be broadcast to all data-layer planning skills.

## Critical Actions
1. **Poka-yoke Update:** Add explicit input validation for the `query` parameter in the MCP handler.
2. **KYT Update:** Ensure all SQL execution in `ontology.go` strictly uses parameterized queries to prevent injection.

## Yokoten Broadcast
- Broadcast the "Native SQLite-First" pattern to other skills like `test-driven-development` and `architectural-anchoring`.