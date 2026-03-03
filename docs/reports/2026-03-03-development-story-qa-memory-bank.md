# Development Story: Interview Q&A TOON Memory Bank

## 1. User Value (Why)
Provide better guidance, persistent memory, and continuous improvement (Kaizen) by analyzing structural patterns and anti-patterns derived from past Socratic Interview Q&A sessions.

## 2. Core Logic (How)
1. **Ingestion:** The `interview` skill is modified to automatically append every resolved Q&A pair to a continuously evolving file at the end of a session.
2. **Storage Format:** The file is structured in **TOON** (Token-Oriented Object Notation) to optimize LLM chunking and Context Engine parsing, treating each Q&A pair as an independent, unrelated unit.
3. **Retrieval (RAG):** To prevent context bloat (Muri) when the file exceeds 50k+ words, a new **Context Engine Go Tool** is created to safely manage sharding and retrieve only semantically relevant Q&A pairs on demand.
4. **Analysis:** A new Markdown Workflow is executed by the agent to consume the Context Engine's retrieved TOON shards and output distilled pattern/anti-pattern guidance.

## 3. Edge Cases & Constraints
- **Context Overburden (Muri):** The single evolving TOON file cannot be read directly by the LLM. It MUST be orchestrated by the Context Engine RAG tool to respect the 16k chunking heuristic.
- **Semantic Isolation:** Because each interview is unrelated, the sharding/retrieval mechanism must treat each Q&A block independently to avoid cross-contamination of unrelated logic.
- **File Locking:** The automatic append by the `interview` skill must respect the Context Engine's POSIX file locks to prevent corruption if multiple sessions run concurrently.

## 4. Verification Criteria
- [ ] The `interview` skill template successfully appends a valid TOON-formatted Q&A object.
- [ ] A new Go MCP tool (e.g., `retrieve_interview_patterns`) is implemented in the Context Engine.
- [ ] The new Context Engine tool successfully chunks and retrieves specific TOON Q&A pairs based on a semantic or keyword query.
- [ ] A new `workflows/analyze-interview-patterns.md` successfully distills actionable guidance from the retrieved TOON context.
