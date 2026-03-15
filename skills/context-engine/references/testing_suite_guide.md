# Context Engine: Testing Suite Strategy (What, How, Why)

This document outlines the systematic approach to verifying the **Context Engine MCP Server**. It follows the **Shisa Kanko** (pointing and calling) and **TPS** (Toyota Production System) principles to ensure 100% deterministic reliability.

---

## 📘 WHAT is being tested?
The suite covers six critical architectural pillars across 17 automated test cases:

1.  **Ingestion (Long-term Memory)**
    - **Path Traversal Defense**: Ensuring the server strictly blocks access to files outside the `WORKSPACE_ROOT`.
    - **Heuristic Chunking**: Verifying that files exceeding 16k characters are safely truncated/chunked.
    - **Query Filtering**: Confirming that the `query` parameter extracts only relevant context windows.
2.  **Scratchpad (Short-term Memory)**
    - **Jidoka Limits**: Verifying the **Soft Limit (8k)** warning and **Hard Limit (10k)** write-block.
    - **Lock Competition**: Testing OS-level file locking and the 5-second "Overrule Heuristic."
3.  **Ontology (Middle-term Memory)**
    - **DAG Cycle Rejection**: Preventing circular dependencies in hierarchical edges (`REQUIRES`, `OWNS`).
    - **Transactional Integrity**: Ensuring a rejected edge does not corrupt the database state, utilizing SQLite's ACID guarantees.
    - **Semantic Traversal (Hybrid RAG)**: Verifying that fuzzy keyword searches (via SQLite FTS5) successfully retrieve exact graph nodes, and confirming malformed queries fail gracefully.
4.  **Diagnostics (Boot Sequence)**
    - **Corruption Detection**: Confirming that a corrupt database triggers the `PRAGMA integrity_check` failure and is handled via quarantine/reset logic.
    - **UUID Registry Verification**: Ensuring every memory artifact maintains a unique identity within its respective table.
5.  **Operational Guardrails (Concurrency)**
    - **Swarm Orchestration**: Verifying that multiple engines can connect to the WAL-mode database simultaneously without "Database locked" errors.
    - **Resilience**: Confirming the engine safely handles interruptions during database operations.
6.  **Memory Maturation (Lifecycle)**
    - **Creation -> Upgrade -> Prune**: Verifying the explicit promotion of volatile scratchpad items into the permanent ontology graph, followed by a surgical pruning of the scratchpad.
    - **Downgrade (Reversion)**: Verifying the deletion of an ontology edge to revert an outdated architectural rule back into the volatile state for re-evaluation.
    - **After-Test Cleanup**: Validating the efficiency of bulk state truncation (`clear_session_state`) and the robust release of the POSIX lock (`.engine.instance.lock`) and storage volumes between boot cycles.

---

## 🛠️ HOW is it being tested?
The suite is built for **Subprocess Isolation** and **Environmental Determinism**.

- **Infrastructure**: Ephemeral Docker containers. Every test function executes `docker run --rm`, ensuring a fresh Go process and no memory leaks.
- **Protocol**: Real MCP Traffic. Tests use the `stdio_client` and `ClientSession` to send actual JSON-RPC payloads, treating the server as a true black box.
- **Orchestration**: `pytest-asyncio` on Windows.
  - **Win32 Policy**: Uses `WindowsProactorEventLoopPolicy` for stable subprocess pipes.
  - **Teardown Wrapper**: Specifically handles the `AnyIO` cancellation noise to ensure a clean exit status across all async contexts.
- **Forensics**: 
  - `pytest_results.txt`: Comprehensive functional verification log.
  - `engine_diagnostics.log`: Server boot sequence and SQLite integrity results.

---

## 🎯 WHY this approach?
We avoid "Mocking" in favor of **Production-Equivalent Verification**.

1.  **Zero Hallucination Tolerance**: The server is the final guardrail for the LLM. If the server behavior isn't tested against real file-locks and real Docker mounts, the guardrail itself becomes a point of failure.
2.  **Jidoka (Autonomation)**: The testing suite proves that the server can self-correct (quarantine) and self-halt (hard limits) without human intervention.
3.  **Poka-yoke (Error Proofing)**: By testing path traversal and DAG cycles as high-priority failures, we ensure that the "Agent" using this engine cannot inadvertently destroy the codebase or create architectural loops.
4.  **Provenance Guarantee**: The UUID registry check ensures that even if a user renames a file, the system's conceptual identity of that memory remains fixed—a critical requirement for mature RAG systems.
