# Sprint: 10 Track Technical Backbone

Goal: move Parts Business OS from planning/prototype into a buildable operational system.

## Sprint policy

Each track has one owner agent, one required output path, and one acceptance gate.

No track can be marked done with description only.

## Track 1: Stable DB schema

Owner: Database Engineer

Required outputs:

- `products/parts-business-os/schema/001_core_schema.sql`
- entity relationship notes
- migration run instructions

Acceptance criteria:

- sellers, users, roles, donor assets, parts, locations, tasks, reservations, orders, shipments, prices, photos and audit logs exist
- foreign keys protect core relationships
- timestamps exist on business-critical tables
- audit log can reference important actions

## Track 2: Auth and roles

Owner: Backend Engineer + Security Reviewer

Required outputs:

- auth model
- role permission matrix
- login/session acceptance tests

Roles:

- platform_admin
- seller_admin
- warehouse_manager
- warehouse_worker
- pricing_manager
- sales_operator
- read_only_auditor

Acceptance criteria:

- user permissions are explicit
- warehouse worker cannot edit financial fields
- pricing manager cannot approve sellers
- read-only auditor cannot mutate data

## Track 3: Part creation flow

Owner: Full Stack Builder

Required outputs:

- create donor asset flow
- create part from donor asset flow
- validation rules
- status lifecycle

Acceptance criteria:

- part cannot exist without seller and donor asset
- part gets internal ID
- part has condition, location state, price state and listing state

## Track 4: Warehouse location engine

Owner: Warehouse Math Agent + Database Engineer

Required outputs:

- location model
- capacity fields
- location recommendation rules
- unlocated parts queue

Acceptance criteria:

- locations have zone, row, shelf, bin, capacity and occupied state
- part receives recommended location
- system can detect full location
- unlocated part is visible in queue

## Track 5: Worker task board

Owner: Product Architect + Frontend Engineer

Required outputs:

- worker task model
- task list screen
- task status workflow

Acceptance criteria:

- manager can assign task
- worker can mark task started/done
- task can link to part, asset, order or shipment
- proof photo flag exists where needed

## Track 6: Pricing and listing intelligence

Owner: Pricing Intelligence Agent + Market Analyst

Required outputs:

- pricing input fields
- competitor price fields
- listing readiness rules
- price review queue

Acceptance criteria:

- part can be marked price_missing, price_review, price_ready
- listing cannot publish without minimum required price data
- pricing logic can store confidence and reason

## Track 7: Order and reservation flow

Owner: Backend Engineer + CFO

Required outputs:

- reservation tables and rules
- order tables and state machine
- payment status and invoice action field

Acceptance criteria:

- reserved part cannot be sold twice
- reservation expiry is visible
- order can contain one or more parts
- order has payment, picking and shipment states

## Track 8: QA automated tests

Owner: QA Automation Engineer

Required outputs:

- `products/parts-business-os/qa/E2E_TEST_MATRIX.md`
- release-blocking test checklist
- bug board format

Acceptance criteria:

- every core workflow has happy path and failure path tests
- VAT/pricing, permissions, upload, reservation and location tests exist
- release cannot pass with blocker bugs

## Track 9: Deploy loop

Owner: DevOps Engineer + SRE Agent

Required outputs:

- deploy plan
- health endpoint spec
- rollback playbook
- logs and backup checklist

Acceptance criteria:

- build steps documented
- deploy steps documented
- health check documented
- rollback trigger documented

## Track 10: Sales/demo page

Owner: Sales Operator + Website Design Agent

Required outputs:

- public demo page requirements
- visual trust checklist
- pricing/package draft
- buyer target list

Acceptance criteria:

- buyer understands value in 5 seconds
- CTA exists
- demo path exists
- pricing and delivery promise are visible

## Sprint done gate

Sprint is done only when at least tracks 1, 3, 4, 8 and 9 have concrete repo artifacts, because these tracks create the technical skeleton.
