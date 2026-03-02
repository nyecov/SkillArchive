# Context Engine: Skill Enforcement Strategy

A sovereign memory server is useless if the agent forgets to use its tools and reverts to flat-file reading or mental hallucination. To guarantee the Context Engine is ALWAYS in use, we must apply **Poka-yoke** (mistake-proofing) at three distinct architectural layers.

By implementing these three layers, the agent loses the "choice" to ignore the server; the engine becomes an inescapable part of the workspace physics.

## 1. The Global "Requires" Hook (Orchestration Layer)
The `Skill Archive` relies on dependency injection. We will force the `context-engine` to be injected into the LLM's system prompt globally.
- **Action:** Add `context-engine` as a mandatory global dependency in the root `system_instructions.txt` or `skills-config.json` file.
- **Effect:** Every single time the agent boots up, regardless of what task it is doing, the system prompt will explicitly instruct it: *"You are bound to the Context Engine. You MUST use the MCP memory tools (`ingest_context`, `read_session_state`) before making decisions."*

## 2. Hardwiring to Shisa Kanko (Methodology Layer)
`shisa-kanko` is the Master Workflow metric for execution. If an agent wants to write code, it *must* use Shisa Kanko. We will embed the Context Engine directly into the Shisa Kanko declaration.
- **Action:** Update `skills/shisa-kanko/SKILL.md` to include a new gate constraint.
- **Constraint:** *"Before executing the Shisa Kanko pointing protocol, you MUST execute the `read_session_state` MCP tool to verify your current phase. You MUST append your final verification result to the scratchpad using `log_session_finding`."*
- **Effect:** The agent cannot legally finish a task without executing the memory tools.

## 3. Tool Deprecation (The Poka-yoke Layer)
You cannot ask an agent to use `plan-with-files` *sometimes* and `log_session_finding` *other times*. Ambiguity breeds hallucination.
- **Action:** We completely delete the `rag-strategy`, `plan-with-files`, and `ontology` markdown skills from the repository.
- **Effect:** If the agent searches its own brain for "how to remember something" or "how to read a big file", the only instruction manual left in the entire repository will be the `context-engine` manual, which strictly points to the MCP tools.

## Summary
By deleting the legacy fallback methods, hardwiring the tools into the `shisa-kanko` master execution loop, and injecting the engine into the global configuration, you transform the Context Engine from an *optional* tool into the mandatory operating system of the agent.
