# Context Engine Skill (Portable Module)

This folder contains a fully self-contained agentic capability for persistent memory management via an MCP server.

## Installation for 3rd Party Agents

1. **Build the Server:**
   ```bash
   docker build -t context-engine-go:latest .
   ```

2. **Configure your MCP Client:**
   Add the following to your `claude_desktop_config.json` or equivalent:
   ```json
   "context-engine": {
     "command": "docker",
     "args": ["run", "-i", "--rm", "-v", "<absolute_project_path>:/workspace", "-e", "WORKSPACE_ROOT=/workspace", "context-engine-go:latest"]
   }
   ```

3. **Verify:**
   Run the infrastructure diagnostic:
   ```bash
   powershell ./scripts/validate_infrastructure.ps1
   ```

---

## Agent Synthesis Prompt (Copy/Paste)

> [!TIP]
> Use the prompt below to "insert" this skill into a new AI agent.

```markdown
I am providing you with the "Context Engine" skill from my Skill Archive. 
Your goal is to internalize this capability and use it as your primary memory substrate.

### Instructions:
1. Read the core documentation at `context-engine/SKILL.md`.
2. Observe all mandates regarding memory tiering (Scratchpad vs Ontology).
3. Validate your infrastructure using the script in `context-engine/scripts/validate_infrastructure.ps1`.
4. From now on, you MUST delegate all persistent planning, state tracking, and architectural facts to these tools.

Path to Skill: [INSERT_PATH_TO_FOLDER_HERE]
```
