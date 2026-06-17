# Release Registry

Date: 2026-06-17  
Owner: SPEC-013 Release Engineer  
Status: active

## Governing rule

No domain purchase, custom public address or equivalent public-address commitment is allowed before functional-product proof is recorded. A local demo, repository preview or temporary platform URL is the required fallback.

Functional-product proof requires one complete core workflow, repeatable smoke-test evidence, a named release owner and a rollback path. A landing page, design mockup or empty shell does not qualify.

## REL-001 Parts Seller OS shell

Local path: `products/_templates/parts-seller-os-one-day-mvp/index.html`  
External link: not recorded  
Functional-product proof: not recorded in this registry  
Domain state: blocked_until_functional_product  
Fallback: use the local static page or repository preview  
Check: local file exists  
Rollback: revert the product commit

## REL-002 CEO Cockpit

Local path: `products/ceo-cockpit/`  
External link: not recorded  
Functional-product proof: pending independent smoke test  
Domain state: blocked_until_functional_product  
Fallback: use the local cockpit path  
Check: pending  
Rollback: revert the product folder

## Next action

Complete a functional workflow and smoke test before adding any custom public address. Keep the no-domain rule active even when a temporary preview is available.
