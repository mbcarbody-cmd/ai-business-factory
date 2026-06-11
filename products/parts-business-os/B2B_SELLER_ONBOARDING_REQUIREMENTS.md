# B2B Seller Onboarding Requirements

This product is B2B. A new seller should not instantly enter the system like a normal public user. A seller applies first, then admin reviews and grants access.

## Seller access model

Correct flow:

1. Seller opens application page.
2. Seller fills company and business information.
3. System validates required fields.
4. Admin reviews application.
5. Admin approves, rejects or asks for more info.
6. Approved seller receives invitation link.
7. Seller creates password and first admin user.
8. Seller chooses VAT / non-VAT mode.
9. Seller enters first stock/import settings.
10. Seller receives onboarding checklist.

## Seller account states

Required states:

- draft application
- submitted
- needs more information
- approved
- rejected
- invited
- active
- suspended
- closed

## Application fields

Company information:

- company name
- company code
- VAT payer yes/no
- VAT code if applicable
- country
- city
- address
- postal code
- company email
- company phone
- website
- contact person
- contact person role

Business information:

- business type
- dismantler / parts seller / importer / repair shop / dealer / other
- years active
- current sales channels
- current monthly order count
- current monthly revenue range
- approximate stock count
- planned monthly part upload count
- main categories sold
- warehouse size or location count
- number of employees
- countries served
- shipping carriers used
- return policy

Inventory information:

- current stock count
- planned upload count per month
- parts categories
- donor asset categories
- average photo count per part
- existing data format CSV / Excel / API / manual
- existing marketplace accounts
- price includes VAT yes/no

Operational readiness:

- can upload photos
- can print labels
- has warehouse locations
- has carrier accounts
- has invoice process
- has return handling
- has employee task process

## Required seller modes

### VAT payer seller

Seller must provide:

- VAT payer status
- VAT code
- default VAT rate
- invoice settings
- net/gross price preference

System must show:

- net price
- VAT amount
- gross price
- clear e-shop wording

### Non-VAT payer seller

Seller must provide:

- non-VAT status confirmation
- invoice wording
- final price mode

System must show:

- final price
- VAT not charged wording
- VAT amount zero

## Admin review checklist

Admin should review:

- company identity
- VAT status
- contact details
- real business activity
- stock count
- upload capacity
- categories
- shipping ability
- return handling
- data quality level
- risk level

## Risk scoring

System should score applications:

- missing company data
- no VAT data where expected
- no real contact
- very low stock count
- unrealistic upload plan
- no shipping method
- no returns process
- suspicious website/email mismatch

Risk result:

- low risk: approve
- medium risk: ask for more info
- high risk: manual review or reject

## Onboarding checklist after approval

Seller must complete:

1. Create admin user.
2. Set VAT mode.
3. Set company invoice data.
4. Add warehouse locations.
5. Add sales channels.
6. Add shipping carriers.
7. Upload first donor asset.
8. Upload first part.
9. Upload photos.
10. Set price.
11. Create test reservation.
12. Create test order.
13. Create test shipment.
14. Review dashboard.

## Access and security

Required:

- invite token expiration
- email verification
- strong password
- optional 2FA later
- role-based access
- admin approval logs
- suspension ability
- audit logs from first action

## Why this matters

This is not a public consumer registration product. It is a controlled B2B seller system. Seller quality affects marketplace quality, order quality, buyer trust and platform risk.

## Product implication

The first public page should be seller application, not direct self-service login.

Public flow:

Apply as seller -> review -> approval -> invitation -> account setup -> onboarding checklist -> first stock upload.
