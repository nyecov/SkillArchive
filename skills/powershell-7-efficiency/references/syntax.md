# PowerShell 5.1 vs PowerShell 7 Syntax Comparison

This table provides a high-signal reference for translating legacy PowerShell 5.1 patterns into high-efficiency PowerShell 7 patterns.

| Feature | PowerShell 5.1 (Legacy) | PowerShell 7 (Modern/Efficient) |
| :--- | :--- | :--- |
| **Pipeline Chain** | `cmd1; if ($?) { cmd2 }` | `cmd1 && cmd2` |
| **Failover Chain** | `cmd1; if (-not $?) { cmd2 }` | `cmd1 || cmd2` |
| **Ternary Logic** | `if ($val) { $a } else { $b }` | `$val ? $a : $b` |
| **Null-Coalescing** | `if ($null -eq $a) { $b } else { $a }` | `$a ?? $b` |
| **Parallel Loop** | Custom Jobs or Workflows (Complex) | `1..100 | ForEach-Object -Parallel { ... }` |
| **Concise Error** | Full stack trace/verbose red text | `ConciseView` (Single-line focus) |
| **Native .NET** | `.NET Framework` | `.NET Core` (faster startup/runtime) |
| **Remoting** | `WinRM` (WS-Man) | `SSH` (Native cross-platform) |

## Parallel Processing Cheat Sheet

When using `ForEach-Object -Parallel`, remember these constraints:

1.  **Variables:** Use `$using:varName` to access variables from the outer scope.
2.  **Thread Safety:** Avoid writing to the same file or a shared non-thread-safe collection (like a basic `ArrayList`) simultaneously.
3.  **Throttling:** Use `-ThrottleLimit` (default is 5) to control concurrency and avoid overwhelming system resources.
4.  **Error Handling:** Exceptions within a parallel block will be collected and reported after all iterations complete, unless `ErrorAction Stop` is used.
