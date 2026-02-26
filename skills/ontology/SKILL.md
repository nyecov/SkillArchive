---
name: Ontology (Structured Agent Memory)
version: 1.0.0
description: >
  Typed knowledge graph methodology for structured agent memory and composable actions. 
  Use to create, query, and enforce constraints across interconnected entities (Person, Project, Task, Event, Document).
category: architecture
tags: [memory, ontology, knowledge-graph, dependencies, architecture, state]
references:
  - name: MCP Integration Governance
    path: ../mcp-integration-governance/SKILL.md
---

# Ontology (Structured Agent Memory)

Most AI agents suffer from "goldfish memory"—forgetting context as the context window rolls, or relying on messy, unstructured semantic search that fails to map exact dependencies between concepts. 

The **Ontology** methodology solves this by teaching the agent to maintain a *typed knowledge graph* for structured memory. It governs how the agent should remember facts, relate them to one another, and persist them across long contexts or discrete skill invocations.

## When to Activate

Trigger this skill when the user asks:
- *"Remember that..."*
- *"What do I know about X?"*
- *"Link concept X to concept Y."*
- *"Show me the dependencies for this project."*
- Or when multiple discrete skills (e.g., Code Review + Test Generation) need to share a unified state.

## Core Concepts

### 1. Entities

Instead of storing knowledge as flat text blobs, knowledge must be modeled as discrete **Entities** with strictly typed properties.

Standard Entity Types:
- `Person`: { id, name, role, email, context }
- `Project`: { id, name, status, deadline, owner_id }
- `Task`: { id, title, status, project_id, assigned_to_id }
- `Event`: { id, timestamp, description, related_entities[] }
- `Document`: { id, path, summary, dependent_modules[] }

### 2. Edges (Relationships)

Entities are useless without edges. Edges must be directional and semantically meaningful.

Standard Edge Types:
- `DEPENDS_ON` (Task A -> Task B)
- `OWNED_BY` (Project -> Person)
- `IMPLEMENTS` (Document -> Task)
- `REFERENCES` (Document A -> Document B)

### 3. Constraints

The ontology enforces logical consistency.
- A `Task` cannot have a `status: "Complete"` if it `DEPENDS_ON` a `Task` with `status: "Pending"`.
- A `Project` cannot be created without an `OWNED_BY` edge pointing to a valid `Person`.

## Implementation Workflow

### Phase 1: Ingestion
When the user provides new facts (e.g., *"Alice is the new lead for the Backend project"*):
1. **Identify the Entities:** `Person: Alice`, `Project: Backend`.
2. **Identify the Edge:** `OWNED_BY` (or `LEAD_BY`).
3. **Persist the change:** Update the local graph state (typically stored via an MCP database server like SQLite, Memory, or a simple `.agent/ontology.json`).

### Phase 2: Retrieval
When the user asks a complex dependency question (e.g., *"If I change the Auth module, what breaks?"*):
1. Do not just use text search.
2. Query the Knowledge Graph starting at `Document: Auth_Module`.
3. Traverse `REFERENCES` and `IMPLEMENTS` edges backward.
4. Report the exact interconnected cascade.

## Relationship to MCP

The **Ontology Skill** dictates *how* to think about structured memory. However, the exact mechanism for *storing* and *querying* this graph (e.g., SQLite, Neo4j, or a flat JSON file) should be handled by an **MCP Server** (see the `tools-management` skill). 

Do not write raw database connection scripts in the agent's contextual layer. Ask the active Memory MCP Server to create the entities and edges on your behalf.
