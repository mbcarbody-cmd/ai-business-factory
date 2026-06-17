# Offer Acceptance and Payment Path

Date: 2026-06-17  
Owner: SPEC-024 Commercial Closer  
Status: active

Product: Parts Seller OS paid pilot.  
Default scope: one seller workflow using the buyer's sample parts data.  
Delivery window: 72 hours after paid status, accepted scope, usable sample data and named delivery owner are all recorded.  
Price range: 300-900 EUR setup, followed by an optional monthly plan only after validation.

## Canonical state path

`draft -> review_ready -> sent -> accepted -> invoice_issued -> payment_pending -> paid -> started -> delivered -> closed`

A declined or expired offer moves to `closed_lost`. A scope change after acceptance returns the offer to `review_ready` and requires a new acceptance record.

## Acceptance evidence

Required before `accepted`:

- client company and business contact;
- accepted scope and exclusions;
- accepted price, currency and tax treatment;
- acceptance timestamp and evidence reference;
- sample-data state;
- delivery owner and target delivery date.

## Payment evidence

Required before `paid`:

- invoice or payment-request identifier;
- amount and currency matching the accepted offer;
- payment method;
- payment timestamp;
- bank, processor or accounting reference;
- verifier and verification timestamp.

Do not store card details, banking credentials or unnecessary personal data in the repository. Evidence may be a redacted accounting reference or a link to an approved private record.

## Execution gate

No real pilot may move to `started` until scope, price, usable sample data, delivery owner and verified payment are recorded. A written CEO exception may allow `started_before_paid`, but it must include the commercial reason, exposure limit and collection deadline and must never be presented as paid-pilot evidence.

## Operating fallback

Until automated checkout is implemented, use a written offer plus an ordinary invoice or approved payment request. Record all state transitions in `OPS/commercial/offer_acceptance_payment_register_2026_06_17.json`.

## Done rule

The payment path exists when the register schema is valid. The first paid pilot is complete only when one register row reaches `paid` with external evidence; a template or internal dry run is not payment proof.
