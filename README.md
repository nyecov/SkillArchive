# Skill Archive

Management and storage for AI agent skills.

## Structure
- `skills/`: Markdown skill files with YAML frontmatter. Contains high-level cognitive methodologies.
- `tools/`: Low-level standalone execution scripts (Bash/Python).
- `templates/`: Standard formats for new skills.

## Rules
- All paths within the project MUST be relative.
- Absolute paths are ONLY allowed if they point to external repositories.

## 📚 Skill Directory

### Architecture

- **[MCP & API-Design-First Governance](skills/interface-governance/SKILL.md)**
  > Use when designing, building, auditing, or consuming MCP servers and clients. Integrates API-Design-First principles to ensure interfaces are optim...
  > *Tags:* `#architecture` `#meta` `#methodology`

- **[Ontology (Structured Agent Memory)](skills/ontology/SKILL.md)**
  > Typed knowledge graph methodology for structured agent memory and composable actions.  Use to create, query, and enforce constraints across interco...
  > *Tags:* `#context` `#design`

- **[Shusa: The Chief Engineer Model](skills/shusa-leadership/SKILL.md)**
  > The Shusa (Chief Engineer) leadership model for technical ownership and product vision. Ensures that a single individual (or agent) maintains total...
  > *Tags:* `#design` `#leadership` `#methodology`

- **[Swarm Orchestration](skills/swarm-orchestration/SKILL.md)**
  > Protocols for multi-agent coordination and delegation.  Ensures that specialized sub-agents are tasked precisely and their outputs are synthesized ...
  > *Tags:* `#communication` `#design` `#kubernetes`

- **[TOON Serialization Procedure](skills/toon-token-oriented-notation/SKILL.md)**
  > Procedure for serializing structured data into Token-Oriented Object Notation. Used to optimize LLM context windows and improve retrieval accuracy ...
  > *Tags:* `#architecture`

- **[Value Stream Mapping (VSM) for Agents](skills/vsm/SKILL.md)**
  > Use when diagnosing slow workflows, high token consumption, or unexplained latency in multi-step tasks. Handles current-state mapping, bottleneck i...
  > *Tags:* `#design` `#methodology` `#optimization`

### Cognition

- **[Comprehend: The Understanding Gate (Policy)](skills/comprehend-understanding/SKILL.md)**
  > Use before debugging, extending, or shipping code the user cannot explain. Handles 4-level comprehension gates, rubber duck escalation, and hard/so...
  > *Tags:* `#cognition`

- **[Deglaze: Anti-Sycophancy (Tactical Toolkit)](skills/deglaze-tactics/SKILL.md)**
  > Use when reviewing AI-generated solutions, validating user comprehension, or stress-testing proposals. Handles 5 constraint-pressure techniques: Co...

- **[Gemba: The Cognitive Context Engine](skills/gemba/SKILL.md)**
  > Use to establish a factual baseline of the codebase. Mandates direct observation before reasoning.
  > *Tags:* `#context` `#methodology` `#research`

- **[Hansei: Agentic Self-Reflection](skills/hansei/SKILL.md)**
  > Use when a plan fails, a bug is found, or a post-mortem is needed. Mandates 5-Whys root-cause analysis.
  > *Tags:* `#cognition` `#methodology`

- **[RAG Strategy: Context Optimization](skills/rag-strategy/SKILL.md)**
  > Optimization of Retrieval-Augmented Generation.  Focuses on minimizing "Search Waste" (Motion Muda) by ensuring high-signal context retrieval and e...
  > *Tags:* `#context` `#optimization`

### Engineering

- **[Anchor: Architectural Coherence](skills/anchor-coherence/SKILL.md)**
  > Use when starting a project, making architectural decisions, or when AI-suggested changes conflict with established patterns. Handles anchor docume...
  > *Tags:* `#design`

- **[Docker Optimization Procedure](skills/docker-engineering/SKILL.md)**
  > Procedure for auditing and optimizing Docker containers. Focuses on minimizing build Muda, image size, and attack surface using multi-stage builds ...
  > *Tags:* `#docker` `#engineering` `#optimization` `#security`

- **[Isolate: Systematic Debugging](skills/isolate-debugging/SKILL.md)**
  > Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed. Handles 5-step hypothesis-driven debugging, binary search isol...
  > *Tags:* `#debugging`

- **[Kubernetes Hardening Procedure](skills/kubernetes-engineering/SKILL.md)**
  > Procedure for auditing and hardening Kubernetes manifests. Ensures resource discipline (Muda reduction), resilience gates (Jidoka), and security in...
  > *Tags:* `#engineering` `#kubernetes` `#security`

- **[Ship: Production Readiness](skills/ship-production/SKILL.md)**
  > Use when code is "feature complete" and approaching deployment, or when verifying production readiness. Handles staging gates, 6-domain ship checkl...

### Meta

- **[Skill Authoring & Management (SAM)](skills/skill-authoring-management/SKILL.md)**
  > Use when creating, reviewing, or managing agent skills.  Provides the authoritative "Gold Standard" for content and formatting, management of skill...
  > *Tags:* `#meta`

