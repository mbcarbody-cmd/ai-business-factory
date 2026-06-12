# Decision Memory

Purpose: prevent agents from re-deciding the same things and wasting cycles.

## Format

- Date
- Decision
- Why
- Owner
- Linked task/output
- Review date

## Decisions

### 2026-06-12 — Core OS before product expansion

Decision: close the operating-system layers before expanding product count.

Why: the audit showed the missing layer is the operating loop: research -> decide -> task -> build -> review -> deploy -> sell -> learn.

Owner: CEO / Master Agent + COO-1 Execution Architect

Linked output: `OPS/CORE_OS_STATUS.md`, `OPS/task_board.json`

Review date: next weekly OPS review

### 2026-06-12 — File-backed work only

Decision: agent work must create or update a repo file, URL, product artifact, test result, sales path or delivery proof.

Why: generic strategy documents do not create autonomous execution.

Owner: JUDGE-1 Release Gate Judge

Linked output: `OPS/product_gates/release_checklist.md`

Review date: every release gate
