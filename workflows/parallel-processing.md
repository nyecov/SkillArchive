---
id: b1a8d88f-1096-47b0-aaab-eebc900a17d1
name: parallel-processing
version: 1.0.0
level: methodology
description: High-speed execution pattern via parallel Map-Reduce, delegating chunks of work to concurrent sub-agents or deterministic parallel scripts.
---
# Parallel Processing Workflow (Map-Reduce)

This workflow enables high-speed parallel execution of large tasks by sharding work and fanning it out to either concurrent `generalist` sub-agents (for cognitive tasks) or parallel shell scripts (for deterministic tasks).

## Phase 1: Task Evaluation & Categorization

Before attempting bulk processing, categorize the nature of the task.

### 1. Cognitive vs Deterministic Test
- **Cognitive:** Does the task require reasoning, synthesis, or making contextual decisions? (e.g., "Analyze architecture", "Refactor variable names based on context", "Security audit"). 
  - *Path:* Use **Concurrent Sub-Agents**.
- **Deterministic:** Is the task purely mechanical with clear rules? (e.g., "Find and replace string X", "Format files", "Lint codebase"). 
  - *Path:* Use **Parallel Shell Scripts** (e.g., PowerShell 7 `ForEach-Object -Parallel`).

## Phase 2: Sharding (The "Map" Step)

Chunk the workload into independent, non-overlapping segments.

- Identify the total scope (e.g., "50 files in `/src`").
- Divide the scope into discrete chunks (e.g., 5 chunks of 10 files).
- **CRITICAL CONSTRAINT:** Ensure no chunks mutate the same files or share mutable state to prevent race conditions.

## Phase 3: Execution (The "Fan-Out" Step)

Execute the appropriate parallel strategy.

### Path A: Cognitive Fan-Out (Concurrent Sub-Agents)
Invoke multiple `generalist` tool calls in a single turn.

1. **Assign Persona:** Prepend each request with a highly specific persona instructions. Example: "Role: Senior Backend Engineer. Task: Audit these 10 files for race conditions..."
2. **Assign Shard:** Pass exact file paths or sub-directories for that specific chunk.
3. **Execute:** Fire all `generalist` calls simultaneously. Wait for the host environment to return all results in the next turn.

### Path B: Deterministic Fan-Out (Parallel Scripts)
Generate and execute a highly optimized script.

1. Activate the `powershell-7-efficiency` skill if necessary.
2. Use `Get-ChildItem ... | ForEach-Object -Parallel { ... }` to blast through the workload natively.

## Phase 4: Synthesis (The "Fan-In" Step)

After all parallel tasks complete, perform synthesis.

1. **Review Outputs:** Read the returns from all concurrent sub-agents or script logs.
2. **Handle Failures:** Identify any chunks that failed or timed out. Re-run those specific shards if necessary.
3. **Aggregate:** Synthesize the findings or modifications into a single cohesive report or final commit. 

## Escalation

- If the context window limit is approached during a massive Fan-In, write the intermediate results to a temporary file in `.gemini/tmp/` instead of printing them directly to the conversation.
