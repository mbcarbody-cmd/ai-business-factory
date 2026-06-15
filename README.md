# AI Business Factory

Execution workspace for building autonomous internet businesses. The current priority is a lightweight finished app that can be shown, used, and sold fast.

## Current P0 product

**Content Hook Factory**

A static browser mini-app that turns one product/service brief into a sellable content sprint package:

- product brief intake;
- audience, pain, dream outcome and CTA fields;
- brief quality score;
- 12 hooks;
- 6 posts;
- 3 short video scripts;
- landing hero block;
- outreach / DM text;
- QA score;
- Markdown and JSON export;
- demo data;
- localStorage persistence.

## Live prototype

The public static prototype is served from `website/index.html` by GitHub Pages.

Expected project URL:

```text
https://mbcarbody-cmd.github.io/ai-business-factory/
```

Direct static path:

```text
https://mbcarbody-cmd.github.io/ai-business-factory/website/index.html
```

## Why this pivot happened

AI Pilot OS was rejected by the user as too weak. Parts Seller OS is also parked as too heavy for the first fast app.

Content Hook Factory is lighter because it can be used immediately for content examples, outreach, social posts, landing copy and a 199-399 EUR sprint offer.

## Repo structure

```text
website/                         Live static prototype for Content Hook Factory
products/content-hook-factory/    Current lightweight P0 product brief
OPS/product_gates/                Product stage gates
OPS/competitor_intelligence/      Content samples and pattern capture
OPS/qa/                           QA verdicts and scorecards
OPS/deploy_loop/                  Release checks
scripts/                          OPS audit and validation tools
```

## First execution target

1. Verify the static Content Hook Factory app from `website/index.html`.
2. Use demo data and generate a content pack.
3. Export Markdown and JSON.
4. Convert one user-provided social sample into hooks and content angles.
5. Package the output as a 199-399 EUR content sprint offer.
6. Move to first paid content sprint proof.
