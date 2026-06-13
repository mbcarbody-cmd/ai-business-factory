# Marketplace Roadmap

Owner: MARKET-1 Marketplace General Manager

## Purpose

Create a path from internal operating system to a parts commerce marketplace.

## Strategic path

1. Internal OS for inventory, pricing, location and listing control.
2. Seller cockpit for one seller.
3. Multi-seller listing engine.
4. Buyer search and inquiry/order flow.
5. Payment/order/reservation workflow.
6. Marketplace analytics and liquidity scoring.

## Core modules

### Seller module

- seller profile
- warehouse profile
- roles/users
- listing rules
- payout/payment settings later

### Part module

- part number
- category
- vehicle fitment
- side/position
- condition
- photos
- price
- floor price
- liquidity score
- location
- status

### Parts category tree / taxonomy module

Primary file: `OPS/marketplace/parts_category_tree.json`

Purpose:

- canonical category IDs for every part,
- LT/EN names and aliases for title/search/listing generation,
- side and position normalization,
- storage profile for location suggestion,
- category/subcategory mapping for one-seller MVP,
- stable IDs so analytics, warehouse logic and marketplace search do not depend on messy free text.

MVP rule: every added part must map to `category_id`, `subcategory_id`, `side`, `position` and `storage_profile` before listing or location suggestion.

### Warehouse/location module

- zone
- shelf
- box/bin
- capacity
- dimensions
- weight rules
- occupancy percent
- suggested placement
- pending-location queue

### Listing module

- title
- description
- price
- marketplace status
- channels
- publish/unpublish
- duplicate detection
- quality warnings

### Buyer module

- search
- filter by vehicle/part number/category
- compatibility confidence
- inquiry
- order/reservation

### Order/payment module

- reservation
- invoice/payment state
- pick/pack/ship
- return state
- margin tracking

### Search module

- part number search
- synonym search
- vehicle model search
- category search
- typo handling
- ranking by availability, price and seller reliability

## First MVP slice

Internal seller OS:

1. Add part.
2. Map part to category tree.
3. Assign or suggest location from category/storage profile.
4. Add price and floor price.
5. Generate listing status.
6. Track reservation/order state.
7. Track inventory ageing and dead-stock risk.

## Data entities

- Seller
- Warehouse
- Location
- Part
- PartCategory
- Vehicle
- Listing
- PriceRecord
- Reservation
- Order
- Shipment
- Return
- CompetitorPrice
- DemandSignal

## Gate to start build

Before build starts:

- first workflow diagram exists,
- data model exists,
- category tree exists,
- MVP slice accepted,
- competitor gap checked,
- CFO value case written,
- delivery/use case proof identified.
