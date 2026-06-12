# Role Permission Matrix

Purpose: make Parts Business OS safe for real daily work, not only demo usage.

## Roles

### platform_admin

Owns the whole platform.

Allowed:

- approve or reject sellers
- suspend sellers
- view all tenants
- manage platform settings
- view audit logs

Not allowed:

- silently edit seller financial history without audit log

### seller_admin

Owns one seller account.

Allowed:

- manage seller users
- manage donor assets
- manage parts
- manage locations
- manage pricing
- manage orders and shipments
- view profitability

Not allowed:

- access another seller tenant
- approve own seller application at platform level

### warehouse_manager

Owns warehouse operations.

Allowed:

- create and edit locations
- assign parts to locations
- assign worker tasks
- view parts and stock states
- update picking and packing states

Not allowed:

- edit seller tax profile
- approve sellers
- change final sold price without pricing permission

### warehouse_worker

Executes assigned work.

Allowed:

- view assigned tasks
- start and finish tasks
- upload proof photos
- view required part and location data

Not allowed:

- edit prices
- delete parts
- create orders
- approve refunds
- edit seller settings

### pricing_manager

Owns price and listing readiness.

Allowed:

- edit part prices
- add competitor observations
- mark price_ready
- mark listing_ready
- add pricing reason and confidence

Not allowed:

- approve sellers
- change warehouse capacity
- complete shipment without warehouse permission

### sales_operator

Owns reservation and customer order flow.

Allowed:

- create reservation
- convert reservation to order
- update customer details
- update payment follow-up state

Not allowed:

- reserve sold parts
- override active reservation without manager approval
- edit tax mode

### read_only_auditor

Checks activity without changing data.

Allowed:

- view dashboards
- view audit logs
- view orders
- view parts

Not allowed:

- create, update or delete business records

## Permission test rules

Every protected API endpoint must answer these questions:

1. Which role can call it?
2. Which tenant/seller can the user access?
3. Does this action require audit log?
4. Can this action affect money, stock, tax or delivery?
5. What is the failure response if permission is missing?

## P0 permission tests

Release is blocked unless these tests pass:

- warehouse_worker cannot edit price
- warehouse_worker cannot create order
- pricing_manager cannot approve seller
- sales_operator cannot sell already sold part
- seller_admin cannot access another seller account
- read_only_auditor cannot mutate any record
- unauthenticated user cannot access private API

## Implementation target

Next backend implementation must add middleware:

```text
requireAuth -> requireTenant -> requireRole -> writeAuditIfCritical -> handler
```

## Done gate

This matrix is done only when automated permission tests exist and fail correctly when a role is not allowed.
