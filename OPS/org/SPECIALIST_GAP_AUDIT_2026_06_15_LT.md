# Specialist Gap Audit — Execution Chain

Date: 2026-06-15
Owner: CEO / Master Agent + COO-1 Execution Architect
Status: active
Purpose: identify which missing specialist brains are causing projects to stall between strategy, repo artifacts, deploy, revenue, delivery and paid proof.

## Diagnosis

The system no longer mainly lacks more agents. It lacks several hard-owner specialists who close reality loops.

Current pattern:

1. Strategy exists.
2. Agent rosters exist.
3. Task boards exist.
4. MVP briefs, QA packs, CFO gates and outreach packs exist.
5. But the value chain still stalls before public URL, verified lead rows, payment path, paid pilot, real delivery and user feedback.

This means the missing brain is not "more management". The missing brain is execution-specialist ownership with authority to turn files into working proof.

## Bottleneck chain

Idea -> Product decision -> MVP scope -> Build -> Public deploy -> QA -> Offer -> Verified leads -> Outreach -> Quote/payment -> Paid pilot -> Delivery -> Feedback -> Improve/stop

Current weak links:

- Build to public deploy.
- Outreach pack to verified real leads.
- Offer to quote/payment path.
- Prototype to real pilot workflow.
- QA checklist to actual break-test on live demo.
- Delivery playbook to first client result.
- Marketplace foundations to one-seller working product.

## Missing or underpowered specialist brains

### 1. Revenue Lead Verification Specialist

Mission: replace generic target ideas with exact public company rows.

Why needed: Revenue Ops is blocked when lead rows are not verified.

Owns:

- company name;
- country;
- website/profile;
- source URL;
- contact channel;
- fit reason;
- status;
- duplicate check;
- outreach permission note.

Required output: `OPS/revenue_ops/lead_pipeline.json`

Done proof: at least 50 verified target rows for one active MVP, starting with 10 strongest rows.

### 2. Payment / Quote Operations Specialist

Mission: make every offer payable before outreach is counted.

Why needed: a paid pilot cannot happen if the system has no quote, invoice draft, payment link or bank payment instruction.

Owns:

- Stripe / PayPal / Revolut Business / manual bank payment option;
- invoice draft template;
- written quote template;
- payment status field;
- paid-pilot handoff trigger.

Required output: `OPS/revenue_ops/payment_path.md` and linked rows in `OPS/revenue_ops/lead_pipeline.json`

Done proof: every quote_sent lead has a payable path.

### 3. Public Demo Publisher / Release Engineer

Mission: convert local files into public testable demos with health checks and rollback.

Why needed: a local product is not a sales asset until a buyer can open it.

Owns:

- public URL;
- preview deployment;
- smoke test;
- uptime/health check;
- rollback note;
- release notes.

Required output: `OPS/deploy_loop/public_demo_registry.json`

Done proof: each active MVP has public_url or explicit NO_URL blocker with fallback.

### 4. Product Workflow Architect for Parts Seller OS

Mission: connect category, fitment, location, pricing, listing and reservation rules into one usable seller workflow.

Why needed: marketplace foundations exist, but they must become a working one-seller operating flow.

Owns:

- add part flow;
- category suggestion;
- storage profile and location logic;
- price/floor/confidence calculation;
- listing readiness status;
- export row;
- reserve/sold state;
- exception queue.

Required output: `products/parts-seller-os/WORKFLOW_SPEC.md`

Done proof: one-seller prototype can add, suggest, price, locate, list, reserve and age parts from sample data.

### 5. UX / Conversion Designer

Mission: make demos and pages look trustworthy enough to convert.

Why needed: product pages can exist but still fail trust, clarity and visual quality.

Owns:

- landing page visual hierarchy;
- CTA clarity;
- trust blocks;
- mobile layout;
- pricing presentation;
- before/after workflow screenshots;
- friction removal.

Required output: `OPS/design/conversion_design_review.md`

Done proof: QA conversion scorecard passes minimum threshold before outreach.

### 6. QA Breaker With Release Veto

Mission: break the actual product and block weak releases.

Why needed: a checklist is not enough unless it creates fixes or a release veto.

Owns:

- broken links;
- forms;
- mobile;
- payment path;
- demo workflow;
- trust failures;
- must-fix bugs;
- accepted-risk list.

Required output: `OPS/qa/bug_board.json`

Done proof: release has PASS / BLOCKED / ACCEPTED_RISK verdict.

### 7. Delivery Manager / 72h Pilot Operator

Mission: turn paid pilot into delivered client result.

Why needed: revenue without delivery becomes refund risk and reputation damage.

Owns:

- client intake;
- sample data requirements;
- 72h scope;
- acceptance criteria;
- delivery checklist;
- handoff;
- feedback and upsell trigger.

Required output: `OPS/delivery/pilot_delivery_registry.json`

Done proof: first paid pilot has intake, delivery, QA, handoff and feedback row.

### 8. Customer Discovery / Objection Analyst

