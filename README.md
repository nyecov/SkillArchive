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

### Agent-Safety

- **[Circuit: The Iteration Breaker](skills/cc-circuit-iteration-breaker/SKILL.md)**
  > Use when the same bug persists after 3+ attempts, regressions match fixes, or time spent exceeds the iteration budget. Handles circuit breaker trig...
  > *Tags:* `#circuit` `#iteration-breaker` `#halt` `#budget` `#sunk-cost` `#crowd-control`

- **[Jidoka: Autonomation for AI Agents](skills/jidoka-autonomation/SKILL.md)**
  > Use when an abnormality, unexpected API response, or validation failure occurs during execution. Handles autonomous halt, root-cause analysis, and ...
  > *Tags:* `#jidoka` `#lean` `#ai-safety` `#escalation` `#monitoring`

- **[Secure: Security for the Uninitiated](skills/cc-secure-security/SKILL.md)**
  > Use when implementing authentication, handling user input, storing secrets, or exposing API endpoints. Handles trust boundary analysis, 5-domain se...
  > *Tags:* `#secure` `#security` `#trust-boundary` `#secrets` `#authentication` `#authorization` `#crowd-control`

### Architecture

- **[Ontology (Structured Agent Memory)](skills/ontology/SKILL.md)**
  > Typed knowledge graph methodology for structured agent memory and composable actions.  Use to create, query, and enforce constraints across interco...
  > *Tags:* `#memory` `#ontology` `#knowledge-graph` `#dependencies` `#architecture` `#state`

- **[Tools Management Strategy](skills/tools-management/SKILL.md)**
  > Use when deciding whether to implement an abstraction as a cognitive Skill, an MCP Server, or a low-level Tool (script). Handles the boundary betwe...
  > *Tags:* `#tools` `#automation` `#scripts` `#mcp` `#delegation` `#architecture`

### Cognition

- **[Comprehend: The Understanding Gate](skills/cc-comprehend-understanding/SKILL.md)**
  > Use before debugging, extending, or shipping code the user cannot explain. Handles 4-level comprehension gates, rubber duck escalation, and hard/so...
  > *Tags:* `#comprehend` `#understanding` `#explanation` `#comprehension-debt` `#crowd-control`

- **[Deglaze: Anti-Sycophancy Protocol](skills/cc-deglaze-anti-sycophancy/SKILL.md)**
  > Use when reviewing AI-generated solutions, validating user comprehension, or stress-testing proposals. Handles 5 constraint-pressure techniques: Co...
  > *Tags:* `#deglaze` `#anti-sycophancy` `#constraint-pressure` `#critical-thinking` `#crowd-control`

- **[Hansei: Agentic Self-Reflection](skills/hansei-self-reflection/SKILL.md)**
  > Use when a plan needs critical review, an execution has failed, or a recurring error pattern emerges. Handles proactive plan critique, reactive roo...
  > *Tags:* `#hansei` `#reflection` `#iterative-refinement` `#cognitive-bias` `#lean`

### Communication

- **[Hō-Ren-Sō: Communication Standard for Agents](skills/ho-ren-so-communication/SKILL.md)**
  > Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human operator. Handles structured repor...
  > *Tags:* `#ho-ren-so` `#collaboration` `#hitl` `#reporting` `#coordination` `#lean`

### Continuous-Improvement

- **[Kaizen: Continuous Agentic Improvement](skills/kaizen-continuous-improvement/SKILL.md)**
  > Use when a recurring error, structural bottleneck, or workflow inefficiency is identified. Handles PDCA-based experiment design, controlled rollout...
  > *Tags:* `#kaizen` `#optimization` `#learning` `#evolution` `#pdca` `#lean`

### Data-Serialization

- **[TOON Data Serialization](skills/toon-token-oriented-notation/SKILL.md)**
  > Use when serializing structured data for LLM prompts, agent tool outputs, or AI pipeline payloads. Handles JSON-to-TOON conversion, format selectio...
  > *Tags:* `#toon` `#token-optimization` `#data-format` `#json-alternative` `#llm-efficiency`

