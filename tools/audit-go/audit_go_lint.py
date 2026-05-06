#!/usr/bin/env python3
"""
Audit Go code with golangci-lint.

Runs golangci-lint and reports issues in human-readable and JSON formats.

Usage:
    python audit_go_lint.py [--json] [--path PATH]
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def run_golangci_lint(path: str = ".") -> Dict[str, Any]:
    """Run golangci-lint and parse output."""
    try:
        result = subprocess.run(
            ["golangci-lint", "run", "--json", path],
            capture_output=True,
            text=True,
            timeout=120
        )

        try:
            lint_result = json.loads(result.stdout)
        except json.JSONDecodeError:
            if "command not found" in result.stderr or "not found" in result.stderr:
                return {
                    "tool": "golangci-lint",
                    "error": "golangci-lint not found. Install with: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest",
                    "issues": [],
                    "total": 0,
                    "exit_code": 1
                }
            raise

        issues = []
        for issue_data in lint_result.get("Issues", []):
            issues.append({
                "file": issue_data.get("Pos", {}).get("Filename", "unknown"),
                "line": issue_data.get("Pos", {}).get("Line", 0),
                "column": issue_data.get("Pos", {}).get("Column", 0),
                "message": issue_data.get("Text", ""),
                "linter": issue_data.get("FromLinter", "unknown"),
                "severity": "warning"
            })

        return {
            "tool": "golangci-lint",
            "issues": issues,
            "total": len(issues),
            "exit_code": 0 if len(issues) == 0 else 1
        }
    except FileNotFoundError:
        return {
            "tool": "golangci-lint",
            "error": "golangci-lint not found. Install with: go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest",
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
        output.append("No linting issues detected")
    else:
        output.append(f"[LINT] {result['total']} issue(s) found\n")

        by_file: Dict[str, List] = {}
        for issue in result["issues"]:
            file_key = issue["file"]
            if file_key not in by_file:
                by_file[file_key] = []
            by_file[file_key].append(issue)

        for file_path in sorted(by_file.keys()):
            output.append(f"  {file_path}")
            for issue in by_file[file_path]:
                output.append(f"    [{issue['linter']}] Line {issue['line']}: {issue['message']}")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Go code with golangci-lint")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--path", default=".", help="Path to scan")
    args = parser.parse_args()

    result = run_golangci_lint(args.path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human_output(result))

    sys.exit(result.get("exit_code", 1))


if __name__ == "__main__":
    main()
