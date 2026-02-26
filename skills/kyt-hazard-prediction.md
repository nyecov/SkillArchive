---
name: KYT (Hazard Prediction)
version: 1.0.0
description: A 4-round proactive protocol to identify and solve hidden hazards before acting. Typically performed by a Critic Agent.
category: risk-management
tags: [kyt, hazard-prediction, safety, critic-agent, pre-mortem]
---

# KYT: Hazard Prediction Training for Agents

KYT (Kiken Yochi Training) is a systematic method for identifying dangers before they occur.

## The 4-Round KYT Protocol

### Round 1: Identify the Hazard
- **Action:** List all potential dangers associated with the proposed action.
- *Example:* "Updating the database schema could lock the tables during peak hours."

### Round 2: Determine Critical Danger Points
- **Action:** Narrow down the list to the most severe or likely 'Point of No Return'.
- *Example:* "The critical point is the ALTER TABLE command which is non-reversible without a backup."

### Round 3: Establish Countermeasures
- **Action:** Define specific actions to mitigate the critical danger points.
- *Example:* "I will trigger a snapshot backup of the database 5 minutes before execution."

### Round 4: Set Action Targets
- **Action:** Create a final, binary checklist for the 'Go/No-Go' decision.
- *Example:* "Checklist: Backup verified? Table size checked? Maintenance window active?"

## Implementation Workflow

1. **Independent Pass:** A 'Critic Agent' runs the 4-round KYT on the 'Execution Agent's' plan.
2. **Review:** The Execution Agent must integrate the countermeasures.
3. **Confirm:** Execution only proceeds once all 'Action Targets' are met.
