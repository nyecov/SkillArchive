# 📚 Skill Archive

A comprehensive library of AI agent skills and cognitive frameworks, structurally organized around Lean manufacturing, Kaizen continuous improvement, and Toyota Production System (TPS) methodologies.

## 📂 Repository Structure

| Directory | Purpose |
|-----------|---------|
| `skills/` | High-level cognitive methodologies and tactical frameworks (Markdown + YAML frontmatter). |
| `tools/` | Low-level, standalone execution scripts (Bash/Python). |
| `templates/`| Standardized formatting templates for new skills. |

## 📋 Skill Index

### 🏗️ Architecture

| Skill | Description | Tags |
|-------|-------------|------|
| **[Interface Governance](skills/interface-governance/SKILL.md)** | Use when designing, building, auditing, testing, or consuming MCP servers and clients. Integrates API-Design-First pr... | `architecture` `testing` `mcp` `methodology` |
| **[Ontology](skills/ontology/SKILL.md)** | Typed knowledge graph methodology for structured agent memory and composable actions.  Use to create, query, and enfo... | `context` `design` |
| **[Shusa](skills/shusa-leadership/SKILL.md)** | The Shusa (Chief Engineer) leadership model for technical ownership and product vision. Ensures that a single individ... | `design` `leadership` `methodology` `lean` `TPS` |
| **[Swarm Orchestration](skills/swarm-orchestration/SKILL.md)** | Protocols for multi-agent coordination and delegation.  Ensures that specialized sub-agents are tasked precisely and ... | `communication` `design` `kubernetes` |
| **[Value Stream Mapping](skills/vsm/SKILL.md)** | Use when diagnosing slow workflows, high token consumption, or unexplained latency in multi-step tasks. Handles curre... | `design` `methodology` `optimization` `lean` `TPS` |

### 🧠 Cognition

| Skill | Description | Tags |
|-------|-------------|------|
| **[Comprehend](skills/comprehend-understanding/SKILL.md)** | Use before debugging, extending, or shipping code the user cannot explain. Handles 4-level comprehension gates, rubbe... | `cognition` |
| **[Deglaze](skills/deglaze-tactics/SKILL.md)** | Use when reviewing AI-generated solutions, validating user comprehension, or stress-testing proposals. Handles 5 cons... | `cognition` `safety` `methodology` |
| **[Gemba](skills/gemba/SKILL.md)** | Use to establish a factual baseline of the codebase. Mandates direct observation before reasoning. | `context` `methodology` `research` `lean` `TPS` |
| **[Hansei](skills/hansei/SKILL.md)** | Use when a plan fails, a bug is found, or a post-mortem is needed. Mandates 5-Whys root-cause analysis. | `cognition` `methodology` `lean` `TPS` `kaizen` |
| **[Plan with Files](skills/plan-with-files/SKILL.md)** | Implements file-based planning to organize and track progress on complex tasks using persistent markdown files as wor... | `methodology` `context` `cognition` |
| **[RAG Strategy](skills/rag-strategy/SKILL.md)** | Optimization of Retrieval-Augmented Generation.  Focuses on minimizing "Search Waste" (Motion Muda) by ensuring high-... | `context` `optimization` |

### ⚙️ Engineering

| Skill | Description | Tags |
|-------|-------------|------|
| **[Anchor](skills/anchor-coherence/SKILL.md)** | Use when starting a project, making architectural decisions, or when AI-suggested changes conflict with established p... | `design` |
| **[Isolate](skills/isolate-debugging/SKILL.md)** | Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed. Handles 5-step hypothesis-driven... | `debugging` |
| **[Ship](skills/ship-production/SKILL.md)** | Use when code is "feature complete" and approaching deployment, or when verifying production readiness. Handles stagi... | `engineering` `safety` `methodology` |
| **[Test-Driven Development](skills/test-driven-development/SKILL.md)** | Use when implementing any feature or bugfix, before writing implementation code. Enforces the strict Red-Green-Refact... | `engineering` `testing` `methodology` |
| **[Verification Before Completion](skills/verification-before-completion/SKILL.md)** | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs. Requires running veri... | `safety` `engineering` `debugging` |

### 🔄 Meta

