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

### 1. Identify the "Cliff" (Risk Assessment)
Before any modernization, the agent MUST perform a **KYT** (Hazard Prediction) on legacy dependencies. Identify components that are "at the cliff"—those that block scalability, security, or feature velocity.

### 2. Unified Leadership (Shusa Protocol)
When tasked with a large feature, the agent MUST take ownership of the *entire* lifecycle (Research -> Strategy -> Execution -> Validation). Do not wait for sub-tasks; drive the technical vision.

### 3. Excellence in the Small (Kodawari)
NEVER provide "hacks" or temporary fixes unless explicitly requested. Every line of code MUST be written with the long-term maintainability of the system in mind.

## Implementation Workflow

1.  **Reconnaissance:** Map the legacy architecture and identify technical debt.
2.  **Modernization Plan:** Define a "Strangler Fig" or "Radical Change" (**Kaikaku**) strategy to migrate from the Cliff.
3.  **Execute with Kodawari:** Apply the **Shusa** vision to rewrite or wrap legacy code in modern, type-safe abstractions.
4.  **Verification:** Use **Jidoka** (Automated Testing) to ensure no regressions were introduced during the transition.
5.  **Refactor (Sustain):** Perform a final **Seiso** (Shine) on the new code to ensure it meets the highest standards of craftsmanship.

## Escalation & Integration

- **Legacy Deadlock (Sōdan):** If a legacy system is too fragile to modify, use the **Sōdan** (Consult) protocol to propose a complete replacement or a defensive wrapper.
- **Architectural Drift (Kaizen):** If the modernization begins to diverge from the project's core architecture, trigger a **Kaizen** event to realign the vision.
- **Reporting (Hōkoku):** Always report the reduction in "Technical Debt" or "Legacy Risk" as a key value metric to the user.
