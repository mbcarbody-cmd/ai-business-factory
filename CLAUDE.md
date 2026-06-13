# Claude Code Instructions for AI Business Factory

This repo is an execution operating system, not a note dump.

## Load order

Before making changes, read:

1. `AGENTS.md`
2. `OPS/task_board.json`
3. `OPS/task_board_v2.json` if the task requires anti-stagnation fields
4. The relevant OPS layer file
5. `OPS/security/AI_AGENT_SECURITY_POLICY_LT.md`
6. `OPS/model_council/CLAUDE_CODE_EXECUTION_PLAYBOOK_LT.md`

## Prime rule

No work is done unless it updates a tracked proof artifact.

Valid proof artifacts include:

- task board row,
- memory entry,
- product gate,
- QA bug/checklist,
- deploy health/smoke note,
- revenue pipeline row,
- CFO margin/cost row,
- delivery artifact,
- marketplace workflow/data model,
- security review note.

## Operating loop

Use this loop every session:

1. Find the highest-value P0 task that can be moved now.
2. Confirm owner, output path and done proof.
3. Make the smallest useful change.
4. Run or document test/no-test reason.
5. Update proof path.
6. If blocked, record blocker and fallback task.
7. Do not wait idle.

## Permissions and safety

Never:

- read `.env`, secrets, credentials or private keys,
- push directly to main unless explicitly instructed by the human owner,
- delete data, backups or environment files,
- change production, payment, auth or customer-impacting logic without approval,
- use private customer data in prompts, tests or screenshots,
- access login-gated external pages without explicit permission and policy review.

Prefer:

- feature branches,
- small PR-ready changes,
- local tests,
- smoke tests,
- clear rollback notes,
- `scripts/ops_audit.py` before handoff.

## Output style for every completed task

Return:

- task ID,
- changed files,
- tests run or no-test reason,
- security note,
- risk/rollback note,
- proof path,
- next highest-value task.

## Strong instruction

Act like an owner. Protect revenue, margin, trust, code quality, security and system memory.