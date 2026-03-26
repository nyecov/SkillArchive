# Incident Report: File Explorer Fails to Launch PowerShell 7 (`pwsh`)

## Date
March 26, 2026

## Symptoms
- Typing `pwsh` into the Windows File Explorer address bar failed to launch PowerShell 7.
- An "Access Denied" error dialog appeared, indicating a strict file system permission block pointing to the `C:\Program Files\WindowsApps\...` directory.
- The `pwsh` command worked normally from standard command-line interfaces, but not from the Explorer address bar.
- The legacy `powershell` command (Windows PowerShell 5.1) worked as expected from the Explorer address bar.

## Root Cause
A conflict existed between two different installations of PowerShell 7:
1. A previously installed **Microsoft Store version** (packaged as AppX/MSIX) located in the heavily restricted `C:\Program Files\WindowsApps` directory.
2. A newly installed **MSI version** located in the standard `C:\Program Files\PowerShell\7\` directory.

When `pwsh` was invoked from the Explorer address bar, Windows attempted to resolve the command using an overriding App Execution Alias pointing to the Microsoft Store stub (a 0-byte placeholder file in `%LOCALAPPDATA%\Microsoft\WindowsApps\pwsh.exe`). File Explorer failed to pass the correct security token required to execute the binary directly from its deeply restricted AppX path, resulting in the Access Denied error and blocking the standard MSI installation from running.

## Resolution
To resolve the conflict and restore functionality, the following steps were executed:
1. **Removed Broken Stubs:** Deleted the conflicting 0-byte `pwsh.exe` execution alias placeholder from `%LOCALAPPDATA%\Microsoft\WindowsApps`.
2. **Uninstalled Store Version:** Completely removed the interfering Microsoft Store AppX package using the command: `Get-AppxPackage -Name "*PowerShell*" | Remove-AppxPackage`.
3. **Created System Link:** Created a direct symbolic link in the System32 directory (`C:\Windows\System32\pwsh.exe`) pointing to the valid MSI installation executable (`C:\Program Files\PowerShell\7\pwsh.exe`). This ensures Explorer discovers it identically to the legacy `powershell.exe`.
4. **Cleared Explorer Cache:** Restarted the Windows Explorer process (`Stop-Process -Name explorer; Start-Process explorer`) to flush the cached AppX execution pointers and force it to immediately recognize the new System32 symlink.

## Outcome
Typing `pwsh` in the File Explorer address bar now correctly resolves to the MSI installation and successfully opens PowerShell 7 in the current directory.