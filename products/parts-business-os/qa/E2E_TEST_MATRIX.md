# Parts Business OS E2E Test Matrix

Purpose: stop weak releases. Every core workflow must have happy-path and failure-path tests before release.

## Release blocking rule

A release candidate is blocked if any P0 or P1 test fails.

Priorities:

- P0: money, data integrity, permissions, order/reservation, security
- P1: warehouse, pricing, listing, worker tasks, upload stability
- P2: UX polish, wording, non-critical convenience

## Test area 1: Seller access and roles

Happy path:

- approved seller admin logs in
- seller admin creates worker user
- warehouse worker sees only warehouse/task screens
- pricing manager sees pricing queue

Failure path:

- rejected seller cannot log in
- warehouse worker cannot edit price
- pricing manager cannot approve seller
- read-only auditor cannot mutate records

Blocking level: P0

## Test area 2: Donor asset creation

Happy path:

- seller creates donor asset with category, costs and status
- profitability card stores purchase, transport and dismantling costs

Failure path:

- asset cannot be created without seller
- negative cost values are rejected or flagged
- missing required category blocks save

Blocking level: P1

## Test area 3: Part creation flow

Happy path:

- seller creates part from donor asset
- internal part ID is generated
- OEM codes, condition, defects, dimensions, weight and price fields save
- part appears in donor asset parts list

Failure path:

- part cannot exist without donor asset
- duplicate internal part ID is rejected
- invalid status transition is blocked

Blocking level: P0

## Test area 4: Warehouse locations

Happy path:

- admin creates zones, rows, shelves and bins
- location capacity is saved
- part is assigned to exact location
- unlocated parts queue shows parts without location

Failure path:

- full location cannot receive more volume unless override is approved
- blocked location cannot be recommended
- deleted/archived location cannot hold active parts

Blocking level: P1

## Test area 5: Worker tasks

Happy path:

- manager creates task linked to part
- worker marks task doing and done
- proof photo flag is visible where required

Failure path:

- worker cannot assign tasks to other users without permission
- done task cannot be changed without audit log
- task linked to missing part is rejected

Blocking level: P1

## Test area 6: Pricing and listing readiness

Happy path:

- part moves from price_missing to price_review to price_ready
- competitor observation can be saved
- listing readiness checks required title, condition, price and photo state

Failure path:

- listing cannot publish with missing price
- listing cannot publish with unknown condition unless manually approved
- bad price input is rejected

Blocking level: P0

## Test area 7: Reservation and order

Happy path:

- part can be reserved until a date
- reserved part cannot be sold twice
- reservation converts to order
- order contains one or more parts
- payment, picking, shipment and invoice statuses update

Failure path:

- expired reservation is visible
- sold part cannot be reserved
- part in active reservation cannot be added to another order
- cancelled order releases stock only through controlled transition

Blocking level: P0

## Test area 8: Shipment

Happy path:

- order creates shipment
- carrier, package size, weight, tracking and label state save
- shipment status moves through packed, handed_to_carrier, in_transit, delivered

Failure path:

- shipment cannot exist without order
- delivered shipment cannot be deleted without admin/audit

Blocking level: P1

## Test area 9: VAT and price display

Happy path:

- VAT payer seller shows net, VAT and gross correctly
- non-VAT seller shows VAT not charged wording
- order totals match part sold prices

Failure path:

- VAT mode cannot silently change past orders
- empty VAT settings are blocked for VAT payer

Blocking level: P0

## Test area 10: Audit logs

Happy path:

- price changes are logged
- stock status changes are logged
- order state changes are logged
- permission-sensitive actions are logged

Failure path:

- audited action cannot complete without audit row
- audit log cannot be edited by normal users

Blocking level: P0

## Test area 11: Deploy health

Happy path:

- app starts
- database connection works
- health endpoint returns ok
- logs are created

Failure path:

- failed health check blocks release
- missing env variables block startup
- rollback plan is available

Blocking level: P0

## Release decision

Release can pass only when:

- all P0 tests pass
- all P1 tests pass or have accepted mitigation
- no security blocker exists
- rollback path exists
- known risks are written
