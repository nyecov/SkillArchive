# Context Engine: MCP Tool Schema Reference

*This document is mechanically authoritative. Agent configurations utilizing the Context Engine MCP Server must strictly adhere to the schemas defined below.*

## 1. Context Ingestion
### `ingest_context`
Ingests a file safely. Truncates and chunks files exceeding 16k chars. Handles TOON, JSON, and Markdown.
**Parameters:**
- `target_path` (string) [REQUIRED]: Absolute or relative path to the file to ingest.
- `query` (string) [OPTIONAL]: Specific keyword query to extract relevant chunks.
- `start_offset` (number) [OPTIONAL]: Byte offset to start reading from for paginated file ingestion.

## 2. Short-Term Memory (Volatile Scratchpad)
### `log_session_finding`
Writes a critical finding to the volatile short-term scratchpad. Limits size dynamically.
**Parameters:**
- `finding_text` (string) [REQUIRED]: The finding to record.
- `phase` (string) [REQUIRED]: The current phase: [planning, execution, verification, blocked]

### `read_session_state`
Retrieves the current state of volatile session memory.
**Parameters:** None

### `delete_session_finding`
Removes a specific finding from the volatile scratchpad by its 0-based index.
**Parameters:**
- `index` (number) [REQUIRED]: The 0-based index of the finding to delete.

### `clear_session_state`
Resets the volatile scratchpad, permanently deleting all session findings.
**Parameters:** None

## 3. Middle-Term Memory (Ontology Graph)
### `commit_ontology_edge`
Hard-commits a new relationship to the Knowledge Graph. Hierarchical edges fail if it creates a DAG cycle.
**Parameters:**
- `source_entity` (string) [REQUIRED]: Source node name.
- `edge_type` (string) [REQUIRED]: Enum: REQUIRES, IMPLEMENTS, DEPENDS_ON, OWNS, REFERENCES, CONFLICTS_WITH.
- `target_entity` (string) [REQUIRED]: Target node name.

### `delete_ontology_edge`
Removes an existing edge from the Knowledge Graph. Use to resolve DAG cycles.
**Parameters:**
- `source_entity` (string) [REQUIRED]: Source node name.
- `edge_type` (string) [REQUIRED]: Edge type to remove.
- `target_entity` (string) [REQUIRED]: Target node name.

### `read_ontology_graph`
Queries the Knowledge Graph for an entity's dependencies.
**Parameters:**
- `target_entity` (string) [REQUIRED]: Entity node to query.

