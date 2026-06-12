# Release Candidate Progress Log

Purpose: record real movement from internal alpha toward release candidate.

## 2026-06-12 progress

### RC-002 Auth and roles

Status: materially started, not closed.

Completed artifacts:

- `products/parts-business-os/auth/ROLE_PERMISSION_MATRIX.md`
- `products/parts-business-os/fullstack/src/auth/permissions.js`
- `products/parts-business-os/fullstack/scripts/permission-model-test.js`

What improved:

- role permissions are now represented in code
- permission decisions return explicit denial reasons
- tenant mismatch is modeled
- mutating and audit-required actions are marked
- automated permission model tests exist

Still missing before RC-002 can close:

- auth middleware wired into API routes
- real login/session/token handling
- tenant middleware enforced in live handlers
- permission tests against real API endpoints

### RC-005 QA automation

Status: materially started, not closed.

Completed artifacts:

- `products/parts-business-os/fullstack/scripts/smoke-test.js`
- `products/parts-business-os/fullstack/scripts/p0-api-tests.js`
- `products/parts-business-os/qa/E2E_TEST_MATRIX.md`

What improved:

- critical API flow can be tested with a command
- double reservation is tested
- sold part reservation is tested
- required field rejection is tested
- audit log presence is tested
- package scripts now expose smoke, P0 and permission tests

Still missing before RC-005 can close:

- CI runner
- API permission tests after middleware is wired
- backup/restore test
- upload/photo stress test
- VAT/pricing calculation tests

### RC-006 Deploy and rollback

Status: materially started, not closed.

Completed artifacts:

- `products/parts-business-os/fullstack/scripts/deploy-production.sh`
- `products/parts-business-os/fullstack/deploy/parts-business-os.service`
- `OPS/TECHNICAL_SPINE/DEPLOY_LOOP.md`

What improved:

- service deployment path exists
- deploy script creates app/log folders
- previous release backup is created
- systemd service is installed and restarted
- health check blocks failed deploy

Still missing before RC-006 can close:

- real VPS/server deploy test result
- rollback command automation
- production env checklist
- log rotation
- monitored uptime check

## Current CEO decision

Continue building toward release candidate.

Do not expand product count.

Next highest-impact implementation tasks:

1. Wire permission middleware into live API routes.
2. Create storage adapter boundary.
3. Move JSON direct access behind storage interface.
4. Add migration runner skeleton.
5. Add API permission tests.

## Rule

A release candidate item is not closed just because one file exists. It closes only when code, tests and operating proof exist.
