#!/usr/bin/env python3
"""
Bug/Issue Triage Validator

Validates that bugs and issues have completed the mandatory triage review process.
Expects the following structure relative to the working directory (configurable):

  <backlog-root>/bugs/BUG-*.md
  <backlog-root>/issues/ISSUE-*.md
  <backlog-root>/stories/STORY-*.md
  <backlog-root>/epics/EPIC-*.md

Usage:
    python triage_validator.py [--type bug|issue|all] [--id ID] [--strict]
    python triage_validator.py --backlog-root path/to/backlog/backlog
"""

import os
import sys
from pathlib import Path
from typing import Set, List, Dict
import re
import argparse


def resolve_backlog_root(arg: str) -> Path:
    """Resolve the backlog root directory."""
    if arg:
        p = Path(arg)
    else:
        # Convention: sdlc_backlog/backlog relative to cwd
        candidates = [
            Path.cwd() / "sdlc_backlog" / "backlog",
            Path.cwd() / "backlog",
            Path.cwd(),
        ]
        for c in candidates:
            if (c / "bugs").exists() or (c / "issues").exists():
                p = c
                break
        else:
            p = Path.cwd()
    return p


def get_artifact_files(directory: Path, pattern: str = "*.md") -> List[Path]:
    if not directory.exists():
        return []
    return sorted(directory.glob(pattern))


def extract_id(filepath: Path) -> str:
    return filepath.stem


def read_file_content(filepath: Path) -> str:
    if not filepath.exists():
        return ""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def extract_checkboxes(content: str) -> Dict[str, bool]:
    checked = {}
    for line in content.split('\n'):
        if '- [x]' in line.lower() or '- [X]' in line:
            checked[line.strip()] = True
        elif '- [ ]' in line:
            checked[line.strip()] = False
    return checked


def validate_bug(filepath: Path, stories_dir: Path) -> Dict:
    content = read_file_content(filepath)

    result = {
        'id': extract_id(filepath),
        'valid': True,
        'errors': [],
        'warnings': [],
        'triage_complete': False,
    }

    if '## Bug Triage Review' not in content and '## Triage' not in content:
        result['errors'].append('Missing Triage Review section (## Bug Triage Review or ## Triage)')
        result['valid'] = False

    story_ids = re.findall(r'STORY-[A-Z0-9\-]+', content)
    for story_id in story_ids:
        story_file = stories_dir / f"{story_id}.md"
        if not story_file.exists():
            result['warnings'].append(f'Referenced story not found: {story_id}')

    checkboxes = extract_checkboxes(content)
    triage_checks = [v for k, v in checkboxes.items() if 'review' in k.lower() or 'triage' in k.lower()]
    result['triage_complete'] = all(triage_checks) if triage_checks else False

    return result


def validate_issue(filepath: Path, stories_dir: Path) -> Dict:
    content = read_file_content(filepath)

    result = {
        'id': extract_id(filepath),
        'valid': True,
        'errors': [],
        'warnings': [],
        'triage_complete': False,
    }

    if '## Issue Triage Review' not in content and '## Triage' not in content:
        result['errors'].append('Missing Triage Review section (## Issue Triage Review or ## Triage)')
        result['valid'] = False

    story_ids = re.findall(r'STORY-[A-Z0-9\-]+', content)
    for story_id in story_ids:
        story_file = stories_dir / f"{story_id}.md"
        if not story_file.exists():
            result['warnings'].append(f'Referenced story not found: {story_id}')

    checkboxes = extract_checkboxes(content)
    triage_checks = [v for k, v in checkboxes.items() if 'review' in k.lower() or 'triage' in k.lower()]
    result['triage_complete'] = all(triage_checks) if triage_checks else False

    return result


def main():
    parser = argparse.ArgumentParser(description="Validate Bug/Issue triage completeness")
    parser.add_argument("--type", choices=["bug", "issue", "all"], default="all")
    parser.add_argument("--id", help="Validate only a specific artifact ID")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any triage review is missing")
    parser.add_argument("--backlog-root", default="", help="Path to backlog directory (default: auto-detect sdlc_backlog/backlog)")
    args = parser.parse_args()

    backlog_root = resolve_backlog_root(args.backlog_root)
    bugs_dir = backlog_root / "bugs"
    issues_dir = backlog_root / "issues"
    stories_dir = backlog_root / "stories"

    bugs = get_artifact_files(bugs_dir, "BUG-*.md")
    issues = get_artifact_files(issues_dir, "ISSUE-*.md")

    print("=" * 60)
    print("BUG/ISSUE TRIAGE VALIDATOR")
    print("=" * 60)
    print(f"Backlog root: {backlog_root}")
    print(f"Bugs:    {len(bugs)}")
    print(f"Issues:  {len(issues)}")
    print()

    results = []

    if args.type in ["bug", "all"]:
        for bug_file in bugs:
            if args.id and bug_file.stem != args.id:
                continue
            results.append(validate_bug(bug_file, stories_dir))

    if args.type in ["issue", "all"]:
        for issue_file in issues:
            if args.id and issue_file.stem != args.id:
                continue
            results.append(validate_issue(issue_file, stories_dir))

    valid_count = sum(1 for r in results if r['valid'])
    invalid_count = sum(1 for r in results if not r['valid'])

    print("-" * 60)
    print("VALIDATION SUMMARY")
    print("-" * 60)
    print(f"Valid:   {valid_count}")
    print(f"Invalid: {invalid_count}")
    print()

    for result in results:
        if result['errors']:
            print(f"[INVALID] {result['id']}")
            for err in result['errors']:
                print(f"  - {err}")
        if result['warnings']:
            print(f"[WARN] {result['id']}")
            for warn in result['warnings']:
                print(f"  - {warn}")

    print()
    print("=" * 60)

    if args.strict and invalid_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
