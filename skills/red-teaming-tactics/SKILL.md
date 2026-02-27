---
name: red-teaming-tactics
version: 1.0.0
level: tactical
description: 'Adversarial stress-testing for security and logic.  Use to identify
  bypasses, edge-case failures, and "happy-path" biases in proposed implementations.\'
category: safety
tags:
- safety
- security
references:
- name: Secure Security
  path: ../secure-security/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Deglaze Tactics
  path: ../deglaze-tactics/SKILL.md
---

# Red-Teaming Tactics

Red-teaming is the practice of viewing a system from the perspective of an adversary. While **KYT** identifies hazards and **Secure Security** provides checks, **Red-Teaming** actively attempts to circumvent those very protections. It is the final gate for ensuring that "Safety" is not just "Compliance."

## Core Mandates

### 1. Adversarial Simulation (The Attacker's Mindset)
Before finalizing an implementation, the agent MUST explicitly attempt to "break" the proposed logic.
- **Action:** Formulate a specific attack vector (e.g., "If I am an unauthorized user, can I access this endpoint by manipulating the session cookie?").
- **Constraint:** NEVER assume a check is sufficient because it exists. Prove it by trying to bypass it.
- **Integration:** Acts as an adversarial **Poka-yoke** validator.

### 2. Bypass Analysis
Focus on identifying "Logic Bypasses" rather than just syntax errors.
- **Action:** Test for common vulnerabilities: IDOR (Insecure Direct Object Reference), XSS (Cross-Site Scripting), and Type Confusion.
- **Constraint:** Do not limit testing to the "Happy Path." Specifically target the "Error Paths" and "Edge States."
- **Integration:** Feeds identified vulnerabilities back into **KYT** to establish new countermeasures.

### 3. Proof of Vulnerability (PoV)
A vulnerability is only "fixed" once its Proof of Vulnerability (reproduction script) fails.
- **Action:** Create a minimal "Attack Script" or manual reproduction step that demonstrates the failure.
- **Constraint:** Verification is incomplete until the PoV script is blocked by the new implementation.
- **Integration:** Uses **Genchi Genbutsu** to verify the successful mitigation of the threat.

## Escalation & Halting

- **Jidoka:** If a critical bypass (e.g., secret leakage, unauthorized write) is discovered that cannot be mitigated within the current architecture, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to report the PoV and proposed fix to the user.

## Implementation Workflow

1. **Trigger:** Completion of a feature involving auth, input, or sensitive data.
2. **Execute:** 
   - Identify the "Crown Jewels" (the data/action being protected).
   - Formulate 2-3 attack vectors.
   - Attempt the bypass (The Red-Teaming Pass).
3. **Verify:** Use the PoV script to confirm the vulnerability and its subsequent fix.
4. **Output:** A hardened implementation and a summary of the defeated attack vectors.
