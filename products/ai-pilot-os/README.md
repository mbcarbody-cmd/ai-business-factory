# AI Pilot OS

Status: active P0 lightweight app  
Owner: CEO-C Build Factory + CEO-B Revenue  
Live path: `website/index.html`

## Why this exists

The previous P0 direction was too heavy for a first finished app. Parts Seller OS remains useful later, but it needs domain data, marketplace rules, storage logic and more validation.

AI Pilot OS is the lighter first app because it directly supports the first money path:

`lead -> offer -> quote -> payment path -> 72h delivery -> QA -> handoff -> maintenance upsell`

## What the app does now

The current static browser app supports:

- lead intake;
- lead fit scoring;
- package selection;
- quote text generation;
- payment path tracking;
- pipeline stages;
- paid pilot marking;
- 72h delivery checklist;
- handoff text;
- QA/proof score;
- JSON and CSV export;
- demo data;
- localStorage persistence.

## What it does not do yet

- It does not process real payments.
- It does not send email automatically.
- It does not use a backend database.
- It does not verify public URL automatically.

## P0 done criteria

This product is P0-done only when:

1. the static app loads from `website/index.html`;
2. demo data can be added;
3. a lead can move from intake to quote/payment/delivery;
4. QA score can produce PASS/BLOCKED;
5. export works;
6. public URL is verified or an explicit NO URL blocker is recorded;
7. at least one real or manually created lead/quote/payment path row exists.

## First revenue offer

Primary offer:

**299 EUR 72h AI Automation Pilot**

Scope:

- one intake or lead/admin workflow;
- one small automation or workflow helper;
- QA pass;
- handoff text;
- maintenance upsell.

Not included:

- complex custom software;
- long integrations without access;
- guaranteed sales results;
- unlimited revisions.
