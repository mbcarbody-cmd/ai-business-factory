# Parts Seller OS Prototype

Owner: MARKET-2 Warehouse Autonomy Director
Status: local prototype draft
Updated: 2026-06-13

## Purpose

Turn the marketplace roadmap into a one-seller operating workflow before building a full marketplace.

## First workflow

`add_part -> suggest_location -> set_price_and_floor -> generate_listing_status -> reserve_or_order -> ageing_dead_stock_signal`

## Run locally

From repository root:

```bash
python3 -m http.server 4173
```

Open:

```text
http://localhost:4173/products/parts-seller-os/index.html
```

## Current limitation

This is a static prototype. It proves the workflow and UI direction, not yet live database logic.

## Next build step

Create a data-backed prototype using `OPS/marketplace/parts_os_mvp_data_model.json` as the build contract.
