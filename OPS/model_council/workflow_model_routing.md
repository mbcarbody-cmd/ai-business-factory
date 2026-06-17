# Workflow Model Routing and Challenger Policy

Date: 2026-06-17
Owner: AI Workflow Engineer + Evaluation Engineer + CFO
Status: active

## Purpose

Use the best model or tool for each job instead of sending every task to one general model. Routing must optimize quality, proof, cost, latency and risk.

## Routing dimensions

Every task is classified by:

- domain: parts, warehouse, pricing, sales, coding, design, legal/risk, research;
- consequence: reversible, customer-facing, financial, destructive or irreversible;
- evidence need: deterministic data, web verification, repository state, human judgment;
- complexity: single-step, multi-step, tool-heavy, long-context;
- output type: decision, code, structured data, message, calculation, workflow action;
- freshness: stable, current, real-time;
- confidence and fallback requirement.

## Route classes

1. **Deterministic engine first** — mathematics, stock balances, capacity, price formulas, validation and state transitions.
2. **Specialist agent first** — domain judgment, workflow decisions and exception handling.
3. **Multi-model council** — high-value strategy, unclear evidence, pricing uncertainty, legal/reputation risk and product selection.
4. **Tool-grounded route** — repository, email, public web, payment, deployment or analytics facts.
5. **Human gate** — spending, contracts, irreversible publication, legal commitments and high-impact exceptions.

## Champion/challenger rule

For important recurring workflows, keep:

- one champion route used in production;
- at least one challenger prompt/model/tool route;
- a shared evaluation set;
- cost, latency and quality records;
- a rollback route.

No challenger becomes champion because it sounds better. It must beat the champion on the defined primary KPI and pass all protected-capability regressions.

## Required routing record

Every routed task must record:

- task id;
- selected route;
- why that route was selected;
- expected quality/cost/latency;
- fallback route;
- confidence;
- actual result;
- evaluation score;
- whether the route should gain or lose future traffic.

## Traffic allocation

- New challenger: maximum 10% of eligible low-risk tasks.
- Proven challenger: up to 30%.
- Promotion candidate: up to 50% with Judge monitoring.
- Champion: remaining traffic.
- Critical failure: immediate quarantine and rollback.

## Commercial routing law

The cheapest route is not automatically best. The best route is the lowest total-cost route that reaches accepted proof without rework, risk breach or lost revenue.

## Anti-lock-in rule

Critical workflows must have:

- one primary model/tool route;
- one fallback model/tool route;
- one deterministic or manual emergency path where possible;
- versioned prompts and schemas;
- no hidden dependency on a single vendor-specific behavior.

## Daily improvement requirement

The Model Council must compare at least three meaningful workflow routes daily and update the routing ledger only when evidence supports a change.
