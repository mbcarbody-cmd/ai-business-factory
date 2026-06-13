# Deploy Loop SOP

Owner: CTO-2 DevOps Commander
Updated: 2026-06-13

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

| Product | Repo path | Status | Run / deploy command | Health check | Rollback | Owner |
|---|---|---|---|---|---|---|
| AI Agent Setup landing | `website/` | local_only | `python3 -m http.server 4173` then open `/website/index.html` | `curl -I http://localhost:4173/website/index.html` | revert `website/` changes | CTO-2 DevOps Commander |
| CEO Cockpit Demo | `products/ceo-cockpit/` | local_only | `python3 -m http.server 4173` then open `/products/ceo-cockpit/index.html` | `curl -I http://localhost:4173/products/ceo-cockpit/index.html` | revert `products/ceo-cockpit/` changes | CTO-2 DevOps Commander |
| Parts Seller OS Prototype | `products/parts-seller-os/` | local_only | `python3 -m http.server 4173` then open `/products/parts-seller-os/index.html` | `curl -I http://localhost:4173/products/parts-seller-os/index.html` | revert `products/parts-seller-os/` changes | MARKET-2 Warehouse Autonomy Director |

## Pre-deploy checklist

1. Product stage is at least `deploy_ready` in `OPS/product_gates/product_stages.json`.
2. QA bug board has no open critical bugs.
3. Smoke test is documented.
4. Health check exists.
5. Rollback instruction exists.
6. Release note exists.
7. Security review exists for public/auth/data changes.

## Post-deploy checklist

1. Run health check.
2. Run smoke test.
3. Record deploy status.
4. Notify Judge if failure.
5. Create QA item if smoke test fails.

## CEO Cockpit local smoke test

- Start local static server from repository root.
- Open `http://localhost:4173/products/ceo-cockpit/index.html`.
- Confirm four KPI cards are visible.
- Confirm task, QA, revenue and CFO sections are visible.
- Confirm public-hosting limitation is documented.

## Parts Seller OS local smoke test

- Start local static server from repository root.
- Open `http://localhost:4173/products/parts-seller-os/index.html`.
- Confirm six workflow steps are visible.
- Confirm demo example table is visible.
- Confirm full marketplace is explicitly blocked until one-seller workflow works.

## Public deployment blocker

The cockpit and seller OS prototype have local demo paths, but public hosting is still pending. Do not claim public demo proof until hosted URLs are recorded here.

## Rollback note template

- Date:
- Product:
- Failed version/commit:
- Last known good version/commit:
- Rollback steps:
- Data migration risk:
- Owner:
- Result:
