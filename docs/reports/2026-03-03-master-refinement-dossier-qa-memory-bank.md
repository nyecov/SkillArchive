# Master Refinement Dossier: Interview Q&A TOON Memory Bank

**Topic:** Context Engine / Interview Skill Integration
**Goal:** Provide better guidance and continuous improvement by analyzing patterns from an automatically evolving Interview Q&A collection.

## 1. The Verified Story (Phase 1)
- **Core Logic:** The `interview` skill will automatically append Q&A pairs to a continuously evolving file at the end of sessions. The file is structured in **TOON** (Token-Oriented Object Notation). To prevent context bloat, a new **Context Engine Go Tool** will safely manage sharding and retrieve only semantically relevant Q&A pairs for analysis by a new Markdown workflow.
- **Verification Criteria:** The new Context Engine tool successfully chunks and retrieves specific TOON Q&A pairs based on a semantic query without exceeding the 16k context window.

## 2. The Lean Audit (Phase 2)
The full Lean analysis identified critical operational hazards:
- **Muri (Overburden) & Muda (Waste):** The LLM parsing 50k+ words sequentially in raw text is computationally wasteful and guarantees context window crashes.
- **Hazard (KYT):** Allowing the `interview` skill to natively append to the TOON file risks syntax corruption and POSIX lock contention across multiple agent sessions. All ingestion MUST be routed through a strictly validated Context Engine endpoint.

## 3. The Strategic Architecture (Phase 3)
A TPS Architecture Proposal (A3) was formulated to safely execute the feature:
- **Future State:** Two new dedicated MCP tools (`append_interview_qa` and `retrieve_interview_patterns`) will be built into the Go server. They will utilize a memory-efficient `bufio.Scanner` streaming parser to completely offload the computational parsing burden from the LLM context window directly to the Go binary.
- **Execution Plan (Heijunka):** Level the execution into 3 manageable batches:
  1. Build the Go Engine (Streaming Parser & MCP Handlers).
  2. Write BDD Verification Tests.
  3. Skill & Workflow Integration (`SKILL.md` update & `analyze-interview-patterns.md` creation).

## 4. Organizational Guardrails (Jidoka)
- **Poka-yoke Interlock:** The new `append_interview_qa` tool MUST strictly enforce the `gofrs/flock` POSIX file lock to guarantee mutual exclusion across Docker containers writing to the shared `.gemini/mem` volume, treating the Q&A bank with the same respect as the core ontology graph.

---
*Status: Topic Refinement Complete. The feature has been conceptually verified, structurally mapped, and a safe, Lean architectural roadmap is established for implementation.*