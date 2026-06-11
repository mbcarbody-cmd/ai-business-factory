# Nuance Rules

Agents must not only list visible fields. They must infer business rules, edge cases and workflow consequences.

## Mandatory questions

After every screenshot or workflow review, agents must ask:

- Who is the user?
- Is it B2B, B2C or internal admin?
- Is access open, invite-only or approval-based?
- What happens before this screen?
- What happens after this screen?
- What user states exist?
- What seller or customer types exist?
- What tax modes exist?
- What approval steps exist?
- What can fail?
- What must be logged?
- What must be protected?
- What must stay fast?
- What edge cases can break the workflow?

## Seller platform rule

For seller platforms, agents must always check:

- seller application
- company data
- VAT payer or non-VAT mode
- planned stock count
- planned monthly upload count
- sales channels
- shipping ability
- return process
- approval flow
- invite flow
- suspension flow

## Responsibility

- Analyst finds hidden rules.
- Product role converts them to requirements.
- Builder waits for hidden rules before building.
- QA tests edge cases.
- Auditor records missed details.

## Example

A login page does not mean public self-registration.

For B2B seller systems, the correct flow may be:

application -> review -> approval -> invite -> account setup -> onboarding.
