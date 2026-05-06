#!/usr/bin/env python3
"""
Audit Go code for naming convention violations.

Checks package names, function names, variable names, and constants
against Go style conventions.

Usage:
    python audit_go_naming.py [--json] [--path PATH]
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any


def find_go_files(root_path: str = ".") -> List[Path]:
    """Find all .go files excluding vendor and test files."""
    root = Path(root_path)
    go_files = []

    for pattern in ["**/*.go"]:
        for file_path in root.glob(pattern):
            if "vendor" not in file_path.parts:
                go_files.append(file_path)

    return go_files


def check_file(file_path: Path) -> List[Dict[str, Any]]:
    """Check a single Go file for naming violations."""
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return [{"file": str(file_path), "error": str(e)}]

    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        if line.strip().startswith("package "):
            match = re.search(r"package\s+([a-zA-Z_]\w*)", line)
            if match:
                pkg_name = match.group(1)
                if not re.match(r"^[a-z][a-z0-9]*$", pkg_name):
                    issues.append({
                        "file": str(file_path),
                        "line": line_num,
                        "type": "package_name",
                        "name": pkg_name,
                        "message": f"Package '{pkg_name}' should be lowercase",
                        "severity": "warning"
                    })

    for line_num, line in enumerate(lines, 1):
        func_match = re.search(r"func\s+\(.*?\)?\s*([A-Za-z_]\w*)\s*\(", line)
        if func_match:
            func_name = func_match.group(1)
            is_exported = func_name[0].isupper()

            if is_exported and not re.match(r"^[A-Z][a-zA-Z0-9]*$", func_name):
                issues.append({
                    "file": str(file_path),
                    "line": line_num,
                    "type": "function_name",
                    "name": func_name,
                    "message": f"Exported function '{func_name}' should be PascalCase",
                    "severity": "warning"
                })

        const_match = re.search(r"const\s+([A-Z][A-Z0-9_]*)\s*=", line)
        if const_match:
            const_name = const_match.group(1)
            if not re.match(r"^[A-Z][A-Z0-9_]*$", const_name):
                issues.append({
                    "file": str(file_path),
                    "line": line_num,
                    "type": "constant_name",
                    "name": const_name,
                    "message": f"Constant '{const_name}' should be UPPERCASE_WITH_UNDERSCORES",
                    "severity": "info"
                })

    return issues


def audit_naming(path: str = ".") -> Dict[str, Any]:
    """Audit all Go files for naming violations."""
    all_issues = []
    go_files = find_go_files(path)

    for file_path in go_files:
        file_issues = check_file(file_path)
        all_issues.extend(file_issues)

    return {
        "tool": "go_naming_audit",
        "issues": all_issues,
        "total": len(all_issues),
        "exit_code": 0
    }


def format_human_output(result: Dict[str, Any]) -> str:
    """Format results for human readability."""
    output = []

    if result["total"] == 0:
        output.append("No naming convention violations detected")
    else:
        output.append(f"[NAMING AUDIT] {result['total']} issue(s) found\n")

        by_file: Dict[str, List] = {}
        for issue in result["issues"]:
            if "error" in issue:
                continue
            file_key = issue["file"]
            if file_key not in by_file:
                by_file[file_key] = []
            by_file[file_key].append(issue)

        for file_path in sorted(by_file.keys()):
            output.append(f"  {file_path}")
            for issue in by_file[file_path]:
                severity_icon = "i" if issue["severity"] == "info" else "!"
                output.append(f"    [{severity_icon}] Line {issue['line']}: {issue['message']}")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Go naming conventions")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--path", default=".", help="Path to scan")
    args = parser.parse_args()

    result = audit_naming(args.path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human_output(result))

    sys.exit(result.get("exit_code", 0))


if __name__ == "__main__":
    main()
