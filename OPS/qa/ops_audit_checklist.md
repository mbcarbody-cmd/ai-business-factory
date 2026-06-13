# OPS Audit Checklist

Owner: CTO-3 Systems Reliability Breaker
Status: active
Updated: 2026-06-13

## Purpose

This checklist is the manual guardrail until a CI script is added locally.

## Required files

- `OPS/task_board.json`
- `OPS/CORE_OS_STATUS.md`
- `OPS/agent_memory/README.md`
- `OPS/agent_memory/decision_log.md`
- `OPS/agent_memory/weak_work_patterns.md`
- `OPS/operating_loops/ANTI_STAGNATION_ENGINE.md`
- `OPS/competitor_intelligence/competitors.json`
- `OPS/product_gates/product_stages.json`
- `OPS/deploy_loop/deploy_sop.md`
- `OPS/qa/bug_board.json`
- `OPS/revenue_ops/lead_pipeline.json`
- `OPS/cfo/costs.json`
- `OPS/delivery/72h_delivery_playbook.md`
- `OPS/marketplace/roadmap.md`
- `OPS/marketplace/parts_os_mvp_data_model.json`
- `OPS/model_council/AI_CAPABILITY_RADAR_2026.md`
- `products/ceo-cockpit/index.html`

## Required task fields

Every task must have:

- id
- title
- layer
- owner
- status
- priority
- deadline
- money_path_or_strategic_reason
- next_role
- next_action
- blocker
- fallback_next_task
- output_path
- done_proof
- proof_status
- proof_verified_by

## Audit rules

- Blocked task without fallback is invalid.
- Done task without proof path is invalid.
- Done task with missing proof is invalid.
- Ready task without deadline is invalid.
- New sales action without lead tracking is invalid.
- New deploy without health check and rollback is invalid.
- New product without gate status is invalid.

## Next automation task

Convert this checklist into a local CI script once the task board schema stabilizes.
