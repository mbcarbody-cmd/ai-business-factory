# AI Pilot OS Release Check

Date: 2026-06-15  
Owner: DevOps Agent-C4  
Status: active

## Product

AI Pilot OS lightweight static app.

## Local check

Path:

- `website/index.html`

Required local smoke test:

1. Open `website/index.html`.
2. Press `Užkrauti demo`.
3. Confirm KPI cards update.
4. Open Pipeline tab and confirm demo rows exist.
5. Open Quote tab and confirm quote text is generated.
6. Save payment detail and confirm status becomes payment-ready.
7. Open Delivery tab and tick checklist items.
8. Open QA tab and confirm QA PASS/BLOCKED score renders.
9. Export JSON or CSV and confirm output is shown.

## Public URL check

Expected GitHub Pages URL:

```text
https://mbcarbody-cmd.github.io/ai-business-factory/
```

Public release can be claimed only when:

- URL opens;
- hero and CTA are visible;
- demo data can be loaded;
- tabs work;
- quote text generates;
- QA score renders;
- no critical console/runtime error is visible during basic use.

## Current deploy verdict

Local static app exists. Public URL still needs independent verification.

## Rollback

Rollback to previous commit if:

- app does not load;
- tabs do not work;
- demo data breaks;
- localStorage JS errors block use;
- mobile layout is unusable.
