# Public Data Collection Playbook

Date: 2026-06-13
Owner: CI-1 Market Spy Chief + CISO / Security Judge
Status: active
Purpose: collect public competitor, pricing, lead and marketplace signals without risking accounts, legal exposure, customer trust or weak unverifiable data.

## Prime rule

Public data collection is allowed only when it is lawful, respectful and useful for a tracked OPS task.

No collection is counted as work unless it updates one of these artifacts:

- `OPS/data_intelligence/source_registry.json`
- `OPS/data_intelligence/scrape_queue.json`
- `OPS/competitor_intelligence/competitors.json`
- `OPS/revenue_ops/lead_pipeline.json`
- `OPS/marketplace/parts_os_mvp_data_model.json`
- `OPS/qa/bug_board.json`

## Allowed sources

Allowed:

- public pricing pages,
- public company websites,
- public marketplace search/result pages that do not require login,
- official docs/help pages,
- public business directories where automated access is permitted,
- our own inventory/export files,
- manually collected public observations.

Not allowed:

- login-gated scraping without API or explicit permission,
- bypassing CAPTCHAs, anti-bot systems or rate limits,
- using stolen cookies/tokens/sessions,
- collecting private personal data beyond normal B2B contact details,
- scraping pages that clearly forbid automated access in robots/terms,
- sending outbound messages automatically without human-approved campaign rules.

## Collection method ladder

Use the lowest-risk method first:

1. Official API or export.
2. Public page manual verification.
3. Respectful scraper with robots/terms check, rate limit and source URL.
4. Human review for ambiguous sites.
5. Do not collect if legality or account risk is unclear.

## Required record fields

Every source row must include:

- source id,
- source type,
- URL/domain,
- intended data,
- allowed method,
- robots/terms status,
- rate limit,
- owner,
- last checked date,
- output path,
- risk level,
- next action.

## Rate and quality rules

- Default max rate: 1 request per 10 seconds per domain unless official docs allow more.
- Always store source URL and checked date.
- Price data must include currency and whether VAT is included if visible.
- Lead data must include exact public source and contact channel.
- If a field is guessed, mark confidence `low` and do not use it in CFO or outbound decisions.

## Immediate priorities

1. Verify public pricing/CTA for the top 20 competitors.
2. Replace seed revenue targets with exact public B2B leads.
3. Build Parts Seller OS test data from public marketplace examples and our own inventory.
4. Feed collected findings into product gates and CFO logic.

## Done definition

This layer is done only when scraped or manually collected public data moves a task from seed/theory to verified action with proof path.