# 📚 Skill Archive

A comprehensive library of AI agent skills and cognitive frameworks, structurally organized around Lean manufacturing, Kaizen continuous improvement, and Toyota Production System (TPS) methodologies.

## 📂 Repository Structure

| Directory | Purpose |
|-----------|---------|
| `skills/` | High-level cognitive methodologies and tactical frameworks (Markdown + YAML frontmatter). |
| `tools/` | Low-level, standalone execution scripts (Bash/Python). |
| `workflows/`| Multi-step protocols for complex agent tasks. |
| `templates/`| Standardized formatting templates for new skills. |

## 📋 Skill Index

### 🗂️ Agile / SDLC

| Skill | Description | Tags |
|-------|-------------|------|
| **[Agile Architecture](skills/architectural-anchoring/SKILL.md)** | Use when making architectural decisions, enforcing layer boundaries, or when AI-suggested changes conflict with established patterns. Mandates ANCHOR.md enforcement, ADR logs, and Clean Architecture layer rules. | `agile` `architecture` `clean-architecture` |
| **[Agile Backlog](skills/agile-backlog/SKILL.md)** | Use when creating, editing, or reviewing Agile artifacts: Initiatives, Epics, Stories, Subtasks, Issues, Bugs. Enforces hierarchy and BDD acceptance criteria. | `agile` `backlog` `methodology` |
| **[Agile Release Gate](skills/agile-release-gate/SKILL.md)** | Use when preparing final release sign-off. Governs the pre-release audit checklist, traceability verification, and Release Memo compilation. | `agile` `release` `engineering` |
| **[Agile SDLC](skills/agile-sdlc/SKILL.md)** | Use when orchestrating the full SDLC across Agile, TDD, and testing stages. Governs Planning → Dev → CI → Verification → Regression → Release transitions. | `agile` `sdlc` `methodology` |
| **[Agile Testing](skills/agile-testing/SKILL.md)** | Use when authoring Test Plans, Test Designs, or Test Executions. Handles UI, back-end, integration, and regression testing artifacts. | `agile` `testing` `methodology` |
| **[Spec Mapping](skills/spec-mapping/SKILL.md)** | Use when mapping a spec document into the backlog as epics + stories with a coverage ledger. Anti-hallucination, append-only workflow with convergence gates. | `agile` `spec` `mapping` |

### 🏗️ Architecture

| Skill | Description | Tags |
|-------|-------------|------|
| **[Interface Governance](skills/interface-governance/SKILL.md)** | Use when designing, building, auditing, testing, or consuming MCP servers and clients. Integrates API-Design-First pr... | `architecture` `testing` `mcp` `methodology` |
| **[Shusa](skills/shusa-leadership/SKILL.md)** | The Shusa (Chief Engineer) leadership model for technical ownership and product vision. Ensures that a single individ... | `design` `leadership` `methodology` `lean` `TPS` |
| **[Swarm Orchestration](skills/swarm-orchestration/SKILL.md)** | Protocols for multi-agent coordination and delegation.  Ensures that specialized sub-agents are tasked precisely and ... | `communication` `design` `kubernetes` |
| **[Value Stream Mapping](skills/vsm/SKILL.md)** | Use when diagnosing slow workflows, high token consumption, or unexplained latency in multi-step tasks. Handles curre... | `design` `methodology` `optimization` `lean` `TPS` |

### 🧠 Cognition

| Skill | Description | Tags |
|-------|-------------|------|
| **[Comprehend](skills/comprehension-gate/SKILL.md)** | Use before debugging, extending, or shipping code. Acts as a strict policy gate implementing Risk-Tiered comprehensio... | `cognition` `safety` `routing` `methodology` |
| **[Deglaze](skills/logic-deglazing/SKILL.md)** | Use when reviewing AI-generated solutions, validating user comprehension, or stress-testing proposals. Handles 5 cons... | `cognition` `safety` `methodology` |
| **[Gemba](skills/gemba/SKILL.md)** | Use to establish a factual baseline of the codebase. Mandates direct observation before reasoning and enforces a stru... | `context` `methodology` `research` `lean` `TPS` |
| **[Hansei](skills/hansei/SKILL.md)** | Use when a plan fails, a bug is found, or a post-mortem is needed. Mandates 5-Whys root-cause analysis. | `cognition` `methodology` `lean` `TPS` `kaizen` |

### ⚙️ Engineering

