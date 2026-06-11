# Core Build Backlog

Goal: convert requirements into buildable work packages for a final B2B Parts and Asset Business OS.

## Build rule

No feature is done until it has:

- database tables
- backend endpoints
- frontend screen
- validation rules
- audit logs
- role permissions
- QA test cases
- performance expectation
- security check

## Phase 1: B2B seller onboarding and access

### Work package 1.1 Seller application page

User story:

As a seller, I apply for access by entering company and operational data.

Required:

- company data form
- VAT payer / non-VAT selection
- current stock count
- planned monthly upload count
- categories
- warehouse and shipping info
- return process info
- submit state

Done when:

- seller can submit application
- admin can see it
- missing required fields are blocked
- application status is saved

### Work package 1.2 Admin approval

Required:

- admin application list
- approve
- reject
- ask for more info
- risk score
- invite link generation

Done when:

- admin approves seller
- seller gets invite state
- rejected seller cannot access product

### Work package 1.3 Seller account setup

Required:

- invite token
- password setup
- first seller admin user
- seller company settings
- VAT mode lock / edit rules

Done when:

- approved seller creates first admin user
- login works
- seller dashboard opens

## Phase 2: Company, VAT and pricing core

### Work package 2.1 Seller tax profile

Required:

- VAT payer mode
- VAT code
- default VAT rate
- net/gross storage preference
- invoice text mode

Done when:

- VAT payer prices calculate net, VAT and gross
- non-VAT seller shows VAT amount zero
- e-shop displays correct wording

### Work package 2.2 Price display service

Required:

- internal price formatting
- e-shop price formatting
- B2B net/gross formatting
- discount calculation
- delivery cost separation

Done when:

- every price clearly says VAT included, plus VAT, or VAT not charged

## Phase 3: Universal asset and category engine

### Work package 3.1 Asset categories

Required categories:

- cars
- motorcycles
- buses
- trucks
- tractors
- agricultural machinery
- construction machinery
- trailers
- boats
- jet skis
- snowmobiles / snow bikes
- ATVs / UTVs
- planes
- helicopters
- other machines

Done when:

- seller can choose category when creating donor asset
- fields adapt by category

### Work package 3.2 Donor asset creation

Required:

- asset title
- category
- technical data
- purchase price
- transport cost
- dismantling cost
- storage cost
- other costs
- location
- photo
- notes

Done when:

- seller creates donor asset
- profitability card calculates total cost

## Phase 4: Parts lifecycle

### Work package 4.1 Part creation

Required:

- linked donor asset
- part category
- internal part ID
- title
- OEM/reference codes
- condition
- defect description
- location
- price
- status

Done when:

- part is created from donor asset
- part appears in donor asset parts list

### Work package 4.2 Photo upload

Required:

- at least 25 photos per part
- multi upload
- progress
- thumbnails
- main photo
- reorder
- rotate/crop basics
- hidden/internal-only flag

Done when:

- user uploads 25 photos without page freeze

### Work package 4.3 Part status lifecycle

Required states:

- draft
- in warehouse
- listed
- reserved
- sold
- returned
- written off
- hidden

Done when:

- state changes are controlled and logged

## Phase 5: Warehouse and tasks

### Work package 5.1 Locations

Required:

- zones
- rows
- shelves
- bins
- QR/barcode
- capacity
- occupied/free/full state

Done when:

- part can be assigned to exact location
- parts without location queue exists

### Work package 5.2 Worker tasks

Required:

- task creation
- assign worker
- task linked to asset, part, order or shipment
- status
- time tracking
- proof photo where needed

Done when:

- manager can assign and track work

## Phase 6: Reservation, order, payment and shipping

### Work package 6.1 Reservation

Required:

- reserve part
- customer type
- delivery type
- payment method
- discount
- reservation until date
- cancel reason

Done when:

- reserved part cannot be sold twice
- expired reservation is visible

### Work package 6.2 Sale and order

Required:

- convert reservation to order
- direct sale
- order status
- payment status
- picking status
- shipment status
- invoice action
- audit log

Done when:

- order can be completed from one or more parts

### Work package 6.3 Shipping

Required:

- carrier
- package size
- weight
- tracking
- label state
- manifest state
- shipment photos

Done when:

- shipment can be created and tracked

## Phase 7: Profitability and analytics

### Work package 7.1 Donor asset profitability

Required:

- total cost
- sold revenue without VAT
- remaining stock value
- refunds
- write-off value
- balance
- ROI

Done when:

- donor asset shows live break-even and profit state

### Work package 7.2 Dashboard

Required:

- turnover
- stock value
- orders
- returns
- delayed orders
- unpaid orders
- parts without price
- parts without location
- seller performance

Done when:

- dashboard helps daily operations

## Phase 8: QA, performance and security gates

Required:

- E2E test matrix
- upload stress test
- price/VAT tests
- role permission tests
- audit log tests
- backup restore test
- performance checks
- security review

Done when:

- release candidate passes all gates
