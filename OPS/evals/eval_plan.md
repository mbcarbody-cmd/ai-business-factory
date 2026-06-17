# Agent Evaluation and Regression Plan

Date: 2026-06-17
Owner: Evaluation Engineer + Judge Agent
Status: active

## Purpose

Stop agents from claiming improvement without measurable proof. Every important agent capability must have repeatable test cases, failure thresholds and a rollback rule.

## Evaluation families

1. **Business judgment** — buyer, pain, value, margin, risk, priority, next action and kill criteria.
2. **Execution completeness** — object created or changed, status moved, proof recorded, fallback defined.
3. **Parts commerce** — code normalization, category, fitment confidence, price/floor, listing readiness, location, reservation and stock state.
4. **Warehouse/WMS** — dimensions, weight, category constraints, capacity, directed putaway, scan confirmation, stock movement and exception handling.
5. **Revenue** — verified lead, personalized message, reply handling, quote, payment path, delivery handoff and renewal.
6. **Quality and safety** — unsupported claims, duplicated work, broken links, secrets, permissions, platform rules and data provenance.
7. **Tool use** — correct tool selection, successful execution, error recovery, audit log and idempotency.
8. **Learning quality** — lesson provenance, causal hypothesis, reusable rule, regression case, promotion decision and post-change effect.

## Mandatory case types

Every promoted change needs:

- one normal case;
- one edge case;
- one adversarial or misleading-input case;
- one regression case from a previously solved failure;
- one commercial or operational effect check.

## Scoring

- Accuracy and factual support: 25
- Complete operational action: 20
- Business value and prioritization: 15
- Risk, permissions and compliance: 15
- Proof and auditability: 10
- Cost and latency: 5
- Robustness and fallback: 10

Promotion threshold: **85/100**, no critical veto, and no regression greater than 3 percentage points on a protected capability.

## Protected capabilities

A learning change may never silently degrade:

- source and price provenance;
- stock accuracy;
- location and capacity constraints;
- payment evidence;
- legal/privacy limits;
- security and access control;
- release rollback;
- margin floor;
- truthful completion claims.

## Champion/challenger protocol

1. Run the current agent instruction/model/tool route as champion.
2. Run the proposed instruction/model/tool route as challenger on the same cases.
3. Compare success, score, cost, latency and veto breaches.
4. Promote only the smallest change that explains the improvement.
5. Keep the prior version available for rollback.
6. Recheck the promoted change after seven days of real use.

## Skill gates

- `research_only`: may inspect and draft, not change production state.
- `supervised`: may execute with Judge review.
- `autonomous`: may execute reversible work inside permission limits.
- `trusted_owner`: may own a full specialty workflow and challenge CEO direction.
- `quarantined`: no production work until remediation cases pass.

## Daily eval requirement

Every day the system must add at least three meaningful cases from real failures, customer behavior, warehouse exceptions, revenue friction or verified market changes. Synthetic cases are allowed only when real data is unavailable and must be marked as simulation.

## Done proof

A capability is improved only when:

- the evaluation case exists;
- champion and challenger results exist;
- the change is versioned;
- affected agents are identified;
- the skill ledger is updated;
- the knowledge sync bus records propagation;
- post-change metrics confirm or reject the promotion.
