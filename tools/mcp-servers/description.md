# MCP Servers Configuration

The project is configured to use several Model Context Protocol (MCP) servers to extend the agent's capabilities with external tools, web interactions, and long-term memory.

These are configured in `.gemini/settings.json`.

## Configured Servers

| Server | Purpose | Tools Provided |
|--------|---------|----------------|
| **Playwright** | Full browser automation. | `navigate`, `click`, `fill`, `screenshot`, `accessibility_tree`. |
| **Fetch** | Simple web content retrieval. | `fetch`, `fetch_markdown`. |
| **SQLite** | Database interaction. | `query`, `read_schema`. |
| **Everything-Search** | Windows system file search. | `search`. |
| **Context Engine** | Project-specific memory & RAG. | `ingest_context`, `log_session_finding`, `commit_ontology_edge`, etc. |
| **GitHub** | Repository management. | `create_issue`, `search_repositories`, `create_pull_request`, etc. |
| **Sequential Thinking** | Structured step-by-step reasoning. | `sequential_thinking`. |
| **Git** | Local repository management. | `git_status`, `git_commit`, `git_log`, etc. |
| **Memory** | Persistent knowledge graph. | `create_entity`, `create_relation`, `search_graph`, etc. |
| **PostgreSQL** | Database query and schema inspection. | `query`, `list_tables`, `describe_table`. |
| **Notion** | Workspace knowledge management. | `search_notion`, `read_page`, `update_page`. |
| **Sentry** | Error tracking and debugging. | `list_issues`, `get_issue_details`, `get_event`. |

## Authentication Setup
Several servers require API keys or connection strings. Open `.gemini/settings.json` and replace the placeholder values with your actual credentials:
- `GITHUB_PERSONAL_ACCESS_TOKEN` for GitHub
- `NOTION_API_TOKEN` for Notion
- `SENTRY_AUTH_TOKEN` for Sentry
- Provide the connection URL for the `postgres` server directly in its arguments list.

## Usage
These servers are started automatically by the Gemini CLI when needed. No manual startup is required unless debugging connectivity (use `powershell ./skills/context-engine/scripts/validate_infrastructure.ps1` for Context Engine).