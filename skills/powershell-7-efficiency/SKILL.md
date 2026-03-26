---
id: 3f55c95e-172c-4782-884c-1fa77a4b531f
name: powershell-7-efficiency
version: 1.0.0
level: methodology
category: engineering
tags:
- engineering
- scripting
- automation
- performance
- cross-platform
description: Use when writing or optimizing PowerShell 7 scripts. Mandates the use of modern features like pipeline chaining, parallel processing, and ternary operators to ensure high-performance, cross-platform code.
---

# PowerShell 7 Efficiency

This skill mandates the use of modern PowerShell 7 (`pwsh`) features to maximize performance, readability, and cross-platform reliability.

## Core Efficiency Mandates

### 1. Modern Pipeline Operators
Use pipeline chain operators for concise logic control.
- **SUCCESS Chain (`&&`):** Only run the second command if the first succeeds.
  - `npm install && npm run build`
- **FAILURE Chain (`||`):** Run the second command only if the first fails.
  - `Test-Path ./config.json || New-Item ./config.json`

### 2. Parallel Processing
Use `-Parallel` for I/O bound or heavy computational tasks on collections.
- **Workflow:** `$items | ForEach-Object -Parallel { # Do work } -ThrottleLimit 10`
- **Note:** Remember that variables outside the script block must be accessed via the `$using:` scope (e.g., `$using:myVar`).

### 3. Concise Logical Operators
Avoid verbose `if/else` blocks for simple assignments.
- **Ternary Operator:** `<condition> ? <true-val> : <false-val>`
  - `$msg = $isSuccess ? "Passed" : "Failed"`
- **Null-Coalescing Operator:** `$val = $a ?? $b` (Returns `$a` unless it is null, then returns `$b`).
- **Null-Coalescing Assignment:** `$val ??= $defaultValue` (Assigns only if `$val` is null).

### 4. Performance Optimization (The "Anti-Patterns")
- **NEVER use `+=` on Arrays:** This creates a copy of the entire array. Use `[System.Collections.Generic.List[object]]` or a `StringBuilder` for high-volume string concatenation.
- **Streaming over Buffering:** Prefer passing data through the pipeline (`|`) rather than storing entire datasets in variables before processing.
- **Native .NET Speed:** For ultra-high performance (e.g., massive file reads), drop into .NET directly: `[System.IO.File]::ReadLines($path)`.

### 5. Error Management
- Use `ConciseView` (default in PS7) for cleaner logs.
- Always use `ErrorAction Stop` with `try/catch` blocks for predictable failure handling in automation.

### 6. Cross-Platform Reliability
- **Path Separators:** Always use `Join-Path` or forward slashes `/`. PowerShell 7 handles forward slashes correctly on all platforms.
- **Encoding:** PS7 defaults to UTF-8 without BOM. Use this consistently to avoid "Mojibake" when moving scripts between Windows and Linux.

## Workflows

### 1. Verification of Environment
Before running a complex script, verify the host is actually PowerShell 7:
`$isCoreCLR ? "Running PS7+" : "Running legacy PS5.1"`

### 2. Batch Processing Optimization
When processing files, combine `Get-ChildItem` with `-Parallel` to reduce execution time for large directories.

```powershell
Get-ChildItem -Filter *.log | ForEach-Object -Parallel {
    $content = Get-Content $_.FullName
    # High-speed processing here
}
```

## Referencing
- Refer to [SYNTAX.md](references/syntax.md) for a side-by-side comparison of PowerShell 5 vs 7 syntax.
