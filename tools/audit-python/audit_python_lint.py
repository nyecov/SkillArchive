#!/usr/bin/env python3
"""
Audit Python code with pylint and ruff.

Runs pylint and/or ruff linters and reports issues.

Usage:
    python audit_python_lint.py [--json] [--path PATH] [--linter pylint|ruff|both]
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import List, Dict, Any


def run_pylint(path: str = ".") -> Dict[str, Any]:
    """Run pylint and parse output."""
    try:
        result = subprocess.run(
            ["pylint", "--exit-zero", "--output-format=json", path],
            capture_output=True,
            text=True,
            timeout=120
        )

        try:
            issues_raw = json.loads(result.stdout)
        except json.JSONDecodeError:
            if "not found" in result.stderr.lower():
                return {
                    "linter": "pylint",
                    "error": "pylint not found. Install with: pip install pylint",
                    "issues": []
                }
            raise

        issues = []
        for issue in issues_raw:
            issues.append({
                "file": issue.get("path", "unknown"),
                "line": issue.get("line", 0),
                "column": issue.get("column", 0),
                "message": issue.get("message", ""),
                "symbol": issue.get("symbol", "unknown"),
                "type": issue.get("type", "unknown").lower(),
                "severity": "error" if issue.get("type") == "error" else "warning"
            })

        return {
            "linter": "pylint",
            "issues": issues,
            "total": len(issues)
        }
    except FileNotFoundError:
        return {
            "linter": "pylint",
            "error": "pylint not found. Install with: pip install pylint",
            "issues": []
        }
    except subprocess.TimeoutExpired:
        return {
            "linter": "pylint",
            "error": "pylint timed out",
            "issues": []
        }


def run_ruff(path: str = ".") -> Dict[str, Any]:
    """Run ruff and parse output."""
    try:
        result = subprocess.run(
            ["ruff", "check", "--output-format=json", path],
            capture_output=True,
            text=True,
            timeout=120
        )

        try:
            lint_result = json.loads(result.stdout)
        except json.JSONDecodeError:
            if "not found" in result.stderr.lower():
                return {
                    "linter": "ruff",
                    "error": "ruff not found. Install with: pip install ruff",
                    "issues": []
                }
            raise

        issues = []
        for issue in lint_result if isinstance(lint_result, list) else []:
            issues.append({
                "file": issue.get("filename", "unknown"),
                "line": issue.get("location", {}).get("row", 0),
                "column": issue.get("location", {}).get("column", 0),
                "message": issue.get("message", ""),
                "code": issue.get("code", "unknown"),
                "severity": "error" if issue.get("fix") else "warning"
            })

        return {
            "linter": "ruff",
            "issues": issues,
            "total": len(issues)
        }
    except FileNotFoundError:
        return {
            "linter": "ruff",
            "error": "ruff not found. Install with: pip install ruff",
            "issues": []
        }
    except subprocess.TimeoutExpired:
        return {
            "linter": "ruff",
            "error": "ruff timed out",
            "issues": []
        }


def audit_lint(path: str = ".", linter: str = "both") -> Dict[str, Any]:
    """Run linting audits."""
    results = []
    total_issues = 0

    if linter in ["pylint", "both"]:
        pylint_result = run_pylint(path)
        results.append(pylint_result)
        total_issues += len(pylint_result.get("issues", []))

    if linter in ["ruff", "both"]:
        ruff_result = run_ruff(path)
        results.append(ruff_result)
        total_issues += len(ruff_result.get("issues", []))

    all_issues: List[Dict] = []
    for result in results:
        all_issues.extend(result.get("issues", []))

    return {
        "tool": "python_lint_audit",
        "linters_run": [r["linter"] for r in results],
        "issues": all_issues,
        "total": total_issues,
        "exit_code": 0
    }


def format_human_output(result: Dict[str, Any]) -> str:
    """Format results for human readability."""
    output = []

    if result["total"] == 0:
        output.append("No linting issues detected")
    else:
        output.append(f"[LINTING ISSUES] {result['total']} issue(s) found\n")

        by_file: Dict[str, List] = {}
        for issue in result["issues"]:
            file_key = issue.get("file", "unknown")
            if file_key not in by_file:
                by_file[file_key] = []
            by_file[file_key].append(issue)

        for file_path in sorted(by_file.keys()):
            output.append(f"  {file_path}")
            for issue in sorted(by_file[file_path], key=lambda x: x.get("line", 0)):
                severity_icon = "!" if issue.get("severity") == "error" else "~"
                code = issue.get("symbol") or issue.get("code") or ""
                output.append(f"    [{severity_icon}] Line {issue.get('line', '?')}: {code} -- {issue.get('message', '')}")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Python code with linters")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--path", default=".", help="Path to scan")
    parser.add_argument("--linter", choices=["pylint", "ruff", "both"], default="both",
                       help="Which linter(s) to run")
    args = parser.parse_args()

    result = audit_lint(args.path, args.linter)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human_output(result))

    sys.exit(result.get("exit_code", 0))


if __name__ == "__main__":
    main()
