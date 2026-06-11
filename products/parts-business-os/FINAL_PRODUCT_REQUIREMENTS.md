# Parts Business OS - Final Product Requirements

Goal: build a complete working operating system for parts businesses. This is not a demo target.

## Final product definition

The product is final only when a real business can use it daily for:

purchase -> dismantling -> part creation -> photo -> pricing -> location -> listing -> sale -> payment -> packing -> shipping -> returns -> analytics -> profit control.

## Universal vehicle and machine categories

The system must support parts for many categories, not only cars.

Required top categories:

1. Cars
2. Motorcycles
3. Buses
4. Trucks
5. Tractors
6. Agricultural machinery
7. Construction machinery
8. Trailers
9. Boats
10. Jet skis
11. Snowmobiles / snow bikes
12. ATVs / UTVs
13. Planes
14. Helicopters
15. Other machines and equipment

Each category must support its own fields, but the core parts workflow stays the same.

## Core modules

### 1. Dashboard Control Room

Must show:

- turnover
- profit
- order count
- return count
- delayed orders
- unpaid orders
- active listings
- parts without price
- parts without photos
- parts without location
- parts without OEM / reference code
- worker tasks
- marketplace sync health
- stock value
- donor vehicle profit

### 2. Purchase / donor asset module

Must support:

- donor vehicle or machine purchase
- purchase cost
- transport cost
- dismantling cost
- storage cost
- other costs
- total cost
- planned revenue
- actual revenue with tax
- actual revenue without tax
- balance
- ROI
- linked parts
- asset photo
- vehicle or machine parameters
- activity history

### 3. Universal asset parameter system

For cars, motorcycles, trucks, tractors, boats, planes and other categories, the system must support flexible fields:

- manufacturer
- model
- modification
- year
- VIN or serial number
- engine code
- engine size
- fuel type
- power
- gearbox
- drivetrain
- steering position
- body type
- color
- color code
- mileage / hours
- registration / plate where needed
- category-specific technical fields

### 4. Parts module

Must support:

- internal part ID
- part title
- category
- donor asset link
- OEM / reference codes
- marketplace external IDs
- condition
- defect description
- notes
- price
- cost
- tax mode
- location
- status
- reserved state
- sold state
- returned state
- written-off state
- photo gallery
- marketplace status per channel
- activity history

### 5. Photo Studio

Must support:

- multiple photos
- main photo selection
- photo order
- rotate left / right
- angle adjustment
- crop
- basic edit
- save
- image status
- AI photo quality warning
- duplicate photo warning
- missing angle warning

### 6. Warehouse and location system

Must support:

- zones
- rows
- shelves
- bins
- pallet places
- location barcode / QR
- location capacity
- empty / occupied / full state
- part put-away task
- part move task
- part location history
- parts without location queue

### 7. Tasks and workers

Must support:

- users
- employees
- roles
- permissions
- task assignment
- task priority
- task status
- task linked to part, asset, order or shipment
- worker statistics
- time tracking
- audit trail

### 8. Sales channels and integrations

Must support channel accounts and status for:

- own web shop
- RRR-like marketplace
- eBay
- Allegro
- Amazon
- Autoteile-Markt
- dalys.lt
- other third-party channels

Must include:

- channel account connection state
- safe credential storage
- active / inactive state
- listing sync queue
- error queue
- update account action
- export templates
- marketplace-specific status per part

### 9. Orders module

Must support:

- all orders
- new orders
- priority orders
- delayed orders
- unfinished orders
- failed orders
- returns
- documents
- sales reports
- order detail page
- customer details
- order status
- payment status
- picking status
- shipment status
- expected delivery date
- issue/comment field
- linked parts
- invoice actions
- shipment label actions
- activity history

### 10. Order filters

Must support filters by:

- order status
- sale type
- picking status
- expected delivery date
- paid / unpaid
- sales channel account
- payment type
- customer
- shipment
- ordered by
- date range
- payment deadline
- delay
- deleted orders visibility
- active sales
- part manufacturer
- part model
- part year
- part condition
- part location
- purchase ID

### 11. Payments and finance

Must support:

- payment method
- bank transfer
- payment received status
- invoices
- invoice printing
- documents
- tax mode
- discounts
- refunds
- return amount
- finance reports
- average sold item value
- revenue by channel
- revenue by region
- revenue by size / weight

### 12. Shipping and packing

Must support:

- carrier selection
- shipment ID
- package size
- package weight
- requested carrier
- confirmed shipment
- tracking code
- manifest status
- submitted to carrier state
- label print
- shipment photo
- packing material usage
- packing task
- failed shipment queue

### 13. Returns and disputes

Must support:

- return request
- return reason
- received return
- refund status
- dispute status
- linked order
- linked part
- restock or write-off decision
- return rate analytics

### 14. Audit log / operation history

Must log:

- part created
- price added
- price changed
- location changed
- photo added or edited
- uploaded to marketplace
- order created
- payment changed
- shipment created
- return created
- status changed
- user action

Every log entry must include:

- entity type
- entity ID
- user
- old value
- new value
- timestamp
- source

### 15. AI Operations Layer

AI should assist with:

- donor asset profit forecast
- parts worth removing
- missing field detection
- duplicate part detection
- pricing suggestion
- listing title generation
- listing description generation
- OEM / reference helper
- photo quality check
- suggested warehouse location
- slow-moving stock warning
- overpriced / underpriced stock warning
- late order risk
- unpaid order risk
- return risk
- worker productivity insights

## What was missing from earlier plans

The screenshots revealed these missing layers:

- universal vehicle/machine category taxonomy
- donor asset profitability as a first-class module
- detailed operation history
- photo editor workflow
- marketplace account management
- marketplace sync queue and error queue
- dense advanced filters
- order filters that include part filters
- payment and shipment detail states
- packing material tracking
- returns and disputes
- worker task accountability
- barcode / QR support
- saved filter presets
- category-specific technical fields

## Product release gate

No release until these are complete:

- auth and roles
- database
- core modules
- universal category taxonomy
- tests
- security review
- backup plan
- deploy script
- public page
- user guide
- support process
- first target customer list
