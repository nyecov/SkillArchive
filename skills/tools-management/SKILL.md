---
name: tools-management
version: 1.0.0
description: >
  Use when deciding whether to implement an abstraction as a cognitive Skill, an MCP Server, or a low-level Tool (script).
  Handles the boundary between high-level reasoning methodologies and low-level task automation, framework patterns, and API wrappers.
category: meta
tags: [tools, automation, scripts, mcp, delegation, architecture]
references:
  - name: MCP Integration Governance
    path: ../mcp-governance/SKILL.md
  - name: Skill of Skills (Meta-Skill)
    path: ../skill-of-skill-authoring/SKILL.md
---

# Tools Management Strategy

The agent ecosystem is flooded with "skills" that are actually just low-level automation scripts, specific API wrappers, or framework-specific rules (e.g., "Playwright Tester", "Vercel React Guidelines", "PDF Generator"). 

These fall below the threshold of a **Skill**. A true Skill in this Archive represents a high-level cognitive methodology (e.g., *how to debug systematically*, *how to review code critically*). A **Tool** represents mechanization.

This skill governs how to classify, store, and utilize these lower-level abstractions without polluting the cognitive Skill Archive.

## Classification: Skill vs Tool vs MCP

Before adopting an abstraction from the community or building your own, classify it:

| Classification | Characteristics | Example | Implementation |
|---|---|---|---|
| **Skill** | Cognitive methodology, framework-agnostic, teaches *how to think/approach* a problem. | Systematic Debugging (KYT, CC Isolate), PDCA (Kaizen) | `skills/skill-name/SKILL.md` |
| **Tool (Script)** | Mechanized action, platform/framework-specific, automates *how to execute* a task. | Running Playwright tests, parsing a PDF, downloading a YouTube sub. | Bash script, Python file in the archive's `tools/tool-name/` directory, accompanied by a `description.md`. |
| **MCP Server** | Connects to external services, databases, or APIs; provides isolated context/tools. | GitHub issue creator, Notion page analyzer, AWS cost fetcher. | MCP Server process via `stdio` or HTTP. |
| **Guidelines** | Syntactic rules or framework-specific best practices. | "Always use Next.js Server Components", "Tailwind CSS Rules". | System prompt injection, `.cursorrules`, or `docs/`. |

## Core Mandates

### 1. Architectural Classification
Before adopting an abstraction, classify it as a Skill (Cognitive), Tool (Mechanized), or MCP (External/Stateful).
- **Action:** Use the Classification Matrix to determine the appropriate storage location and format.
- **Constraint:** NEVER create a high-level `SKILL.md` for a "thin wrapper" around a single CLI command or API call.
- **Integration:** Directly impacts the **Skill of Skill Authoring** by defining the boundary of "Cognitive Procedures."

### 2. Tool Nesting & Scope
Store mechanized scripts within the skill's folder if they are specific to a methodology, or in the global `tools/` directory if they are generally useful.
- **Action:** Nest methodology-specific scripts (e.g., binary search test runners) inside `skills/{skill-name}/scripts/`.
- **Constraint:** Global tools MUST include a `description.md` to be discoverable by the agent.
- **Integration:** Supports **Lean Principles (Muda)** by reducing "Motion" (Navigational) waste.

### 3. Delegation to MCP
Delegate complex state management, external API access, or proprietary data handling to MCP Servers.
- **Action:** Use MCP for Jira, Gmail, or cloud service interactions. Use local scripts for filesystem and build operations.
- **Constraint:** Do not store sensitive API keys or complex state logic in local shell scripts.
- **Integration:** Follows the protocols established in **MCP Integration Governance**.

## Escalation & Halting

- **Jidoka:** If a tool's complexity exceeds the limits of a local script (e.g., it starts requiring state management), trigger a Jidoka halt to evaluate migration to MCP.
- **Hō-Ren-Sō:** Use the Hōkoku (Report) protocol to announce the addition of new mechanized tools to the project's capability set.

## Implementation Workflow

1. **Trigger:** A new automation or cognitive requirement is identified.
2. **Execute:** Apply the classification logic to choose between a Skill, Tool, or MCP.
3. **Verify:** Confirm the implementation follows the "No Thin Wrappers" and "Relative Path" rules.
4. **Output:** A cleanly abstracted capability (Skill/Tool/MCP) that enhances the agent's efficiency.

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Skill Bloat** | Skill Archive reaches 50+ files, mostly consisting of framework tutorials and CLI wrappers. | Purge specific tools; convert them to raw scripts or project `.rules` files. |
| **The "Prompt Engineer" Tool** | Re-writing API documentation into a `SKILL.md` so the agent knows how to use an API. | Use MCP to expose the API natively with strong JSON schemas. |
| **Cognitive Offloading** | Asking a python script to "analyze" logic rather than compute state. | Scripts should *execute* (Tool); the Agent should *analyze* (Skill). |
