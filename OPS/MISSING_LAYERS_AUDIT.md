# Missing Layers Audit — converted to active OPS layers

Date: 2026-06-12

This audit originally listed what was missing for a serious autonomous product company system. The missing layers have now been converted into file-backed operating layers.

## Why the layers were missing

The repo had product direction and agent leadership definitions, but the agents did not yet have mandatory work surfaces. That created a gap between strategy and execution.

Root causes:

1. Roles existed before workflows.
2. Strategy documents existed before task state.
3. Product ambition existed before deploy, QA, CFO, revenue and delivery gates.
4. Agents had responsibilities, but not enough required output files.
5. There was no hard operating rule that work is not done until it changes a tracked artifact.

## Fixed layer map

| Layer | Original missing item | Active file-backed layer |
|---|---|---|
| True task board | shared task database, owner, status, next role, output path, priority | `OPS/task_board.json` |
| Agent memory | decisions, weak-work memory, competitor findings, lessons | `OPS/agent_memory/` |
| Competitor intelligence | alternatives, price/features/positioning/gaps | `OPS/competitor_intelligence/` |
| Product maturity gates | stages, release checklist, sell-ready checklist | `OPS/product_gates/` |
| Real deployment loop | deploy, service status, health check, rollback | `OPS/deploy_loop/` |
| QA and critic layer | breaker, missing feature report, unusable demo report | `OPS/qa/` |
| Revenue operations | target, contact, reply, demo, invoice state | `OPS/revenue_ops/` |
| CFO layer | cost, build time, price, margin, break-even | `OPS/cfo/` |
| Customer delivery layer | intake, delivery SOP, handoff, support process | `OPS/delivery/` |
| Marketplace vision map | internal OS to marketplace, seller/buyer/listing/payment/search | `OPS/marketplace/roadmap.md` |

## New operating loop

research -> decide -> task -> build -> review -> deploy -> sell -> learn

## Current status

The layers are no longer just missing notes. They now exist as repo files and must be used by agents.

Core control file: `OPS/CORE_OS_STATUS.md`

Task control file: `OPS/task_board.json`

## Remaining real work

The structure is now created, but it must be populated and used:

1. Add real competitors.
2. Add real leads.
3. Run product gate reviews.
4. Add deploy commands and health checks for actual deployed products.
5. Record QA bugs from real demos.
6. Track real cost, time, margin and paid pilots.
7. Use delivery intake on the first paid client.
8. Convert marketplace roadmap into first MVP data model and workflow.

## Hard rule from now on

Agent output without an updated OPS file, product artifact, test proof, deploy proof, sales path or delivery proof is not counted as completed work.
