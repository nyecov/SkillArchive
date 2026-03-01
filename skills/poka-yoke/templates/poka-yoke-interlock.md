# Poka-yoke Interlock Declaration Template

When establishing or triggering an interlock constraint, the agent MUST output the schema check or dependency verification using this exact schema to document the physical constraint.

```markdown
# Poka-yoke Interlock Declaration

## 1. Interlock Type
- **Type:** [Schema Enforcement / State Machine Constraint / Prerequisite Interlock]
- **Target Component:** [The specific tool, function, or transition being protected]

## 2. Validation Criteria
- **Constraint Rule:** [What exact condition MUST be met to proceed?]
- **Current State:** [What is the current measured state?]

## 3. Interlock Status
- [ ] PASS (Condition met, proceeding to execution)
- [ ] HALT (Condition failed, triggering Jidoka)

## 4. Countermeasure (If HALT)
- **Hansei (Root Cause):** [Why did the interlock trip?]
- **Next Action:** [What must be fixed before the interlock is cleared?]
```
