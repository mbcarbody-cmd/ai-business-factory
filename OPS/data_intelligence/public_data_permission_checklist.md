# Public Data Permission Checklist

Date: 2026-06-13
Owner: CISO / Security Judge + CI-2 Pricing & Offer Analyst
Status: active

Use this checklist before any scripted public-page retrieval or before relying on manually captured public data in sales, CFO or product decisions.

## Required checks

1. The page is publicly accessible without login.
2. The page is not personal/private data.
3. The intended data is business-relevant and minimal.
4. A source URL and checked date will be saved.
5. The domain's public rules do not clearly prohibit this use.
6. The method is low-rate and non-disruptive.
7. No CAPTCHA, paywall, login or technical barrier is bypassed.
8. No cookies, sessions, tokens or private accounts are used.
9. Output path is listed in `OPS/data_intelligence/source_registry.json`.
10. A human can verify the result before it is used for outbound or pricing decisions.

## Decision

- `approved_manual`: manual public verification only.
- `approved_scripted_low_rate`: scripted retrieval allowed after checks are passed.
- `blocked`: do not use the source.
- `needs_human_review`: ambiguous; escalate to CISO / Security Judge.

## Output template

- Source id:
- Domain:
- Intended data:
- Decision:
- Reason:
- Checked by:
- Checked date:
- Output path:
- Notes:

## Hard stop

Do not build or run data collection code for a source marked `blocked` or `needs_human_review`.