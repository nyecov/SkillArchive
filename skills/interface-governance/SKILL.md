---
name: interface-governance
version: 1.3.0
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
- **Constraint:** NEVER expose raw, low-level system calls directly. Wrap them in "Agent-Friendly" abstractions. NEVER create a "God Tool" that does everything via one generic command string; split into focused, single-purpose tools with typed schemas.
- **Integration:** Directly reduces **Motion Muda** by making the right tool obvious to the agent.

### 2. Rigorous Schema Enforcement (The Poka-yoke)
Every tool input and resource URI MUST follow a strict, documented JSON Schema.
- **Action:** Define every parameter with `type`, `description`, and `required` status. Use enums and pattern constraints to restrict the LLM's "Hallucination Space."
- **Constraint:** Untyped pass-throughs (e.g., `inputSchema: { type: "object" }` with no properties) are strictly prohibited. Every parameter must be defined with type and description.
- **Integration:** Acts as an integration-level **Poka-yoke**.

### 3. Human-in-the-Loop Safeguards
Explicitly mark and gate destructive operations to prevent unintended state changes.
- **Action:** Set `destructiveHint: true` for any tool that modifies or deletes persistent data.
- **Constraint:** NEVER auto-execute destructive tools without explicit human-in-the-loop (HITL) authorization.
- **Integration:** Binds to **Hō-Ren-Sō** Sōdan protocol for authorization.

### 4. Empirical Verification (Evaluations)
Building a server is not enough; it MUST be verified for LLM usability using the Evaluation Protocol.
- **Action:** Create complex, multi-step questions that require the agent to autonomously discover and use the server's tools to solve them (e.g., Search for an ID -> Fetch the details).
- **Constraint:** Do not consider an MCP Server "complete" based solely on passing unit tests or manual CLI checks. If an agent fails the evaluation, do NOT fix the agent; fix the server's tool descriptions or schemas.
- **Integration:** Implements **Genchi Genbutsu** (Go and See for Yourself).

### 5. Lifecycle & Security Hardening
Manage the data flowing through the governed interface to prevent catastrophic leaks.
- **Action:** Validate all inputs against schemas and sanitize outputs.
- **Constraint:** NEVER expose secrets or credentials through resource reads. Filter sensitive fields server-side before transmitting data to the LLM context.
- **Integration:** Feeds directly into **CC Secure**.

## Escalation & Halting

- **Jidoka:** Trigger an autonomous halt if a tool returns a protocol error (`-32602`), if input schema validation fails, or if an agent consistently fails an evaluation due to hallucinating parameters.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if tool execution results in ambiguous state changes or to propose schema/description refactors based on evaluation failures.

## Implementation Workflow

1. **Trigger:** A new MCP server is being designed, an existing server requires an audit, or an agent is failing to reliably use a provided interface.
2. **Execute:** Define Primitives (Tool, Resource, Prompt). Enforce rigid JSON schemas and semantic trigger descriptions for all interfaces. Filter sensitive outputs and gate destructive actions.
3. **Verify:** Execute the **Phase 3 Evaluation Protocol**: Explore via MCP Inspector, generate 5-10 complex multi-step questions, and run them with an agent.
4. **Output:** A verified, schema-rigid MCP interface and a documented evaluation report proving LLM usability.
