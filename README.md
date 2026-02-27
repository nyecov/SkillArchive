# Skill Archive: A Lean AI Engineering Environment

Management and storage for AI agent skills, engineered with **Lean Principles** (Toyota Production System) at its absolute core. This repository provides a structured methodology for AI agents to operate with maximum efficiency, zero waste, and uncompromising quality.

## Structure
- `skills/`: Markdown skill files with YAML frontmatter. Contains high-level cognitive methodologies, categorized by Lean principles.
- `tools/`: Low-level standalone execution scripts (Bash/Python).
- `templates/`: Standard formats for new skills.

## Rules
- All paths within the project MUST be relative.
- Absolute paths are ONLY allowed if they point to external repositories.

---

## 📥 Importing Skills

Importing skills from this library into your agent's environment is straightforward. No installation scripts are required.

1. **Locate the Skill:** Find the desired skill folder within the `skills/` directory of this repository.
2. **Copy the Folder:** Copy the entire skill folder (e.g., `skills/lean-foundations`).
3. **Paste into Agent Skills:** Paste the copied folder into your agent's designated skills directory (e.g., `.gemini/skills/`).

**Dependency Note:** While skills are designed to be standalone methodologies, many work best in tandem. For example:
- Importing **[Kaizen](skills/kaizen/SKILL.md)** works best if **[Hansei](skills/hansei/SKILL.md)** is also imported for root-cause analysis.
- **[Shisa Kanko](skills/shisa-kanko/SKILL.md)** is greatly enhanced when paired with **[Genchi Genbutsu](skills/genchi-genbutsu/SKILL.md)** for execution verification.
- **[Lean Foundations](skills/lean-foundations/SKILL.md)** establishes stability through 3M & 5S for comprehensive waste elimination.

Review the skill's description to understand if related cognitive patterns might benefit your workflow.

---

## 📚 Lean-Core Agent Skills

These skills dictate how an AI agent thinks, plans, and acts, ensuring that every operation is optimized, safe, and verifiable.

### 1. The Lean Foundation (Stability & Waste Elimination)
*Focuses on establishing a stable environment, observing reality, and identifying/removing waste (Muda).*

- **[Lean Foundations: Stability through 3M & 5S](skills/lean-foundations/SKILL.md)**
  - **What it does:** Establishes a baseline for workflow stability by addressing variation (Mura), overburden (Muri), and waste (Muda), alongside 5S organization.
  - **Impact:** Creates a predictable, consistent environment where specialized AI agents can operate without structural friction.
  - **Usage:** Apply when setting up a new environment, stabilizing an erratic workflow, or establishing foundational rules.

- **[Value Stream Mapping (VSM) for Agents](skills/vsm/SKILL.md)**
  - **What it does:** Maps the end-to-end flow of information and actions to identify bottlenecks and non-value-added steps.
  - **Impact:** Provides a strategic overview for optimizing complex multi-step tasks and reducing overall lead time.
  - **Usage:** Use to diagnose and redesign complex workflows that span multiple agents or require excessive tool calls.

- **[Heijunka (Production Leveling)](skills/heijunka/SKILL.md)**
  - **What it does:** Breaks down large, complex tasks into uniform, manageable units of work to prevent system overload.
  - **Impact:** Prevents context window exhaustion and ensures steady, reliable progress without erratic bursts of activity.
  - **Usage:** Apply when confronted with massive refactors, bulk file processing, or large-scale data migrations.

- **[Gemba: The Cognitive Context Engine](skills/gemba/SKILL.md)**
  - **What it does:** Forces the agent to directly observe the actual codebase using tools rather than relying on assumptions.
  - **Impact:** Eliminates hallucinations by grounding all reasoning in verified, current facts.
  - **Usage:** Invoke at the start of any new task or when confronted with ambiguous or undocumented systems.

### 2. Built-in Quality & Safety (Jidoka)
*Focuses on stopping to fix problems, mistake-proofing, and rigorous security.*

- **[Jidoka: Autonomation for AI Agents (The Andon Cord)](skills/jidoka/SKILL.md)**
  - **What it does:** Empowers the agent to stop immediately when an error is detected, preventing the compounding of defects.
  - **Impact:** Ensures high quality by catching bugs at the source and preventing flawed code from progressing.
  - **Usage:** Trigger automatically upon test failures, compilation errors, or unexpected tool outputs.

