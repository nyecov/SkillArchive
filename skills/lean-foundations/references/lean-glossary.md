# Lean Glossary & Concepts

This document provides the foundational background for the concepts utilized in the `lean-foundations` methodology.

## The 3 Ms: The Trio of Inefficiency

1.  **Mura (Unevenness):** Inconsistency in workflow, logic, or output.
2.  **Muri (Overburden):** Pushing the model or context window beyond its optimal limits.
3.  **Muda (Waste):** Activities that consume resources without adding value.

## The 7 Wastes of Agentic Workflows (Muda)

Agents MUST actively monitor and eliminate these common wastes:
1. **Over-generation:** Writing more code than is strictly necessary (e.g., adding "just-in-case" features).
2. **Waiting:** Stalling on slow API calls without parallelizing tasks.
3. **Transportation (Context Bloat):** Pushing unnecessarily large context windows, causing hallucinations.
4. **Over-processing:** Using complex reasoning for tasks that simple deterministic scripts or regex could solve.
5. **Inventory (Unused Data):** Storing intermediate state or variables never consumed by the final execution.
6. **Motion (Navigational Waste):** Endless searching through directories due to imprecise initial pointing.
7. **Defects (Hallucinations):** Producing incorrect outputs that require rework. This is the worst form of waste.

## The 5S Framework for Agentic Workspaces

1.  **Seiri (Sort):** Distinguish between necessary and unnecessary files/context. Delete logs and trial scripts.
2.  **Seiton (Set in Order):** A place for everything. Follow established project structures.
3.  **Seiso (Shine):** Clean the workspace. Remove "dead code" and outdated comments.
4.  **Seiketsu (Standardize):** Use templates (`skill-template.md`) and consistent naming.
5.  **Shitsuke (Sustain):** Perform regular **Hansei** to ensure the standards are maintained.
