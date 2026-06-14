# AI Business Factory

Execution workspace for building autonomous internet businesses. The current priority is no longer a generic AI agent offer.

## Current product

**Parts Seller OS**

A one-seller operating system for used auto parts commerce:

- part intake from OEM code, vehicle, condition and notes
- automatic category and storage profile suggestion
- used-part pricing suggestion with floor price, confidence and manual-review triggers
- warehouse location suggestion and pending-location fallback
- listing readiness status: needs category, needs photo, needs price, manual review, ready to publish, reserved, sold
- marketplace export feed for RRR/Ovoko, Allegro/eBay-style listings and CSV
- order/reservation state so sold parts do not stay active by mistake
- CFO view: purchase cost, asking price, floor price and gross margin signal

## Live prototype

The public static prototype is served from `website/index.html` by GitHub Pages.

Expected project URL:

```text
https://mbcarbody-cmd.github.io/ai-business-factory/
```

The prototype currently stores data in browser `localStorage`. This is enough to validate the workflow and UI, but it is not yet a production database-backed system.

## Repo structure

```text
website/                         Live static prototype
products/parts-seller-os/         Product build contract and MVP notes
OPS/marketplace/                  Category, pricing, location, listing and fitment rules
OPS/task_board_v2.json            Proof-based task board
OPS/product_gates/                Product stage gates
OPS/revenue_ops/                  Revenue and pilot pipeline
scripts/                          OPS audit and validation tools
```

## First execution target

1. Make the one-seller Parts Seller OS prototype useful with real used-part workflow.
2. Add 20-50 real/synthetic parts and test pricing/location/listing logic.
3. Connect persistent storage.
4. Add import/export flows for marketplace channels.
5. Add photo intake and Recar/RRR/eBay pipeline decisions.
6. Move from local prototype to a paid pilot or internal working tool.