| Skill | Description | Tags |
|-------|-------------|------|
| **[Anchor](skills/architectural-anchoring/SKILL.md)** | Use when starting a project, making architectural decisions, or when AI-suggested changes conflict with established p... | `design` `architecture` |
| **[Code Review](skills/code-review/SKILL.md)** | Use when performing a structured code review. Handles impact analysis, code quality audit, and regression confirmation. | `engineering` `code-review` `quality` |
| **[Isolate (Root Cause Isolation)](skills/root-cause-isolation/SKILL.md)** | Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed. Handles 5-step hypothesis-driven debugging, binary search isolation, minimal reproduction, and tactical grep-powered discovery. | `debugging` `engineering` `search` |
| **[PowerShell 7 Efficiency](skills/powershell-7-efficiency/SKILL.md)** | Use when writing or optimizing PowerShell 7 scripts. Mandates the use of modern features like pipeline chaining, para... | `engineering` `scripting` `automation` `performance` `cross-platform` |
| **[Refactor Safely](skills/refactor-safely/SKILL.md)** | Use when planning or executing a refactor. Enforces impact analysis before edits and continuous test validation after each step. | `engineering` `refactoring` `safety` |
| **[Ship](skills/release-management/SKILL.md)** | Use when code is "feature complete" and approaching deployment, or when verifying production readiness. Handles stagi... | `engineering` `safety` `methodology` |
| **[Test-Driven Development (TDD)](skills/test-driven-development/SKILL.md)** | Use when implementing any feature or bugfix, before writing implementation code. Enforces the strict Red-Green-Refact... | `engineering` `testing` `methodology` `git` |
| **[Verification Before Completion](skills/completion-verification/SKILL.md)** | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs. Requires running veri... | `safety` `engineering` `debugging` |

### 📌 Memory

| Skill | Description | Tags |
|-------|-------------|------|
| **[Context Engine](skills/context-engine/SKILL.md)** | Use when required to retrieve information, learn codebase rules, read files over 4,000 tokens, or record short-term p... | `memory` `mcp` `rag` `state` |

### 🔄 Meta

