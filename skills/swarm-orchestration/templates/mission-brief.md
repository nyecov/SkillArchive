# Swarm Mission Brief: [Task/Component Name]

When delegating tasks to specialized sub-agents, the Lead Agent MUST provide this standardized brief to prevent context fragmentation and ensure architectural harmony (Wa).

```markdown
# Mission Brief: [Specific Task Name]

## 1. Objective
- **Value Stream:** [What exactly is the sub-agent building or analyzing?]
- **Success Criteria:** [What proves the task is complete?]

## 2. Anchors & Constraints
- **Architectural Anchor:** [What existing design pattern must not be violated?]
- **Explicit Constraint:** [What is the sub-agent explicitly forbidden from doing?]

## 3. Required Output Format
- **Deliverable:** [e.g., A new file, a code patch, a JSON report]
- **Verification Method:** [How the Lead Agent will audit the result]
```