# Ontology Verification Report

When an agent executes an Ingestion or Retrieval operation on the Knowledge Graph, it MUST output its final state using this exact Markdown schema containing a YAML block. YAML is strictly mandated for flawless LLM token ingestion during subsequent reasoning steps.

```markdown
# Ontology State Report

## 1. Operation Context
- **Action:** [ Ingestion | Retrieval ]
- **Target Entity:** [Entity Name]

## 2. Poka-yoke Verification
- [x] No circular dependencies (DAG integrity)
- [x] Entities explicitly typed

## 3. Graph Mutation / Retrieval (YAML)
```yaml
Entities:
  - id: [Unique Identifier]
    type: [Person | Project | Task | Document | Event]
    properties:
      [key]: [value]

Edges:
  - source: [Entity ID]
    target: [Entity ID]
    relation: [e.g., DEPENDS_ON, CONTRIBUTES_TO, BLOCKS]
```
