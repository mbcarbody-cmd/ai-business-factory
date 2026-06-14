# Auto Parts Price Check PWA

Status: working static PWA prototype
Date: 2026-06-14

## What it does

A quick sanity-check tool for used auto parts sellers.

Inputs:

- part name,
- OEM/code,
- new part price signal,
- condition,
- rarity,
- demand.

Outputs:

- price confidence,
- ask price hypothesis,
- floor price hypothesis,
- missing data,
- QA action: READY, MANUAL REVIEW or BLOCK.

## Important rule

The generated price is a hypothesis, not a final market fact. Final pricing still needs real comps/source URLs.

## Monetization

Can be used as:

- lead magnet,
- 299 EUR seller audit module,
- pricing module inside Parts Seller OS.
