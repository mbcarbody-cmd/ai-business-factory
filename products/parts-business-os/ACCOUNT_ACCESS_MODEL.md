# Account Access Model

Purpose: define the complete account hierarchy for the B2B Parts and Asset Business OS.

## Core rule

This is not one simple login system. It needs several account layers with strict separation.

## Account layers

### 1. Master Account

The platform owner account.

Can:

- see all sellers
- see all seller applications
- approve or reject sellers
- suspend sellers
- access global dashboard
- manage platform settings
- manage global categories
- manage global marketplace templates
- manage global pricing rules
- manage support tickets
- view platform-level analytics
- create platform admin accounts
- inspect audit logs

Cannot:

- silently change seller stock without audit log
- bypass security logging
- access customer private data without reason logging

### 2. Platform Admin Account

Internal platform staff account.

Can:

- review seller applications
- approve seller onboarding if permission granted
- support sellers
- inspect seller setup issues
- manage help content
- manage category mapping
- investigate failed syncs
- view operational dashboards

Permissions depend on role:

- support admin
- finance admin
- technical admin
- marketplace admin
- security admin

### 3. Seller Organization Account

The company account for a seller.

Contains:

- company data
- VAT mode
- invoice settings
- warehouse settings
- sales channel settings
- shipping settings
- return settings
- subscription/billing status later

Seller organization can be:

- application
- approved
- invited
- active
- suspended
- closed

### 4. Seller User Accounts

Users inside a seller organization.

Roles:

- seller owner
- seller admin
- manager
- pricing specialist
- warehouse worker
- photographer
- packing worker
- finance user
- support/order user
- readonly auditor

Permissions must be role-based.

### 5. Customer / Buyer Account

E-shop buyer account.

Types:

- guest customer
- individual customer
- business customer

Customer can:

- browse stock
- see clear price wording
- place order
- view own orders
- view invoices where allowed
- request return
- save delivery data

Customer cannot:

- access seller admin
- see internal seller cost
- see donor asset profitability
- see internal audit logs

## Login areas

The system should separate login areas:

- platform master/admin login
- seller portal login
- e-shop customer login

They may share authentication service, but permissions and UI must be separated.

## User isolation rules

Required:

- seller A cannot see seller B data
- customer cannot see seller internal data
- warehouse worker sees only allowed tasks
- finance user sees finance screens only
- platform admin actions are audited
- master account actions are audited

## Important permissions

### Donor asset

- create donor asset
- edit donor asset
- view cost
- view profitability
- delete/archive donor asset

### Parts

- create part
- edit part
- upload photos
- edit photos
- set price
- change location
- reserve part
- sell part
- write off part

### Orders

- view orders
- edit order
- change payment status
- create shipment
- cancel order
- handle return

### Finance

- view cost
- view margin
- view VAT reports
- create invoice
- issue refund

### Settings

- manage users
- manage roles
- manage VAT settings
- manage sales channels
- manage carrier settings
- manage invoice settings

## Invite flow

Seller users should be invited by seller owner or seller admin.

Flow:

1. Seller admin enters email.
2. Chooses role.
3. Invite token is generated.
4. User sets password.
5. User accepts terms.
6. User becomes active.

Invite security:

- token expiration
- one-time token
- audit log
- resend invite
- revoke invite

## Master account protection

Master account must have stronger protection:

- strong password
- 2FA later
- IP/session logging
- action audit log
- no shared master password
- emergency recovery procedure
- limited number of master users

## Account status model

User statuses:

- invited
- active
- disabled
- suspended
- deleted/archive

Organization statuses:

- application
- review
- approved
- invited
- active
- suspended
- closed

Customer statuses:

- guest
- registered
- verified
- blocked

## Audit requirements

Must log:

- login
- failed login
- invite created
- invite accepted
- role changed
- seller approved
- seller suspended
- VAT mode changed
- price changed
- order status changed
- payment status changed
- shipment created
- customer data viewed by admin

## Final access model

Platform owner controls the ecosystem.
Platform admins operate the platform.
Seller organizations manage their own stock and staff.
Seller users work by permissions.
Customers buy in e-shop.

No account type should accidentally see another account type's private data.
