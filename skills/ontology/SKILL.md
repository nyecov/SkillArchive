---
name: ontology
version: 1.0.0
description: 'Typed knowledge graph methodology for structured agent memory and composable
  actions.  Use to create, query, and enforce constraints across interconnected entities
  (Person, Project, Task, Event, Document).\'
category: architecture
tags:
- context
- design
references:
- name: MCP Integration Governance
  path: ../interface-governance/SKILL.md
- name: Ontology Output Template
  path: ./templates/ontology-output-template.md
level: technical
---

# Ontology

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

- **Jidoka:** Trigger an autonomous halt immediately if an edge modification results in a circular dependency in a Directed Acyclic Graph (DAG) state, or if attempting to create an Entity without a strict type constraint.
- **Hō-Ren-Sō:** Escalate to the human operator if the ontology reveals conflicting factual predicates from different sources, or if asked to drastically alter a pre-existing root schema.

## Implementation Workflow

1. **Trigger:** The workspace exposes new structured logic requiring persistence (Ingestion) or requests dependency impact analysis (Retrieval).
2. **Execute:** 
   - *If Ingestion:* Identify target Entities (e.g., `Person: Alice`), strictly type them, define directional Edges (`OWNED_BY`), and mutate the underlying graph state.
   - *If Retrieval:* Reject unstructured text search. Traverse the target Entity backward through its directional Edges to determine root-cause interconnectivity.
   - *Parsing:* If triggered by unstructured human text, translate explicit Entities before processing.
3. **Verify:** Assure no circular dependencies were injected during the state mutation and that every node touched maintains at least one valid outbound/inbound edge.
4. **Output:** Render the strict YAML format defined in the `Ontology Output Template`.

## Progressive Resources

For the exact diagnostic output schema to use post-validation, read:
👉 **[Ontology Output Template](templates/ontology-output-template.md)**

## Relationship to MCP

The **Ontology Skill** dictates *how* to think about structured memory. However, the exact mechanism for *storing* and *querying* this graph should be handled by an **MCP Server**. 

