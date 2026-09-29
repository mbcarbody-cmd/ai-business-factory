#!/usr/bin/env python3
"""Fail CI on dangerous GitHub Actions security patterns."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT / ".github" / "workflows"
errors = []

sha_use = re.compile(r"^\s*uses:\s*[^\s@]+@([0-9a-fA-F]{40})(?:\s+#.*)?$", re.M)
any_use = re.compile(r"^\s*uses:\s*([^\s]+)\s*$", re.M)

for path in sorted(WF.glob("*.y*ml")):
    text = path.read_text(encoding="utf-8")
    # A PR-triggered workflow must never receive repository write permission.
    if re.search(r"(?m)^\s*pull_request\s*:", text) and re.search(r"(?m)^\s*contents\s*:\s*write\s*$", text):
        errors.append(f"{path}: pull_request workflow has contents: write")
    if re.search(r"(?m)^\s*pull_request_target\s*:", text):
        errors.append(f"{path}: pull_request_target is forbidden")
    # Third-party actions must be immutable. Local ./ actions are exempt.
    for match in any_use.finditer(text):
        use = match.group(1)
        if use.startswith("./"):
            continue
        if not re.search(r"@[0-9a-fA-F]{40}(?:\s+#.*)?$", use):
            errors.append(f"{path}: mutable action ref: {use}")
    # Never interpolate common untrusted event fields directly inside run blocks.
    for needle in ("github.event.pull_request.title", "github.event.pull_request.body", "github.event.issue.title", "github.event.issue.body", "github.event.comment.body"):
        if "${{ " + needle + " }}" in text:
            errors.append(f"{path}: untrusted event data interpolated directly: {needle}")

if errors:
    print("SECURITY POLICY FAIL")
    for error in errors:
        print("-", error)
    raise SystemExit(1)
print("PASS workflow security policy")
