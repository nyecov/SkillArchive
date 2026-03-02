---
id: 919ca7c6-1f70-4b7a-acc4-6b825c968edd
name: context-engine
version: 1.0.0
description: Use when required to retrieve information, learn codebase rules, read files over 4,000 tokens, or record short-term plans. This skill governs all agent memory operations via the MCP Server.
category: memory
level: technical
tags:
- memory
- mcp
- rag
- state
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Tools Management Strategy
  path: ../tools-management/SKILL.md
- name: Context Engine Specification
  path: ./references/Context_Engine_Specification.md
- name: Memory Tiering Dossier
  path: ./references/memory_tiering_dossier.md
- name: Agent Querying Guide
  path: ./references/querying-guide.md
- name: Testing Suite Strategy
  path: ./references/testing_suite_guide.md
- name: MCP Connection Script
  path: ./scripts/connect.sh
- name: Lifecycle Verification Tests
  path: ./testing/test_lifecycle.py
- name: Docker Compose Configuration
  path: ./docker-compose/docker-compose.yml
---
# Context Engine

This skill dictates how agents build, access, and maintain context. You **MUST** delegate all context and memory retrieval to the deterministic `Context Engine` MCP server tools.

## Core Mandates

### 1. Mandatory Tool Usage
- **Action:** You must ALWAYS use the `context-engine` MCP tools to observe files, document plans, and record facts.
- **Constraint:** NEVER attempt to write notes directly to raw `.txt` or `.md` files in the `.gemini/mem` directory. Manual edits will be quarantined and reverted by boot-time diagnostics.
- **Provenance:** All memory artifacts possess a unique UUIDv4. The server guarantees persistence across file moves and renames.

### 2. The Scratchpad (Short-Term Memory)
- **Action:** Use `log_session_finding` to record intent, discovered bugs, or phase changes (Memory Creation).
- **Action:** Use `read_session_state` to regain situational awareness before initiating `shisa-kanko`.
- **Action (Pruning):** Use `delete_session_finding` to surgically cull outdated items, or `clear_session_state` to wipe the slate clean after major phase completions.
- **Limits:** The server enforces a Soft Limit (8k chars) and a Hard Limit (10k chars). If blocked, synthesize findings into the Ontology and prune the scratchpad immediately.

### 3. The Knowledge Graph (Long-Term Memory)
- **Action (Upgrade):** Use `commit_ontology_edge` to harden architectural rules (e.g., "Module A REQUIRES Module B") out of your volatile scratchpad.
- **Action (Downgrade):** Use `delete_ontology_edge` to refactor broken graph logic or resolve Cycle Erors. Move the discarded concepts back to the scratchpad if re-evaluation is needed.
- **Constraint:** Hierarchical edges (`REQUIRES`, `DEPENDS_ON`, `OWNS`) cannot create circular dependencies.
- **Integrity:** The system uses `ontology.json` with atomic `Sync()` writes. 

### 4. Token-Safe Ingestion
- **Action:** Use `ingest_context` to safely retrieve file chunks. It automatically token-caps the return to ~16,000 characters to protect your context window.

## Escalation & Halting (Troubleshooting)

- **Singleton Violation:** If the server fails to boot, ensure no other engine instances are active. The engine enforces a **Structural Singleton** guard.
- **Boot Recovery:** If MCP tools are unresponsive, run `powershell ./scripts/validate_infrastructure.ps1` to diagnose daemon, image, and lock status.

## MCP Client Configuration Standard

For an agent to connect natively to this engine, its MCP configuration (e.g., `claude_desktop_config.json` or agent CLI config) MUST be set to execute the container via `stdio`. To eliminate "Cold Start" latency, the engine should be run in Daemon mode.

**Windows (PowerShell):**
```json
"context-engine": {
  "command": "powershell",
  "args": ["-NoProfile", "-Command", "& '<path_to_workspace>/.gemini/skills/context-engine/scripts/connect.ps1'"]
}
```

**macOS/Linux (Bash):**
```json
"context-engine": {
  "command": "bash",
  "args": ["<path_to_workspace>/.gemini/skills/context-engine/scripts/connect.sh"]
}
```
*Note: If daemon mode is unavailable, the fallback ephemeral execution is `docker run -i --rm -v <workspace_root>:/workspace context-engine-go:latest`.*

## Implementation Workflow (Maturation)

1. **Awareness:** Run `read_session_state` and `ingest_context` to regain context.
2. **Creation:** Save thoughts via `log_session_finding`.
3. **Upgrade:** Harden architectural facts into permanent memory using `commit_ontology_edge`.
4. **Deletion (Prune):** Immediately execute `delete_session_finding` to clear the hardened items from your volatile scratchpad.

## Precision Example: Maturation Sequence

```markdown
1. log_session_finding(finding="User prefers HSL over Hex in CSS scripts.")
2. [Observe consistency over 3 turns]
3. commit_ontology_edge(source="UserPreferences", target="HSL_Colors", relation="REQUIRES")
4. delete_session_finding(index=0)
```
