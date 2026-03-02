# Context Engine: MCP Tool Schemas

To comply with the `interface-governance` skill (API-Design-First, Poka-yoke error prevention), here are the exact JSON Schema definitions for the tools the Go MCP server must expose to the agent.

## 1. `ingest_context`
**Description:** Ingests a file to return context safely. Truncates and chunks files exceeding 4k tokens. Natively handles TOON, JSON, and Markdown files.

```json
{
  "type": "object",
  "properties": {
    "target_path": {
      "type": "string",
      "description": "Absolute or relative path to the file or directory to ingest."
    },
    "query": {
      "type": "string",
      "description": "(Optional) Specific keyword or semantic query to extract relevant chunks from massive files. If omitted, the top of the file is returned up to the token limit."
    }
  },
  "required": ["target_path"]
}
```

## 2. `log_session_finding`
**Description:** Writes a critical finding, error, or logic decision to the volatile short-term scratchpad memory. Prevents context drift during complex tasks.

```json
{
  "type": "object",
  "properties": {
    "finding_text": {
      "type": "string",
      "description": "The specific fact, decision, or error string to record."
    },
    "phase": {
      "type": "string",
      "enum": ["planning", "execution", "verification", "blocked"],
      "description": "The current phase of the agentic workflow."
    }
  },
  "required": ["finding_text", "phase"]
}
```

## 3. `read_session_state`
**Description:** Retrieves the current state of the volatile session memory, including recent findings and the active phase. Call this before making significant task decisions.

```json
{
  "type": "object",
  "properties": {},
  "required": []
}
```

## 4. `commit_ontology_edge`
**Description:** Hard-commits a new relationship/rule to the long-term Knowledge Graph. The server will actively reject the commit if it creates a circular dependency (DAG violation).

```json
{
  "type": "object",
  "properties": {
    "source_entity": {
      "type": "string",
      "description": "The name of the source entity or node (e.g. 'AuthenticationModule', 'DatabaseConfig')."
    },
    "edge_type": {
      "type": "string",
      "enum": ["REQUIRES", "IMPLEMENTS", "DEPENDS_ON", "CONFLICTS_WITH", "OWNS"],
      "description": "The directional relationship type from the source to the target."
    },
    "target_entity": {
      "type": "string",
      "description": "The name of the target entity or node."
    }
  },
  "required": ["source_entity", "edge_type", "target_entity"]
}
```

## 5. `read_ontology_graph`
**Description:** Queries the long-term Knowledge Graph for an entity's upstream and downstream dependencies.

```json
{
  "type": "object",
  "properties": {
    "target_entity": {
      "type": "string",
      "description": "The specific entity node to query within the global ontology."
    }
  },
  "required": ["target_entity"]
}
```
