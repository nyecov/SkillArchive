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

### 1. Entity-Based Modeling
Model all knowledge as discrete, strictly-typed Entities rather than flat, unstructured text blobs.
- **Action:** Identify the Entity Type (Person, Project, Task, Document) and its required properties before persistence.
- **Constraint:** DO NOT store "loose" facts that are not anchored to a specific Entity in the graph.
- **Integration:** Directly supports the **Poka-yoke** principle of "Schema Enforcement."

### 2. Explicit Relationship Mapping (Edges)
Define semantically meaningful, directional Edges between entities to map the "web of meaning."
- **Action:** Assign specific relationship types (e.g., `DEPENDS_ON`, `OWNED_BY`, `CONTRIBUTES_TO`) between every new and existing entity.
- **Constraint:** NEVER create an entity without at least one relationship to the existing graph; avoid orphaned knowledge silos.
- **Integration:** Feeds into **Nemawashi** by providing the dependency map for impact analysis.

### 3. Consistency Enforcement
Enforce logical rules and type constraints across the graph to prevent contradictory or malformed state.
- **Action:** Validate that a change (e.g., marking a Task as 'Complete') does not violate edge-based logic (e.g., if it still has 'Pending' dependencies).
- **Constraint:** Reject any update that would result in a circular dependency in a Directed Acyclic Graph (DAG) structure.
- **Integration:** Triggers a **Jidoka** halt if a logical inconsistency is detected.

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

