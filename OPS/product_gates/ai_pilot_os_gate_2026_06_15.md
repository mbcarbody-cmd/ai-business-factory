# AI Pilot OS Product Gate

Date: 2026-06-15  
Owner: JUDGE-1 Release Gate Judge  
Status: active / lightweight P0

## Decision

AI Pilot OS becomes the current lightweight P0 app.

Parts Seller OS is not deleted, but it is moved out of immediate P0 execution because it is heavier and depends on domain-specific data, storage logic, marketplace integration and seller workflow proof.

## Why this gate exists

The first app must be finished enough to demonstrate a revenue path faster than a domain-heavy marketplace/parts system.

AI Pilot OS is allowed because it directly supports:

- lead capture;
- offer packaging;
- quote generation;
- payment path tracking;
- 72h delivery checklist;
- QA proof;
- handoff and maintenance upsell.

## Gate constraints

- Do not expand into generic agency website only.
- Do not claim payment processing exists; only payment path tracking exists.
- Do not claim email automation exists; outreach remains manual until API integration exists.
- Do not mark revenue complete without a real lead/quote/payment row.
- Do not return Parts Seller OS to P0 until this lightweight app has public URL proof and at least one payment-path proof row.

## Current proof

- Static app updated at `website/index.html`.
- Product brief created at `products/ai-pilot-os/README.md`.

## Next gate

AI Pilot OS can move from `lightweight_p0` to `sell_ready` only when:

1. QA scorecard verdict is recorded;
2. release/public URL proof is recorded;
3. at least one quote/payment path row exists;
4. README points to the correct current product;
5. Product Factory enforcement checks include the new app.
