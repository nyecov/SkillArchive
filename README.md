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

### ⛩️ Lean System
> Core methodologies based on Lean, Jidoka, and Kaizen principles.

- **[Gemba (Static Observation)](skills/gemba/SKILL.md)**
  > Use to ensure situational awareness by observing the "Real Place" (the codebase).  Prioritizes empirical data over assumptions or model-cached know...
  > *Tags:* `#gemba` `#observation` `#facts` `#reality` `#lean`

- **[Genchi Genbutsu (Dynamic Verification)](skills/genchi-genbutsu/SKILL.md)**
  > Use to "Go and See for Yourself." Mandates empirical verification of all hypotheses  and findings through direct execution and testing.
  > *Tags:* `#genchi-genbutsu` `#verification` `#facts` `#testing` `#lean`

- **[Hansei: Agentic Self-Reflection](skills/hansei/SKILL.md)**
  > Use when a plan needs critical review, an execution has failed, or a recurring error pattern emerges. Handles proactive plan critique, reactive roo...
  > *Tags:* `#hansei` `#reflection` `#iterative-refinement` `#cognitive-bias` `#lean`

- **[Heijunka (Production Leveling)](skills/heijunka/SKILL.md)**
  > Use to level the workload and prevent token/context spikes (Muri).  Handles the decomposition of massive tasks into manageable, consistent batches.
  > *Tags:* `#heijunka` `#leveling` `#context-management` `#optimization` `#lean`

- **[Hō-Ren-Sō: Communication Standard for Agents](skills/ho-ren-so/SKILL.md)**
  > Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human operator. Handles structured repor...
  > *Tags:* `#ho-ren-so` `#collaboration` `#hitl` `#reporting` `#coordination` `#lean`

- **[Jidoka: Autonomation for AI Agents (The Andon Cord)](skills/jidoka/SKILL.md)**
  > Use when an abnormality, unexpected API response, or validation failure occurs during execution. Handles autonomous halt, root-cause analysis, and ...
  > *Tags:* `#jidoka` `#andon` `#signal` `#lean` `#ai-safety` `#escalation` `#monitoring`

- **[KYT: Hazard Prediction Training for Agents](skills/kyt/SKILL.md)**
  > Use before executing high-risk operations, destructive commands, or irreversible changes. Handles 4-round hazard identification, countermeasure des...
  > *Tags:* `#kyt` `#hazard-prediction` `#safety` `#critic-agent` `#pre-mortem` `#lean`

- **[Kaizen: Continuous Agentic Improvement](skills/kaizen/SKILL.md)**
  > Use when a recurring error, structural bottleneck, or workflow inefficiency is identified. Handles PDCA-based experiment design, controlled rollout...
  > *Tags:* `#kaizen` `#optimization` `#learning` `#evolution` `#pdca` `#lean`

- **[Kodawari: Devoted Craftsmanship](skills/kodawari-craftsmanship/SKILL.md)**
  > Kodawari (Devoted Craftsmanship) for high-quality, self-documenting code. Mandates the relentless pursuit of perfection in the details, ensuring ar...
  > *Tags:* `#kodawari` `#craftsmanship` `#quality` `#readability` `#wa` `#lean`

- **[Lean Foundations: Stability through 3M & 5S](skills/lean-foundations/SKILL.md)**
  > Foundational Lean principles for stabilizing workflows through the 3 Ms (Mura, Muri, Muda)  and the 5S workplace organization framework. Focuses on...
  > *Tags:* `#lean` `#3m` `#5s` `#mura` `#muri` `#stability` `#organization`

- **[Lean: Eradicating Agentic Waste (Muda)](skills/muda/SKILL.md)**
  > Use when a workflow feels slow, bloated, or produces unnecessary output. Handles classification of 7 waste types (Muda), value definition, surgical...
  > *Tags:* `#lean` `#muda` `#efficiency` `#optimization` `#value`

- **[Nemawashi (Foundation Building)](skills/nemawashi/SKILL.md)**
  > Use to lay the groundwork for changes through impact analysis and consensus building.  Ensures all dependencies are identified and stakeholders are...
  > *Tags:* `#nemawashi` `#consensus` `#alignment` `#impact-analysis` `#lean`

- **[Poka-yoke: Mistake-proofing AI Workflows](skills/poka-yoke/SKILL.md)**
  > Use when designing validation gates, enforcing schemas, or preventing invalid tool calls. Handles deterministic guardrails, prerequisite interlocks...
  > *Tags:* `#poka-yoke` `#guardrails` `#validation` `#deterministic` `#reliability` `#lean`

- **[Shisa Kanko Engineering Master Workflow](skills/shisa-kanko/SKILL.md)**
  > Use when executing code changes, tool calls, or multi-step engineering tasks. Handles context isolation, intent declaration, deterministic verifica...
  > *Tags:* `#vibecoding` `#ai-safety` `#lean` `#shisa-kanko` `#jidoka` `#poka-yoke` `#hansei` `#kyt` `#ho-ren-so` `#agentic-workflows`

- **[Shusa: The Chief Engineer Model](skills/shusa-leadership/SKILL.md)**
  > The Shusa (Chief Engineer) leadership model for technical ownership and product vision. Ensures that a single individual (or agent) maintains total...
  > *Tags:* `#shusa` `#leadership` `#ownership` `#architecture` `#lean`

