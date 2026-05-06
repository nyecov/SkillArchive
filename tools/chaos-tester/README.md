# chaos-tester

Prompts for adversarial edge-case and chaos test scenario generation for a source file. Use during the Red Phase of TDD for high-risk logic to surface boundary conditions and failure modes before writing the primary test suite.

## Usage

```powershell
# Basic — generates chaos test prompt for a source file
.\Invoke-Chaos-Tester.ps1 -SourceFile ".\internal\domain\solver\solver.go"

# With resilience guide for additional context
.\Invoke-Chaos-Tester.ps1 -SourceFile ".\src\parser.py" -ResilienceGuide ".\docs\error-handling.md"
```

## Output

Prints a structured prompt for an AI model covering:

- Boundary conditions (min/max, empty, null)
- Invalid input combinations
- Concurrent access / race conditions
- Resource exhaustion
- Error propagation paths
- State machine violations

## When to use

During the `[Red]` phase for any logic that handles:
- Mathematical constraints or thresholds
- Complex state machines
- External data parsing
- Resource allocation or combinatorial search
