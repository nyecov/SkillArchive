---
name: jidoka
version: 2.0.0
level: methodology
category: safety
description: 'Use when an abnormality occurs, an iteration threshold is breached, or before executing any action flagged by the Layer 1 tripwire heuristic. Mandates reactive and proactive halting for root cause analysis.'
tags:
- methodology
- safety
- lean
- TPS
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: Hansei (Self-reflection)
  path: ../hansei/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Ho-Ren-So (Communication)
  path: ../ho-ren-so/SKILL.md
---

# Jidoka (Autonomation)

Jidoka is the ultimate safety mechanism in the agentic workflow. It acts physically as the **Andon Cord**, "Stopping the Line" to prevent the compounding of errors. Modernized Jidoka operates in a Dual-Layer architecture: acting as a swift reactive emergency brake when an error occurs, and a proactive circuit-breaker triggered only by deterministic physical heuristics.

## Core Mandates

### 1. The Reactive Halt (Layer 0)
Stop the line immediately if the iteration loop becomes unproductive or a hard interlock is breached.
- **Action:** Halt the workflow and initiate a Hansei root-cause analysis.
- **Constraint:** Do NOT attempt to "guess" a fix or power through after a halt is triggered.
- **Integration:** Binds to **Poka-yoke**; if any schema or deterministic interlock fails, the pipeline trips instantly.

#### Reactive Halt Triggers:
- **Budget Exhaustion:** The same bug persists after 3-5 failed attempts.
- **Debt Compounding:** New bugs outpace bug fixes.
- **Poka-yoke Breach:** A validation script explicitly fails.

### 2. The Proactive Tripwire (Layer 1)
To protect against catastrophic actions with zero latency, evaluate every proposed execution command against deterministic heuristic tripwires.
- **Action:** Before executing generic commands, ensure the command does not contain destructive patterns.
- **Constraint:** If a file edit attempts to modify/delete >100 lines at once without tests, or if a shell command contains patterns like `rm -rf`, `DROP TABLE`, `truncate`, or targets critical system directories (e.g., `.git/`), the agent MUST stop execution and invoke Layer 2.

### 3. The Circuit Breaker (Layer 2 - Subagent)
If the Layer 1 tripwire is hit, the agent does NOT proceed independently. It utilizes an isolated subagent to explicitly assess the risk.
- **Action:** Launch the `browser_subagent` (or equivalent execution subagent) with the explicit task of evaluating the blast radius of the proposed command. 
- **Constraint:** If the subagent confirms the action is high-risk without proper user consent, trigger the Andon Cord halt immediately. Do NOT run the command.

### 4. Human Escalation (Hō-Ren-Sō)
Transition from autonomous execution to human-in-the-loop 'Consultation' mode.
- **Action:** Use the Sōdan (Consult) protocol to alert the operator detailing the exact Abnormality, Location, and Hypothesis.
- **Integration:** Aligns with **Hō-Ren-Sō** to securely pass state to the human operator.

## Escalation & Halting

- **Jidoka:** This skill *is* the primary halting mechanism. It triggers automatically when a threshold is breached or a Layer 1 -> Layer 2 pattern flags high risk.
- **Hō-Ren-Sō:** Immediately use the Sōdan (Consult) protocol after an autonomous halt. Present three distinct paths to the user: **Stop** (resume later), **Revert** (undo), or **Restart** (pivot strategy).

## Implementation Workflow

1. **Trigger:** The agent proposes an action that hits a Layer 1 Tripwire heuritsic, or the agent experiences a repeating error loop.
2. **Execute:** 
   - *If reactive:* Stop immediately.
   - *If proactive:* Dispatch a subagent to evaluate the blast radius of the proposed action.
3. **Verify:** Check the subagent output or perform Hansei. If the risk is high or the error loop is confirmed, execute the HALT protocol.
4. **Output:** Format the diagnostic report using Hō-Ren-Sō principles and pause the pipeline for user input.