- **[Skill External Synthesis](skills/external-synthesis/SKILL.md)**
  > Use when researching, designing, or authoring new agent skills. Guides the agent to search external repositories like the Claude Cookbook and Clawh...
  > *Tags:* `#meta` `#research`

- **[Tools Management Strategy](skills/tools-management/SKILL.md)**
  > Use when deciding whether to implement an abstraction as a cognitive Skill, an MCP Server, or a low-level Tool (script). Handles the boundary betwe...
  > *Tags:* `#architecture` `#design` `#meta`

### Methodology

- **[Genchi Genbutsu (Dynamic Verification)](skills/genchi-genbutsu/SKILL.md)**
  > Use to "Go and See for Yourself." Mandates empirical verification of all hypotheses  and findings through direct execution and testing.
  > *Tags:* `#methodology` `#research` `#testing`

- **[Heijunka (Production Leveling)](skills/heijunka/SKILL.md)**
  > Use to level the workload and prevent token/context spikes (Muri).  Handles the decomposition of massive tasks into manageable, consistent batches.
  > *Tags:* `#methodology` `#optimization`

- **[Hō-Ren-Sō: Communication Standard for Agents](skills/ho-ren-so/SKILL.md)**
  > Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human operator. Handles structured repor...
  > *Tags:* `#communication` `#methodology`

- **[Kaizen: Continuous Agentic Improvement](skills/kaizen/SKILL.md)**
  > Use when a recurring error, structural bottleneck, or workflow inefficiency is identified. Handles PDCA-based experiment design, controlled rollout...
  > *Tags:* `#methodology` `#optimization`

- **[Kodawari: Devoted Craftsmanship](skills/kodawari-craftsmanship/SKILL.md)**
  > Kodawari (Devoted Craftsmanship) for high-quality, self-documenting code. Mandates the relentless pursuit of perfection in the details, ensuring ar...
  > *Tags:* `#design` `#methodology`

- **[Lean Foundations: Stability through 3M & 5S](skills/lean-foundations/SKILL.md)**
  > Foundational Lean principles for stabilizing workflows through the 3 Ms (Mura, Muri, Muda)  and the 5S workplace organization framework. Focuses on...
  > *Tags:* `#methodology`

- **[Lean: Eradicating Agentic Waste (Muda)](skills/muda/SKILL.md)**
  > Use when a workflow feels slow, bloated, or produces unnecessary output. Handles classification of 7 waste types (Muda), value definition, surgical...
  > *Tags:* `#methodology` `#optimization`

- **[Nemawashi (Foundation Building)](skills/nemawashi/SKILL.md)**
  > Use before suggesting major refactors or architectural changes. Mandates impact analysis and A3 proposals.
  > *Tags:* `#methodology`

- **[Shisa Kanko Engineering Master Workflow](skills/shisa-kanko/SKILL.md)**
  > Use when executing code changes, tool calls, or multi-step tasks. Mandates pointing, calling, and verification.
  > *Tags:* `#cognition` `#communication` `#methodology` `#safety`

- **[Yokoten: Horizontal Deployment](skills/yokoten/SKILL.md)**
  > Horizontal deployment of knowledge and best practices.  Used to "broadcast" successful patterns or critical fixes from one module to all other rele...
  > *Tags:* `#methodology`

### Safety

- **[Circuit: The Iteration Breaker](skills/circuit-breaker/SKILL.md)**
  > Use when the same bug persists after 3+ attempts, regressions match fixes, or time spent exceeds the iteration budget. Handles circuit breaker trig...
  > *Tags:* `#safety`

- **[Jidoka: Autonomation for AI Agents (The Andon Cord)](skills/jidoka/SKILL.md)**
  > Use when an abnormality, error, or validation failure occurs. Mandates an autonomous halt and root-cause analysis.
  > *Tags:* `#methodology` `#safety`

- **[KYT: Hazard Prediction Training for Agents](skills/kyt/SKILL.md)**
  > Use before executing high-risk, destructive, or irreversible commands (rm, drop, reset). Mandates hazard prediction.
  > *Tags:* `#methodology` `#safety`

- **[Poka-yoke: Mistake-proofing AI Workflows](skills/poka-yoke/SKILL.md)**
  > Use when designing validation gates, enforcing schemas, or preventing invalid tool calls. Handles deterministic guardrails, prerequisite interlocks...
  > *Tags:* `#methodology` `#safety`

- **[Red-Teaming Tactics](skills/red-teaming-tactics/SKILL.md)**
  > Adversarial stress-testing for security and logic.  Use to identify bypasses, edge-case failures, and "happy-path" biases in proposed implementations.
  > *Tags:* `#safety` `#security`

- **[Secure: Security for the Uninitiated](skills/secure-security/SKILL.md)**
  > Use when handling auth, user input, secrets, or API endpoints. Mandates trust-boundary audits.
  > *Tags:* `#security`

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
