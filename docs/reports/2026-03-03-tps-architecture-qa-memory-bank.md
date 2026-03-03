# TPS Architecture Review: Interview Q&A Memory Bank

## 1. Shusa Strategy & Vision
**Vision:** Elevate unstructured, conversational interview history into a strictly formatted, queryable knowledge base (TOON) to enable continuous improvement (Kaizen) and pattern recognition.
**Misalignment Target:** Do not allow the `interview` skill to natively read or write raw Markdown logs. This violates the Context Engine's mandate as the sole sovereign memory platform and introduces severe Context Bloat (Muri) and file-corruption hazards.

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks:** 
  - Over-processing: The LLM parsing 50k+ words of raw markdown to find a specific pattern.
  - Defect Hazard: The LLM breaking TOON syntax boundaries during raw file appends.
- **Future State Architecture:** 
  - The Context Engine server will house two new dedicated MCP tools (`append_interview_qa` and `retrieve_interview_patterns`) backed by a highly memory-efficient `bufio.Scanner` streaming parser in Go. This offloads the computational parsing burden from the LLM context window directly to the Go binary.

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** 
  - The Go server (`cmd/server/main.go`) must register the two new tools.
  - A new internal Go module (`internal/interview`) must be created to handle the logic.
  - The `interview` skill (`SKILL.md`) must be fundamentally updated to trigger the append tool at the end of the session.
  - A new workflow (`workflows/analyze-interview-patterns.md`) must be authored.

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan:**
  1. **Batch 1 (The Go Engine):** Build `internal/interview/qa_bank.go`. Implement the streaming TOON parser and the `append`/`retrieve` MCP handlers. 
  2. **Batch 2 (Verification):** Write BDD tests (e.g., `test_qa_bank.py`) to prove the streaming parser respects the 16k context limits and isolates the TOON blocks correctly.
  3. **Batch 3 (Skill & Workflow Integration):** Update `skills/interview/SKILL.md` to automate the append. Author `workflows/analyze-interview-patterns.md` to guide the pattern extraction process.
- **Critical Hazards Isolated:** 
  - **Context Crash:** The retrieval tool pulling too many matches and overflowing the 16k context limit.
  - **Volume Corruption:** The `append` tool failing to use the established `gofrs/flock` cross-container guardrail.

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** 
  - The `retrieve_interview_patterns` tool MUST contain a hard-coded 16,000 character truncation circuit breaker. If the retrieved blocks exceed this limit, it must truncate and append a `[WARNING: TRUNCATED]` message to explicitly notify the agent.
- **Poka-yoke Interlocks:** 
  - The `append_interview_qa` tool must use the exact same `gofrs/flock` POSIX file lock logic established in `pokayoke/singleton.go` to guarantee mutual exclusion across Docker containers writing to the shared `.gemini/mem` volume.
