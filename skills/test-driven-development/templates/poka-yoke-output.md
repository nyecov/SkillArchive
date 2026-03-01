# TDD Cycle Verification Template

When a TDD cycle is complete, the agent MUST output the final verification using exactly this Markdown schema to prove the cycle was followed:

```markdown
# TDD Cycle Verification: [Feature/Bug Name]

## 1. The Red Phase
- **Failing Test Name:** [Name of the test]
- **Observed Failure Log:** [Brief snippet of the exact AssertionError or failure, proving it failed correctly]

## 2. The Green Phase
- **Implementation Added:** [Brief description of the minimal code added]
- **Green Verification Log:** [Brief snippet showing the test suite passing]

## 3. The Refactor Phase (Optional)
- **Refactoring Applied:** [Description of cleanup performed, or N/A]
```
