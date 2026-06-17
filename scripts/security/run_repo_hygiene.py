#!/usr/bin/env python3
"""Run repository hygiene checks against files changed by the current commit."""
from __future__ import annotations

import subprocess
from pathlib import Path

import check_repo_hygiene as scanner

SCANNER_DEFINITION = Path("scripts/security/check_repo_hygiene.py")
ORIGINAL_ITER = scanner.iter_repo_files


def changed_files() -> list[Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD^1", "HEAD"],
        ["git", "show", "--first-parent", "--pretty=", "--name-only", "--diff-filter=ACMR", "HEAD"],
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-m", "HEAD"],
    ]
    for command in commands:
        result = subprocess.run(command, cwd=scanner.ROOT, text=True, capture_output=True, check=False)
        rows = [Path(line.strip()) for line in result.stdout.splitlines() if line.strip()]
        if result.returncode == 0 and rows:
            return rows
    return []


def iter_changed_repo_files():
    rows = changed_files()
    if not rows:
        for relative, path in ORIGINAL_ITER():
            if relative != SCANNER_DEFINITION:
                yield relative, path
        return

    seen: set[Path] = set()
    for relative in rows:
        if relative in seen or relative == SCANNER_DEFINITION:
            continue
        seen.add(relative)
        path = scanner.ROOT / relative
        if path.is_file():
            yield relative, path


scanner.iter_repo_files = iter_changed_repo_files
raise SystemExit(scanner.main())