### Diagnostics

- **[Value Stream Mapping (VSM) for Agents](skills/vsm-value-stream-mapping/SKILL.md)**
  > Use when diagnosing slow workflows, high token consumption, or unexplained latency in multi-step tasks. Handles current-state mapping, bottleneck i...
  > *Tags:* `#vsm` `#mapping` `#architecture` `#bottlenecks` `#flow` `#lean`

### Engineering-Standards

- **[Anchor: Architectural Coherence](skills/cc-anchor-coherence/SKILL.md)**
  > Use when starting a project, making architectural decisions, or when AI-suggested changes conflict with established patterns. Handles anchor docume...
  > *Tags:* `#anchor` `#architecture` `#coherence` `#drift-prevention` `#crowd-control`

- **[Isolate: Systematic Debugging](skills/cc-isolate-debugging/SKILL.md)**
  > Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed. Handles 5-step hypothesis-driven debugging, binary search isol...
  > *Tags:* `#isolate` `#debugging` `#systematic` `#hypothesis` `#single-variable` `#crowd-control`

- **[Poka-yoke: Mistake-proofing AI Workflows](skills/poka-yoke-mistake-proofing/SKILL.md)**
  > Use when designing validation gates, enforcing schemas, or preventing invalid tool calls. Handles deterministic guardrails, prerequisite interlocks...
  > *Tags:* `#poka-yoke` `#guardrails` `#validation` `#deterministic` `#reliability` `#lean`

- **[Ship: Production Readiness](skills/cc-ship-production/SKILL.md)**
  > Use when code is "feature complete" and approaching deployment, or when verifying production readiness. Handles staging gates, 6-domain ship checkl...
  > *Tags:* `#ship` `#production` `#deployment` `#monitoring` `#staging` `#crowd-control`

### Integration

- **[MCP Integration Governance](skills/mcp-integration-governance/SKILL.md)**
  > Use when designing, building, auditing, or consuming MCP servers and clients. Handles tool design, resource exposure, transport selection, security...
  > *Tags:* `#mcp` `#model-context-protocol` `#tools` `#resources` `#json-rpc` `#agent-integration`

### Meta

- **[Skill of Skills: Meta-Skill Authoring Guide](skills/skill-of-skill-authoring/SKILL.md)**
  > Use when creating, reviewing, or refining agent skills. Provides the authoritative checklist and workflow for writing high-efficiency, token-optima...
  > *Tags:* `#meta-skill` `#skill-authoring` `#progressive-disclosure` `#token-efficiency` `#agent-skills`

### Philosophy

- **[Lean: Eradicating Agentic Waste (Muda)](skills/lean-principles-muda/SKILL.md)**
  > Use when a workflow feels slow, bloated, or produces unnecessary output. Handles classification of 7 waste types (Muda), value definition, surgical...
  > *Tags:* `#lean` `#muda` `#efficiency` `#optimization` `#value`

### Risk-Management

- **[KYT: Hazard Prediction Training for Agents](skills/kyt-hazard-prediction/SKILL.md)**
  > Use before executing high-risk operations, destructive commands, or irreversible changes. Handles 4-round hazard identification, countermeasure des...
  > *Tags:* `#kyt` `#hazard-prediction` `#safety` `#critic-agent` `#pre-mortem` `#lean`

### Software-Engineering

- **[Shisa Kanko Engineering Master Workflow](skills/shisa-kanko-vibecoding/SKILL.md)**
  > Use when executing code changes, tool calls, or multi-step engineering tasks. Handles context isolation, intent declaration, deterministic verifica...
  > *Tags:* `#vibecoding` `#ai-safety` `#lean` `#shisa-kanko` `#jidoka` `#poka-yoke` `#hansei` `#kyt` `#ho-ren-so` `#agentic-workflows`

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
