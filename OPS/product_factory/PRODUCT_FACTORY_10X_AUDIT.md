# Product Factory 10x Audit Checklist

Updated: 2026-06-15  
Owner: QA Critic-C5 / Product Factory COO  
Status: active

## Purpose

Validate that the product factory expansion is real, measurable and tied to production output.

## Required files

- `OPS/org/product_factory_10x_staffing.json`
- `OPS/org/PRODUCT_FACTORY_10X_STAFFING_LT.md`
- `OPS/product_factory/DAILY_PRODUCT_FACTORY_LOOP_LT.md`
- `OPS/TASK_BOARD/product_factory_10x_tasks_2026_06_15.json`

## Required staffing checks

- total_functions = 10
- workers_per_function = 10
- total_worker_agents = 100
- every function has mission, KPI, input and output
- every function has exactly 10 worker-agent roles
- every worker-agent belongs to one production function

## Required task checks

- manifest contains 10 operating tasks
- each task has owner, status, priority, next_role, next_action, output_path and done_proof
- blocked tasks require blocker and fallback before they can remain active
- ready tasks must point to an executable next_action
- done tasks require proof path or public/revenue/client verification

## Required daily checks

Each active product cycle must answer:

1. What was shipped?
2. What moved closer to money?
3. What is blocked?
4. What fallback was started?
5. What did QA reject?
6. What did CFO recommend?
7. What is the next highest-value action?

## Release rule

A product or feature cannot be called done unless it has at least one proof type:

- repo file path
- public URL
- smoke test note
- QA verdict
- conversion verdict
- lead pipeline row
- outreach sequence
- quote/payment path
- CFO verdict
- client or revenue verification
