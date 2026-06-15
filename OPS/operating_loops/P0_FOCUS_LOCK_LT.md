# P0 Focus Lock

Date: 2026-06-15  
Owner: CEO / Master Agent + COO-1 Execution Architect  
Status: ACTIVE / BLOCKING

## Purpose

Stop the system from spreading into too many unknown projects while the first lightweight app and revenue loop are not yet working.

## Current focus

The immediate P0 priority is **AI Pilot OS**, not the heavier Parts Seller OS.

Current P0 flow:

`lead -> fit score -> offer -> quote -> payment path -> 72h delivery checklist -> QA -> handoff -> maintenance upsell -> first paid pilot proof`

## Focus rules

1. No new unrelated product build starts while AI Pilot OS is not sell-ready.
2. Parts Seller OS remains parked as a later/heavier product until the lightweight app has public URL proof and payment-path proof.
3. New ideas may be captured only as backlog, not active P0 build.
4. Active build capacity goes first to:
   - AI Pilot OS static app,
   - public URL / release proof,
   - quote and payment path,
   - real lead row,
   - QA PASS/BLOCKED verdict,
   - first 72h paid pilot proof.
5. Any agent proposing a new product must state what current P0 proof it would delay.
6. A task is not progress unless it reduces distance to working app, payment path, paid pilot, deploy proof or delivery proof.

## Why this lock was updated

User corrected the direction on 2026-06-15: do not continue Parts Seller OS as the first app. Start with a lighter app first.

Parts Seller OS is still useful, but it is too heavy as the immediate app because it requires domain data, storage/location logic, marketplace rules and seller-specific workflow validation.

AI Pilot OS is lighter and closer to first revenue.

## P0 lane order

1. Keep AI Pilot OS working in `website/index.html`.
2. Run local smoke test and QA verdict.
3. Verify public URL or record NO URL blocker.
4. Enter one real lead manually.
5. Generate quote and attach payment path.
6. Collect first paid pilot or record exact blocker.
7. Deliver 72h pilot with handoff and maintenance upsell.

## Kill criteria for distractions

Reject or backlog anything that does not answer one of these questions:

- Does it help get a real lead?
- Does it help send a quote?
- Does it help attach payment path?
- Does it help deliver a 72h pilot?
- Does it help verify deploy/QA/revenue proof?

If the answer is no, it is not active P0 work.
