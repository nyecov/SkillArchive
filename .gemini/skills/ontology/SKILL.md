---
name: ontology
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

## Core Mandates

### 1. Model Knowledge as Typed Entities
Instead of storing knowledge as flat text blobs, knowledge must be modeled as discrete **Entities** with strictly typed properties.

### 2. Define Explicit Relationships (Edges)
Entities are useless without edges. Edges must be directional and semantically meaningful (e.g., `DEPENDS_ON`, `OWNED_BY`).

### 3. Enforce Logical Consistency
The ontology enforces logical consistency. A `Task` cannot have a `status: "Complete"` if it `DEPENDS_ON` a `Task` with `status: "Pending"`.

## Escalation & Halting

- **Jidoka:** Trigger an autonomous halt if an entity creation request violates type constraints or if an edge would create a circular dependency in a DAG.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if the ontology reveals conflicting facts from different sources or if the user asks for a structural change to the entity schema.

## Implementation Workflow

### Phase 1: Ingestion
When the user provides new facts (e.g., *"Alice is the new lead for the Backend project"*):
1. **Identify the Entities:** `Person: Alice`, `Project: Backend`.
2. **Identify the Edge:** `OWNED_BY` (or `LEAD_BY`).
3. **Persist the change:** Update the local graph state.

### Phase 2: Retrieval
When the user asks a complex dependency question (e.g., *"If I change the Auth module, what breaks?"*):
1. Do not just use text search.
2. Query the Knowledge Graph starting at the target entity.
3. Traverse edges backward to report the exact interconnected cascade.

## Relationship to MCP

The **Ontology Skill** dictates *how* to think about structured memory. However, the exact mechanism for *storing* and *querying* this graph should be handled by an **MCP Server**. 

