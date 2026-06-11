# Performance, QA and VAT Requirements

Goal: the system must be smooth, stable and usable as a final product, not a prototype.

## Performance principles

The site must not feel heavy.

Required:

- fast login
- fast search
- fast filters
- fast order page
- fast part page
- fast photo upload feedback
- lazy loading for images
- pagination or virtual lists for large tables
- compressed images
- cached lookup lists
- no huge blocking scripts
- database indexes for all frequent filters
- background jobs for slow sync/export tasks
- health checks for server services
- logs for errors and slow requests

## Target speed rules

- page shell loads under 2 seconds on normal connection
- search results respond under 1 second for common filters
- order page opens under 1 second after data is cached
- photo upload gives visible feedback immediately
- long operations go to background queue
- no table should try to render thousands of rows at once

## Critical end-to-end flows to test

Every release must test these flows:

1. Login
2. Role and permission check
3. Donor asset creation
4. Vehicle or machine technical data entry
5. Part creation from donor asset
6. Part photo upload
7. Photo rotate / crop / main photo selection
8. Part price creation
9. Part location assignment
10. Part reservation
11. Reservation expiry or cancellation
12. Convert reservation to sale
13. Direct sale without reservation
14. Order creation
15. Payment status change
16. Picking task
17. Packing task
18. Shipment creation
19. Label / tracking state
20. Return creation
21. Donor asset profitability calculation
22. VAT payer pricing
23. Non-VAT payer pricing
24. E-shop price display
25. Audit log after each important action

## VAT / non-VAT company support

The system must support two seller types:

### VAT payer seller

Required:

- seller profile has VAT payer = true
- VAT code field
- default VAT rate field
- prices can be stored net and gross
- invoices show net amount, VAT amount and gross amount
- e-shop shows clear text: price with VAT included or net plus VAT depending page context
- B2B exports must include VAT breakdown

### Non-VAT payer seller

Required:

- seller profile has VAT payer = false
- VAT amount is always zero
- price is final sale price
- invoice and e-shop must clearly state VAT is not charged
- reports must not invent VAT
- marketplace exports must use no-VAT logic

## Customer types

The system must support:

- guest
- individual customer
- business customer

Each order must store:

- customer type
- country
- billing data
- delivery data
- VAT number where applicable
- payment method
- delivery type

## E-shop price display rules

For every visible price in the e-shop:

- show amount
- show currency
- show whether VAT is included, excluded or not charged
- show delivery cost separately
- show discount separately
- show total clearly before checkout

Examples:

- VAT payer: 100.00 EUR incl. VAT
- VAT payer B2B context: 82.64 EUR + 17.36 EUR VAT = 100.00 EUR
- Non-VAT payer: 100.00 EUR, VAT not charged

## Profitability calculation tests

Donor asset calculation must test:

- purchase price
- transport cost
- dismantling cost
- storage cost
- other costs
- total cost
- planned revenue
- sold revenue with VAT
- sold revenue without VAT
- remaining stock value
- written-off stock
- returns
- balance
- ROI percentage

Formula requirements:

- total_cost = purchase + transport + dismantling + storage + other
- balance = sold_revenue_without_vat + remaining_stock_value - total_cost - refunds - write_off_value
- ROI = balance / total_cost when total_cost > 0

## Resource control

Avoid unnecessary server load:

- image processing runs in background
- marketplace sync runs in queue
- analytics are precomputed or cached
- repeated filter options are cached
- heavy reports have date limits
- file uploads have size limits
- thumbnail generation is separated from original upload
- logs rotate automatically

## Security and stability checks

Each release must check:

- protected admin routes
- role-based access
- upload file type validation
- upload size limits
- no public environment secrets
- no public API keys
- session expiration
- password reset safety
- audit log integrity
- backup restore test
- server service restart test

## Release rule

The product cannot be called final until performance, VAT logic, QA, security, deployment and backup checks are complete.
