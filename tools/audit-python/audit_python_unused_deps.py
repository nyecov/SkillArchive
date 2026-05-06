#!/usr/bin/env python3
"""
Audit Python code for unused imports.

Detects unused imports in Python files using AST parsing.

Usage:
    python audit_python_unused_deps.py [--json] [--path PATH]
"""

import ast
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Set, Tuple


def find_python_files(root_path: str = ".") -> List[Path]:
    """Find all .py files excluding venv and __pycache__."""
    root = Path(root_path)
    py_files = []

    exclude_dirs = {"venv", "__pycache__", ".venv", "env", "node_modules"}

    for file_path in root.rglob("*.py"):
        if not any(part in exclude_dirs for part in file_path.parts):
            py_files.append(file_path)

    return py_files


class ImportVisitor(ast.NodeVisitor):
    """AST visitor to find imports and usage."""

    def __init__(self):
        self.imports: Dict[str, Tuple[int, str]] = {}
        self.used_names: Set[str] = set()

    def visit_Import(self, node: ast.Import):
        """Handle 'import X' statements."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imports[name] = (node.lineno, "import")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        """Handle 'from X import Y' statements."""
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            if name != "*":
                self.imports[name] = (node.lineno, "from")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        """Track name usage."""
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        """Track attribute access."""
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        self.generic_visit(node)


def check_file(file_path: Path) -> List[Dict[str, Any]]:
    """Check a single Python file for unused imports."""
    issues = []

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        return [{"file": str(file_path), "error": str(e)}]

    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return [{"file": str(file_path), "error": f"Syntax error: {e}"}]

    visitor = ImportVisitor()
    visitor.visit(tree)

    for name, (line_no, import_type) in visitor.imports.items():
        if name not in visitor.used_names:
            if not name.startswith("_"):
                issues.append({
                    "file": str(file_path),
                    "line": line_no,
                    "import": name,
                    "type": import_type,
                    "message": f"'{name}' imported but unused",
                    "severity": "warning"
                })

    return issues


def audit_unused_deps(path: str = ".") -> Dict[str, Any]:
    """Audit all Python files for unused imports."""
    all_issues: List[Dict[str, Any]] = []
    py_files = find_python_files(path)

    for file_path in py_files:
        all_issues.extend(check_file(file_path))

    clean_issues = [i for i in all_issues if "error" not in i]

    return {
        "tool": "python_unused_deps",
        "issues": clean_issues,
        "total": len(clean_issues),
        "exit_code": 0
    }


def format_human_output(result: Dict[str, Any]) -> str:
    """Format results for human readability."""
    output = []

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

        for file_path in sorted(by_file.keys()):
            output.append(f"  {file_path}")
            for issue in by_file[file_path]:
                output.append(f"    Line {issue['line']}: {issue['import']} (unused)")

    return "\n".join(output)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Audit Python for unused imports")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--path", default=".", help="Path to scan")
    args = parser.parse_args()

    result = audit_unused_deps(args.path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_human_output(result))

    sys.exit(result.get("exit_code", 0))


if __name__ == "__main__":
    main()