Mission: learn why buyers say yes/no and feed that back into product, page and outreach.

Why needed: no-reply is not information unless converted into hypothesis and next segment.

Owns:

- objections;
- no-reply analysis;
- buyer language;
- pains;
- must-have features;
- pricing objections;
- segment pivots.

Required output: `OPS/revenue_ops/objection_log.md`

Done proof: every 20 outreach attempts create one product/copy/pricing change or pause decision.

### 9. Data Provenance / Scraping Compliance Specialist

Mission: ensure all collected public data is allowed, traceable and safe to use.

Why needed: competitor and lead data must not become legal/technical risk.

Owns:

- source URL;
- method;
- collected_at;
- permission status;
- rate limit;
- confidence;
- blocked methods;
- data retention note.

Required output: `OPS/data_intelligence/provenance_ledger.json`

Done proof: competitor and lead rows include provenance and allowed-use status.

### 10. Integrations Specialist

Mission: connect the product to real seller systems and export paths.

Why needed: Parts Seller OS becomes more valuable when it can import/export to real channels.

Owns:

- CSV import/export;
- marketplace feed format;
- photo URL fields;
- order/reservation status;
- API/no-API fallback;
- manual upload workflow;
- connector backlog.

Required output: `OPS/integrations/parts_seller_connectors.md`

Done proof: one-seller prototype can export at least one usable listing/feed row.

### 11. Analytics / Event Tracking Specialist

Mission: measure actual buyer behavior and product usage.

Why needed: without events the system guesses instead of learning.

Owns:

- page visits;
- CTA clicks;
- form submits;
- payment link clicks;
- demo actions;
- drop-off points;
- daily metrics summary.

Required output: `OPS/analytics/event_tracking_plan.md`

Done proof: every public demo has at least basic events or manual measurement plan.

### 12. Security / Secrets / Access Specialist

Mission: prevent public repo and automation mistakes from leaking secrets or creating unsafe access.

Why needed: faster automation increases security risk.

Owns:

- secret scanning;
- environment variable rules;
- access roles;
- safe scraping boundaries;
- customer data handling;
- deployment security checklist.

Required output: `OPS/security/release_security_check.md`

Done proof: no release is promoted without secret/access/data-risk check.

## Specialist priority order

P0 now:

1. Revenue Lead Verification Specialist.
2. Payment / Quote Operations Specialist.
3. Public Demo Publisher / Release Engineer.
4. Product Workflow Architect for Parts Seller OS.
5. UX / Conversion Designer.
6. QA Breaker With Release Veto.
7. Delivery Manager / 72h Pilot Operator.

P1 next:

8. Customer Discovery / Objection Analyst.
9. Data Provenance / Scraping Compliance Specialist.
10. Integrations Specialist.
11. Analytics / Event Tracking Specialist.
12. Security / Secrets / Access Specialist.

## Missing ownership rule

Every specialist must have:

- one canonical output file;
- one metric;
- one next action;
- one blocker/fallback field;
- authority to block weak work;
- proof condition tied to revenue, URL, QA, delivery or data provenance.

## Immediate task additions

### SG-001 Verify first exact lead rows

Owner: Revenue Lead Verification Specialist
Priority: P0
Output: `OPS/revenue_ops/lead_pipeline.json`
Proof: 10 exact public seller rows with contact channel and source URL.
Fallback: use EU/UK public marketplace profiles if direct websites are not found.

### SG-002 Create first payable pilot path

Owner: Payment / Quote Operations Specialist
Priority: P0
Output: `OPS/revenue_ops/payment_path.md`
Proof: quote template + manual bank payment instructions + payment status fields.
Fallback: written quote and manual bank payment path before automated payment link.

### SG-003 Publish first public demo registry

Owner: Public Demo Publisher / Release Engineer
Priority: P0
Output: `OPS/deploy_loop/public_demo_registry.json`
Proof: public URL or explicit NO_URL blocker, smoke test and rollback note.
Fallback: GitHub Pages / static hosting / local demo recording note.

### SG-004 Write Parts Seller OS workflow spec

Owner: Product Workflow Architect for Parts Seller OS
Priority: P0
Output: `products/parts-seller-os/WORKFLOW_SPEC.md`
Proof: add -> suggest -> price -> locate -> list -> export -> reserve flow.
Fallback: static workflow spec first, interactive prototype next.

### SG-005 Create conversion design review

Owner: UX / Conversion Designer
Priority: P0
Output: `OPS/design/conversion_design_review.md`
Proof: page clarity, visual trust, CTA, pricing and mobile review with fix list.
Fallback: manual review using screenshots/static page.

## CEO conclusion

The system should not add more generic managers now. It should add specialist closers.

The missing brain parts are:

- real lead verification;
- payable offer path;
- public demo publishing;
- workflow architecture;
- conversion design;
- release veto QA;
- paid-pilot delivery.

Until those are owned, more agents mostly create more files. With these specialists, the chain can move from repo-output to revenue-proof.
