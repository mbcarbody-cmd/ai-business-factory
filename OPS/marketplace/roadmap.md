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
2. Assign or suggest location.
3. Add price and floor price.
4. Generate listing status.
5. Track reservation/order state.
6. Track inventory ageing and dead-stock risk.

## Data entities

- Seller
- Warehouse
- Location
- Part
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
- MVP slice accepted,
- competitor gap checked,
- CFO value case written,
- delivery/use case proof identified.
