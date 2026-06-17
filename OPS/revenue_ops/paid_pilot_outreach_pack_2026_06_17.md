# Parts Seller OS paid-pilot outreach pack

Date: 2026-06-17  
Owner: SPEC-021 Revenue Operations Specialist + SPEC-024 Commercial Closer  
Status: message_ready_not_sent

## Operating rule

Use only the official public business routes recorded in `OPS/data_intelligence/lead_review_queue_2026_06_15.json`. Personalize the first line, send one message per business, and record the timestamp and result. No automated bulk sending. A reply, acceptance or payment must be recorded as external evidence; this document is not revenue proof.

## Pilot offer

- One seller workflow configured around sample used-parts data.
- Core flow: intake, category and storage profile, price and floor guidance, location suggestion, listing readiness, marketplace feed draft, reservation and next action.
- Delivery target: 72 hours after accepted scope, usable sample data, named owner and verified payment.
- Setup range: EUR 300-900 depending on scope; recommended first offer EUR 600.
- Low-friction CTA: 15-minute fit call or a sample file containing 20-50 parts.

---

## LRQ-001 — ASM Auto Recycling

**Route:** official contact page or the published business email recorded in the lead queue.  
**Subject:** Pilot to reduce manual used-parts listing and warehouse decisions

Hello ASM Auto Recycling team,

You already operate across vehicle salvage and recycled-parts inventory, so I am not proposing a generic AI project. We have built a focused Parts Seller OS workflow that takes a dismantled part from intake through category and storage profile, price and floor guidance, warehouse-location suggestion, listing readiness and marketplace-feed preparation.

I would like to configure a paid pilot around 20-50 sample parts from one ASM workflow. The aim is to identify where your team loses time or margin between dismantling, storage and listing, then deliver one working workflow within 72 hours after scope, sample data and payment are confirmed.

Would a 15-minute fit call be useful, or could you point me to the person responsible for recycled-parts inventory and listing operations?

Regards,
Vitalijus

**CTA:** fit call or referral to inventory/listing owner.  
**Recommended opening price:** EUR 600.

---

## LRQ-002 — LKQ SYNETIQ

**Route:** official Solutions for business or General enquiries form.  
**Subject:** Used-parts workflow pilot for dismantling-to-listing operations

Hello LKQ SYNETIQ team,

Your dismantling, recycling and green-parts operation is a strong fit for a narrow workflow pilot rather than a broad software pitch. Parts Seller OS is designed to structure part intake, taxonomy, pricing confidence, storage placement, listing readiness and export preparation in one auditable flow.

The proposed pilot uses 20-50 sample parts from one operational lane and produces a working workflow plus a clear record of manual-review points, blocked listings and next actions. Delivery is targeted within 72 hours after scope, usable sample data and payment are confirmed.

Could this be reviewed by the person responsible for green-parts inventory systems, pricing operations or marketplace listing workflows?

Regards,
Vitalijus

**CTA:** route to inventory systems, pricing or listing owner.  
**Recommended opening price:** EUR 900 because of likely enterprise complexity; reduce scope rather than price if needed.

---

## LRQ-003 — BreakerLink

**Route:** official Become a Supplier form.  
**Subject:** Supplier-side Parts Seller OS pilot for faster quote-ready inventory

Hello BreakerLink team,

BreakerLink connects buyers with suppliers, so the quality and readiness of supplier inventory directly affects quote speed and conversion. We have built Parts Seller OS to help a used-parts supplier structure intake, category and fitment fields, pricing confidence, warehouse location, photo and listing readiness, and export-ready records.

I am proposing a paid pilot using 20-50 parts from one supplier workflow. The result would be a working supplier-side process that exposes missing data before a quote or listing is created and produces a cleaner marketplace-feed draft.

Would you be open to reviewing this as a supplier-enablement pilot, or introducing one suitable breaker from your network for the first paid implementation?

Regards,
Vitalijus

**CTA:** platform review or introduction to one supplier.  
**Recommended opening price:** EUR 600 for one supplier workflow.

---

## LRQ-004 — PartsGateway

**Route:** official Join as Supplier form.  
**Subject:** Pilot to improve supplier inventory readiness before buyer quotes

Hello PartsGateway team,

PartsGateway depends on suppliers being able to identify, price, locate and respond with the correct used part quickly. Parts Seller OS is a focused operational workflow for part intake, taxonomy and position fields, price and floor guidance, warehouse placement, listing readiness and export preparation.

I would like to run a paid pilot with one supplier and 20-50 sample parts. The goal is to reduce incomplete records and manual searching before a supplier can answer a buyer request. A working pilot would be delivered within 72 hours after scope, sample data and payment are confirmed.

Could you review this as a supplier-enablement test or connect me with one active supplier who would benefit from a structured inventory workflow?

Regards,
Vitalijus

**CTA:** supplier-enablement review or one supplier introduction.  
**Recommended opening price:** EUR 600.

---

## LRQ-005 — Ovoko

**Route:** official seller partnership / Let's talk form.  
**Subject:** Parts Seller OS pilot for seller inventory quality and listing readiness

Hello Ovoko partnerships team,

Ovoko already solves marketplace distribution for used vehicle parts. The proposed pilot sits one step earlier: helping a seller create cleaner inventory records before they reach the marketplace. Parts Seller OS structures intake, category and side/position data, pricing confidence, warehouse location, photo and listing readiness, and marketplace-feed preparation.

I would like to configure a paid pilot for one seller using 20-50 sample parts. The output would be one working seller workflow and measurable visibility into records blocked by price, location, photos or missing fitment data.

Would this be relevant to your seller-success or inventory-product team, or could you introduce one seller suitable for a first pilot?

Regards,
Vitalijus

**CTA:** seller-success/product review or one seller introduction.  
**Recommended opening price:** EUR 600.

---

## Follow-up sequence

1. Day 0: send the individualized first message through the approved official route.
2. Day 3: one concise follow-up with the specific operational outcome and 20-50-part sample request.
3. Day 7: final close-the-loop message; mark no response and move to the next verified lead.
4. Positive reply: create a record in `OPS/commercial/offer_acceptance_payment_register_2026_06_17.json` and use the canonical acceptance and payment states.
5. Paid status: create the delivery record and start only when the required evidence fields are complete.

## Proof fields after sending

For each lead record: message version, route used, sent timestamp, sender, response state, next action, evidence reference and owner. Do not mark a paid pilot or delivery complete from a sent message alone.
