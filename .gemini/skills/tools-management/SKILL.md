---
name: tools-management
version: 1.0.0
description: >
  Use when deciding whether to implement an abstraction as a cognitive Skill, an MCP Server, or a low-level Tool (script).
  Handles the boundary between high-level reasoning methodologies and low-level task automation, framework patterns, and API wrappers.
category: architecture
tags: [tools, automation, scripts, mcp, delegation, architecture]
references:
  - name: MCP Integration Governance
    path: ../mcp-integration-governance/SKILL.md
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

### 1. The "No Thin Wrappers" Rule

Do NOT create a high-level `SKILL.md` just to wrap a single CLI command or API call. 

✅ **Good (Tool Script):** A simple `generate_pdf.py` script stored in `tools/pdf-generator/`, alongside a `description.md`, invoked directly by the agent when it needs to generate a PDF.

### 2. Nesting Tools Inside Skills

When a cognitive Skill requires specific mechanized actions to accomplish its goals, store those tools as scripts *within the skill's folder*.

```
skills/
  cc-isolate-debugging/
    SKILL.md              <-- The cognitive methodology (binary search isolation)
    scripts/
      run_test_subset.sh  <-- The tool (mechanization)
```

**Rule of Thumb:** If the tool is only useful in the context of one methodology, nest it. If it is generally useful across the entire repository (e.g., "Reset Database"), put it in its own folder within the archive's `tools/` directory, complete with a `description.md`.

### 3. Offloading to MCP

If a Tool requires complex state management, external API keys, rate limiting, or connection to proprietary data sources, **do not** write it as a local shell script. Delegate it to an **MCP Server**.

- If you want the agent to read Jira tickets → Use MCP.
- If you want the agent to automate Gmail → Use MCP.
- If you want the agent to run a local Vite dev server → Use a bash script (Tool).

See `mcp-integration-governance/SKILL.md` for details on building MCP servers.

### 4. Framework Patterns belong in Context, not Skills

Many community "skills" (like Vercel React Best Practices) are just coding guidelines. These do not belong in the Skill Archive. They belong directly in the project contextual layer.

- Use `.cursorrules`, `.windsurfrules`, or a global AI configuration file (`.agent/rules.md`).
- Do not burden the agent's dynamic skill-loading mechanism with static syntax preferences.

## Implementation Workflow

When faced with a new automation requirement (e.g., "I need the agent to test the web app"):

1. **Does it require critical thinking and a multi-step methodology?** 
   - Yes: Write a `SKILL.md`.
2. **Does it require external API access or specific application state?**
   - Yes: Build an MCP Server.
3. **Is it just a list of coding preferences or syntax rules?**
   - Yes: Put it in a project-specific rule file (e.g. `.cursorrules`).
4. **Is it a repeatable mechanized task (e.g. running a test suite, generating a report)?**
   - Yes: Write a bash/python script inside its own folder in the archive's `tools/` directory, and include a `description.md`.
   - **Crucial:** After adding the tool, run `python generate_readme.py` in the archive root to index it in the global directory.

## Anti-Patterns

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Skill Bloat** | Skill Archive reaches 50+ files, mostly consisting of framework tutorials and CLI wrappers. | Purge specific tools; convert them to raw scripts or project `.rules` files. |
| **The "Prompt Engineer" Tool** | Re-writing API documentation into a `SKILL.md` so the agent knows how to use an API. | Use MCP to expose the API natively with strong JSON schemas. |
| **Cognitive Offloading** | Asking a python script to "analyze" logic rather than compute state. | Scripts should *execute* (Tool); the Agent should *analyze* (Skill). |
