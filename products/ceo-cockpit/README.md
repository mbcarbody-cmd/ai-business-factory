# CEO Cockpit Demo

Owner: CTO-1 Product Factory Architect
Status: local demo ready
Updated: 2026-06-13

## Purpose

Make the operating system visible. The cockpit shows task status, blockers, QA bugs, revenue pipeline, CFO economics and next actions.

## Run locally

From repository root:

```bash
python3 -m http.server 4173
```

Then open:

```text
http://localhost:4173/products/ceo-cockpit/index.html
```

## Smoke test

1. Page opens without console-breaking errors.
2. Four KPI cards are visible.
3. Task board table renders.
4. QA bug list renders.
5. Revenue and CFO summary render.
6. If JSON fetch fails, fallback demo data is shown with a warning.

## Health check

```bash
python3 -m http.server 4173
curl -I http://localhost:4173/products/ceo-cockpit/index.html
```

Expected: HTTP 200.

## Rollback

Revert changes under:

- `products/ceo-cockpit/`
- `OPS/deploy_loop/deploy_sop.md`
- `OPS/qa/bug_board.json`
- `OPS/task_board.json`

## Current limitation

This is a local static demo. Public hosting is still pending and must be added before public sales proof claims.
