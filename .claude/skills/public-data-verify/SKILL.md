---
name: public-data-verify
description: Verify public competitor, lead or market signal data with source proof and safety checks.
---

# Public Data Verify Skill

Use this skill when updating competitor intelligence, revenue leads or market signal files.

## Required inputs

- Target OPS task id.
- Source id from `OPS/data_intelligence/source_registry.json` or new proposed source row.
- Intended output path.

## Steps

1. Read `OPS/data_intelligence/PUBLIC_DATA_COLLECTION_PLAYBOOK.md`.
2. Read `OPS/data_intelligence/public_data_permission_checklist.md`.
3. Confirm the source is public and permitted.
4. Record source URL and checked date.
5. Mark confidence: `high`, `medium`, `low`.
6. Update the relevant OPS output file.
7. If confidence is low, do not use the data for CFO pricing or outbound decisions.

## Not allowed

- No login-gated pages.
- No cookies, sessions or tokens.
- No private personal data.
- No automated outbound messages.
- No bypassing technical barriers.

## Required output

- Source checked.
- Data captured.
- Confidence.
- Safety decision.
- Output path.
- Next action.