#!/usr/bin/env python3
"""Basic repository hygiene scanner.

This script blocks obviously unsafe files and risky text markers.
It is intentionally simple. Use GitHub secret scanning, push protection,
CodeQL, Dependabot and a dedicated secret scanner for deeper checks.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SELF_REL_PATH = Path("scripts/security/check_repo_hygiene.py")

SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "dist",
    "build",
    "coverage",
    ".next",
    ".cache",
}

FORBIDDEN_NAMES = {
    ".env",
    ".env.local",
    ".env.production",
    ".env.development",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
}

FORBIDDEN_SUFFIXES = {
    ".pem",
    ".p12",
    ".pfx",
    ".jks",
    ".keystore",
}

RISKY_TEXT_MARKERS = [
    "BEGIN PRIVATE KEY",
    "BEGIN RSA PRIVATE KEY",
    "BEGIN OPENSSH PRIVATE KEY",
    "DATABASE_URL=",
    "PASSWORD=",
    "SECRET=",
    "TOKEN=",
    "API_KEY=",
    "DEBUG=true",
    "debug: true",
    "bypass auth",
    "disable auth",
    "skip auth",
]

ALLOWLIST_WORDS = [
    "replace_me",
    "placeholder",
    "example",
    "dummy",
    "test value",
]

TEXT_SUFFIXES = {
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".py",
    ".html",
    ".css",
    ".toml",
}


def should_scan(path: Path) -> bool:
    return path.name == ".gitignore" or path.suffix in TEXT_SUFFIXES or path.name.endswith(".env.example")


def allowlisted(line: str) -> bool:
    lower = line.lower()
    return any(word in lower for word in ALLOWLIST_WORDS)


def should_skip_risky_text_scan(rel: Path) -> bool:
    """Avoid self-scan false positives from the scanner's own marker list."""
    return rel == SELF_REL_PATH


def iter_repo_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            yield path.relative_to(ROOT), path


def main() -> int:
    findings: list[str] = []

    for rel, path in iter_repo_files():
        name = path.name.lower()

        if name in FORBIDDEN_NAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"Forbidden sensitive file: {rel}")

        if not should_scan(path) or should_skip_risky_text_scan(rel):
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            findings.append(f"Could not read {rel}: {exc}")
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if allowlisted(line):
                continue
            upper_line = line.upper()
            for marker in RISKY_TEXT_MARKERS:
                if marker.upper() in upper_line:
                    findings.append(f"Risky marker '{marker}' in {rel}:{line_no}")

    if findings:
        print("Repo hygiene scan failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Repo hygiene scan passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
