---
name: Hō-Ren-Sō (Report, Contact, Consult)
version: 1.0.0
description: The fundamental communication protocol for multi-agent systems and human-in-the-loop (HITL) synchronization.
category: communication
tags: [ho-ren-so, collaboration, hitl, reporting, coordination]
---

# Hō-Ren-Sō: Communication Standard for Agents

Hō-Ren-Sō ensures that information flows smoothly across the system, preventing silos and ambiguity.

## The Three Pillars

### 1. Hōkoku (Report)
- **What:** Reporting progress and results to the supervisor/human.
- **Format:** Brief, factual, and chronological.
- **Timing:** When a milestone is reached or a task is completed.

### 2. Renraku (Contact)
- **What:** Informing peers or stakeholders of facts without personal opinion or bias.
- **Format:** "Fact X has occurred. System State Y is now active."
- **Timing:** Immediately upon a change in the environment (e.g., "The API is currently returning 500 errors").

### 3. Sōdan (Consult)
- **What:** Seeking advice or a decision when encountering an ambiguous or high-risk situation.
- **Format:** Present the problem, the context, and proposed options for the human to choose from.
- **Timing:** *Before* taking a non-deterministic or high-impact action.

## Implementation Workflow

1. **State Tracking:** Maintain a clear log of what has been reported (Hōkoku) and shared (Renraku).
2. **Ambiguity Trigger:** If a decision branch has >1 viable path, trigger a Sōdan (Consultation).
3. **Feedback Integration:** Incorporate human advice into the current state.
