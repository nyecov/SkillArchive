---
name: interface-governance
version: 1.2.0
level: technical
description: Use when designing, building, auditing, testing, or consuming MCP servers and clients. Integrates API-Design-First principles and empirical evaluation protocols to ensure interfaces are optimized for LLM discoverability and reliability.
category: architecture
tags:
- architecture
- testing
- mcp
- methodology
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
- name: Genchi Genbutsu (Dynamic Verification)
  path: ../genchi-genbutsu/SKILL.md
---

# Interface Governance

The Model Context Protocol (MCP) is the open standard for connecting AI agents to external tools, data sources, and services. In Vibe Coding and Agentic development, the MCP server is the **Sovereign Interface**—it is the only way the agent interacts with the world. This skill governs the design-first approach to building and verifying interfaces optimized for LLM discoverability, reasoning, and reliability.

## Core Mandates

### 1. API-Design-First (Discoverability)
Design the interface for the *consumer* (the LLM), not the *provider* (the underlying API).
- **Action:** Define tool names and descriptions as "Triggers." Use semantic, verb-noun naming (e.g., `search_code_base` instead of `execute_grep`).
- **Constraint:** NEVER expose raw, low-level system calls directly. Wrap them in "Agent-Friendly" abstractions.
- **Integration:** Directly reduces **Motion Muda** by making the right tool obvious to the agent.

### 2. Rigorous Schema Enforcement (The Poka-yoke)
Every tool input and resource URI MUST follow a strict, documented JSON Schema.
- **Action:** Define every parameter with `type`, `description`, and `required` status. Use enums and pattern constraints to restrict the LLM's "Hallucination Space."
- **Constraint:** Untyped pass-throughs (e.g., `type: object` with no properties) are strictly prohibited.
- **Integration:** Acts as an integration-level **Poka-yoke**.

### 3. Human-in-the-Loop Safeguards
Explicitly mark and gate destructive operations to prevent unintended state changes.
- **Action:** Set `destructiveHint: true` for any tool that modifies or deletes persistent data.
- **Constraint:** NEVER auto-execute destructive tools without explicit human-in-the-loop (HITL) authorization.

### 4. Empirical Verification (Evaluations)
Building a server is not enough; it MUST be verified for LLM usability using the **Evaluation Protocol**.
- **Action:** Create complex, multi-step questions that require the agent to autonomously discover and use the server's tools to solve them.
- **Constraint:** Do not consider an MCP Server "complete" based solely on passing unit tests or manual CLI checks.
- **Integration:** Implements **Genchi Genbutsu** (Go and See for Yourself).

## Escalation & Halting

- **Jidoka:** Trigger an autonomous halt if a tool returns a protocol error (`-32602`), if input schema validation fails, or if an agent consistently fails an evaluation due to hallucinating parameters.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if tool execution results in ambiguous state changes or to propose schema/description refactors based on evaluation failures.

## Implementation Workflow

### Phase 1: Server Design & Primitive Selection
| Primitive | Use When | Example |
|-----------|----------|---------|
| **Tool** | Mutation or computation | `create_issue`, `query_database`, `send_email` |
| **Resource** | Read-only context data | `file:///config.json`, `db://users/schema` |
| **Prompt** | Interaction template | `code_review`, `summarize_document` |

### Phase 2: Implementation (Schema & Descriptions)
Every tool definition requires:
- `name`: Unique, verb-noun identifier.
- `description`: "Trigger" oriented (when to call it, not how it works).
- `inputSchema`: Every parameter typed, documented, and required where applicable.
- `annotations`: Behavioral hints (`readOnlyHint`, `destructiveHint`, etc.).

### Phase 3: Empirical Evaluation (Testing)
1. **Reconnaissance**: Explore the server using the MCP Inspector.
2. **Evaluation Generation**: Create 5-10 complex, independent, read-only questions.
3. **Question Design**: Design questions that require at least two sequential tool calls (e.g., Search for an ID -> Fetch the details).
4. **Execution**: Run the questions with an agent. If the agent fails, do NOT fix the agent; fix the server's tool descriptions or schemas.

### Phase 4: Lifecycle & Security Hardening
- **Validate**: All inputs must undergo schema validation.
- **Sanitize**: Strip sensitive data from outputs.
- **HITL**: Gated authorization for destructive operations.

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **God tool** | One tool does everything via a `command` string | Split into focused, single-purpose tools with typed schemas |
| **Untyped input** | `inputSchema: { type: "object" }` | Define every parameter with type and description |
| **Missing evaluation** | Server "works" in unit tests but agent fails to use it | Run a full **Phase 3 Evaluation Protocol** |
| **Secrets in resources**| Credentials exposed through resource reads | Filter sensitive fields server-side |
