# Shisa Kanko Declaration Template

When performing the Pointing and Calling procedure, agents MUST output their isolation and logic statements using this exact schema to maintain deterministic safety before modifying the system.

```markdown
# Shisa Kanko Declaration

## [TARGET_ISOLATION]
- **File:** [Path to file]
- **Lines:** [Line range]
- **Exact Code Snippet:**
  ```[language]
  [Exact text to be modified, verified via read_file]
  ```

## [LOGIC_DECLARATION]
- **Intent:** [Specific code change to be made]
- **Success Criteria:** [What proves the change is correct]
- **Verification Method (TDD):** [The exact command or test that MUST pass after execution]
```
