---
id: 9d6f3e12-8c4b-4a5d-b0e1-2f3a4b5c6d7e
name: analyze-interview-patterns
version: 1.0.0
level: methodology
description: 'Use when requested to extract patterns, anti-patterns, or architectural guidance from the historical Interview Q&A memory bank.'
category: methodology
tags:
- learning
- kaizen
- context-engine
- yokoten
references:
- name: Context Engine (Core Logic)
  path: ../skills/context-engine/SKILL.md
- name: Interview Skill
  path: ../skills/interview/SKILL.md
- name: Yokoten (Horizontal Deployment)
  path: ../skills/yokoten/SKILL.md
requires:
- context-engine
---
# Analyze Interview Patterns

This workflow acts as the intelligence extraction layer for the Interview Memory Bank. By retrieving historical TOON chunks via the Context Engine, the agent can identify recurring logical friction points, systemic anti-patterns, or highly successful requirement definitions to broadcast (Yokoten) to future workflows.

## Core Mandates

### 1. RAG Orchestration (Muri Prevention)
NEVER attempt to read the raw `interview_qa_bank.toon` file directly. It may contain 50k+ words and will crash your context window.
- **Action:** You MUST use the Context Engine's `retrieve_interview_patterns` MCP tool to pull semantic chunks.
- **Constraint:** If the tool returns a `[WARNING: TRUNCATED AT 16000 CHARS]`, you MUST refine your query to be more specific rather than proceeding with a partial context.

### 2. Pattern Synthesis
Analyze the retrieved TOON blocks (`[Q: ...] 
 [A: ...]`) for systemic trends rather than isolated facts.
- **Action:** Look for anti-patterns (e.g., repeatedly failing to define sad-paths) or positive patterns (e.g., a specific Deglaze tactic that worked well).
- **Constraint:** Do not simply regurgitate the Q&As. You must distill them into an actionable "Standard" or "Rule".

## Implementation Workflow

1. **Trigger:** User asks to "analyze interview patterns regarding [topic/general]."
2. **Execute:** 
   - Call `retrieve_interview_patterns` using the requested topic as the `query` (or empty string for general recent patterns).
   - If truncation occurs, refine the query and call again.
   - Analyze the retrieved TOON blocks.
3. **Verify:** Ensure the extracted patterns are actually actionable directives, not just observations.
4. **Output:** Render a **Kaizen Guidance Report** summarizing the Anti-Patterns, Verified Patterns, and a Yokoten proposal for updating existing skills.

## Poka-yoke Output Template

```markdown
# Kaizen Guidance: Interview Patterns

## 1. Analyzed Query
[The search term used]

## 2. Identified Anti-Patterns (Muda)
- **Anti-Pattern 1:** [Description of recurring friction] -> **Correction:** [How to avoid it]

## 3. Verified Patterns (Value)
- **Pattern 1:** [Description of a highly effective approach found in the logs]

## 4. Yokoten Proposal
[Specific recommendation on which existing Skill or Template should be updated based on these findings]
```