| Skill | Description | Tags |
|-------|-------------|------|
| **[External Synthesis](skills/external-synthesis/SKILL.md)** | Use when researching new agent skills. Guides the agent to search external repositories and synthesize patterns into ... | `meta` `research` |
| **[Skill Authoring Management](skills/skill-authoring-management/SKILL.md)** | Use when creating, reviewing, or managing agent skills.  Provides the authoritative "Gold Standard" for content and f... | `meta` |
| **[Tools Management](skills/tools-management/SKILL.md)** | Use when deciding whether to implement an abstraction as a cognitive Skill, an MCP Server, or a low-level Tool (scrip... | `architecture` `design` `meta` |
| **[Workflow Management](skills/workflow-management/SKILL.md)** | Use when creating, reviewing, or managing workflows. Ensures workflows meet the structural standards and prevents doc... | `meta` `architecture` |

### 📐 Methodology

| Skill | Description | Tags |
|-------|-------------|------|
| **[Development Story Interview](skills/interview/SKILL.md)** | Use when a user requests feature scoping, requirement definition, or planning a new idea. Applies Socratic questionin... | `methodology` `lean` `cognition` `heijunka` `context-engine` |
| **[Genchi Genbutsu](skills/genchi-genbutsu/SKILL.md)** | Use to "Go and See for Yourself." Mandates empirical verification of all hypotheses and findings through direct execu... | `methodology` `research` `testing` `lean` `TPS` |
| **[Heijunka](skills/heijunka/SKILL.md)** | Use to level the workload and prevent token/context spikes (Muri).  Handles the decomposition of massive tasks into m... | `methodology` `optimization` `lean` `TPS` |
| **[Hō-Ren-Sō](skills/ho-ren-so/SKILL.md)** | Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human oper... | `communication` `methodology` `lean` `TPS` |
| **[Incident Management](skills/incident-management/SKILL.md)** | Use when creating, updating, resolving, or referencing incident reports. Handles the lifecycle of incidents (active/r... | `debugging` `cognition` `context` `research` |
| **[Kaizen](skills/kaizen/SKILL.md)** | Use when a recurring error, structural bottleneck, or workflow inefficiency is identified (either manually or via Han... | `methodology` `optimization` `lean` `TPS` `kaizen` |
| **[Kodawari Craftsmanship](skills/kodawari-craftsmanship/SKILL.md)** | Use during any code modification or creation task as an always-active operating principle. Mandates the relentless pu... | `design` `methodology` `lean` `TPS` |
| **[Lean Foundations](skills/lean-foundations/SKILL.md)** | Foundational Lean principles for stabilizing workflows through the 3 Ms (Mura, Muri, Muda) and the 5S framework. Focu... | `methodology` `optimization` `lean` `TPS` |
| **[Nemawashi](skills/nemawashi/SKILL.md)** | Use before suggesting major refactors or architectural changes. Mandates impact analysis and A3 proposals. | `methodology` `lean` `TPS` |
| **[Shisa Kanko](skills/shisa-kanko/SKILL.md)** | Use when executing code changes, tool calls, or multi-step tasks. Mandates pointing, calling, and verification. | `methodology` `safety` `lean` `TPS` `cognition` `communication` `routing` |
| **[Yokoten](skills/yokoten/SKILL.md)** | Horizontal deployment of knowledge and best practices.  Used to "broadcast" successful patterns or critical fixes fro... | `methodology` `lean` `TPS` `kaizen` |

### 🛡️ Safety

| Skill | Description | Tags |
|-------|-------------|------|
| **[Jidoka (Autonomation)](skills/jidoka/SKILL.md)** | Use when an abnormality occurs, an iteration threshold is breached, or before executing any action flagged by the Lay... | `methodology` `safety` `lean` `TPS` |
| **[KYT](skills/kyt/SKILL.md)** | Use before executing high-risk, destructive, or irreversible commands (rm, drop, reset). Mandates hazard prediction. | `methodology` `safety` `lean` `TPS` |
| **[Poka-yoke](skills/poka-yoke/SKILL.md)** | Use when designing validation gates, enforcing schemas, or preventing invalid tool calls. Handles deterministic guard... | `methodology` `safety` `lean` `TPS` |
| **[Red-Teaming](skills/red-teaming-tactics/SKILL.md)** | Adversarial stress-testing for security and logic.  Use to identify bypasses, edge-case failures, and "happy-path" bi... | `safety` `security` |
| **[Secure](skills/security-enforcement/SKILL.md)** | Use when handling auth, user input, secrets, or API endpoints. Mandates trust-boundary audits. | `security` |

## 🤖 Agent Index

> Sub-agents for use with Claude Code's `/agents` system or the Anthropic Agent SDK. Copy into your project's `.claude/agents/` directory. All are naturalized — remove any remaining project-specific references before use.

| Agent | Model | Role |
|---|---|---|
| **[Analyst](agents/analyst.md)** | sonnet | Spec mapping, gap analysis, citation integrity |
| **[Architect](agents/architect.md)** | opus | Clean Architecture enforcement, interface contracts, ADR stewardship |
| **[Developer](agents/developer.md)** | haiku | TDD execution, code implementation, subtask management |
| **[DevOps](agents/devops.md)** | sonnet | CI/CD pipelines, Docker, environment parity, infrastructure backlog |
| **[Product Owner](agents/product-owner.md)** | sonnet | Initiatives, Epics, Stories, BDD ACs, backlog prioritization |
| **[Release Manager](agents/release-manager.md)** | opus | Final sign-off, release memo, traceability audit, gap closure |
| **[Scrum Master](agents/scrum-master.md)** | sonnet | SDLC governance, traceability auditing, blocker resolution |
| **[Security Lead](agents/security-lead.md)** | opus | Security review, input validation, safety gating, veto authority |
| **[Tester](agents/tester.md)** | haiku | Test Plans, Test Designs, Test Executions, regression safety |
| **[UX Designer](agents/ux-designer.md)** | sonnet | Design system, visual spec sync, accessibility, UI sign-off |

## 📋 Workflow Index

| Workflow | Description |
|----------|-------------|
| **[Lean Analysis Workflow](workflows/1-lean-analysis.md)** | Run a full Lean analysis on a document or topic using all 9 lean-tagged skills as analytical lenses |
| **[Kaizen Sprint Workflow](workflows/2-kaizen-sprint.md)** | Standardized procedure for a rapid Kaizen iteration focusing on a single, isolated module. |
| **[TPS Architecture Review Workflow](workflows/3-tps-architecture-review.md)** | Run a heavy-duty system-level architectural review for major refactors, cross-domain integrations, or organizational ... |
| **[AI Agent Skill Import](workflows/ai-agent-skill-import.md)** | Procedure for synthesizing new agentic capabilities from an external repository into the local Skill Archive. |
| **[Master Topic Refinement Workflow (with Context Engine)](workflows/master-topic-refinement-with-context-engine.md)** | A multi-phase refinement protocol enhanced by the Context Engine to ensure a topic, documentation, or codebase reache... |
| **[Master Topic Refinement Workflow](workflows/master-topic-refinement.md)** | A multi-phase refinement protocol to ensure a topic, documentation, or codebase reaches the highest level of Lean qua... |
| **[Parallel Processing Workflow (Map-Reduce)](workflows/parallel-processing.md)** | High-speed execution pattern via parallel Map-Reduce, delegating chunks of work to concurrent sub-agents or determini... |

## 🛠️ Tools Index

> Standalone, low-level execution scripts. See the [Tools Management Strategy](skills/tools-management/SKILL.md).

| Tool | Description |
|------|-------------|
| **[__pycache__](tools/__pycache__)** |  |
| **[context-heijunka](tools/context-heijunka)** | This tool implements the **Heijunka (Production Leveling)** and **Swarm Orchestration** principles to prevent LLM context overburden (Muri) when analyzing external repositories. |
| **[docx-tools](tools/docx-tools)** | A Python automation script using `python-docx` to read and generate Word documents programmatically. |
| **[git-worktree-setup](tools/git-worktree-setup)** | An automation bash script that streamlines the process of checking out a new feature branch in an isolated directory using Git Worktrees, followed by automated project setup. |
| **[image-converter](tools/image-converter)** |  |
| **[mcp-servers](tools/mcp-servers)** | The project is configured to use several Model Context Protocol (MCP) servers to extend the agent's capabilities with external tools, web interactions, and long-term memory. |
| **[pdf-tools](tools/pdf-tools)** | A Python tool leveraging `PyMuPDF` (`fitz`) for fast, robust PDF manipulation. |
| **[playwright-scaffold](tools/playwright-scaffold)** | A JavaScript automation script that injects a best-practice Playwright testing environment into any web project. |
| **[xlsx-tools](tools/xlsx-tools)** | A Python script using `openpyxl` to extract data from Excel spreadsheets efficiently. |
| **[youtube-transcript](tools/youtube-transcript)** | A Python automation tool using `yt-dlp` to fetch transcriptions and subtitles for YouTube videos. |
| **[agile-hierarchy-validator](tools/agile-hierarchy-validator)** | PowerShell: validates parentage hierarchy and link integrity across backlog and test artifacts. Enforces Initiative→Epic→Story→Subtask and TP→TS→TD→TX chains. |
| **[agile-turn-commit](tools/agile-turn-commit)** | PowerShell: automates end-of-turn hierarchy validation, SDLC path staging, `[Phase] ID: Message` commit, and push. |
| **[audit-go](tools/audit-go)** | Python: four standalone Go code-quality scripts — lint (golangci-lint), naming conventions, unused imports (go vet), and standards (error handling, docs). |
| **[audit-python](tools/audit-python)** | Python: four standalone Python code-quality scripts — lint (pylint/ruff), naming conventions (AST), unused imports (AST), and standards (docstrings, function length). |
| **[backlog-tools](tools/backlog-tools)** | PowerShell: New-Issue, Triage-Issues, Export-BacklogSummary, and Search-AllArtifacts for managing SDLC backlog artifacts. |
| **[chaos-tester](tools/chaos-tester)** | PowerShell: generates a structured AI prompt for adversarial edge-case and chaos test scenarios for a given source file. |
| **[git-hooks](tools/git-hooks)** | PowerShell: install-hooks.ps1 (pre-commit framework installer) and git-pre-commit.ps1 (Go auto-fixer shim for goimports + go mod tidy). |
| **[spec-gap-tools](tools/spec-gap-tools)** | PowerShell: Find-SpecGaps.ps1 — lists spec files with no corresponding .map-spec ledger entry. |
| **[tdd-phase-verifier](tools/tdd-phase-verifier)** | Python: lints a git commit range to enforce [Red]/[Green]/[Refactor] TDD commit-prefix conventions. Configurable story-ID pattern and test-file patterns. |
| **[triage-validator](tools/triage-validator)** | Python: validates that bugs and issues have completed the mandatory triage review process. Auto-detects backlog root. |
atory triage review process. Auto-detects backlog root. |