- **[Poka-yoke: Mistake-proofing AI Workflows](skills/poka-yoke/SKILL.md)**
  - **What it does:** Implements "mistake-proofing" mechanisms that make it impossible (or very difficult) to perform an action incorrectly.
  - **Impact:** Drastically reduces human and agent error by enforcing strict schemas, types, and validation gates.
  - **Usage:** Apply when designing APIs, creating new tools, or writing scripts that handle sensitive data.

- **[Isolate: Systematic Debugging](skills/isolate-debugging/SKILL.md)**
  - **What it does:** Provides a rigorous, scientific method for isolating the root cause of a bug rather than guessing.
  - **Impact:** Reduces time spent "thrashing" during debugging and guarantees the identification of the true underlying issue.
  - **Usage:** Invoke whenever a bug is non-trivial, or after an initial fix attempt fails.

- **[KYT: Hazard Prediction Training for Agents](skills/kyt/SKILL.md)**
  - **What it does:** Forces a "Hazard Prediction Training" pause to identify potential catastrophic outcomes before taking action.
  - **Impact:** Prevents accidental data loss, destructive system modifications, or unrecoverable state changes.
  - **Usage:** Required before running any commands that delete files, drop databases, or force-push.

- **[Red-Teaming Tactics](skills/red-teaming-tactics/SKILL.md)**
  - **What it does:** Adopts an adversarial mindset to actively look for ways to break, bypass, or exploit a proposed solution.
  - **Impact:** Hardens the system against edge cases and security vulnerabilities before the code is committed.
  - **Usage:** Apply during the strategy phase of critical implementations or when reviewing security-sensitive code.

- **[Secure: Security for the Uninitiated](skills/secure-security/SKILL.md)**
  - **What it does:** Enforces strict security audits across trust boundaries, ensuring secure handling of credentials and inputs.
  - **Impact:** Prevents the introduction of vulnerabilities like injection, exposed secrets, or broken access control.
  - **Usage:** Mandatory when touching authentication, authorization, or code processing external user input.

### 3. Continuous Improvement & Standardization (Kaizen)
*Focuses on incremental improvement, reflection, and spreading good practices globally.*

- **[Kaizen: Continuous Agentic Improvement](skills/kaizen/SKILL.md)**
  - **What it does:** Facilitates continuous, incremental improvement through the Plan-Do-Check-Act (PDCA) cycle.
  - **Impact:** Ensures the agent's methodologies and the project's codebase are constantly evolving and improving.
  - **Usage:** Invoke to permanently fix recurring issues or optimize a slow, reliable process.

- **[Hansei: Agentic Self-Reflection](skills/hansei/SKILL.md)**
  - **What it does:** Conducts deep self-reflection to understand *why* a failure occurred using 5-Whys root-cause analysis.
  - **Impact:** Prevents the same mistake from happening twice by updating standards based on lessons learned.
  - **Usage:** Required after resolving a severe bug, a failed plan, or a difficult implementation.

- **[Yokoten: Horizontal Deployment](skills/yokoten/SKILL.md)**
  - **What it does:** Takes a solution developed in one area and systematically applies it to all other applicable areas.
  - **Impact:** Maximizes the ROI of problem-solving by ensuring global consistency and preventing localized regressions.
  - **Usage:** Apply after a successful refactor, security patch, or optimization to spread the benefit.

- **[Anchor: Architectural Coherence](skills/anchor-coherence/SKILL.md)**
  - **What it does:** Establishes "Anchor" files to lock in core architectural decisions, preventing unauthorized drift.
  - **Impact:** Maintains structural integrity (Wa) and ensures long-term alignment with the original design vision.
  - **Usage:** Use when defining new architectures, or to check if proposed changes violate established project invariants.

- **[Shisa Kanko Engineering Master Workflow](skills/shisa-kanko/SKILL.md)**
  - **What it does:** Adapts "Pointing and Calling" safety systems, ensuring deliberate execution and immediate verification.
  - **Impact:** Drastically reduces careless errors and hallucinated paths by forcing explicit acknowledgment of state.
  - **Usage:** The default execution workflow for all code modifications and tool operations.

