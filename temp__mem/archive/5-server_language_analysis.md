# Language Analysis: Context Engine MCP Server

The requirements for the Context Engine dictate a **highly lightweight**, **multi-stage Docker build** suitable for **thin clients**, capable of natively parsing **TOON (Token-Oriented Object Notation), JSON, and Markdown**, and implementing the **Model Context Protocol (MCP)**.

Here is an evaluation of the four requested languages against these strict constraints.

## 1. Rust

- **Docker Image Size (Multi-Stage):** ~5MB - 15MB. (Using a dynamic builder stage, then copying the statically compiled binary to a bare `SCRATCH` or `Alpine` runtime image).
- **Resource Footprint:** Negligible. Extremely fast cold starts and virtually no memory overhead, making it the supreme choice for thin clients.
- **Parsing Extensibility:** Best-in-class parsers (`serde_json` and `pulldown-cmark` for Markdown). For the custom **TOON** format, Rust offers peerless structural string parsing via libraries like `nom` or native fast regex arrays. JSON schema validation is exceptionally strict and memory-safe.
- **MCP Ecosystem:** Relies on community-driven crates (like `mcp-rs`), as Anthropic's official SDKs primarily target TS/Python.
- **Verdict:** **EXCELLENT**. The ultimate solution for a bulletproof, microscopic Docker image, though it trades off with slower initial compilation times.

## 2. Go (Golang)

- **Docker Image Size (Multi-Stage):** ~10MB - 20MB. Very similar to Rust.
- **Resource Footprint:** Extremely lightweight. Statically compiled Go binaries run perfectly in `SCRATCH` docker containers, zero runtime dependencies required.
- **Parsing Extensibility:** Very strong standard library for JSON and string manipulation natively required for the custom **TOON** format (e.g. `strings.Split`, regex). Excellent community packages for Markdown (`yuin/goldmark`).
- **MCP Ecosystem:** ModelContextProtocol adoption in Go is growing fast with solid community SDKs (e.g., `mark3labs/mcp-go`), as writing simple JSON-RPC over stdio in Go is trivial.
- **Verdict:** **EXCELLENT**. An outstanding balance. It yields the same microscopic Docker footprint as Rust but offers significantly faster build and compilation times for iteration.

## 3. TypeScript (Node.js / Bun)

- **Docker Image Size (Multi-Stage):** ~80MB - 150MB. You must always ship the JavaScript runtime (V8 engine). Even using `node:alpine` or `oven/bun:alpine`, the base layer is significantly heavier than compiled languages.
- **Resource Footprint:** Moderate. Requires the JS runtime to boot, consuming more baseline RAM than Go/Rust.
- **Parsing Extensibility:** Excellent JSON handling natively. Markdown requires external dependencies (e.g., `marked`). Writing a custom **TOON** parser is easy using standard JavaScript string manipulation.
- **MCP Ecosystem:** **The Gold Standard.** Anthropic's official TypeScript SDK is the most mature, feature-rich, and well-documented implementation of the Protocol.
- **Verdict:** **POOR to MODERATE**. It has the best MCP library support by far, but it fundamentally **fails** the requirement for a truly "lightweight" image for thin clients due to the inescapable Node/Bun runtime overhead.

## 4. Python (Current Initial Design)

- **Docker Image Size (Multi-Stage):** ~100MB - 150MB. Like TypeScript, it requires shipping the bloated Python interpreter (`python:3.11-slim` or `alpine`).
- **Resource Footprint:** Moderate to High. Heaviest memory footprint and slowest start times among the four.
- **Parsing Extensibility:** Natively handles JSON. **TOON** is easily handled by Python runtime string splitting and native `re` (regex). Markdown requires libraries.
- **MCP Ecosystem:** Official, fully-featured SDK supplied out-of-the-box by Anthropic.
- **Verdict:** **POOR**. While heavily supported for AI logic, Python is the worst choice for minimizing image sizes and satisfying the strict "thin client" distribution constraint.

---

## Recommendation

If the primary non-functional requirements are **lightweight distribution** (thin clients) and a **microscopic multi-stage Docker profile**:

**You must choose Go or Rust.**

1. **Choose Go** if you want rapid iteration, faster Docker builds, simpler concurrency for filesystem locking, and an extremely capable standard library for JSON-RPC. (Highly Recommended)
2. **Choose Rust** if you prioritize absolute mathematical safety in your state engine schemas, zero-cost abstractions, and the absolute smallest possible final image byte-size.

*(Note: If we pivot to Go or Rust, we lose the official `mcp-sdk-python`, but building an MCP stdio server in Go/Rust is highly documented and well-supported by robust community libraries.)*
