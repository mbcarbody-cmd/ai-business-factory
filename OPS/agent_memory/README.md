# Agent Memory Layer

Owner: PMO-2 Documentation & Memory Keeper
Status: active
Updated: 2026-06-13

## Purpose

This folder is the long-term memory of the operating system. It prevents agents from repeating weak work, forgetting decisions, rebuilding the same plans, or treating unfinished work as done.

## Memory rule

No important decision is valid until it is written into one of these files:

- `decision_log.md` — strategic and operating decisions.
- `lessons_learned.md` — mistakes, improvements, and repeated patterns.
- `weak_work_patterns.md` — examples of outputs that are not acceptable.

## Required entry format

Each memory entry must include:

- Date.
- Trigger.
- Decision or lesson.
- Reason.
- Affected OPS layer.
- Next enforcement rule.
- Proof path.

## Agent behavior

Before starting work, every agent must check whether a relevant decision or lesson already exists. After finishing work, the agent must add a memory entry if the work changed strategy, workflow, pricing, delivery, QA, deploy, security, marketplace logic, or revenue assumptions.

## Done definition

Memory is not a note archive. Memory is done only when it changes future behavior.
