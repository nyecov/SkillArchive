# TPS Architecture Review: Context Engine

## 1. Shusa Strategy & Vision
- **Shusa Strategy:** Transform agent memory from an unstructured, fluid context window into a strict programmable state machine.
- **Product Vision:** The *Context Engine* will serve as the sole, deterministic working and long-term memory broker for the agent—eliminating Transportation Bloat and resolving memory hallucinations by forcing all file ingestion, scratchpad logging, and semantic ontology mapping through a native CLI tool (`context_operator.py`).

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks:** Relaying raw files into context windows purely to extract facts causes severe Over-processing and Transportation Waste. The LLM must manually format memory markdown, which breaks under token pressure.
- **Future State Architecture:** A single `context-engine` skill acting solely as a manual for `context_operator.py`. The agent identifies a knowledge gap, queries the tool, and the backend engine handles semantic chunking, json state logging, and long-term knowledge graph persistence invisibly.

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** All methodology skills across the `Skill Archive` that reference `ontology`, `rag-strategy`, or `plan-with-files` (e.g., `shisa-kanko`, `lean-foundations`) will require refactoring.
- **Identified Conflicts:** Potential disruption of "Wa" during the migration period, as agents may fall back on legacy unstructured planning if the CLI interface proves too difficult to query.

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan:** 
  1. **Alpha Build:** Isolate and develop `context_operator.py`.
  2. **Skill Wrapper:** Draft the strict `context-engine` `SKILL.md` instruction set.
  3. **Parallel Deployment:** Allow the new tool to operate alongside the old skills for validation.
  4. **Cutover:** Deprecate `rag-strategy`, `plan-with-files`, `ontology` and update all global references.
- **Critical Hazards Isolated:** "System Amnesia"—deprecating the old planning methodologies before the new tool is verifiably battle-tested.

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** If `context_operator.py` returns schema exceptions, execution errors, or token limits exceeded three consecutive times, the agent must immediately deploy a Jidoka halt and request human intervention.
- **Poka-yoke Interlocks:** The CLI tool itself must handle graph parsing and error wrapping natively, throwing structured, human-readable errors instead of raw Python stack traces into the agent's context window.
