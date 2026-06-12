# Production Product Lock

Purpose: prevent the project from confusing a runnable demo with a finished product.

## Product status

Current status: internal alpha skeleton.

The current runnable fullstack app proves the core workflow, but it is not the final product.

## Final product target

Parts Business OS is final only when a real business can use it daily to run used parts operations without developer help.

The product must support:

- seller onboarding
- user login
- role permissions
- donor asset creation
- part creation
- photo workflow
- warehouse locations
- worker tasks
- pricing and listing readiness
- reservation and order flow
- shipment tracking
- profitability dashboard
- audit logs
- backups
- deploy and rollback
- support handoff
- public sales/demo page

## Non-negotiable rule

Do not call this product complete because the demo runs.

Demo is proof. Product is operations.

## Production completion gates

### Gate 1: Data gate

Required:

- SQL-backed storage
- migrations
- seed data
- backup and restore procedure
- data integrity tests

Blocked while:

- core business state lives only in JSON
- no migration path exists
- backup restore is untested

### Gate 2: Access gate

Required:

- login
- session or token handling
- password reset or invite flow
- role permission matrix
- permission tests

Blocked while:

- demo user is hardcoded
- warehouse worker can access financial/admin actions

### Gate 3: Operations gate

Required:

- asset -> part -> location -> task -> reservation -> order flow
- double-sale prevention
- status transition rules
- audit logs for critical actions
- worker-friendly screens

Blocked while:

- any core state transition can happen without validation or audit

### Gate 4: QA gate

Required:

- P0/P1 automated tests
- release-blocking smoke test
- bug board
- manual test checklist
- QA critic approval

Blocked while:

- tests are documentation only
- no automated command can fail a weak release

### Gate 5: Deploy gate

Required:

- deploy script
- health endpoint
- service config
- logs
- rollback playbook
- production env checklist

Blocked while:

- product can only be run manually from local terminal

### Gate 6: Business gate

Required:

- public sales page
- pricing packages
- buyer target list
- onboarding checklist
- 72 hour delivery SOP
- support process

Blocked while:

- product cannot be sold, delivered and supported

## Agent execution rule

Every agent must treat this file as the source of truth.

When an agent says done, it must name the gate it closed and the file path that proves it.

## Next hard target

Move from internal alpha skeleton to release candidate by closing Gates 1, 2, 4 and 5 first.
