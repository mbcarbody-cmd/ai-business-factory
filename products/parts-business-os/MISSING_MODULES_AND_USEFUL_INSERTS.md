# Missing Modules and Useful Inserts

Source: user-provided screenshots from internal parts business systems. This document captures what is still missing and what useful improvements should be inserted into the final product.

## 1. Universal category system

The product must not be limited to cars.

Required asset categories:

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
- snowmobiles and snow bikes
- ATVs and UTVs
- planes
- helicopters
- other machines and equipment

## 2. Category-specific technical fields

A universal system needs shared fields plus category-specific fields.

Shared fields:

- manufacturer
- model
- modification
- year
- VIN / serial number / hull ID
- engine code
- engine size
- fuel or power type
- power
- gearbox / drive system
- color
- color code
- mileage / hours
- condition
- location
- notes

Examples by category:

- cars: body type, steering side, drivetrain, registration year
- motorcycles: frame number, engine number, cc, type, ABS, odometer
- trucks: axle configuration, wheelbase, gross weight, body configuration
- tractors: working hours, PTO, hydraulics, cabin, attachments
- boats: hull ID, length, material, inboard/outboard, engine hours
- jet skis: hull ID, jet pump, impeller, engine hours
- planes: serial number, airframe hours, engine hours, certificate status
- helicopters: airframe hours, rotor hours, component certificates

## 3. Reservation and internal sale flow

Observed missing layer: reservation modal.

Required fields:

- order type
- payment method
- customer type: guest / individual / business
- delivery type: pickup / shipping
- comment
- currency
- sale price
- discount percentage
- discount amount
- reservation until date

Useful additions:

- reserve stock immediately
- prevent double sale
- reservation expiry warning
- convert reservation to order
- cancel reservation with reason
- audit log for reservation changes

## 4. Vehicle and donor asset information page

Observed detailed vehicle data.

Required fields:

- fuel type
- mileage or hours
- engine size
- engine power
- engine code
- gearbox type
- gearbox code
- body type
- driven wheels / drivetrain
- steering side / position
- color
- color code
- interior
- defect notes
- production period
- production year
- first registration year
- VIN
- plate number where allowed
- dismantling status
- dismantling date
- manufacturer
- model
- modification

Useful additions:

- AI decode VIN / serial data where possible
- AI missing field warning
- AI mismatch warning between VIN and entered fields
- AI profit forecast per donor asset

## 5. Donor asset statistics

Observed statistics card:

- acquired date
- time since acquired
- profit
- purchase price
- revenue
- total stock value
- remaining parts value and count
- sold parts value and count
- parts without price value and count
- sales channel revenue split

Required additions:

- ROI percentage
- break-even progress
- days to break-even
- slow-moving donor assets
- profitable vs unprofitable donor assets
- AI suggestion: reduce prices / bundle parts / promote stock

## 6. Order detail page

Observed order detail fields:

- order state
- order type
- date
- ordered by
- location
- comment / external link
- part list with images
- prices
- invoice area
- payment block
- delivery address or pickup
- payment method
- paid status
- shipping provider
- tracking number
- shipping photos
- shipping label
- print invoice action

Required additions:

- picking checklist
- packing checklist
- scan before shipping
- shipment photo proof
- worker assigned to packing
- late order warning
- unpaid order warning
- order risk score

## 7. Photo and image editor

Observed photo viewer and editor:

- photo thumbnails
- main image preview
- rotate left / right
- reset
- angle slider
- crop
- edit
- text tool
- save

Required additions:

- main photo selector
- required photo angles by category
- AI duplicate photo detection
- AI bad background warning
- AI blurred photo warning
- AI missing defect photo warning
- before publishing quality gate

## 8. Operation history

Observed operation history:

- user initials
- action time
- uploaded to marketplace
- changed price from old to new
- added price

Required audit fields:

- entity type
- entity ID
- user
- action
- old value
- new value
- timestamp
- source channel
- IP/session metadata for security where appropriate

## 9. Advanced filters

Observed filters are very deep. Our product needs saved power filters.

Required:

- manufacturer
- model
- modification
- year from / to
- category
- fuel / power type
- engine size from / to
- engine power from / to
- body / machine type
- color
- color code
- steering / drive side
- drivetrain
- gearbox
- location
- condition
- marketplace status
- channel status
- price from / to
- upload date from / to
- OEM / reference code
- VIN / serial / hull ID
- active sales
- unpriced parts
- defective parts
- hidden parts

Useful additions:

- saved filter presets
- manager default filters
- worker default filters
- export filter results
- bulk edit selected results

## 10. Marketplace channel control

Observed sales channel cards:

- eBay
- RRR-like marketplace
- Allegro
- Amazon
- Autoteile-Markt
- dalys.lt
- other channels

Required:

- channel account connection
- active / inactive state
- safe credential storage
- sync status
- error queue
- update account action
- marketplace-specific templates
- per-channel listing status

Useful additions:

- AI channel recommendation
- AI title adaptation per marketplace
- AI translation per marketplace
- channel profitability report

## 11. Shipping and packing

Observed shipment fields:

- search by ID, shipment number or receiver
- requested carrier
- ordered shipment
- manifest
- submitted to carrier

Required:

- package type
- package size
- weight
- carrier
- tracking
- manifest
- label
- shipment photos
- packing material usage
- packing task
- failed shipment queue

## 12. Missing final-product modules

These are still required for a 100 percent working product:

- auth and roles
- permission matrix
- real database
- audit log
- universal asset category engine
- donor asset profitability
- part lifecycle
- photo studio
- price history
- marketplace sync queue
- warehouse locations
- barcode / QR scanning
- worker task board
- order workflow
- payment workflow
- shipment workflow
- returns workflow
- finance reports
- analytics dashboard
- backup system
- monitoring
- security review
- user guide
- support process

## Strategic insertion: AI operations layer

AI must not be just a chat box. It must be inside workflows:

- AI suggests missing fields
- AI validates category-specific data
- AI predicts donor asset profit
- AI suggests part price
- AI detects photo quality issues
- AI suggests warehouse location
- AI creates worker tasks
- AI warns about late orders
- AI finds slow-moving stock
- AI compares channels
- AI calculates profitability by donor asset and category

## Product direction

The product should become Parts and Asset Business OS, not only auto parts inventory.

Final flow:

asset purchase -> technical data -> dismantling -> parts -> photos -> pricing -> location -> marketplace channels -> order -> payment -> packing -> shipping -> return -> audit -> analytics -> AI improvement loop.
