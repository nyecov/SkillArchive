---
description: Procedural workflow to guide AI agents in discovering, verifying, and internalizing a skill from the Skill Archive library without hallucination.
---

# AI Agent Skill Import

A deterministic procedure for an AI agent to correctly internalize a new skill from the Skill Archive library. It actively prevents hallucination, ensures all dependencies are verified in bulk, and provides a structured recovery path if the skill requires missing resources.

## Input

The user provides:
- The target skill name or file path they wish the AI agent to import and internalize.

## Execution Phases

Run each phase sequentially. Only proceed to the next phase once the outputs of the current phase are fully realized.

---

### Phase 1: Context Discovery & Dependency Dry-Run

Before executing any logic, the importing agent MUST map and verify the entire dependency tree of the target skill.

1. **Locate Root:** Identify the `Skill Archive/` directory on the local filesystem.
2. **Parse Core:** Load the target skill document: `skills/[target-name]/SKILL.md`.
3. **Map Dependencies:** Locate all `references:` defined in the skill's YAML frontmatter.
4. **Dry-Run Paths:** Map all referenced file paths (e.g., `../other-skill/SKILL.md`, `templates/schema.md`) to absolute paths based on the local system.
5. **Verify Existence:** Verify that every single mapped dependency actually exists on the filesystem. **Constraint:** Do not stop at the first missing file; compile a complete list of all missing dependencies at once.

---

### Phase 2: Jidoka Evaluation (Halt Protocol)

Assess the results of the Phase 1 Dependency Dry-Run.

1. **Gate Check:** If all dependencies exist, proceed to Phase 3.
2. **Jidoka Halt:** If ANY dependencies are missing, immediately invoke a **Jidoka Halt** and stop the import process.
3. **Task File Generation:** Generate a progress task file (e.g., in `.gemini/tmp/import_task.md`) containing exactly these fields:
    - **Current Step:** Context Discovery & Dry-Run
    - **Attempted File Paths:** [List of all absolute paths the agent tried to resolve]
    - **Specific Missing Link(s):** [List of all dependencies that failed the existence check]
    - **Pending Actions:** [What the agent intended to do next]
4. **Hō-Ren-Sō:** Present the generated progress task file to the user and ask for their preference or guidance exactly *once*. Await user instructions before taking any further action.

---

### Phase 3: Internalize Mandates

Once all dependencies are successfully verified, structurally parse the skill documentation to understand its requirements.

1. **Load Templates:** Check the `templates/` directory (if referenced) for required output schemas and load them into context.
2. **Extract Logic:** Identify and map the **Action / Constraint / Integration** trio for every mandate within the skill:
    - **ACTION:** What the agent MUST execute.
    - **CONSTRAINT:** What the agent MUST NOT do (Poka-yoke).
    - **INTEGRATION:** How the skill connects to the broader ecosystem.

---

### Phase 4: Shisa Kanko (Correctness Declaration)

Before actively applying the skill to the user's core request, the agent MUST explicitly output a 4-point readiness check.

1. Output the following standard schema to the user:
   - **TARGET:** [Skill Name & Version]
   - **OBJECTIVE:** [1-sentence purpose]
   - **CRITICAL CONSTRAINT:** [The most important Poka-yoke from the skill]
   - **RESOURCES:** [List of resolved absolute paths for the skill and its references]
2. **Comprehension Gate:** If any of the logic remains ambiguous to the agent, trigger a Halt and ask the user for clarification. **Do NOT hallucinate procedures.**

---

### Phase 5: Execution

With the skill fully internalized and the readiness check passing, apply the skill.

1. **Trigger:** Process the user's initial core request through the lens of the newly internalized skill logic.
2. **Apply:** Follow the skill's specific workflow with 0% deviation.
3. **Output:** Deliver the expected task artifact or completion status.
