#!/usr/bin/env python3
"""Run the repository hygiene scanner without scanning its marker definitions."""
from pathlib import Path

import check_repo_hygiene as scanner

ORIGINAL_ITER = scanner.iter_repo_files
SCANNER_DEFINITION = Path("scripts/security/check_repo_hygiene.py")


def iter_repo_files_without_definition():
    for relative, path in ORIGINAL_ITER():
        if relative == SCANNER_DEFINITION:
            continue
        yield relative, path


scanner.iter_repo_files = iter_repo_files_without_definition
raise SystemExit(scanner.main())
