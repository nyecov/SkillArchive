---
name: MCP Integration Governance
version: 1.0.0
description: >
  Use when designing, building, auditing, or consuming MCP servers and clients.
  Handles tool design, resource exposure, transport selection, security hardening, and lifecycle management for Model Context Protocol integrations.
category: integration
tags: [mcp, model-context-protocol, tools, resources, json-rpc, agent-integration]
references:
  - name: MCP Specification (Official)
    url: https://modelcontextprotocol.io/specification/latest
  - name: MCP Architecture Overview
    url: https://modelcontextprotocol.io/docs/concepts/architecture
  - name: MCP SDKs
    url: https://modelcontextprotocol.io/docs/sdk
  - name: MCP Inspector (Dev Tool)
    url: https://github.com/modelcontextprotocol/inspector
  - name: Reference Server Implementations
    url: https://github.com/modelcontextprotocol/servers
  - name: CC Secure (Security Guardrails)
    path: ../cc-secure-security/SKILL.md
  - name: Poka-yoke (Validation Gates)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: Jidoka (Halt on Anomaly)
    path: ../jidoka-autonomation/SKILL.md
---

# MCP Integration Governance

The Model Context Protocol (MCP) is the open standard for connecting AI agents to external tools, data sources, and services. It replaces ad-hoc API integrations with a structured, discoverable, and secure client-server protocol. This skill governs how to design, build, and consume MCP integrations correctly.

## Core Architecture

| Participant | Role | Example |
|-------------|------|---------|
| **Host** | AI application that coordinates clients | Claude Desktop, IDE agent extensions |
| **Client** | Maintains connection to a server, obtains context | One client per server, managed by host |
| **Server** | Exposes tools, resources, and prompts | Filesystem server, database connector, API wrapper |

| Layer | Protocol | Purpose |
|-------|----------|---------|
| **Data** | JSON-RPC 2.0 | Lifecycle, capability negotiation, tool/resource/prompt exchange |
| **Transport** | stdio or Streamable HTTP (+SSE) | Message framing and delivery |

## Server Design Workflow

### 1. Choose the Right Primitive

Before writing code, classify what you're exposing:

| Primitive | Use When | Agent Interaction | Example |
|-----------|----------|-------------------|---------|
| **Tool** | The agent needs to perform an action or computation | Agent invokes with parameters, receives result | `create_issue`, `query_database`, `send_email` |
| **Resource** | The agent needs read-only context data | Agent reads by URI, may subscribe to updates | `file:///config.json`, `db://users/schema`, `git://repo/log` |
| **Prompt** | The agent needs a reusable interaction template | Agent selects and fills template arguments | `code_review`, `summarize_document` |

**Decision rule:** If it mutates state or performs computation → **Tool**. If it provides context → **Resource**. If it structures a conversation pattern → **Prompt**.

### 2. Design Tools Correctly

Every tool definition requires:

```
name:         Unique, verb-first identifier (e.g., "search_issues", "create_file")
description:  What it does, when to use it, what it returns
inputSchema:  JSON Schema — every parameter typed and documented
outputSchema: JSON Schema (optional) — defines expected output structure
annotations:  Behavioral hints (readOnlyHint, destructiveHint, idempotentHint, openWorldHint)
```

**Rules:**
1. **Name as verb-noun**: `get_user`, `create_ticket`, `search_logs` — never `user` or `data`.
2. **Description is trigger, not summary**: State when to call the tool and what it returns, not how it works internally.
3. **Schema every parameter**: No untyped `object` pass-throughs. Every field must have `type`, `description`, and `required` status.
4. **Use annotations**: Mark destructive tools (`destructiveHint: true`) so hosts can gate them with user confirmation. Mark read-only tools (`readOnlyHint: true`) so hosts can auto-approve them.
5. **Return structured data**: Prefer JSON in `text` content over raw strings. Include error context in failure responses (`isError: true`).

### 3. Expose Resources Correctly

Resources are identified by URIs and are read-only context:

```
uri:         Unique identifier (file://, https://, db://, or custom scheme)
name:        Human-readable label
description: What this resource contains
mimeType:    Content type (text/plain, application/json, image/png)
```

