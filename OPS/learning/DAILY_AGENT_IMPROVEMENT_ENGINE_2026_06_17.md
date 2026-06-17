# Daily Agent Improvement Engine

Date: 2026-06-17
Owner: Chief Learning Officer + Judge Agent + Domain Leads
Status: active

## Purpose

Force every agent to become measurably better every day. Reading, summarizing or creating policy files does not count as learning unless a tested operational rule, tool, dataset, prompt, workflow or decision threshold improves.

## Daily loop

1. Capture failures, wins, objections, pricing misses, user corrections, QA bugs, blocked tasks and external market signals.
2. Convert raw events into reusable lessons with source, confidence, scope and expiry date.
3. Create evaluation cases from real work.
4. Run champion-versus-challenger tests on the old and proposed method.
5. Promote only changes that improve quality, speed, revenue, cost, accuracy or safety without breaking regressions.
6. Share the promoted lesson with all affected agents.
7. Demote, retrain or restrict agents that repeatedly fail the same class of task.

## Required daily proof

Minimum per day across the factory:

- 10 learning events captured;
- 3 normalized lessons;
- 3 new or improved evaluation cases;
- 3 champion-challenger comparisons;
- 1 tested operational improvement promoted or 1 harmful rule removed;
- 1 cross-agent knowledge sync;
- 1 regression run on previously solved cases.

## Learning event schema

Each event must contain:

- event_id;
- agent_id;
- task_id;
- object affected;
- expected result;
- actual result;
- error or success pattern;
- evidence path;
- financial or operational impact;
- proposed lesson;
- confidence;
- reviewer;
- next test.

## Promotion gates

A lesson may become a production rule only when:

- evidence is real and traceable;
- at least one evaluation case reproduces the problem;
- challenger beats champion on the defined metric;
- regression tests do not degrade critical old cases;
- Judge Agent approves scope and rollback;
- the rule has an owner, version and review date.

## Agent skill score

Each specialist receives a rolling score from 0 to 100:

- 30% task outcome quality;
- 20% proof quality;
- 15% speed and throughput;
- 15% commercial or operational impact;
- 10% error recurrence rate;
- 10% knowledge sharing.

Rules:

- score >= 90: champion;
- 80-89: production-ready;
- 70-79: supervised;
- 60-69: retraining required;
- below 60: removed from critical work until re-certified.

## Anti-fake-learning rules

The following do not count by themselves:

- reading an article;
- summarizing a video;
- creating another agent role;
- writing another strategy document;
- changing a prompt without evaluation;
- claiming improvement without before/after metrics;
- copying a competitor feature without a buyer or workflow test.

## Mandatory learning layers

### Experience Replay Ledger
Stores real tasks, failures, corrections and successful outputs so agents train on actual factory history.

### Evaluation Harness
Keeps canonical test cases for pricing, listing, WMS, sales, outreach, payment, delivery and QA.

### Champion-Challenger Lab
Compares current production method against new prompts, tools, models, rules or workflows.

### Skill Graph and Certification
Maps every agent to explicit capabilities, score, evidence, weaknesses and re-certification date.

### Knowledge Distillation Router
Routes a verified lesson only to agents that need it, avoiding global prompt bloat.

### Forgetting and Expiry Layer
Removes outdated, contradicted or low-confidence lessons instead of allowing memory pollution.

### Model and Tool Router
Chooses the best model or tool per task based on measured quality, speed, cost and risk.

### Red-Team and Adversarial Layer
Continuously attacks workflows, claims, calculations, permissions and security assumptions.

## Daily owner update

The learning owner update must report only:

- what capability improved;
- old versus new score;
- what was promoted;
- what was rejected;
- what agents were promoted, demoted or retrained;
- measurable KPI effect;
- unresolved blocker and fallback.

## Hard rule

An agent that repeats the same material error twice without creating a reusable lesson, evaluation case and prevention control is automatically downgraded and removed from unsupervised execution for that task class.
