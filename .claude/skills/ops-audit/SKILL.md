---
name: ops-audit
description: Validate the core OPS operating system before handoff or PR.
---

# OPS Audit Skill

Use this skill after any meaningful repo change.

## Steps

1. Read `AGENTS.md` and `CLAUDE.md`.
2. Run `python3 scripts/ops_audit.py` if it exists.
3. If the script does not exist, manually check:
   - `OPS/task_board.json`
   - `OPS/task_board_v2.json`
   - `OPS/CORE_OS_STATUS.md`
   - `OPS/qa/bug_board.json`
   - `OPS/cfo/costs.json`
   - `OPS/revenue_ops/lead_pipeline.json`
   - `OPS/marketplace/parts_os_mvp_data_model.json`
4. Report missing owners, statuses, next actions, output paths, proof status and blockers.
5. Create or update a bug-board item when audit finds a release/deploy/revenue blocker.

## Required output

- Audit result: pass/fail.
- Files checked.
- Blocking issues.
- Non-blocking issues.
- Proof path.
- Next highest-value task.

## Hard rule

Do not mark a task done when proof is missing.