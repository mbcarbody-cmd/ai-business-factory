# Recar Detailed Entity and Workflow Model

Source: user-provided screenshots of an internal used-parts operating system. This document extracts workflow and entity architecture only. It is not a copy plan.

## Key discovery

The system is not only stock management. It connects:

vehicle purchase -> profitability -> vehicle parameters -> extracted parts -> part photos -> price changes -> marketplace channels -> orders -> payments -> shipments -> user activity.

## Purchase / donor vehicle detail page

Observed purchase card fields:

- purchase ID
- title
- type
- created by / entered by
- color code
- location
- comment
- created date
- edited date

Observed profitability fields:

- vehicle purchase price
- dismantling cost
- transport cost
- storage cost
- other costs
- total cost
- planned revenue
- sales amount with VAT
- sales amount without VAT
- balance

Observed vehicle parameter fields:

- manufacturer
- model
- modification
- engine code
- year
- VIN
- body type
- color
- fuel type
- engine size
- gearbox
- drivetrain
- steering side
- mileage
- vehicle image

Required in our product:

- donor vehicle entity
- vehicle cost ledger
- planned revenue field
- real sales sum
- balance and ROI
- linked parts list
- vehicle photo gallery
- user activity log
- AI profitability estimate
- AI suggested parts-to-remove checklist

## Parts extracted from donor vehicle

Observed parts table fields:

- part image
- part title
- part codes / OEM codes
- donor vehicle info
- part ID
- location
- price
- comment
- status
- marketplace status indicator
- row actions

Observed statuses:

- in warehouse
- uploaded to marketplace
- price changed

Required in our product:

- part entity linked to donor vehicle
- internal part ID
- OEM code list
- marketplace IDs
- location field
- price field
- cost field
- condition field
- defect description
- comments
- status timeline
- marketplace status per channel
- part photo gallery
- AI missing data detector
- AI price assistant
- AI title and description generator

## Part detail page

Observed part page sections:

- part name
- detail set
- status
- internal ID
- OEM code
- color code
- cost
- price
- condition
- location
- notes
- defect description
- comment
- photos
- set details

Photo viewer/editor observations:

- multiple thumbnails
- main image preview
- rotate left / rotate right
- reset
- angle slider
- crop tool
- edit tool
- text tool
- save action

Required in our product:

- built-in photo gallery
- rotate/crop/basic edit
- photo order management
- main photo selection
- AI photo quality check
- background/lighting warning
- watermark/export-ready image generation later

## Operations log

Observed operation feed:

- user initials
- time ago
- uploaded to marketplace
- changed price from X to Y
- added price

Required in our product:

- audit_logs table
- every important change saved
- who did it
- what changed
- old value
- new value
- timestamp
- linked entity

Events to log:

- part created
- part edited
- price changed
- location changed
- uploaded to channel
- order created
- order shipped
- return created
- photo changed
- status changed

## Order module detail

Observed order filters:

- order status
- sale type
- picking status
- latest expected delivery date
- paid status
- sales channel account
- payment type
- customer search
- issue status
- shipment
- ordered by
- issue date
- ordered date
- payment deadline
- delay
- show deleted orders
- active sales

Observed detail filters inside orders:

- manufacturer
- model
- modification
- body type
- year from / to
- fuel type
- engine size from / to
- gearbox
- color
- vehicle type
- comment
- purchase ID

Required in our product:

- order filters
- nested part filters inside orders
- payment status
- picking status
- shipment status
- expected delivery date
- late warning
- deleted order visibility
- customer search
- issue/comment flow
- AI risk warning for late or unpaid orders

## Sales channel module

Observed channel cards:

- Amazon
- eBay
- RRR
- Allegro
- Autoteile-Markt
- dalys.lt
- Telehaber
- third-party listings

Observed actions:

- add/update account
- activate
- connected account state

Required in our product:

- sales_channels table
- channel_accounts table
- per-channel listing status
- add/update credentials UI
- safe credential storage rules
- active/inactive state
- channel sync queue
- channel error queue
- listing export templates

## Shipment module

Observed shipment page fields:

- search by ID, shipment number or receiver data
- ID
- requested carrier
- ordered shipment
- manifest
- submitted to carrier

Required in our product:

- shipments table
- package fields
- carrier requested
- carrier confirmed
- manifest status
- tracking code
- submitted to carrier state
- label print status
- packing task
- shipment issue queue

## Users module

Observed users page.

Required in our product:

- users
- roles
- permissions
- activity stats
- task assignment
- audit trail

## Locations module

Observed simple search by location name.

Required in our product:

- zones
- rows
- shelves
- bins
- QR/barcode per location
- location capacity
- empty/full state
- part location history
- AI suggested location

## Stronger architecture for our final product

Modules required:

1. Dashboard Control Room
2. Donor Vehicle Profitability
3. Vehicle Intake
4. Part Creation
5. Photo Studio
6. Pricing Intelligence
7. Warehouse Locations
8. Worker Tasks
9. Marketplace Channels
10. Orders and Payments
11. Shipping and Packing
12. Returns
13. Audit Logs
14. Security and Roles
15. AI Operations Layer

## AI advantage layer

Our system should do what classic systems do not do well:

- predict donor vehicle profit before purchase
- suggest which parts to remove
- detect missing part fields
- suggest price from history and market
- suggest warehouse location
- generate listing titles and descriptions
- warn about bad photos
- detect slow-moving stock
- detect overpriced or underpriced stock
- warn about late orders
- warn about unpaid orders
- calculate worker productivity
- calculate profit by donor vehicle

## Final product implication

A 100 percent working product needs both operational modules and intelligence modules.

Without donor vehicle profitability, warehouse execution, marketplace channels, order/shipment flow and audit logs, it is only a prototype.
