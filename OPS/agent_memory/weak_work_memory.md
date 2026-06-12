# Weak Work Memory

Purpose: remember work patterns that produced low value, so future agents avoid them.

## Pattern 1 — Role descriptions without operating files

Date: 2026-06-12

Issue: the repo had strong role definitions, but some roles did not yet have required files where their work had to be recorded.

Result: agents could sound strategic while not moving task state, revenue state, QA state, deploy state or delivery state.

Correction: every agent now needs to update a file-backed layer or produce a concrete artifact.

Linked files:

- `OPS/CORE_OS_STATUS.md`
- `OPS/task_board.json`
- `OPS/product_gates/release_checklist.md`

## Pattern 2 — More ideas before closing the loop

Date: 2026-06-12

Issue: expanding product ideas before closing research -> decide -> task -> build -> review -> deploy -> sell -> learn creates chaos.

Correction: new ideas enter product gates first and must show buyer, price logic, QA path, deploy path and sales path.

Linked file: `OPS/product_gates/product_stages.json`

## Pattern 3 — Work without money awareness

Date: 2026-06-12

Issue: product and agent work can look busy while not increasing revenue probability.

Correction: P0 work must connect to revenue, delivery, deploy, QA, CFO, marketplace value, or core OS closure.

Linked files:

- `OPS/revenue_ops/lead_pipeline.json`
- `OPS/cfo/costs.json`
- `OPS/delivery/72h_delivery_playbook.md`
