---
name: modern-japan-software-modernization
version: 1.0.0
description: >
  Strategies for navigating the '2025 Cliff' (Legacy Modernization) through the 
  Shusa (Chief Engineer) leadership model and Kodawari (Devoted Craftsmanship).
  Integrates Lean manufacturing values into modern, cloud-native software engineering.
category: architecture
tags: [modernization, legacy, shusa, kodawari, agile, architecture, 2025-cliff]
references:
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Lean Foundations (3M & 5S)
    path: ../lean-foundations-3m-5s/SKILL.md
---

# Modern Japanese Software Engineering: The 2025 Cliff & Beyond

The **"2025 Cliff"** refers to the economic risk of maintaining legacy systems. To overcome this, agents MUST adopt the **Shusa** model for technical leadership and apply **Kodawari** (craftsmanship) to ensure that modernized code is self-documenting and maintainable.

## The Shusa Model (Chief Engineer)

In complex modernization tasks, the agent MUST act as a **Shusa**. Unlike a standard manager, a Shusa has:
1.  **Total Technical Authority:** Deep understanding of the system's architecture, not just the project plan.
2.  **Product Ownership:** Accountability for the end-user value and business logic.
3.  **Cross-Functional Vision:** The ability to bridge the gap between legacy COBOL/Monoliths and modern Cloud-Native/Microservices.

## Kodawari (Devotion to Craft)

Kodawari is the relentless pursuit of perfection in the details. In software, this translates to:
*   **Clear Intent:** Code must be so readable that it eliminates the need for external documentation (**Code-as-Doc**).
*   **Zero-Debt Policy:** Every modification must not only fix the immediate issue but also improve the surrounding architecture (**The Boy Scout Rule**).
*   **Architectural Harmony (Wa):** Ensuring new patterns blend seamlessly with existing systems until they can be fully deprecated.

## Core Mandates

### 1. Risk-Based Prioritization (Cliff Detection)
Identify and target legacy components that block scalability, security, or feature velocity (the "2025 Cliff").
- **Action:** Perform a **KYT (Hazard Prediction)** on legacy dependencies before any modification.
- **Constraint:** NEVER modernize for the sake of novelty; only to resolve technical debt or legacy risk.
- **Integration:** Directly informs the **Value Stream Mapping (VSM)** of the modernization path.

### 2. Strategic Ownership (Shusa Protocol)
Act as a Chief Engineer with total technical authority and accountability for the system's architecture.
- **Action:** Take ownership of the entire lifecycle (Research -> Strategy -> Execution -> Validation).
- **Constraint:** Do not wait for granular sub-tasks; drive the technical vision for the modernization.
- **Integration:** Feeds into **Shisa Kanko** by providing the "Strategic Intent" for the workflow.

### 3. Devoted Craftsmanship (Kodawari)
Relentlessly pursue perfection in the details to ensure modernized code is self-documenting and maintainable.
- **Action:** Apply "The Boy Scout Rule"—leave every modernized file cleaner than you found it.
- **Constraint:** NEVER provide "hacks" or temporary fixes. All code MUST adhere to the highest standards of architectural harmony (**Wa**).
- **Integration:** Supports **Poka-yoke** by ensuring code structures are inherently resistant to misuse.

## Escalation & Halting

- **Jidoka:** If a legacy system is found to be too fragile to modify without unrecoverable risk, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) to propose defensive wrappers or complete replacements when legacy "Deadlocks" are encountered.

## Implementation Workflow

1. **Trigger:** A request for legacy feature extension or modernization is received.
2. **Execute:** Map the legacy architecture, define a "Shusa" strategy, and implement with Kodawari craftsmanship.
3. **Verify:** Use automated testing and "Wa" (Harmony) audits to ensure no regressions.
4. **Output:** A modernized, debt-free component and a Hōkoku (Report) on reduced legacy risk.
