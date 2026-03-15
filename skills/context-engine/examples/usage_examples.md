# Context Engine Usage Examples

This directory provides concrete examples of interaction with the Context Engine MCP tools.

## 1. Scratchpad Maturation Flow

### Phase 1: Planning (Memory Creation)
```json
// LLM sends
{
  "method": "tools/call",
  "params": {
    "name": "log_session_finding",
    "arguments": {
      "finding_text": "Discovered that the CSS flexbox layout is breaking on Safari.",
      "phase": "planning"
    }
  }
}
```

### Phase 2: Execution (Knowledge Hardening)
```json
// LLM sends
{
  "method": "tools/call",
  "params": {
    "name": "commit_ontology_edge",
    "arguments": {
      "source_entity": "Safari_Layout_Bug",
      "edge_type": "REQUIRES",
      "target_entity": "Flexbox_Gap_Polyfill"
    }
  }
}
```

### Phase 3: Verification (Memory Pruning)
```json
// LLM sends
{
  "method": "tools/call",
  "params": {
    "name": "delete_session_finding",
    "arguments": {
      "index": 0
    }
  }
}
```

## 2. Token-Safe File Ingestion

### Large File Pagination
```json
// First call (initial chunk)
{
  "method": "tools/call",
  "params": {
    "name": "ingest_context",
    "arguments": {
      "target_path": "server/cmd/server/main.go"
    }
  }
}

// Second call (offset chunk)
{
  "method": "tools/call",
  "params": {
    "name": "ingest_context",
    "arguments": {
      "target_path": "server/cmd/server/main.go",
      "start_offset": 16000
    }
  }
}
```
