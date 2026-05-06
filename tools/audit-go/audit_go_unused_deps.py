#!/usr/bin/env python3
"""
Audit Go code for unused imports.

Detects unused imports in Go source files using go vet.
Reports findings in human-readable and JSON formats.

Usage:
    python audit_go_unused_deps.py [--json] [--path PATH]
"""

import subprocess
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any


def check_unused_imports(path: str = ".") -> Dict[str, Any]:
    """Check for unused imports using go vet."""
    try:
        result = subprocess.run(
            ["go", "vet", "./..."],
            capture_output=True,
            text=True,
            cwd=path
        )

        issues = []
        for line in result.stderr.split("\n"):
            if "imported but not used" in line:
                match = re.search(r'(\S+):(\d+):\d+: imported and not used: "(.+?)"', line)
                if match:
                    issues.append({
                        "file": match.group(1),
                        "line": int(match.group(2)),
                        "package": match.group(3),
                        "severity": "warning",
                        "type": "unused_import"
                    })

        return {
            "tool": "go_vet",
            "issues": issues,
            "total": len(issues),
            "exit_code": 0 if len(issues) == 0 else 1
        }
    except FileNotFoundError:
        return {
            "tool": "go_vet",
            "error": "go not found. Ensure Go 1.21+ is installed.",
            "issues": [],
            "total": 0,
            "exit_code": 1
        }


def format_human_output(result: Dict[str, Any]) -> str:
    """Format results for human readability."""
    output = []

    if "error" in result:
        output.append(f"[ERROR] {result['error']}")
        return "\n".join(output)

    if result["total"] == 0:
        output.append("No unused imports detected")
    else:
        output.append(f"[UNUSED IMPORTS] {result['total']} issue(s) found\n")

        by_file: Dict[str, List] = {}
        for issue in result["issues"]:
            file_key = issue["file"]
            if file_key not in by_file:
                by_file[file_key] = []
            by_file[file_key].append(issue)

        for file_path, issues in sorted(by_file.items()):
            output.append(f"  {file_path}")
            for issue in issues:
                output.append(f"    Line {issue['line']}: {issue['package']} (unused)")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Go code for unused imports")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--path", default=".", help="Path to scan (default: current directory)")
    args = parser.parse_args()

    result = check_unused_imports(args.path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human_output(result))

    sys.exit(result.get("exit_code", 1))


if __name__ == "__main__":
    main()
