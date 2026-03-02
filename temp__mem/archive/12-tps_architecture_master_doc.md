# TPS Architecture Review: Master Documentation Refinement

## 1. Shusa Strategy & Vision
- **Vision Affirmation:** The vision remains strong. This review addresses the "glaze" identified in the Lean Analysis—specifically fortifying the technical mechanics of the Go implementation to meet the core "Thin Client" value proposition.

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks (Theoretical):** 
  1. Token Counting dependency.
  2. Stale filesystem locks (if the container crashes mid-write, the scratchpad might stay locked forever).
- **Future State Architecture:** 
  - Tokenization is replaced by an absolute 16,000-character payload cutoff.
  - File locking implements a `Timeout` and `Force-Unlock` mechanism. If a lock on `current_session.json` is older than 5 seconds, the server assumes a crash and overrules it.

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** The Go server cannot be built natively using Anthropic's official SDK as they do not provide one for Go. 
- **Identified Conflicts:** We must rely on community MCP Go bindings. We will formally adopt `github.com/mark3labs/mcp-go` as the core framework for the `stdio` server, ensuring we do not reinvent the JSON-RPC wheel.

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan (Revised):**
  1. Initialize `go mod` with `mcp-go` dependency.
  2. Write the 16,000-character `ingest` heuristic.
  3. Write the timeout-aware file locking.
- **Critical Hazards Isolated:** Handling TOON parsing. Since TOON uses `[count]{fields}\n[data]\t[data]` structure, the Go string parser must be extremely resilient to malformed tabs or missing brackets.

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** If the `mcp-go` library fails to initialize the `stdio` pipes correctly inside the Docker container (which can happen if Docker intercepts stdout), the server must immediately `panic` and log to standard error.
- **Poka-yoke Interlocks:** The server explicitly returns an MCP `ToolError` if it receives a request for a file path outside the `/workspace` mount, physically interblocking Path Traversal vulnerabilities.
