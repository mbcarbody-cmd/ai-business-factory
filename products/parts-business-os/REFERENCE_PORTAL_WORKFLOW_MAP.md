# Reference Portal Workflow Map

Source: user-provided screenshots of an internal seller portal. This document extracts workflow architecture only. It is not a clone plan.

## Observed top-level modules

- Main dashboard
- Analytics
- Vehicles
- Parts
- Warehousing
- Orders
- Finance
- Shipments
- Tasks
- Employees
- Settings
- Help
- Sales channels

## Dashboard patterns

Observed dashboard cards and charts:

- sales revenue by period
- returns amount
- online sales
- local sales
- internet sales count
- revenue line chart
- parts without price
- order status summary
- returns and disputes
- seller status indicators
- average sold part value
- sold parts by channel

Required in our product:

- revenue by channel
- uploaded parts vs sold parts
- average sale price
- return ratio
- cancelled order ratio
- late order ratio
- worker productivity
- parts without price
- parts without location
- parts without photos
- parts without OEM code

## Orders module

Observed order list includes:

- search
- date from
- date to
- sales channel filter
- delivery method filter
- status filter
- order ID and date
- sales channel
- parts column with thumbnail and item count
- customer column
- invoice document icon
- carrier column
- carrier icons
- photo / label action buttons
- status label with timestamp
- order value
- actions column

Required in our product:

- all orders
- priority orders
- new orders
- overdue orders
- unfinished orders
- returns list
- sales reports
- documents
- order status timeline
- payment status
- shipment status
- invoice status

## Shipping module

Observed shipping functions:

- new shipment
- all shipments
- shipment reports
- packaging materials
- carrier integrations
- label print actions
- shipment status

Required in our product:

- carrier provider table
- package size and weight
- shipping label generation placeholder
- tracking number
- shipment history
- packing task for workers
- packing material inventory
- failed shipment queue

## Parts module

Observed parts functions:

- add part
- add single part
- add sold part
- part search
- all parts
- parts without price
- sold parts
- reserved parts
- mass actions

Required in our product:

- part ID
- OEM codes
- vehicle fitment
- VIN source vehicle
- category
- side
- condition
- defect notes
- warehouse location
- price
- photo workflow
- listing status
- reservation status
- sold status
- return status
- bulk edit
- bulk price update

## Vehicle module

Observed vehicle functions:

- add vehicle
- vehicle search
- all vehicles
- vehicle statistics

Required in our product:

- vehicle intake
- VIN
- make/model/year/body/engine
- donor vehicle photos
- dismantling task list
- parts extracted from vehicle
- vehicle profitability
- unsold stock by vehicle

## Warehouse module

Observed warehouse functions:

- all storage locations
- fill storage location

Required in our product:

- warehouse map
- shelf/rack/bin hierarchy
- location capacity
- occupied/free status
- part put-away task
- move part task
- missing location queue
- barcode or QR location label

## Employee and task module

Observed employee and task functions:

- tasks
- employees
- user statistics

Required in our product:

- employees
- roles and permissions
- task assignment
- task status
- time tracking
- worker performance
- task history
- photo proof
- part linked to task

## Settings module

Observed settings functions:

- integrations
- stock import and export
- invoice generation settings
- printing settings
- vacation mode
- order settings
- sales channels

Required in our product:

- sales channel settings
- import/export settings
- print templates
- invoice templates
- carrier settings
- user roles
- security settings
- API key storage rules
- vacation / away mode

## Data model draft

Core tables:

- users
- roles
- employees
- vehicles
- parts
- part_photos
- warehouse_locations
- orders
- order_items
- customers
- shipments
- invoices
- returns
- tasks
- sales_channels
- integrations
- analytics_events
- settings
- audit_logs

## Better-than-reference ideas

Our system should add AI and automation:

- AI price suggestion
- AI missing field detection
- AI photo quality check
- AI part title and listing text
- AI OEM / fitment helper
- AI warehouse location suggestion
- AI task creation from missing data
- AI order risk warning
- AI late order warning
- AI return risk warning
- AI sales channel comparison
- AI profit per donor vehicle

## Security requirements

Because this is an operational business system, final product must include:

- role based access
- protected admin pages
- safe file upload rules
- audit log
- API key protection
- backup plan
- login session protection
- server health checks
- log monitoring

## Product conclusion

The final system is not only a parts listing tool. It must be a full operating system for a used parts business:

vehicle intake -> parts creation -> photos -> price -> storage -> listing -> order -> invoice -> shipping -> return -> analytics -> worker accountability.