- **[Value Stream Mapping (VSM) for Agents](skills/vsm/SKILL.md)**
  > Use when diagnosing slow workflows, high token consumption, or unexplained latency in multi-step tasks. Handles current-state mapping, bottleneck i...
  > *Tags:* `#vsm` `#mapping` `#architecture` `#bottlenecks` `#flow` `#lean`

### Architecture

- **[MCP Integration Governance](skills/mcp-governance/SKILL.md)**
  > Use when designing, building, auditing, or consuming MCP servers and clients. Handles tool design, resource exposure, transport selection, security...
  > *Tags:* `#mcp` `#model-context-protocol` `#tools` `#resources` `#json-rpc` `#agent-integration`

- **[Ontology (Structured Agent Memory)](skills/ontology/SKILL.md)**
  > Typed knowledge graph methodology for structured agent memory and composable actions.  Use to create, query, and enforce constraints across interco...
  > *Tags:* `#memory` `#ontology` `#knowledge-graph` `#dependencies` `#architecture` `#state`

- **[TOON Data Serialization](skills/toon-token-oriented-notation/SKILL.md)**
  > Use when serializing structured data for LLM prompts, agent tool outputs, or AI pipeline payloads. Handles JSON-to-TOON conversion, format selectio...
  > *Tags:* `#toon` `#token-optimization` `#data-format` `#json-alternative` `#llm-efficiency`

### Cognition

- **[Comprehend: The Understanding Gate (Policy)](skills/comprehend-understanding/SKILL.md)**
  > Use before debugging, extending, or shipping code the user cannot explain. Handles 4-level comprehension gates, rubber duck escalation, and hard/so...
  > *Tags:* `#comprehend` `#understanding` `#explanation` `#comprehension-debt` `#crowd-control`

- **[Deglaze: Anti-Sycophancy (Tactical Toolkit)](skills/deglaze-tactics/SKILL.md)**
  > Use when reviewing AI-generated solutions, validating user comprehension, or stress-testing proposals. Handles 5 constraint-pressure techniques: Co...
  > *Tags:* `#deglaze` `#anti-sycophancy` `#constraint-pressure` `#critical-thinking` `#crowd-control`

### Engineering

- **[Anchor: Architectural Coherence](skills/anchor-coherence/SKILL.md)**
  > Use when starting a project, making architectural decisions, or when AI-suggested changes conflict with established patterns. Handles anchor docume...
  > *Tags:* `#anchor` `#architecture` `#coherence` `#drift-prevention` `#crowd-control`

- **[Docker Engineering Standards](skills/docker-engineering/SKILL.md)**
  > Comprehensive Docker engineering standards.  Covers multi-stage builds, layer caching, BuildKit optimization, security (non-root), and production-g...
  > *Tags:* `#docker` `#devops` `#multi-stage` `#BuildKit` `#security` `#optimization` `#production`

- **[Isolate: Systematic Debugging](skills/isolate-debugging/SKILL.md)**
  > Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed. Handles 5-step hypothesis-driven debugging, binary search isol...
  > *Tags:* `#isolate` `#debugging` `#systematic` `#hypothesis` `#single-variable` `#crowd-control`

- **[Kubernetes Engineering Standards](skills/kubernetes-engineering/SKILL.md)**
  > Production-grade Kubernetes engineering standards.  Covers resource management, resilience (probes), security (PodSecurityContext), and manifest op...
  > *Tags:* `#kubernetes` `#k8s` `#devops` `#orchestration` `#security` `#resilience` `#production`

- **[Ship: Production Readiness](skills/ship-production/SKILL.md)**
  > Use when code is "feature complete" and approaching deployment, or when verifying production readiness. Handles staging gates, 6-domain ship checkl...
  > *Tags:* `#ship` `#production` `#deployment` `#monitoring` `#staging` `#crowd-control`

### Meta

- **[Skill Authoring & Management (SAM)](skills/skill-authoring-management/SKILL.md)**
  > Use when creating, reviewing, or managing agent skills.  Provides the authoritative "Gold Standard" for content and formatting, management of skill...
  > *Tags:* `#meta-skill` `#skill-management` `#gold-standard` `#skill-authoring` `#progressive-disclosure` `#token-efficiency`

- **[Skill External Synthesis](skills/external-synthesis/SKILL.md)**
  > Use when researching, designing, or authoring new agent skills. Guides the agent to search external repositories like the Claude Cookbook and Clawh...
  > *Tags:* `#skill-authoring` `#synthesis` `#research` `#external-resources` `#clawhub`

- **[Tools Management Strategy](skills/tools-management/SKILL.md)**
  > Use when deciding whether to implement an abstraction as a cognitive Skill, an MCP Server, or a low-level Tool (script). Handles the boundary betwe...
  > *Tags:* `#tools` `#automation` `#scripts` `#mcp` `#delegation` `#architecture`

### Safety

- **[Circuit: The Iteration Breaker](skills/circuit-breaker/SKILL.md)**
  > Use when the same bug persists after 3+ attempts, regressions match fixes, or time spent exceeds the iteration budget. Handles circuit breaker trig...
  > *Tags:* `#circuit` `#iteration-breaker` `#halt` `#budget` `#sunk-cost` `#crowd-control`

- **[Secure: Security for the Uninitiated](skills/secure-security/SKILL.md)**
  > Use when implementing authentication, handling user input, storing secrets, or exposing API endpoints. Handles trust boundary analysis, 5-domain se...
  > *Tags:* `#secure` `#security` `#trust-boundary` `#secrets` `#authentication` `#authorization` `#crowd-control`

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
