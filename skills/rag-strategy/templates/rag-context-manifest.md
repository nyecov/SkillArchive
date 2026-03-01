# RAG Context Manifest Template

When executing a RAG search or context retrieval, the agent MUST output the results using this exact schema to maintain deterministic relevance and prevent context bloat.

```markdown
# RAG Context Manifest

## 1. Information Need
- **Target Logic:** [What specific symbols, functions, or facts were being searched for?]

## 2. Retrieved Context (High-Signal)
- **File:** [Path to file]
- **Relevance:** [Why this specific snippet is necessary to answer the prompt]
- **Snippet:**
  ```[language]
  [The isolated context-aware chunk]
  ```

## 3. Verification
- [ ] Relevance Check: Snippet directly addresses the Information Need.
- [ ] Bloat Check: Snippet does not contain excessive/unrelated surrounding noise.
```
