# Marketplace Foundation Completeness Audit

Date: 2026-06-13
Owner: CEO-A / Parts OS General Manager + JUDGE-1 Release Gate Judge
Status: ACTIVE / BUILD-READY FOR ONE-SELLER PROTOTYPE

## Why this exists

A marketplace or seller OS cannot be considered build-ready if basic foundations are missing. Agents must not move to UI, sales claims or roadmap expansion while foundational inventory logic is absent.

This audit was created after a gap was found: the Parts Seller OS roadmap and sample data existed, but a canonical vehicle parts category tree was not present until 2026-06-13.

## Non-negotiable build foundations

The Parts Seller OS cannot advance beyond `validated_problem -> build_ready` unless these foundations exist and are referenced by product gates, roadmap and QA.

| Foundation | Required artifact | Current status | Blocking rule |
|---|---|---|---|
| Parts category tree | `OPS/marketplace/parts_category_tree.json` | DONE | No add-part workflow without canonical category ids. |
| Data model | `OPS/marketplace/parts_os_mvp_data_model.json` | DONE | Part entity must use `category_id`, `subcategory_id`, `storage_profile` and status/confidence fields. |
| Workflow rules | `OPS/marketplace/parts_workflow_rules.json` | DONE | Add-part, location, pricing, listing, reservation and ageing rules must be explicit. |
| Location placement logic | `OPS/marketplace/location_rules.json` | DONE | System must suggest where the part goes, or send it to pending-location queue. |
| Listing status rules | `OPS/marketplace/listing_status_rules.json` | DONE | Listing cannot be ready without title, price, category, location and photo/exception logic. |
| Vehicle fitment model | `OPS/marketplace/vehicle_fitment_seed.json` | DONE | Vehicle make/model/generation/year compatibility must not be uncontrolled text. |
| Pricing decision logic | `OPS/marketplace/pricing_rules.json` | DONE | Price, floor price, confidence and manual-review logic must be explicit. |
| QA audit enforcement | `scripts/ops_audit.py` | DONE | Audit fails if core marketplace or 4x org foundations are missing. |

## Agent failure diagnosis

The agent system treated roadmap/data-model text as enough progress. That is wrong.

Root causes:

1. Product gate was partial and did not hard-require the category tree.
2. QA critic checked file existence, not business-foundation completeness.
3. Marketplace owner did not run a first-principles inventory workflow audit: "Can a real part be added, classified, located, priced and listed?"
4. Task board allowed `in_progress` work without demanding all prerequisite foundations.

## New operating rule

For every product, agents must ask:

> What boring foundational table, enum, rule or workflow must exist before a useful product can work?

For Parts Seller OS, the minimum foundation chain is:

`part intake -> category tree -> vehicle fitment -> side/position -> condition -> location suggestion -> pricing -> listing readiness -> reservation/order -> ageing/dead-stock action`

If any link is missing, the product is not build-ready.

## Current gate result

Foundation layer is now complete enough to allow the smallest **one-seller local prototype**.

Allowed now:

- build local UI/workflow for sample parts,
- use category tree,
- use location rules,
- use listing status rules,
- use pricing rules,
- use vehicle fitment seed,
- test 3 sample parts through the workflow.

Still not allowed:

- full marketplace build,
- public selling claim without working demo,
- paid pilot promise without delivery scope and QA proof,
- new unrelated build work that consumes CEO-A/CEO-C P0 capacity.

## Immediate next actions

1. Build `products/parts-seller-os/` local prototype.
2. Show 3 parts passing through add -> classify -> locate -> price -> listing status.
3. Add QA critic bug board entries for broken flow.
4. Update CFO value case for one-seller pilot.
5. CEO-B converts prototype into exact lead/offering path.

## Proof rule

A foundation is not done because it is mentioned in a plan. It is done only when:

- a repo file exists,
- the file has owner/status/date,
- product gate references it,
- task board references it,
- QA/audit can check it,
- first MVP workflow uses it.
