# Weak Work Patterns

Owner: PMO-2 Documentation & Memory Keeper
Status: active
Updated: 2026-06-13

## Pattern 1 — Plan without proof

Weak output: a strategy paragraph that does not update an OPS file, product artifact, sales record, delivery artifact, test, or deploy proof.

Required correction: create or update a tracked artifact and reference the proof path.

## Pattern 2 — Ready forever

Weak output: a task stays `ready` without deadline, blocker, fallback action, or owner movement.

Required correction: move it to `in_progress`, `blocked`, or `done`. If blocked, create an unblock task and switch to the next highest-value executable task.

## Pattern 3 — Seed rows pretending to be verified data

Weak output: seed competitors or seed leads are treated as market proof.

Required correction: mark seed data as unverified and create a public-verification task.

## Pattern 4 — Build without sell path

Weak output: new features are built before a buyer, offer, margin, delivery scope, and follow-up path exist.

Required correction: product gate and CFO review must approve the build or limit it to a narrow internal proof.

## Pattern 5 — Deploy words without health check

Weak output: a product is called deploy-ready without run command, health check, smoke test, rollback note, and owner.

Required correction: update `OPS/deploy_loop/deploy_sop.md` before release claims.

## Pattern 6 — Agent role without operating surface

Weak output: an agent has a title but no file, KPI, decision right, or proof obligation.

Required correction: assign the agent to a task board item and an OPS output path.