| Skill | Description | Tags |
|-------|-------------|------|
| **[External Synthesis](skills/external-synthesis/SKILL.md)** | Use when researching, designing, or authoring new agent skills. Guides the agent to search external repositories like... | `meta` `research` |
| **[Skill Authoring Management](skills/skill-authoring-management/SKILL.md)** | Use when creating, reviewing, or managing agent skills.  Provides the authoritative "Gold Standard" for content and f... | `meta` |
| **[Tools Management](skills/tools-management/SKILL.md)** | Use when deciding whether to implement an abstraction as a cognitive Skill, an MCP Server, or a low-level Tool (scrip... | `architecture` `design` `meta` |

### 📐 Methodology

| Skill | Description | Tags |
|-------|-------------|------|
| **[Development Story Interview](skills/story-interview/SKILL.md)** | Use when a user requests feature scoping, requirements definition, or wants to plan a new development story, bugfix, ... | `methodology` `methodology` `lean` `cognition` `heijunka` |
| **[Genchi Genbutsu](skills/genchi-genbutsu/SKILL.md)** | Use to "Go and See for Yourself." Mandates empirical verification of all hypotheses  and findings through direct exec... | `methodology` `research` `testing` `lean` `TPS` |
| **[Heijunka](skills/heijunka/SKILL.md)** | Use to level the workload and prevent token/context spikes (Muri).  Handles the decomposition of massive tasks into m... | `methodology` `optimization` `lean` `TPS` |
| **[Hō-Ren-Sō](skills/ho-ren-so/SKILL.md)** | Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human oper... | `communication` `methodology` `lean` `TPS` |
| **[Kaizen](skills/kaizen/SKILL.md)** | Use when a recurring error, structural bottleneck, or workflow inefficiency is identified. Handles PDCA-based experim... | `methodology` `optimization` `lean` `TPS` `kaizen` |
| **[Kodawari](skills/kodawari-craftsmanship/SKILL.md)** | Kodawari (Devoted Craftsmanship) for high-quality, self-documenting code. Mandates the relentless pursuit of perfecti... | `design` `methodology` `lean` `TPS` |
| **[Lean Foundations](skills/lean-foundations/SKILL.md)** | Foundational Lean principles for stabilizing workflows through the 3 Ms (Mura, Muri, Muda) and the 5S framework. Focu... | `methodology` `optimization` `lean` `TPS` |
| **[Nemawashi](skills/nemawashi/SKILL.md)** | Use before suggesting major refactors or architectural changes. Mandates impact analysis and A3 proposals. | `methodology` `lean` `TPS` |
| **[Shisa Kanko](skills/shisa-kanko/SKILL.md)** | Use when executing code changes, tool calls, or multi-step tasks. Mandates pointing, calling, and verification. | `cognition` `communication` `methodology` `safety` `lean` `TPS` |
| **[Yokoten](skills/yokoten/SKILL.md)** | Horizontal deployment of knowledge and best practices.  Used to "broadcast" successful patterns or critical fixes fro... | `methodology` `lean` `TPS` `kaizen` |

### 🛡️ Safety

| Skill | Description | Tags |
|-------|-------------|------|
| **[Jidoka](skills/jidoka/SKILL.md)** | Use when an abnormality, error, validation failure, or workflow loop occurs. Mandates an autonomous halt and root-cau... | `methodology` `safety` `lean` `TPS` |
| **[KYT](skills/kyt/SKILL.md)** | Use before executing high-risk, destructive, or irreversible commands (rm, drop, reset). Mandates hazard prediction. | `methodology` `safety` `lean` `TPS` |
| **[Poka-yoke](skills/poka-yoke/SKILL.md)** | Use when designing validation gates, enforcing schemas, or preventing invalid tool calls. Handles deterministic guard... | `methodology` `safety` `lean` `TPS` |
| **[Red-Teaming](skills/red-teaming-tactics/SKILL.md)** | Adversarial stress-testing for security and logic.  Use to identify bypasses, edge-case failures, and "happy-path" bi... | `safety` `security` |
| **[Secure](skills/secure-security/SKILL.md)** | Use when handling auth, user input, secrets, or API endpoints. Mandates trust-boundary audits. | `security` |

## 🛠️ Tools Index

> Standalone, low-level execution scripts. See the [Tools Management Strategy](skills/tools-management/SKILL.md).

| Tool | Description |
|------|-------------|
| **[context-heijunka](tools/context-heijunka)** | This tool implements the **Heijunka (Production Leveling)** and **Swarm Orchestration** principles to prevent LLM context overburden (Muri) when analyzing external repositories. |
| **[docx-tools](tools/docx-tools)** | A Python automation script using `python-docx` to read and generate Word documents programmatically. |
| **[git-worktree-setup](tools/git-worktree-setup)** | An automation bash script that streamlines the process of checking out a new feature branch in an isolated directory using Git Worktrees, followed by automated project setup. |
| **[pdf-tools](tools/pdf-tools)** | A Python tool leveraging `PyMuPDF` (`fitz`) for fast, robust PDF manipulation. |
| **[playwright-scaffold](tools/playwright-scaffold)** | A JavaScript automation script that injects a best-practice Playwright testing environment into any web project. |
| **[xlsx-tools](tools/xlsx-tools)** | A Python script using `openpyxl` to extract data from Excel spreadsheets efficiently. |
| **[youtube-transcript](tools/youtube-transcript)** | A Python automation tool using `yt-dlp` to fetch transcriptions and subtitles for YouTube videos. |
