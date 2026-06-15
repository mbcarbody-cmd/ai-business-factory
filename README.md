# AI Business Factory

Execution workspace for building autonomous internet businesses. The current priority is a lightweight finished app before heavier domain products.

## Current P0 product

**AI Pilot OS**

A small static browser app for selling and delivering the first 72h AI pilot:

- lead intake;
- lead fit scoring;
- package selection;
- quote generation;
- payment path tracking;
- pipeline stages;
- paid pilot marking;
- 72h delivery checklist;
- QA/proof score;
- handoff text;
- maintenance upsell;
- JSON/CSV export;
- demo data;
- localStorage persistence.

## Live prototype

The public static prototype is served from `website/index.html` by GitHub Pages.

Expected project URL:

```text
https://mbcarbody-cmd.github.io/ai-business-factory/
```

The prototype currently stores data in browser `localStorage`. This is enough to validate the workflow and UI, but it is not yet a production database-backed system.

## Important pivot note

Parts Seller OS is not deleted, but it is no longer the immediate P0 app. It is parked until the lightweight AI Pilot OS reaches a stronger sell-ready/revenue-proof state.

Reason: Parts Seller OS is heavier and depends on domain-specific data, marketplace logic, storage/location rules, and seller workflow validation. AI Pilot OS is simpler and closer to first revenue.

## Repo structure

```text
website/                         Live static prototype for AI Pilot OS
products/ai-pilot-os/             Current lightweight P0 product brief
products/parts-seller-os/         Parked heavier domain product notes
OPS/product_gates/                Product stage gates
OPS/revenue_ops/                  Revenue and pilot pipeline
OPS/delivery/                     72h delivery playbook
OPS/qa/                           QA verdicts and scorecards
OPS/deploy_loop/                  Release checks
scripts/                          OPS audit and validation tools
```

## First execution target

1. Verify the static AI Pilot OS app from `website/index.html`.
2. Use demo data and run the full app flow: lead -> quote -> payment path -> delivery checklist -> QA.
3. Enter one real lead manually.
4. Attach quote/payment path proof.
5. Verify or record public URL status.
6. Move to first paid pilot proof.
