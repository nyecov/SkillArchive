#!/usr/bin/env python3
"""
Audit Go code for standards compliance.

Checks for:
- Error handling coverage
- Documentation on exported symbols

Usage:
    python audit_go_standards.py [--json] [--path PATH]
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any


def find_go_files(root_path: str = ".") -> List[Path]:
    """Find all .go files excluding vendor."""
    root = Path(root_path)
    go_files = []

    for pattern in ["**/*.go"]:
        for file_path in root.glob(pattern):
            if "vendor" not in file_path.parts:
                go_files.append(file_path)

    return go_files


def check_error_handling(file_path: Path) -> List[Dict[str, Any]]:
    """Check for potentially missing error handling."""
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return issues

    lines = content.split("\n")

    error_patterns = [
        r"\.Write\(",
        r"\.Read\(",
        r"\.Close\(",
        r"json\.Marshal",
        r"json\.Unmarshal",
        r"os\.Open",
        r"os\.Create",
    ]

    for line_num, line in enumerate(lines, 1):
        if "err" in line or "error" in line or "defer" in line:
            continue

        for pattern in error_patterns:
            if re.search(pattern, line):
                if line_num < len(lines):
                    next_line = lines[line_num] if line_num < len(lines) else ""
                    if "err" not in next_line and "if" not in line:
                        issues.append({
                            "file": str(file_path),
                            "line": line_num,
                            "type": "missing_error_handling",
                            "message": "Possible unhandled error",
                            "severity": "info"
                        })
                break

    return issues


def check_documentation(file_path: Path) -> List[Dict[str, Any]]:
    """Check for missing documentation on exported symbols."""
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception:
        return issues

    lines = content.split("\n")

    for line_num, line in enumerate(lines, 1):
        if re.match(r"^\s*(func|type|const|var)\s+[A-Z]", line):
            if line_num > 1:
                prev_line = lines[line_num - 2].strip()
                if not prev_line.startswith("//"):
                    symbol_match = re.search(r"(func|type|const|var)\s+([A-Z]\w*)", line)
                    if symbol_match:
                        issues.append({
                            "file": str(file_path),
                            "line": line_num,
                            "type": "missing_doc",
                            "symbol": symbol_match.group(2),
                            "message": f"Exported symbol '{symbol_match.group(2)}' lacks documentation",
                            "severity": "info"
                        })

    return issues


def audit_standards(path: str = ".") -> Dict[str, Any]:
    """Audit Go code for standards compliance."""
    all_issues = []
    go_files = find_go_files(path)

    for file_path in go_files:
        if "_test.go" in str(file_path):
            continue

        all_issues.extend(check_error_handling(file_path))
        all_issues.extend(check_documentation(file_path))

    return {
        "tool": "go_standards_audit",
        "issues": all_issues,
        "total": len(all_issues),
        "exit_code": 0
    }


def format_human_output(result: Dict[str, Any]) -> str:
    """Format results for human readability."""
    output = []

    if result["total"] == 0:
        output.append("No standards violations detected")
    else:
        output.append(f"[STANDARDS AUDIT] {result['total']} issue(s) found\n")

        by_type: Dict[str, List] = {}
        for issue in result["issues"]:
            issue_type = issue["type"]
            if issue_type not in by_type:
                by_type[issue_type] = []
            by_type[issue_type].append(issue)

        for issue_type in sorted(by_type.keys()):
            issues = by_type[issue_type]
            output.append(f"  [{issue_type}] {len(issues)} issue(s)")
            for issue in sorted(issues, key=lambda x: (x["file"], x["line"])):
                output.append(f"    {issue['file']}:{issue['line']} -- {issue['message']}")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Go standards and architecture")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--path", default=".", help="Path to scan")
    args = parser.parse_args()

    result = audit_standards(args.path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human_output(result))

    sys.exit(result.get("exit_code", 0))


if __name__ == "__main__":
    main()
