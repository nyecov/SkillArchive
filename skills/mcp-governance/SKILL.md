---
name: mcp-governance
version: 1.0.0
description: >
  Use when designing, building, auditing, or consuming MCP servers and clients.
  Handles tool design, resource exposure, transport selection, security hardening, and lifecycle management for Model Context Protocol integrations.
category: architecture
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
    path: ../secure-security/SKILL.md
  - name: Poka-yoke (Validation Gates)
    path: ../poka-yoke/SKILL.md
  - name: Jidoka (Halt on Anomaly)
    path: ../jidoka/SKILL.md
---

# MCP Integration Governance

The Model Context Protocol (MCP) is the open standard for connecting AI agents to external tools, data sources, and services. It replaces ad-hoc API integrations with a structured, discoverable, and secure client-server protocol. This skill governs how to design, build, and consume MCP integrations correctly.

## Core Mandates

### 1. Architectural Primitive Selection
Strictly classify every integration as a Tool (Mutation/Computation), Resource (Read-only Context), or Prompt (Interaction Template).
- **Action:** If it mutates state or computes → Tool. If it provides context → Resource.
- **Constraint:** DO NOT create "God Tools" that handle multiple unrelated operations; keep them single-purpose and focused.
- **Integration:** Directly impacts the **Tools Management Strategy** classification.

### 2. Rigorous Schema Enforcement
Every tool input and resource URI MUST follow a strict, documented JSON Schema to ensure deterministic interaction.
- **Action:** Define every parameter with `type`, `description`, and `required` status. 
- **Constraint:** Untyped pass-throughs (e.g., `type: object` with no properties) are strictly prohibited.
- **Integration:** Acts as an integration-level **Poka-yoke** for the agent.

### 3. Human-in-the-Loop Safeguards
Explicitly mark and gate destructive operations to prevent unintended state changes.
- **Action:** Set `destructiveHint: true` for any tool that modifies or deletes persistent data.
- **Constraint:** NEVER auto-execute destructive tools without explicit human-in-the-loop (HITL) authorization.
- **Integration:** Connects to the **Sōdan (Consult)** protocol in **Hō-Ren-Sō**.

## Escalation & Halting

- **Jidoka:** Trigger an autonomous halt if a tool returns a protocol error (`-32602`), if input schema validation fails, or if a path traversal attempt is detected.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if tool execution results in ambiguous state changes or if human authorization is required for a destructive operation.

## Implementation Workflow

### Phase 1: Server Design & Primitive Selection

Before writing code, classify what you're exposing:

| Primitive | Use When | Agent Interaction | Example |
|-----------|----------|-------------------|---------|
| **Tool** | The agent needs to perform an action or computation | Agent invokes with parameters, receives result | `create_issue`, `query_database`, `send_email` |
| **Resource** | The agent needs read-only context data | Agent reads by URI, may subscribe to updates | `file:///config.json`, `db://users/schema`, `git://repo/log` |
| **Prompt** | The agent needs a reusable interaction template | Agent selects and fills template arguments | `code_review`, `summarize_document` |

**Decision rule:** If it mutates state or performs computation → **Tool**. If it provides context → **Resource**. If it structures a conversation pattern → **Prompt**.

### Phase 2: Tool & Resource Implementation

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

Every resource requires:

```
uri:         Unique identifier (file://, https://, db://, or custom scheme)
name:        Human-readable label
description: What this resource contains
mimeType:    Content type (text/plain, application/json, image/png)
```

**Rules:**
1. **Use standard URI schemes** where applicable: `file://` for filesystem, `https://` for web content, `git://` for repos.
2. **Use resource templates** for parameterized access: `db://users/{user_id}/profile` — never expose a "query anything" resource.
3. **Implement subscriptions** for resources that change.
4. **Never expose secrets** through resources.

### Phase 3: Lifecycle & Security Hardening

1. **Initialize**: Respond to `initialize` with server capabilities and protocol version.
2. **Negotiate**: Read client capabilities to determine available features.
3. **Validate**: All tool inputs must undergo schema validation.
4. **Sanitize**: Strip sensitive data from outputs before returning results.
5. **Shutdown**: Clean up connections and flush state on disconnect.

## Testing & Verification

1. **Use MCP Inspector** (`npx @modelcontextprotocol/inspector`) to test tools, resources, and prompts interactively.
2. **Verify capability negotiation** — inspect the `initialize` response.
3. **Test each tool** — call with valid and invalid parameters.
4. **Test each resource** — read by URI and verify MIME type.

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **God tool** | One tool that does everything via a `command` string | Split into focused, single-purpose tools with typed schemas |
| **Untyped input** | `inputSchema: { type: "object" }` with no properties | Define every parameter with type, description, and required |
| **Missing annotations** | Destructive tools auto-execute without user consent | Add `destructiveHint: true` for write/delete operations |
| **Secrets in resources** | API keys or credentials exposed through resource reads | Filter sensitive fields; use environment variables server-side |
| **No error context** | Generic "Error occurred" responses | Return specific error messages with actionable details |
| **Monolithic server** | One server exposes 50+ tools from different domains | Split into domain-specific servers |
