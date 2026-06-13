# Task Source of Truth

Owner: COO-2 Operations Controller
Status: active
Updated: 2026-06-13

`OPS/task_board.json` is the operating source of truth.

External tickets may support execution, but they must reference a task ID from the board.

## Rules

- New work starts in the task board.
- Every execution ticket must reference an `OPS-000` task ID.
- A ticket is not done until the task board proof path is updated.
- Vague work items must be renamed, merged into a board task, or archived.
- The board must contain owner, status, deadline, blocker, fallback, next action, output path, proof status and verifier.

## Proof

The valid proof file is `OPS/task_board.json`.
