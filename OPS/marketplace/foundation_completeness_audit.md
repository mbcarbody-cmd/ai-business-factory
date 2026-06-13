# Marketplace Foundation Completeness Audit

Date: 2026-06-13
Owner: MARKET-1 Marketplace General Manager + JUDGE-1 Release Gate Judge
Status: ACTIVE / BLOCKING

## Why this exists

A marketplace or seller OS cannot be considered build-ready if basic foundations are missing. Agents must not move to UI, sales claims or roadmap expansion while foundational inventory logic is absent.

This audit was created after a gap was found: the Parts Seller OS roadmap and sample data existed, but a canonical vehicle parts category tree was not present until 2026-06-13.

## Non-negotiable build foundations

The Parts Seller OS cannot advance beyond `validated_problem -> build_ready` unless these foundations exist and are referenced by product gates, roadmap and QA:

| Foundation | Required artifact | Current status | Blocking rule |
|---|---|---|---|
| Parts category tree | `OPS/marketplace/parts_category_tree.json` | DONE | No add-part workflow without canonical category ids. |
| Data model | `OPS/marketplace/parts_os_mvp_data_model.json` | PARTIAL / UPDATE REQUIRED | Part entity must use `category_id` and `subcategory_id`, not only free-text category. |
| Workflow rules | `OPS/marketplace/parts_workflow_rules.json` | REQUIRED NEXT | Add-part, location, pricing, listing, reservation and ageing rules must be explicit. |
| Location placement logic | `OPS/marketplace/location_rules.json` | REQUIRED NEXT | System must suggest where the part goes, or send it to pending-location queue. |
| Listing status rules | `OPS/marketplace/listing_status_rules.json` | REQUIRED NEXT | Listing cannot be ready without title, price, photo or documented no-photo exception. |
| Vehicle fitment model | `OPS/marketplace/vehicle_fitment_seed.json` | REQUIRED NEXT | Vehicle make/model/generation/year compatibility must not be uncontrolled text. |
| Pricing decision logic | `OPS/marketplace/pricing_rules.json` | REQUIRED NEXT | Price, floor price, confidence and manual-review logic must be explicit. |
| QA audit enforcement | `scripts/ops_audit.py` | UPDATE REQUIRED | Audit must fail if core marketplace foundations are missing. |

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

## Immediate next actions

1. Update `parts_os_mvp_data_model.json` to use `category_id`, `subcategory_id`, `storage_profile`, `fitment_confidence`, `pricing_confidence` and `listing_status`.
2. Add workflow/rule files for location, listing, pricing and vehicle fitment.
3. Update product gate for Parts Commerce OS to require all foundation artifacts before `build_ready`.
4. Update `scripts/ops_audit.py` so it fails if these files are missing or if the category tree lacks required fields.
5. Add task board items for every missing foundation instead of leaving them implicit.

## Proof rule

A foundation is not done because it is mentioned in a plan. It is done only when:

- a repo file exists,
- the file has owner/status/date,
- product gate references it,
- task board references it,
- QA/audit can check it,
- first MVP workflow uses it.
