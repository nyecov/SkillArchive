# Configuration Reference

This document serves as a centralized reference for infrastructure-heavy configuration data, preventing context window pollution in procedural Skill files.

## Context Engine: MCP Client Configuration Standard

For an agent to connect natively to this engine, its MCP configuration (e.g., `claude_desktop_config.json` or agent CLI config) MUST be set to execute the container via `stdio`. To eliminate "Cold Start" latency, the engine should be run in Daemon mode.

### Windows (PowerShell)
```json
"context-engine": {
  "command": "powershell",
  "args": ["-NoProfile", "-Command", "& '<path_to_workspace>/.gemini/skills/context-engine/scripts/connect.ps1'"]
}
```

### macOS/Linux (Bash)
```json
"context-engine": {
  "command": "bash",
  "args": ["<path_to_workspace>/.gemini/skills/context-engine/scripts/connect.sh"]
}
```

> **Note:** If daemon mode is unavailable, the fallback ephemeral execution is `docker run -i --rm -v <workspace_root>:/workspace context-engine-go:latest`.
