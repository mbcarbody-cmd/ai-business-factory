# Content Hook Factory Product Gate

Date: 2026-06-15
Owner: JUDGE-1 Release Gate Judge
Status: active / lightweight P0

## Decision

Content Hook Factory becomes the current lightweight P0 app.

AI Pilot OS is parked. Parts Seller OS remains parked as a heavier domain product.

## Why this gate exists

The user rejected the previous app and requested the next idea/app. The new P0 must create a visible output immediately and connect to the content-intelligence direction.

Content Hook Factory is allowed because it directly supports:

- hook generation;
- social post generation;
- short video script generation;
- landing hero generation;
- outreach DM generation;
- content sprint packaging;
- Markdown/JSON export;
- a 199-399 EUR sprint offer.

## Gate constraints

- Do not claim the app uses a real LLM/API; it is a static template-based MVP.
- Do not claim guaranteed results from content.
- Do not copy user-provided social samples; extract only reusable mechanics.
- Do not return parked apps to P0 unless user explicitly asks.

## Current proof

- Static app updated at `website/index.html`.
- Root `index.html` points to the new app.
- Product brief created at `products/content-hook-factory/README.md`.
- P0 Focus Lock updated.

## Next gate

Content Hook Factory can move from `lightweight_p0` to `sell_ready` only when:

1. QA verdict is recorded;
2. release/public URL proof is recorded;
3. one real content sample is converted into assets;
4. one 199-399 EUR offer page/copy block is produced;
5. enforcement checks include the new app.
