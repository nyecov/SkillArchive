---
name: toon-token-oriented-notation
version: 1.2.0
level: technical
description: 'Procedure for serializing structured data into Token-Oriented Object
  Notation. Used to optimize LLM context windows and improve retrieval accuracy for
  tabular datasets.

  '
category: architecture
tags:
- architecture
references:
- name: Muda (Waste Eradication)
  path: ../muda/SKILL.md
---

# TOON Serialization Procedure

TOON is used to compress uniform tabular data for LLM consumption. This procedure ensures deterministic conversion and token-savings verification.

## Core Mandates

### 1. Tabular Eligibility Audit
Before serializing, the agent MUST verify the data's "Tabular Eligibility" (>70% uniform objects).
- **Action:** Compare TOON token count vs. JSON compact token count.
- **Constraint:** NEVER use TOON for deeply nested (>3 levels) or irregular data where JSON compact is more efficient.

### 2. Schema Injection
Every TOON block MUST be preceded by the `[N]{fields}` header syntax.
- **Action:** Explicitly define field names in the header to ensure the LLM maintains a clear schema.
- **Integration:** This is a structural **Poka-yoke** to prevent column-misalignment hallucinations.

## Implementation Workflow

1. **Trigger:** Large tabular dataset detected in a prompt or tool output.
2. **Audit:** Confirm tabular eligibility and level of nesting.
3. **Serialize:** Convert to TOON using the `[count]{fields}` header and tab delimiters.
4. **Verify:** Perform a sample "Retrieval Test" to ensure the data is readable by the agent.
