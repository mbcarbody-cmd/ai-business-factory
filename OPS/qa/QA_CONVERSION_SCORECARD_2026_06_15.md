# QA Conversion Scorecard

Updated: 2026-06-15  
Owner: PF10X-06-W01 QA Critic Captain  
Status: active

## Purpose

Product releases must pass both technical checks and money-path checks before they are called done.

## Pass rule

A product or page can move to done when the score is 80/100 or higher. If the score is lower, the Judge must record either a revise decision or an accepted exception.

## Checks

| Check | Weight | Pass condition |
|---|---:|---|
| Page loads | 10 | Main page opens without visible issue |
| Mobile layout | 10 | Content is readable on phone width |
| Primary CTA | 10 | CTA is visible near the top |
| Offer clarity | 15 | Buyer, pain, outcome and pilot offer are clear fast |
| Pricing clarity | 10 | Price or price range is visible |
| Payment path | 10 | Payment link, invoice path or explicit blocker is documented |
| Lead capture | 10 | Form, email CTA or manual contact path exists |
| Trust proof | 10 | Workflow proof, sample data or QA/CFO proof is visible |
| Links | 10 | Navigation and CTA links point to existing sections |
| Next action | 5 | Execution queue has owner and next action |

## First target

Product: Parts Seller OS paid pilot MVP shell.

Paths to check:

- `products/_templates/parts-seller-os-one-day-mvp/index.html`
- `OPS/product_factory/mvp_briefs/parts_seller_os_paid_pilot_2026_06_15.md`
- `OPS/revenue_ops/parts_seller_os_paid_pilot_outreach_2026_06_15.md`
- `OPS/cfo/parts_seller_os_paid_pilot_cfo_gate_2026_06_15.json`

Current score: pending manual review.

Next action: run scorecard after revenue and CFO files exist.
