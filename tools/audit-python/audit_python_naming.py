#!/usr/bin/env python3
"""
Audit Python code for PEP 8 naming conventions.

Checks:
- Function names (lowercase with underscores / snake_case)
- Class names (PascalCase)
- Variable names (snake_case)

Usage:
    python audit_python_naming.py [--json] [--path PATH]
"""

import ast
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any


def find_python_files(root_path: str = ".") -> List[Path]:
    """Find all .py files excluding venv."""
    root = Path(root_path)
    py_files = []

    exclude_dirs = {"venv", "__pycache__", ".venv", "env"}

    for file_path in root.rglob("*.py"):
        if not any(part in exclude_dirs for part in file_path.parts):
            py_files.append(file_path)

    return py_files


class NamingVisitor(ast.NodeVisitor):
    """AST visitor to check naming conventions."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.issues: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Check function naming."""
        if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
            if not node.name.startswith("__"):
                self.issues.append({
                    "file": str(self.file_path),
                    "line": node.lineno,
                    "type": "function_name",
                    "name": node.name,
                    "message": f"Function '{node.name}' should be snake_case",
                    "severity": "warning"
                })
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        """Check async function naming."""
        if not re.match(r"^[a-z_][a-z0-9_]*$", node.name):
            if not node.name.startswith("__"):
                self.issues.append({
                    "file": str(self.file_path),
                    "line": node.lineno,
                    "type": "function_name",
                    "name": node.name,
                    "message": f"Async function '{node.name}' should be snake_case",
                    "severity": "warning"
                })
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        """Check class naming."""
        if not re.match(r"^[A-Z][a-zA-Z0-9]*$", node.name):
            self.issues.append({
                "file": str(self.file_path),
                "line": node.lineno,
                "type": "class_name",
                "name": node.name,
                "message": f"Class '{node.name}' should be PascalCase",
                "severity": "warning"
            })
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        """Check variable naming."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                name = target.id
                if not name.startswith("_"):
                    if re.match(r"^[A-Z][A-Z0-9_]*$", name):
                        pass  # constant — fine
                    elif re.match(r"^[a-z_][a-z0-9_]*$", name):
                        pass  # snake_case — fine
                    else:
                        self.issues.append({
                            "file": str(self.file_path),
                            "line": node.lineno,
                            "type": "variable_name",
                            "name": name,
                            "message": f"Variable '{name}' should be snake_case",
                            "severity": "info"
                        })
        self.generic_visit(node)


def check_file(file_path: Path) -> List[Dict[str, Any]]:
    """Check a single Python file for naming violations."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return [{"file": str(file_path), "error": str(e)}]

    try:
        tree = ast.parse(content)
    except SyntaxError:
        return []

    visitor = NamingVisitor(file_path)
    visitor.visit(tree)

    return visitor.issues


def audit_naming(path: str = ".") -> Dict[str, Any]:
    """Audit all Python files for naming violations."""
    all_issues: List[Dict[str, Any]] = []
    py_files = find_python_files(path)

    for file_path in py_files:
        all_issues.extend(check_file(file_path))

    issues = [i for i in all_issues if "error" not in i]

    return {
        "tool": "python_naming_audit",
        "issues": issues,
        "total": len(issues),
        "exit_code": 0
    }


def format_human_output(result: Dict[str, Any]) -> str:
    """Format results for human readability."""
    output = []

    if result["total"] == 0:
        output.append("No naming convention violations detected")
    else:
        output.append(f"[NAMING AUDIT] {result['total']} issue(s) found\n")

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
                severity_icon = "i" if issue["severity"] == "info" else "~"
                output.append(f"    [{severity_icon}] {issue['file']}:{issue['line']} -- {issue['message']}")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Python naming conventions")
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
