# AI Cost Per Task Addendum

Owner: CFO / Pricing Controller
Status: active
Updated: 2026-06-13

## Purpose

Protect margin when using AI tools, coding agents and model calls.

## Formula

AI cost per task = model/tool spend + operator review time + retry cost + QA cost.

## Required tracking fields

- task type
- product or client
- model or tool used
- estimated calls or minutes
- estimated tool spend
- operator review minutes
- quality level required
- cheaper fallback model or tool
- reason if a stronger model is required

## Model routing rule

| Task type | Default route | Escalate when |
|---|---|---|
| simple rewrite, title, summary | cheap/fast model | brand, legal, or client-facing risk is high |
| data cleanup and classification | cheap/fast model plus QA sample | confidence is low or item value is high |
| pricing reasoning and rare-parts judgment | strong reasoning model | no market comps or expensive part |
| code changes | coding agent with repo rules | tests fail or security/deploy is affected |
| public sales copy | strong model plus Judge/CFO review | promise, pricing or compliance risk exists |
| customer delivery instructions | strong model plus Delivery review | support risk is high |

## CFO rule

No scaling paid delivery until AI/tool cost and operator review time are visible per workflow.
