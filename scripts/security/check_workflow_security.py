#!/usr/bin/env python3
"""Block critical Actions risks; report legacy mutable action refs until migrated."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
WF = ROOT / ".github" / "workflows"
errors, warnings = [], []
any_use = re.compile(r"^\s*uses:\s*([^\s]+)\s*$", re.M)

for path in sorted(WF.glob("*.y*ml")):
    text = path.read_text(encoding="utf-8")
    if re.search(r"(?m)^\s*pull_request\s*:", text) and re.search(r"(?m)^\s*contents\s*:\s*write\s*$", text):
        errors.append(f"{path}: pull_request workflow has contents: write")
    if re.search(r"(?m)^\s*pull_request_target\s*:", text):
        errors.append(f"{path}: pull_request_target is forbidden")
    for match in any_use.finditer(text):
        use = match.group(1)
        if use.startswith("./"):
            continue
        if not re.search(r"@[0-9a-fA-F]{40}(?:\s+#.*)?$", use):
            warnings.append(f"{path}: mutable action ref: {use}")
    for needle in ("github.event.pull_request.title", "github.event.pull_request.body", "github.event.issue.title", "github.event.issue.body", "github.event.comment.body"):
        if "${{ " + needle + " }}" in text:
            errors.append(f"{path}: untrusted event data interpolated directly: {needle}")

for warning in warnings:
    print("WARNING", warning)
if errors:
    print("SECURITY POLICY FAIL")
    for error in errors:
        print("-", error)
    raise SystemExit(1)
print(f"PASS critical workflow policy; legacy mutable refs remaining: {len(warnings)}")