**Rules:**
1. **Use standard URI schemes** where applicable: `file://` for filesystem, `https://` for web content, `git://` for repos.
2. **Use resource templates** for parameterized access: `db://users/{user_id}/profile` — never expose a "query anything" resource.
3. **Implement subscriptions** for resources that change: the client should receive `notifications/resources/updated` when content changes.
4. **Never expose secrets** through resources — filter environment variables, credentials, and tokens before serving.

### 4. Select Transport

| Transport | Best For | Auth | Performance |
|-----------|----------|------|-------------|
| **stdio** | Local processes, same-machine integrations, IDE plugins | Inherits process permissions | Optimal — no network overhead |
| **Streamable HTTP** | Remote servers, cloud services, cross-machine | Bearer tokens, API keys, OAuth | Network-dependent; supports streaming via SSE |

**Decision rule:** If client and server are on the same machine → **stdio**. If the server is remote or shared → **Streamable HTTP**.

### 5. Implement Lifecycle

Every MCP server must handle these lifecycle phases:

1. **Initialize**: Respond to `initialize` with server capabilities (`tools`, `resources`, `prompts`) and protocol version.
2. **Negotiate**: Read client capabilities to determine available features (sampling, roots, elicitation).
3. **Operate**: Handle `tools/call`, `resources/read`, and `prompts/get` requests.
4. **Notify**: Emit `notifications/tools/list_changed` or `notifications/resources/list_changed` when capabilities change at runtime.
5. **Shutdown**: Clean up connections, flush state, release resources on disconnect.

## Security Mandates

### Server-Side (MUST)

1. **Validate all tool inputs** — schema validation is not optional. Reject malformed requests with `-32602 Invalid params`.
2. **Implement access controls** — not every client should access every tool. Use capability negotiation to limit exposure.
3. **Rate-limit tool invocations** — prevent runaway loops from consuming API quotas or database connections.
4. **Sanitize all outputs** — strip sensitive data (tokens, passwords, PII) before returning results.
5. **Path traversal protection** — for filesystem servers, resolve paths against workspace root and reject `../` escapes.

### Client-Side (SHOULD)

1. **Human-in-the-loop for destructive tools** — prompt user confirmation before calling tools annotated with `destructiveHint: true`.
2. **Display tool inputs before execution** — prevent data exfiltration via crafted tool parameters.
3. **Validate tool results before passing to LLM** — malicious servers can inject prompt manipulation in results.
4. **Implement timeouts** — tool calls must not block indefinitely. Default: 30 seconds.
5. **Log all tool usage** — maintain an audit trail for compliance and debugging.

## Error Handling

MCP defines two error categories:

| Category | Mechanism | Examples |
|----------|-----------|---------|
| **Protocol Errors** | JSON-RPC error response (`error` field) | Unknown tool (`-32602`), invalid arguments, server crash |
| **Tool Execution Errors** | Result with `isError: true` | API rate limit, invalid input data, business logic failure |

**Rules:**
1. Protocol errors mean the tool could not be called → the agent should **not retry** with the same parameters.
2. Execution errors mean the tool ran but failed → the agent **may retry** with modified parameters or after backoff.
3. Always return **specific, actionable error messages**: "User 'abc' not found in database 'users'" — never "An error occurred."

## Testing Workflow

1. **Use MCP Inspector** (`npx @modelcontextprotocol/inspector`) to test tools, resources, and prompts interactively.
2. **Verify capability negotiation** — connect a client, inspect the `initialize` response for declared capabilities.
3. **Test each tool** — call with valid parameters (expect success), invalid parameters (expect `-32602`), and edge cases (expect graceful `isError: true`).
4. **Test each resource** — read by URI, verify MIME type correctness, test subscription updates.
5. **Test transport** — if using HTTP, verify auth token handling, SSE streaming, and connection recovery.

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **God tool** | One tool that does everything via a `command` string | Split into focused, single-purpose tools with typed schemas |
| **Untyped input** | `inputSchema: { type: "object" }` with no properties | Define every parameter with type, description, and required |
| **Missing annotations** | Destructive tools auto-execute without user consent | Add `destructiveHint: true` for write/delete operations |
| **Secrets in resources** | API keys or credentials exposed through resource reads | Filter sensitive fields; use environment variables server-side |
| **No error context** | Generic "Error occurred" responses | Return specific error messages with actionable details |
| **Monolithic server** | One server exposes 50+ tools from different domains | Split into domain-specific servers (DB server, API server, filesystem server) |
