# Context Engine: Master Documentation

The **Context Engine** is the sovereign memory manager for the `Skill Archive` agentic ecosystem. It is a lightweight, strictly typed, deterministic **Model Context Protocol (MCP)** server built in Go.

Its core purpose is to completely abstract working and long-term memory away from the LLM, moving it from fluid, hallucination-prone markdown generation to strictly validated, schema-enforced JSON/YAML/TOON operations.

---

## 1. System Architecture

The Context Engine relies on the Model Context Protocol running via `stdio`. Because it handles critical state, it is heavily compartmentalized.

### 1.1. Deployment Profile
- **Language:** Go 1.22+ (Chosen for absolute minimal footprint and robust structural parsing capabilities).
- **Containerization:** Multi-stage Docker build. The final image is `FROM scratch`, packaging only a single, statically compiled binary. Total footprint is <15MB.
- **Service Invocation:** `docker-compose run` over standard I/O pipes. `tty` is explicitly disabled to preserve pure JSON-RPC serialization.
- **State Storage:** The server is stateless. All memory is persisted via a `/workspace` volume mount mapped directly to `.gemini/mem` on the user's host machine.

### 1.2. The Three Pillars of Memory
The engine divides memory into three distinct, non-overlapping domains:
1. **Ingestion (The Lens):** Translating the massive external workspace into token-safe, hyper-focused bites.
2. **The Scratchpad (Working Memory):** Short-term, volatile session logging to prevent contextual drift during complex execution loops.
3. **The Ontology Graph (Long-Term Memory):** Permanent, globally shared architectural rules structured as a Directed Acyclic Graph (DAG) for deterministic, programmatic traversal.

---

## 2. Poka-yoke Error Handling & Recovery

Because this server serves as the sole arbiter of agent memory, it employs severe fault-tolerance.

| Scenario | Server Response (Jidoka) | Recovery Protocol |
| :--- | :--- | :--- |
| **Disk Corruption** (The JSON state file is manually broken by a user). | Initial read fails. The server *does not crash*. | **Quarantine:** Renames the bad file to `.corrupted-[timestamp]`, initializes a new blank session, and returns an MCP Tool Error warning the agent that its scratchpad was wiped. |
| **Hallucinated Args** (The LLM passes an invalid Edge Type). | MCP request is rejected before reaching Go logic. | **Schema Block:** The agent receives `InvalidParams` detailing the enum mismatch, forcing it to self-correct on the next step. |
| **Concurrency Collisions** (Two identical tool calls arrive simultaneously). | Filesystem lock is applied. | **Blocking Waits:** Tool A holds an OS-level file lock on `session.json`. Tool B waits. Data interweaving is mathematically impossible. |
| **Logical Loops** (Agent tries to commit A -> B -> C -> A). | DAG Cycle Detection identifies the paradox. | **Commit Rejection:** Graph mutation is blocked. The agent is informed: `"ERROR: This rule creates a circular dependency."` |
| **Zip Bomb / Token Bomb** (Agent tries to ingest a minified 500MB JS file). | Pre-read stat detects file size. | **Hard Reject:** The server refuses to load the file into RAM, dropping a warning to use a different specialized parser tool. |

---

## 3. Skill Enforcement Integration

A memory server is useless if the agent forgets to use it and relies on its own context window. The Context Engine is mandatorily enforced at three layers:

1. **The Global Hook (Orchestration):** The `context-engine` skill is bolted to the root prompt. The agent is explicitly told it serves the Context Engine and cannot ignore its tools.
2. **The Methodology Interlock (Shisa Kanko):** The master workflow `shisa-kanko` relies on the Context Engine. The agent is structurally forbidden from executing a codebase modification without first invoking the `read_session_state` and `log_session_finding` tools.
3. **The Vacuum (Poka-yoke):** Legacy manual memory skills (`rag-strategy`, `plan-with-files`, `ontology`) are deleted. The agent has no other instructions *how* to memorize, forcing it through the MCP bottleneck.

---

## 4. MCP Tool Specifications

The Go server exposes exactly 5 explicit tools to the agent, governed by rigid schemas.

### 4.1. `ingest_context`
- **Role:** File extraction and RAG chunking.
- **Parsers:** Natively splits and parses **TOON** (Token-Oriented Object Notation), JSON, and Markdown.
- **Constraint:** Hard-capped at 4,000 tokens.
- **Parameters:**
  - `target_path` (string, required): File to ingest.
  - `query` (string, optional): Specific semantic target.

### 4.2. `log_session_finding`
- **Role:** The Scratchpad append. Writes to `current_session.json`.
- **Constraint:** Limited window size (e.g. 15 recent findings) to prevent long-term bloat. Drops the oldest entry automatically.
- **Parameters:**
  - `finding_text` (string, required): The fact to record.
  - `phase` (enum, required): `["planning", "execution", "verification", "blocked"]`.

### 4.3. `read_session_state`
- **Role:** Quick context restoration. Reads the active session state lock.
- **Constraint:** Must be called before `shisa-kanko` pointing.
- **Parameters:** *None.*

### 4.4. `commit_ontology_edge`
- **Role:** Graph mutation. Creates typed connections in `ontology.yaml`.
- **Constraint:** Prohibited from writing if a DAG cycle is created.
- **Parameters:**
  - `source_entity` (string, required).
  - `edge_type` (enum, required): `["REQUIRES", "IMPLEMENTS", "DEPENDS_ON", "CONFLICTS_WITH", "OWNS"]`.
  - `target_entity` (string, required).

### 4.5. `read_ontology_graph`
- **Role:** Knowledge retrieval. Traverses upstream and downstream dependencies.
- **Parameters:**
  - `target_entity` (string, required): The node to inspect.

---

## 5. Development Roadmap
1. `[✔]` Architecture and Scope definition.
2. `[✔]` Docker configuration (Volumes, Pipes, Multi-stage).
3. `[ ]` Scaffold `main.go` and MCP SDK bindings.
4. `[ ]` Implement `modules/ingestion` (TOON, 4k limits).
5. `[ ]` Implement `modules/scratchpad` (Locking).
6. `[ ]` Implement `modules/ontology` (DAG validation).
7. `[ ]` Deprecate legacy skills and update `skills-config.json`.
