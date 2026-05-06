#!/usr/bin/env python3
"""
TDD Red-Phase Verifier.

Lints a commit range to enforce the Red-Green-Refactor convention.

Convention:
    [Red]      STORY-ID: <test description>
        Adds a FAILING test. Diff must touch only test files.
        No net-new production code allowed.

    [Green]    STORY-ID: <implementation summary>
        Implements the minimum production code to make the Red test pass.
        Must be preceded by a [Red] commit for the same STORY-ID in the range.

    [Refactor] STORY-ID: <cleanup summary>
        Behavior-preserving cleanup. No new tests, no new behavior.

Exit codes:
    0  - no violations; range is clean.
    1  - one or more violations.

Default scan range: origin/main..HEAD if HEAD is ahead of origin/main, else
the most recent 50 commits. Override with --range.

Usage:
    python verify_red_phase.py
    python verify_red_phase.py --range HEAD~30..HEAD
    python verify_red_phase.py --range a1b2c3d..d4e5f6a
    python verify_red_phase.py --story-prefix "STORY-" --test-patterns "*_test.go,*_test.py"
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, List, Optional

DEFAULT_STORY_PREFIX = r"[A-Z]+-[A-Z]+-\d+-\d+"

DEFAULT_TEST_PATTERNS = [
    re.compile(r".*_test\.go$"),
    re.compile(r".*_test\.py$"),
    re.compile(r"^tests/features/.+\.feature$"),
    re.compile(r"^tests/.+\.spec\.[jt]s$"),
    re.compile(r"^tests/.+\.test\.[jt]s$"),
]


@dataclass
class Commit:
    sha: str
    subject: str
    files: List[str]
    phase: Optional[str]
    story: Optional[str]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def build_prefix_re(story_prefix: str) -> re.Pattern:
    return re.compile(
        rf"^\[(Red|Green|Refactor)\]\s+({story_prefix})\b",
        re.IGNORECASE,
    )


def is_test_file(path: str, patterns: List[re.Pattern]) -> bool:
    return any(p.match(path) for p in patterns)


def default_range() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-list", "--count", "origin/main..HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        if out and int(out) > 0:
            return "origin/main..HEAD"
    except subprocess.CalledProcessError:
        pass
    return "HEAD~50..HEAD"


def parse_commits(rng: str, prefix_re: re.Pattern) -> List[Commit]:
    log = git("log", rng, "--reverse", "--name-only", "--pretty=format:%H%x00%s%x00")
    if not log.strip():
        return []
    commits: List[Commit] = []
    records = log.split("\n\n")
    for rec in records:
        if not rec.strip():
            continue
        head, *file_lines = rec.split("\n")
        try:
            sha, subject, _ = head.split("\x00")
        except ValueError:
            continue
        files = [f for f in file_lines if f]
        m = prefix_re.match(subject)
        phase = m.group(1).capitalize() if m else None
        story = m.group(2) if m else None
        commits.append(Commit(sha=sha, subject=subject, files=files, phase=phase, story=story))
    return commits


def violations(commits: List[Commit], test_patterns: List[re.Pattern]) -> List[str]:
    errors: List[str] = []
    last_red: dict = {}
    open_red: dict = {}

    for c in commits:
        if c.phase is None:
            continue

        short = c.sha[:8]

        if c.phase == "Red":
            non_test = [f for f in c.files if not is_test_file(f, test_patterns)]
            if non_test:
                errors.append(
                    f"[{short}] [Red] {c.story}: modifies non-test files {non_test} (test files only allowed)."
                )
            last_red[c.story] = c.sha
            open_red[c.story] = c.sha

        elif c.phase == "Green":
            if c.story not in open_red:
                errors.append(
                    f"[{short}] [Green] {c.story}: no preceding [Red] commit for this story in the scan range."
                )
            else:
                del open_red[c.story]

        elif c.phase == "Refactor":
            if c.story not in last_red:
                errors.append(
                    f"[{short}] [Refactor] {c.story}: no [Red]/[Green] cycle observed for this story in the scan range."
                )

    return errors


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--range", dest="rng", default=None, help="Git commit range to scan.")
    parser.add_argument(
        "--story-prefix",
        default=DEFAULT_STORY_PREFIX,
        help="Regex for the story ID portion after [Red]/[Green]/[Refactor].",
    )
    parser.add_argument(
        "--test-patterns",
        default=None,
        help="Comma-separated glob-style patterns for test files (Python regex). Defaults to common _test.go, _test.py, .feature, .spec.ts patterns.",
    )
    args = parser.parse_args(argv)

    prefix_re = build_prefix_re(args.story_prefix)

    test_patterns = DEFAULT_TEST_PATTERNS
    if args.test_patterns:
        test_patterns = [re.compile(p.strip()) for p in args.test_patterns.split(",")]

    rng = args.rng or default_range()
    print(f"verify_red_phase: scanning {rng}", flush=True)

    commits = parse_commits(rng, prefix_re)
    if not commits:
        print("verify_red_phase: no commits in range; nothing to check.")
        return 0

    tdd_commits = [c for c in commits if c.phase]
    print(f"verify_red_phase: {len(commits)} commits ({len(tdd_commits)} TDD-tagged).")

    errs = violations(commits, test_patterns)
    if not errs:
        print("verify_red_phase: PASS")
        return 0

    print("verify_red_phase: FAIL")
    for e in errs:
        print(f" - {e}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
