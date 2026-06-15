# Gap Gate Manual SOP

Date: 2026-06-15
Owner: Audit and Enforcement Closers
Status: active

The automated GitHub Actions file write was blocked during this session. Manual fallback is active.

Run after meaningful repo changes:

```bash
python3 scripts/gap_check_2026_06_15.py
python3 scripts/ops_audit.py
```

Done condition: both checks pass, or every failure becomes a task with owner, output path and fallback.

Next action: add the GitHub Actions gate from a local editor or Codex worker when repository write restrictions allow it.
