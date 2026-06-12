# Deploy Loop

Purpose: make every approved product change deployable, observable and reversible.

## Core rule

No product is release-ready without a deploy path, health check and rollback note.

## Required flow

```text
commit -> build -> test -> deploy -> health check -> smoke test -> release note -> monitor -> rollback if needed
```

## DevOps owner

Owner agent: DevOps Engineer
Support agents:

- SRE / Observability Agent
- QA Automation Engineer
- Security Reviewer
- Product Architect

## Minimum deploy package

Every deployable app must include:

- run command
- build command
- environment variables list
- database migration command
- backup step before migration
- health endpoint
- log location
- rollback command or manual rollback note
- smoke test checklist

## Health endpoint standard

A health endpoint must check:

- app process is alive
- database connection works
- required environment variables are present
- writable upload/storage path exists when file upload is used
- latest migration version is compatible

Health states:

- ok
- degraded
- failed

## Smoke test after deploy

Minimum smoke tests:

1. login page opens
2. admin dashboard opens
3. seller dashboard opens
4. donor asset can be viewed
5. part creation screen opens
6. location queue opens
7. order/reservation screen opens
8. API health returns ok
9. logs contain no startup error

## Rollback triggers

Rollback is required when:

- health endpoint fails
- login fails
- database migration breaks critical flow
- reservation/order flow breaks
- price/VAT calculation breaks
- uploaded files become inaccessible
- P0 security issue appears

## Release note format

Each release note must include:

- date
- commit or version
- changed paths
- features shipped
- tests passed
- known risks
- rollback path
- next task

## Current gap

The repo has strong product requirements, but deploy must become executable. Next build step is to add the actual product-specific run/deploy scripts inside the active product folder.
