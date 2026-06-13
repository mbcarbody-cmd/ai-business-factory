# P0 Revenue War-Room Sprint

Date: 2026-06-13  
Owner: CEO / Master Agent  
Mode: execution over planning

## Mission

Turn the operating system from a file-backed framework into a money-producing machine.

The sprint is not complete because files exist. It is complete only when the system produces movement in at least one of these forms:

- target account enriched,
- message sent,
- reply logged,
- demo booked,
- proposal sent,
- invoice sent,
- paid pilot won,
- demo deployed,
- QA blocker fixed.

## Active offer

**299 EUR 72h AI Automation Pilot**

Promise: one narrow but useful automation or workflow improvement, delivered with intake, scope lock, QA note and handoff.

Do not sell vague AI. Sell one concrete outcome.

## P0 scoreboard

| Metric | Target | Current source |
|---|---:|---|
| Target accounts seeded | 30 | `OPS/revenue_ops/lead_pipeline.json` |
| Exact contacts found | 30 | `OPS/revenue_ops/lead_pipeline.json` |
| First messages sent | 20 | `OPS/revenue_ops/lead_pipeline.json` |
| Positive replies | 3 | `OPS/revenue_ops/lead_pipeline.json` |
| Demo booked | 1 | `OPS/revenue_ops/lead_pipeline.json` |
| Paid pilot | 1 | `OPS/revenue_ops/lead_pipeline.json` |
| First MRR upsell | 99 EUR | `OPS/cfo/costs.json` |

## Work allocation

### CRO-1 Pipeline Commander

Move seed targets into real contact rows. No research without next action.

Output: `OPS/revenue_ops/lead_pipeline.json`

### CRO-2 Outbound Conversion Director

Use the message pack. Send or prepare first outreach. Every message must have a follow-up date.

Output: `OPS/revenue_ops/outreach_messages_lt.md`

### CTO-1 Product Factory Architect

Build CEO Cockpit Demo first. It must show task board, leads, CFO costs and QA blockers.

Output: `products/ceo-cockpit/`

### JUDGE-1 Release Gate Judge

Block overbuilding. Any task that does not help lead, demo, invoice, deploy or delivery must be downgraded.

Output: `OPS/product_gates/product_stages.json`

### CFO / Pricing Controller

Keep 299 EUR pilot profitable. Anything outside pilot scope is custom-priced or rejected.

Output: `OPS/cfo/costs.json`

### MARKET-1 Marketplace General Manager

Do not build full marketplace yet. Build seller OS slice: add part -> suggest location -> price/floor -> listing status -> reservation/order state.

Output: `OPS/marketplace/parts_os_mvp_data_model.json`

## Hard rules

1. No new idea without task board row.
2. No product build without product gate.
3. No outreach without lead row.
4. No proposal without CFO margin check.
5. No deploy without QA, smoke test and rollback note.
6. No full marketplace until internal seller OS workflow proves value.
7. Ready status cannot sit more than 48h.

## Immediate execution order

1. Enrich 30 target accounts.
2. Send first 20 messages.
3. Build CEO cockpit local demo.
4. Verify 20 competitor rows.
5. Run one internal 72h delivery dry-run.
6. Convert dry-run into case study and outreach proof.

## Done proof

Sprint is done only when at least one of the following exists:

- one paid pilot,
- one deployed demo with health check,
- one completed dry-run with handoff and QA,
- one proposal/invoice sent with CFO margin proof.
