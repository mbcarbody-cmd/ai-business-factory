# Recar Workflow Map

Source: user-provided screenshots of another internal parts business system. This document extracts workflow architecture only. It is not a copy plan.

## Observed modules

The left navigation shows a compact icon-based structure:

- home / dashboard
- warehouse or stock overview
- documents or intake
- vehicles
- orders / basket
- tools or service actions
- clipboard / tasks
- users
- logistics / handling
- shipments or forklifts
- packaging / boxes
- finance / payments
- invoices / documents

## Dashboard counters

Observed counters include:

- uploaded parts
- priced parts
- repriced parts
- reservations
- completed orders
- turnover
- completed returns
- return amount
- processed parts
- written-off parts
- picked parts
- ordered shipments
- eBay prepared parts
- eBay uploaded parts
- orders waiting for shipment
- late orders

## Purchase / donor vehicle module

Observed section: Purchases.

Vehicle categories:

- cars
- motorcycles
- trucks

Observed table columns:

- ID
- name / vehicle title
- cost price
- planned revenue
- sold value
- balance

Observed search and filters:

- ID, make, model, year or part name
- type
- manufacturer
- model
- modification
- body type
- fuel type
- engine size from / to
- year from / to
- color
- gearbox
- axle
- steering position
- title
- comment
- location

Required for our product:

- donor vehicle purchase card
- planned revenue per vehicle
- sold revenue per vehicle
- remaining stock value
- profit/loss per donor
- vehicle dismantling task list
- vehicle-to-parts link
- AI vehicle profitability estimate

## Orders module

Observed order analytics and filters:

- current month turnover
- previous month turnover
- yearly turnover
- quarter turnover
- order count
- return count
- order status
- sale type
- picking status
- latest expected delivery date
- paid or not
- sales channel account
- payment type
- customer search
- shipment
- issue date
- ordered date
- payment term
- delay
- part filters inside orders

Observed order table fields:

- order ID
- part thumbnail
- part title
- part location
- ordered by
- order date
- status
- amount without VAT
- paid flag

Required for our product:

- order analytics cards
- order filters
- part filters inside order search
- order table with images
- payment status
- picking status
- late order warning
- order issue / comment field
- AI order risk score

## Parts search module

Observed part filters:

- manufacturer
- model
- modification
- year from / to
- vehicle type
- steering position
- body type
- color
- color code
- engine power
- fuel type
- engine size
- part condition
- RRR status
- eBay status
- price from / to
- location
- comment
- OEM code
- VIN code
- active sales
- show unpriced parts
- hide defective parts
- Allegro status
- upload date range

Required for our product:

- dense advanced search
- saved filter presets
- missing data queues
- unpriced parts queue
- defective parts visibility toggle
- marketplace status columns
- AI missing-field detector
- AI duplicate detector

## Warehouse locations

Observed location search:

- search by location name

Required for our product:

- warehouse location hierarchy
- zone / row / shelf / bin
- location capacity
- location barcode or QR
- put-away task
- move task
- stock by location
- empty and full locations
- AI suggested location

## Users

Observed users section.

Required for our product:

- user list
- roles
- permissions
- worker statistics
- audit log
- task ownership

## Better product direction

Our Parts Business OS should combine the strongest patterns from the observed systems:

1. Dashboard like an operations control room.
2. Donor vehicle profitability from purchase to sold stock.
3. Dense filters for power users.
4. Worker task flow for warehouse execution.
5. Location-aware storage.
6. Multi-channel listing status.
7. Order, payment, picking and shipment flow.
8. AI layer over missing data, pricing, location and risk.

## Data model additions

Add or strengthen these tables:

- donor_vehicles
- donor_vehicle_costs
- donor_vehicle_revenue_plan
- part_marketplace_status
- part_search_index
- order_filters
- payment_status
- picking_status
- warehouse_zones
- warehouse_bins
- worker_activity_log
- marketplace_channels
- pricing_history
- ai_recommendations

## Final target

The final product should not be a simple inventory page. It should be a full operating system:

purchase vehicle -> dismantle -> create parts -> enrich data -> price -> store -> list -> sell -> pick -> pack -> ship -> handle returns -> analyze profit.
