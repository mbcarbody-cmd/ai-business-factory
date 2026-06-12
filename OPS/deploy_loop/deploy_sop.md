# Deploy Loop SOP

Owner: CTO-2 DevOps Commander

## Purpose

Every product must have a repeatable path from repo to running system, with status, smoke test, health check and rollback note.

## Required deploy fields per product

- Product name
- Environment: local / staging / production
- Repo path
- Build command
- Run command
- Deploy command
- Required env vars
- Health check URL or command
- Smoke test steps
- Rollback steps
- Last deploy status
- Owner

## Deploy status model

- not_configured
- local_only
- staging_ready
- production_ready
- deployed
- failed
- rolled_back

## Product deploy registry

| Product | Repo path | Status | Health check | Rollback | Owner |
|---|---|---|---|---|---|
| AI Agent Setup | `website/`, `products/ai-agent-setup/` | local_only | pending | pending | CTO-2 DevOps Commander |
| Parts Commerce OS | `OPS/marketplace/roadmap.md` | not_configured | pending | pending | MARKET-1 Marketplace General Manager |

## Pre-deploy checklist

1. Product stage is at least `deploy_ready` in `OPS/product_gates/product_stages.json`.
2. QA bug board has no open critical bugs.
3. Smoke test is documented.
4. Health check exists.
5. Rollback instruction exists.
6. Release note exists.

## Post-deploy checklist

1. Run health check.
2. Run smoke test.
3. Record deploy status.
4. Notify Judge if failure.
5. Create bug if smoke test fails.

## Rollback note template

- Date:
- Product:
- Failed deploy version/commit:
- Last known good version/commit:
- Rollback command/steps:
- Data migration risk:
- Owner:
- Result:
