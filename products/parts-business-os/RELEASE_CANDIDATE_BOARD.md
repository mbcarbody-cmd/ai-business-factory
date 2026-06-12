# Release Candidate Board

Purpose: convert Parts Business OS from internal alpha into a production candidate.

## Current stage

Stage: internal alpha skeleton

Reason:

- core workflow exists
- smoke test exists
- health endpoint exists
- deploy standard exists
- production gates are now defined

Still blocked from release candidate because:

- storage is JSON-backed
- auth is not implemented
- roles are not enforced in code
- migrations are not implemented
- backup and restore are not tested
- deploy script exists but is not proven on server
- public sales page is not connected to real onboarding

## Release candidate definition

The product becomes release candidate when these tracks are closed with file proof.

### RC-001 SQL-backed storage

Owner: Database Engineer + Backend Engineer
Status: open
Required proof:

- migration runner
- SQL store adapter
- storage tests
- backup command
- restore command

### RC-002 Auth and roles

Owner: Backend Engineer + Security Reviewer
Status: open
Required proof:

- auth middleware
- tenant middleware
- role middleware
- permission tests

### RC-003 Operational workflow hardening

Owner: Product Architect + Full Stack Builder
Status: open
Required proof:

- part status transitions
- reservation conflict checks
- order state machine
- audit log coverage

### RC-004 Warehouse engine v1

Owner: Warehouse Math Agent
Status: open
Required proof:

- capacity recommendation rules
- full/blocked location handling
- unlocated parts queue
- override approval rule

### RC-005 QA automation

Owner: QA Automation Engineer
Status: open
Required proof:

- automated smoke test
- automated P0 API tests
- permission tests
- double-reservation test

### RC-006 Deploy and rollback

Owner: DevOps Engineer + SRE Agent
Status: open
Required proof:

- deploy script
- systemd service
- health check
- log path
- rollback procedure
- server deploy test result

### RC-007 Website and sales readiness

Owner: Sales Operator + Website Design Agent
Status: open
Required proof:

- public page
- pricing package
- target buyer list
- lead capture
- onboarding promise

## RC blocked rule

No agent may mark release candidate complete while any RC item is open.

## Daily execution rule

Every build cycle must close or reduce one RC item.

Acceptable outputs:

- code file
- test file
- migration
- deploy artifact
- UI screen
- sales page
- QA bug closure

Unacceptable outputs:

- idea only
- generic analysis
- duplicated documentation
- work with no next action

## CEO instruction

Do not expand to new products until RC-001, RC-002, RC-005 and RC-006 are materially closed.
