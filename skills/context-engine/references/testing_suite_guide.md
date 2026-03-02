# Context Engine: Testing Suite Strategy (What, How, Why)

This document outlines the systematic approach to verifying the **Context Engine MCP Server**. It follows the **Shisa Kanko** (pointing and calling) and **TPS** (Toyota Production System) principles to ensure 100% deterministic reliability.

---

## 📘 WHAT is being tested?
The suite covers four critical architectural pillars across 15 automated test cases:

1.  **Ingestion (Long-term Memory)**
    - **Path Traversal Defense**: Ensuring the server strictly blocks access to files outside the `WORKSPACE_ROOT`.
    - **Heuristic Chunking**: Verifying that files exceeding 16k characters are safely truncated/chunked.
    - **Query Filtering**: Confirming that the `query` parameter extracts only relevant context windows.
2.  **Scratchpad (Short-term Memory)**
    - **Jidoka Limits**: Verifying the **Soft Limit (8k)** warning and **Hard Limit (10k)** write-block.
    - **Lock Competition**: Testing OS-level file locking and the 5-second "Overrule Heuristic."
3.  **Ontology (Middle-term Memory)**
    - **DAG Cycle Rejection**: Preventing circular dependencies in hierarchical edges (`REQUIRES`, `OWNS`).
    - **Transactional Integrity**: Ensuring a rejected edge does not corrupt the JSON state in `ontology.json`.
4.  **Diagnostics (Boot Sequence)**
    - **Quarantine Logic**: Confirming that malformed or tampered files are moved to `.corrupted-[timestamp]` on boot.
    - **UUID Provenance**: Ensuring every memory artifact maintains a unique, registered identity.
5.  **Operational Guardrails (Singleton)**
    - **Jidoka Halt**: Verifying that secondary server instances are blocked from booting.
    - **Stale Takeover**: Confirming the engine safely recovers from crashes by seizing stale locks.
6.  **Memory Maturation (Lifecycle)**
    - **Creation -> Upgrade -> Prune**: Verifying the explicit promotion of volatile scratchpad items into the permanent ontology graph, followed by a surgical pruning of the scratchpad.
    - **Downgrade (Reversion)**: Verifying the deletion of an ontology edge to revert an outdated architectural rule back into the volatile state for re-evaluation.
    - **After-Test Cleanup**: Validating the efficiency of bulk state truncation (`clear_session_state`) and the robust deletion of the `.engine.instance.lock` and storage volumes between boot cycles.

---

## 🛠️ HOW is it being tested?
The suite is built for **Subprocess Isolation** and **Environmental Determinism**.

- **Infrastructure**: Ephemeral Docker containers. Every test function executes `docker run --rm`, ensuring a fresh Go process and no memory leaks.
- **Protocol**: Real MCP Traffic. Tests use the `stdio_client` and `ClientSession` to send actual JSON-RPC payloads, treating the server as a true black box.
- **Orchestration**: `pytest-asyncio` on Windows.
  - **Win32 Policy**: Uses `WindowsProactorEventLoopPolicy` for stable subprocess pipes.
  - **Teardown Wrapper**: Specifically handles the benign `AnyIO` cancellation noise to ensure a clean exit status.
- **Forensics**: 
  - `mcp_debug.log`: Records every call and response for offline inspection.
  - `engine_diagnostics.log`: Captures the server's internal boot sequence results.

---

## 🎯 WHY this approach?
We avoid "Mocking" in favor of **Production-Equivalent Verification**.

1.  **Zero Hallucination Tolerance**: The server is the final guardrail for the LLM. If the server behavior isn't tested against real file-locks and real Docker mounts, the guardrail itself becomes a point of failure.
2.  **Jidoka (Autonomation)**: The testing suite proves that the server can self-correct (quarantine) and self-halt (hard limits) without human intervention.
3.  **Poka-yoke (Error Proofing)**: By testing path traversal and DAG cycles as high-priority failures, we ensure that the "Agent" using this engine cannot inadvertently destroy the codebase or create architectural loops.
4.  **Provenance Guarantee**: The UUID registry check ensures that even if a user renames a file, the system's conceptual identity of that memory remains fixed—a critical requirement for mature RAG systems.
