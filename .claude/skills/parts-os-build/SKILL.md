---
name: parts-os-build
description: Build or improve the one-seller Parts Seller OS slice using the approved data model.
---

# Parts OS Build Skill

Use this skill only for the first one-seller MVP slice. Do not build the full marketplace yet.

## Source of truth

- `OPS/marketplace/roadmap.md`
- `OPS/marketplace/parts_os_mvp_data_model.json`
- `OPS/product_gates/product_stages.json`
- `OPS/cfo/costs.json`

## MVP slice

Build only:

1. Add part.
2. Suggest location.
3. Set price and floor price.
4. Generate listing status.
5. Reserve/order state.
6. Ageing and dead-stock signal.

## Rules

- Use sample or internal data only.
- No external marketplace publishing.
- No payment integration.
- No production database.
- No customer data.
- Update QA and product gate proof after changes.

## Required output

- Changed files.
- Test/smoke result or no-test reason.
- MVP slice status.
- Known limits.
- Next blocker.
- Proof path.