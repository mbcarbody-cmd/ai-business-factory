# Technical Spine

Purpose: turn the agent system from role documents into an execution machine that builds, tests, deploys and closes work.

This folder is the execution backbone for Parts Business OS.

## Main rule

Agents are not complete when they write analysis. Agents are complete only when their work creates one of:

- database schema or migration
- backend endpoint
- frontend screen
- validation rule
- automated test
- deploy or rollback step
- QA bug report
- release gate result
- sales/demo asset connected to the product

## Current 10-track technical spine

1. Stable DB schema
2. Auth and roles
3. Part creation flow
4. Warehouse location engine
5. Worker task board
6. Pricing and listing intelligence
7. Order and reservation flow
8. QA automated tests
9. Deploy loop
10. Sales/demo page

## Agent execution loop

Every technical task must move through this loop:

```text
Priority -> Owner agent -> Output path -> Implementation -> Test -> QA critic -> Release gate -> Memory update -> Next task
```

## Definition of progress

Progress means changed repo files plus testable acceptance criteria.

A document-only task is allowed only when it unlocks build work in the next task.

## Definition of done

A technical spine task is done only when it has:

- owner agent
- changed paths
- run steps
- test steps
- acceptance criteria
- known risks
- next task
- QA status

## Current priority

Build the backbone of Parts Business OS before adding more disconnected products.

The first execution target is not beauty. It is operational control:

- create asset
- create part
- assign location
- create worker task
- price/list part
- reserve/sell part
- track order
- test flow
- deploy demo
