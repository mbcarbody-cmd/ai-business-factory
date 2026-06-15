# Parts Seller OS Local Runbook

Date: 2026-06-15
Owner: Build Orchestrator
Status: active

## Open local prototype

Open:

`products/parts-seller-os/index.html`

Click:

`Run local workflow proof`

Expected result:

Two sample items produce category, location, value, floor, listing state, export row and reserve state.

## Run logic test

From repo root:

```bash
node products/parts-seller-os/workflow_engine.test.js
```

Expected output:

`Parts Seller OS workflow engine test PASS`

## Done rule

The local prototype is not considered stronger than sample proof until real seller sample data is added.