- **[Kodawari: Devoted Craftsmanship](skills/kodawari-craftsmanship/SKILL.md)**
  - **What it does:** Elevates code from functional to "craftsmanship," focusing on naming, structure, and aesthetic harmony.
  - **Impact:** Produces code that is exceptionally readable, maintainable, and idiomatic to the surrounding project.
  - **Usage:** Apply during the final polish of any implementation or when refactoring legacy code.

### 4. Leadership, Consensus & Orchestration
*Focuses on technical ownership, communication, and multi-agent coordination.*

- **[Shusa: The Chief Engineer Model](skills/shusa-leadership/SKILL.md)**
  - **What it does:** Assumes end-to-end technical responsibility for a feature, acting as the ultimate authority.
  - **Impact:** Prevents "design by committee" and ensures a coherent, unified vision across the system.
  - **Usage:** Adopt this stance when tasked with delivering a complex feature or leading a project refactor.

- **[Nemawashi (Foundation Building)](skills/nemawashi/SKILL.md)**
  - **What it does:** Gathers consensus and analyzes the full impact of a proposed change before formal introduction.
  - **Impact:** Prevents disruptive architectural changes and ensures alignment with system constraints.
  - **Usage:** Required before embarking on large-scale refactoring or significant API changes.

- **[Hō-Ren-Sō: Communication Standard for Agents](skills/ho-ren-so/SKILL.md)**
  - **What it does:** Standardizes communication into Report, Communicate/Update, and Consult formats.
  - **Impact:** Keeps the user informed with high-signal updates and provides clear options when blocked.
  - **Usage:** Use when escalating issues or providing structured updates on tasks.

- **[Swarm Orchestration](skills/swarm-orchestration/SKILL.md)**
  - **What it does:** Coordinates complex tasks by delegating sub-tasks to specialized agents while maintaining context.
  - **Impact:** Enables parallel execution of complex workflows while ensuring the final output remains coherent.
  - **Usage:** Invoke when a task requires diverse expertise.

- **[Ontology (Structured Agent Memory)](skills/ontology/SKILL.md)**
  - **What it does:** Structures agent memory and project context as a queryable, typed knowledge graph.
  - **Impact:** Improves context retrieval, enables complex reasoning, and standardizes data structures.
  - **Usage:** Apply when designing systems that require robust tracking of relationships between entities.

### 5. Advanced Engineering & Procedural Tactics
*Focuses on specific technical implementations optimized for Lean workflows.*

- **[Genchi Genbutsu (Dynamic Verification)](skills/genchi-genbutsu/SKILL.md)**
  - **What it does:** Enforces the principle that truth comes from execution; requires running code, compiling, and testing.
  - **Impact:** Eliminates assumptions and guarantees that solutions actually work in reality.
  - **Usage:** Mandatory for verifying bug fixes, testing features, and validating system state.

- **[Comprehend: The Understanding Gate](skills/comprehend-understanding/SKILL.md)**
  - **What it does:** Ensures full understanding of existing code before modifying it via comprehension gates.
  - **Impact:** Prevents "blind" edits that break existing functionality or introduce subtle regressions.
  - **Usage:** Required when interacting with legacy code, undocumented systems, or complex logic.

- **[Deglaze: Anti-Sycophancy (Tactical Toolkit)](skills/deglaze-tactics/SKILL.md)**
  - **What it does:** Strips away assumptions and fluff to reveal the core truth of a proposed solution.
  - **Impact:** Produces robust, resilient solutions that survive scrutiny and constraint pressure.
  - **Usage:** Apply when reviewing PRs, evaluating plans, or validating AI-generated code.

- **[Docker Optimization Procedure](skills/docker-engineering/SKILL.md)**
  - **What it does:** Applies Lean to containerization, stripping waste from builds and enforcing security best practices.
  - **Impact:** Results in ultra-fast builds, minimal sizes, and hardened security postures.
  - **Usage:** Use when authoring or reviewing Dockerfiles.

