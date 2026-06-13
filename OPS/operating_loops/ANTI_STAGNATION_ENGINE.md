# Anti-Stagnation Engine

Owner: COO-3 Bottleneck Breaker
Status: active
Updated: 2026-06-13

## Prime directive

The system must never sit idle in one place. If one path is blocked, the responsible agent must immediately record the blocker, create or select an unblock action, and switch to the next highest-value executable task.

## Mandatory loop

Run this loop at the start and end of every work cycle:

1. Scan `OPS/task_board.json`.
2. Find open P0 tasks with missing proof.
3. Pick the highest-value task that can be advanced now.
4. Execute the smallest useful proof-producing action.
5. Update the output path.
6. If blocked, write the blocker and fallback task.
7. Move to the next executable task instead of waiting.
8. Add a memory entry when a lesson or decision changes future behavior.

## Priority order

1. Revenue movement.
2. Deploy/demo proof.
3. QA blocker removal.
4. Delivery readiness.
5. CFO margin/cost visibility.
6. Marketplace one-seller workflow.
7. Competitor verification.
8. Documentation only when it controls execution.

## Required task fields

Every task must contain:

- `id`
- `title`
- `layer`
- `owner`
- `status`
- `priority`
- `deadline`
- `money_path_or_strategic_reason`
- `next_role`
- `next_action`
- `blocker`
- `fallback_next_task`
- `output_path`
- `done_proof`
- `proof_status`
- `proof_verified_by`

## Blocker rule

A blocked task is valid only when it has:

- a clear blocker,
- an unblock action,
- a fallback task that can move now,
- an owner,
- a review date.

## Invalid states

- `ready` without deadline.
- `blocked` without fallback.
- `done` without proof path.
- `done` with `proof_status: missing`.
- `in_progress` without next action.
- Strategy output without a tracked artifact.

## Daily scorecard

Track:

- P0 tasks advanced.
- Blockers removed.
- New blockers created.
- Proof paths updated.
- Revenue items moved.
- Deploy/QA checks completed.
- Memory entries added.

## CEO override

CEO can change priorities, but cannot waive proof. If proof is impossible, the task must state why and move to the next best executable path.
