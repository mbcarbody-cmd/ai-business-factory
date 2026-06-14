# RRR Seed UI Patch Plan

Date: 2026-06-14
Owner: Frontend Agent-C2 / UI and Cockpit Builder
Status: ready_for_build

## Goal

Feed the Parts Seller OS prototype with the RRR public seed file:

`OPS/marketplace/rrr_public_seed_samples_2026_06_14.json`

## Why

The current prototype must stop being only a static workflow explanation. It must show at least a few market seed rows with:

- part name,
- OEM/listing code,
- market price signal,
- category guess,
- listing status decision,
- floor/manual-review decision,
- source URL,
- checked_at,
- confidence.

## UI section to add

Add a section named:

`RRR public seed signals now feeding workflow`

Show 4-6 rows from the seed file:

1. Mazda 6 front ABS sensor — code-sensitive brake/electrical pricing.
2. Hyundai Terracan turbo — condition notes required before publish.
3. Hyundai i30 rear bumper lamp — side confirmation required.
4. Hyundai Santa Fe vague body part — bad title risk, block until corrected.
5. Hyundai Santa Fe crankshaft position sensor — low-margin code-driven sensor.
6. Hyundai Santa Fe ignition coil — manual review if sold as set vs single.

## Required UI columns

- Seed ID
- Brand/model/year
- Part name
- Code
- Price signal
- Category guess
- System decision
- Confidence

## Rules

- Do not present RRR seed rows as our catalog.
- Do not claim full scrape.
- Do not hide that this is public sample/provenance data.
- Every shown row must keep source_url, checked_at and confidence.
- The UI must state: `No URL = no fact. No confidence = no price decision.`

## Done proof

The task can move forward when:

- `products/parts-seller-os/index.html` shows the RRR seed section,
- the seed file path is visible in the UI,
- QA confirms the UI does not imply copied catalog ownership,
- one-seller workflow uses these rows for listing/pricing examples.

## Fallback

If direct HTML update is blocked, keep this patch plan as proof path and route the change to Cursor/Claude Code worker under task `OPS-022`.
