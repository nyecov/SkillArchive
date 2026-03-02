# Context Engine MCP Server: Technical Requirements

## 1. Overview
The Context Engine MCP Server is a local, stateless (to the LLM) intermediary that manages the agent's memory pipeline. It enforces rigid Poka-yoke validation and token constraints on context ingestion, short-term scratchpad memory, and long-term knowledge graph persistence.

## 2. Architectural Requirements
- **Protocol:** Must implement the Model Context Protocol (MCP) using `stdio` transport, as it will run locally within the workspace.
- **Language:** Python 3.10+ (Standardized for the `Skill Archive` ecosystem).
- **Storage Strategy:** All memory state must be deterministic and local. A new, not-yet-specified folder in the host workspace will be attached to the Docker container as a volume for storing these memories.
  - Volatile State: JSON or markdown `session_state` files.
  - Ontology State: Directed graphs outlining `Entities` and `Edges`.
- **Parsers:** The server must explicitly know how to parse, extract, and handle data across at least three primary formats: **TOON (Token-Oriented Object Notation)**, **JSON**, and **Markdown**.

## 3. Tool Requirements

The server must expose the following specific tools to the LLM. Each tool must have a highly descriptive, semantic prompt mapped to a rigid JSON schema to comply with `interface-governance`.

### 3.1. Ingestion (`ingest_context`)
- **Purpose:** Replaces raw file dumping (`rag-strategy`).
- **Input:** `target_path` (string), `query` (optional string).
- **Business Logic:**
  - Locate the file or directory.
  - If a specific `query` is provided, apply semantic or keyword extraction.
  - Calculate context size. If result > 4000 tokens, chunk the result and return only the highest-signal chunk, along with metadata indicating truncation.
- **Guardrail:** Hard fail (reject input) if the agent attempts to ingest without a valid path.

### 3.2. Scratchpad (`log_session_finding` & `read_session_state`)
- **Purpose:** Replaces natural language planning (`plan-with-files`).
- **Input (Log):** `finding_text` (string), `phase` (enum: planning, execution, verification, blocked).
- **Business Logic:**
  - Append the `finding_text` to the `.gemini/mem/current_session.json` state machine lock.
  - Prevent context bloating by limiting the scratchpad cache size (e.g., sliding window of the last 10 findings).
- **Return (Read):** A cleanly formatted summary of the current session phase and recent findings.

### 3.3. Knowledge Graph (`commit_ontology_edge` & `read_ontology_graph`)
- **Purpose:** Replaces unstructured long-term memory (`ontology`).
- **Input (Commit):** `source_entity` (string - typed), `edge_type` (enum - e.g., REQUIRES, IMPLEMENTS, DEPENDS_ON), `target_entity` (string - typed).
- **Business Logic:**
  - Mutate a globally persistent `.gemini/mem/global_ontology.yaml` graph file.
  - **Critical Interlock:** Validate that the new edge does not create a circular dependency (DAG violation) before committing. If it does, return an MCP Tool Error.
- **Return (Read):** Traverses the graph from a requested `target_entity` and returns standard dependencies.

## 4. Error Handling & Security (Poka-yoke & Jidoka)
- **Circuit Breakers:** If the agent tries to fetch a file outside the workspace root, throw a security `Path Traversal` exception.
- **Graceful Failure:** Any internal python exceptions (e.g., JSON decode errors on corrupted state files) must be caught and wrapped in a human-readable "Agent Actionable Error" (e.g., "The session state file is corrupted. Clear the state by running Tool X").
- **No Thin Wrappers:** The tools must compute logic (DAG validation, token counting), not just act as thin wrappers around Python's `open()`.

## 5. Deployment Mechanism & Docker Constraints
- **Docker Compose:** The MCP server must be entirely defined and able to be built/run from a single `docker-compose.yml` file.
- **Lightweight Multi-Stage Build:** The Dockerfile MUST use multi-stage builds to produce an extremely lightweight final image, ensuring it is highly available and fast to distribute to thin clients.
- **Volume Mounting:** The container must attach a dedicated volume mapped to a workspace folder (to be specified) so that all memory json/markdown files are persisted to the host and survive container resets.
- **Execution:** The `skills-config.json` in the main repository will eventually map the standard MCP `command` to invoke `docker-compose run` or execute against the running container using `stdio` over `docker exec`.
