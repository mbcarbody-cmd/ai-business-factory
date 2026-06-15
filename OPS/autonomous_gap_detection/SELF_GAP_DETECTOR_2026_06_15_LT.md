# Autonomous Self-Gap Detector — LT

Date: 2026-06-15
Owner: CEO / Master Agent + QA Critic-C5 + COO-1 Execution Architect
Status: active

## Purpose

This layer forces the system to find missing execution proof by itself. The old operating system checked whether files existed, but it did not aggressively check whether the chain reached public demo, verified leads, payment path, QA verdict, paid pilot and delivery proof.

## Mandatory question per CEO cycle

Every CEO cycle must answer:

1. Which revenue or product proof is still missing?
2. Where did the chain stop between repo artifact and buyer proof?
3. Which specialist owns the next proof file?
4. What fallback is active if the main path is blocked?
5. Did every blocker become a task with owner, output and proof condition?

## Reality-loop gates

A product cannot be considered progressing unless it has at least one tracked state for each gate:

- public_url or explicit_no_url_blocker;
- smoke_test_result;
- QA PASS / BLOCKED / ACCEPTED_RISK verdict;
- verified lead rows;
- quote or payment path;
- delivery intake path;
- CFO continue / stop decision;
- next revenue action.

## Specialist auto-routing

| Missing proof | Specialist | Required output |
|---|---|---|
| Exact leads missing | Revenue Lead Verification Specialist | `OPS/revenue_ops/lead_pipeline.json` |
| Payment path missing | Payment / Quote Operations Specialist | `OPS/revenue_ops/payment_path.md` |
| Public URL missing | Public Demo Publisher / Release Engineer | `OPS/deploy_loop/public_demo_registry.json` |
| Seller workflow missing | Product Workflow Architect | `products/parts-seller-os/WORKFLOW_SPEC.md` |
| Conversion quality weak | UX / Conversion Designer | `OPS/design/conversion_design_review.md` |
| Release veto missing | QA Breaker With Release Veto | `OPS/qa/bug_board.json` |
| Delivery proof missing | Delivery Manager / 72h Pilot Operator | `OPS/delivery/pilot_delivery_registry.json` |

## Escalation rule

If a missing proof is detected and no task is created during the same operating cycle, the issue escalates to CEO / Master Agent and COO-1. The escalation must create:

1. task id;
2. owner;
3. output path;
4. proof condition;
5. fallback action;
6. release or revenue block rule.

## Anti-guessing rule

The user should not need to guess what is missing. The system must generate a missing-proof report after every core OS check.

## Done proof

This layer is active when:

- specialist gap task manifest exists;
- specialist required files exist;
- local or CI audit checks those files;
- CORE_OS_STATUS states remaining proof gaps;
- blockers have fallback tasks.