- **[Kubernetes Hardening Procedure](skills/kubernetes-engineering/SKILL.md)**
  - **What it does:** Applies reliability and security principles to Kubernetes, enforcing resource bounds.
  - **Impact:** Ensures stable, predictable, and secure deployments.
  - **Usage:** Use when authoring or debugging Kubernetes manifests.

- **[Ship: Production Readiness](skills/ship-production/SKILL.md)**
  - **What it does:** Implements a rigorous final checklist covering security, performance, and rollback capabilities.
  - **Impact:** Prevents broken releases and ensures safe deployments.
  - **Usage:** Required immediately before pushing code to production.

- **[RAG Strategy: Context Optimization](skills/rag-strategy/SKILL.md)**
  - **What it does:** Optimizes context retrieval for LLMs, focusing on signal-to-noise ratio.
  - **Impact:** Significantly reduces token usage while improving accuracy.
  - **Usage:** Apply when designing knowledge retrieval systems.

- **[TOON Serialization Procedure](skills/toon-token-oriented-notation/SKILL.md)**
  - **What it does:** Compresses structured data into a highly efficient format for LLM consumption.
  - **Impact:** Maximizes context window utilization for vast datasets.
  - **Usage:** Use when feeding large tables or configuration arrays into context.

- **[Tools Management Strategy](skills/tools-management/SKILL.md)**
  - **What it does:** Provides a framework for deciding whether to use a Skill, Tool, or MCP Server.
  - **Impact:** Ensures the right abstraction layer is used, preventing overly complex tools.
  - **Usage:** Apply when expanding capabilities.

- **[Skill Authoring & Management (SAM)](skills/skill-authoring-management/SKILL.md)**
  - **What it does:** Defines the meta-rules and templates for creating new skills.
  - **Impact:** Ensures all skills are consistent, high-quality, and easy to parse.
  - **Usage:** Required whenever drafting a new `SKILL.md`.

- **[MCP & API-Design-First Governance](skills/interface-governance/SKILL.md)**
  - **What it does:** Governs the design of APIs and MCP interfaces to ensure they are LLM-friendly.
  - **Impact:** Produces robust, discoverable interfaces for AI agents.
  - **Usage:** Apply when building or integrating MCP servers.

- **[Skill External Synthesis](skills/external-synthesis/SKILL.md)**
  - **What it does:** Systematically researches and adapts external best practices into the local skill repository.
  - **Impact:** Accelerates development by leveraging community knowledge while maintaining coherence.
  - **Usage:** Invoke when creating a skill with likely prior art in the broader community.

---

## 🛠️ Tools Directory
> Standalone, low-level execution scripts. See [Tools Management Strategy](skills/tools-management/SKILL.md).

- **[docx-tools](tools/docx-tools)**
  > A Python automation script using `python-docx` to read and generate Word documents programmatically.

- **[git-worktree-setup](tools/git-worktree-setup)**
  > An automation bash script that streamlines the process of checking out a new feature branch in an isolated directory using Git Worktrees, followed by automated project setup.

- **[pdf-tools](tools/pdf-tools)**
  > A Python tool leveraging `PyMuPDF` (`fitz`) for fast, robust PDF manipulation.

- **[playwright-scaffold](tools/playwright-scaffold)**
  > A JavaScript automation script that injects a best-practice Playwright testing environment into any web project.

- **[xlsx-tools](tools/xlsx-tools)**
  > A Python script using `openpyxl` to extract data from Excel spreadsheets efficiently.

- **[youtube-transcript](tools/youtube-transcript)**
  > A Python automation tool using `yt-dlp` to fetch transcriptions and subtitles for YouTube videos.

---

## ⚙️ Library Maintenance (Meta Files)

The root directory contains several script and configuration files used exclusively for maintaining this repository. They leverage the AI agent's own capabilities to manage and update the Skill Archive:

- `check_refs.py`: Ensures that all skills correctly reference each other without broken links.
- `generate_readme.py`: Automates the generation of this documentation.
- `skills-config.json`: Configuration mapping for skill metadata.
- `sync_skills.py`: Syncs skills between the repository and local agent environments.
- `update_metadata.py`: Updates the YAML frontmatter within the `SKILL.md` files to keep tags and descriptions consistent.