#!/usr/bin/env python3
"""
Audit Python code for standards and best practices.

Checks for:
- Missing docstrings on public symbols
- Overly long functions (default limit: 50 lines)

Usage:
    python audit_python_standards.py [--json] [--path PATH] [--max-lines N]
"""

import ast
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional


def find_python_files(root_path: str = ".") -> List[Path]:
    """Find all .py files excluding venv."""
    root = Path(root_path)
    py_files = []

    exclude_dirs = {"venv", "__pycache__", ".venv", "env"}

    for file_path in root.rglob("*.py"):
        if not any(part in exclude_dirs for part in file_path.parts):
            py_files.append(file_path)

    return py_files


class StandardsVisitor(ast.NodeVisitor):
    """AST visitor to check standards."""

    def __init__(self, file_path: Path, content: str, max_function_lines: int = 50):
        self.file_path = file_path
        self.lines = content.split("\n")
        self.issues: List[Dict[str, Any]] = []
        self.max_function_lines = max_function_lines

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Check function standards."""
        if not node.name.startswith("_"):
            docstring = ast.get_docstring(node)
            if not docstring:
                self.issues.append({
                    "file": str(self.file_path),
                    "line": node.lineno,
                    "type": "missing_docstring",
                    "name": node.name,
                    "message": f"Public function '{node.name}' lacks docstring",
                    "severity": "info"
                })

            func_length = node.end_lineno - node.lineno
            if func_length > self.max_function_lines:
                self.issues.append({
                    "file": str(self.file_path),
                    "line": node.lineno,
                    "type": "long_function",
                    "name": node.name,
                    "length": func_length,
                    "message": f"Function '{node.name}' is {func_length} lines (limit: {self.max_function_lines})",
                    "severity": "info"
                })

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Check class standards."""
        docstring = ast.get_docstring(node)
        if not docstring and not node.name.startswith("_"):
            self.issues.append({
                "file": str(self.file_path),
                "line": node.lineno,
                "type": "missing_docstring",
                "name": node.name,
                "message": f"Public class '{node.name}' lacks docstring",
                "severity": "info"
            })

        self.generic_visit(node)


def check_file(file_path: Path, max_function_lines: int = 50) -> List[Dict[str, Any]]:
    """Check a single Python file for standards."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return [{"file": str(file_path), "error": str(e)}]

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    visitor = StandardsVisitor(file_path, content, max_function_lines)
    visitor.visit(tree)

    return visitor.issues


def audit_standards(path: str = ".", max_function_lines: int = 50) -> Dict[str, Any]:
    """Audit all Python files for standards compliance."""
    all_issues: List[Dict[str, Any]] = []
    py_files = find_python_files(path)

    for file_path in py_files:
        all_issues.extend(check_file(file_path, max_function_lines))

    issues = [i for i in all_issues if "error" not in i]

    return {
        "tool": "python_standards_audit",
        "issues": issues,
        "total": len(issues),
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

    parser = argparse.ArgumentParser(description="Audit Python standards and best practices")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--path", default=".", help="Path to scan")
    parser.add_argument("--max-lines", type=int, default=50, help="Max function lines before warning (default: 50)")
    args = parser.parse_args()

    result = audit_standards(args.path, args.max_lines)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human_output(result))

    sys.exit(result.get("exit_code", 0))


if __name__ == "__main__":
    main()
