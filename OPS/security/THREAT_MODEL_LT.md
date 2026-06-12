# Threat Model LT

Date: 2026-06-12
Owner: CISO / Security Judge + CTO-1 Product Factory Architect
Purpose: ivardinti pagrindines gresmes AI Business Factory, AI agentams, repo, marketplace, daliu workflow ir klientu duomenims.

## Assets to protect

### Restricted

- API keys,
- database credentials,
- payment provider keys,
- cloud credentials,
- email credentials,
- GitHub tokens,
- customer private data,
- production backups.

### Confidential

- pricing logic,
- supplier lists,
- lead pipeline,
- customer delivery docs,
- marketplace roadmap,
- internal agent instructions.

### Internal

- task board,
- product gates,
- QA bugs,
- delivery SOP,
- cost logic.

### Public

- landing pages,
- public docs,
- public offers.

## Main threat actors

1. Opportunistic scanners.
2. Competitors scraping public data.
3. Malicious users testing public endpoints.
4. Supply chain attackers through packages/actions.
5. AI prompt injection through external content.
6. Accidental insiders or careless agents.
7. Leaked token users.
8. Bad customers abusing automations.

## Attack surfaces

- GitHub repository,
- issues and PRs,
- AI coding tools,
- CI/CD workflows,
- environment variables,
- website/landing forms,
- lead capture forms,
- admin dashboards,
- marketplace APIs,
- warehouse/location data,
- email integrations,
- external APIs,
- logs and screenshots.

## Top risks

### RISK-001 Secret leak in repo

Impact: critical.

Controls:
- `.gitignore`,
- secret scanning,
- push protection,
- CI secret scanner,
- no real secrets in examples.

### RISK-002 AI agent excessive agency

Impact: critical.

Controls:
- permission levels,
- no production deploy,
- no destructive commands,
- PR review,
- task ID requirement.

### RISK-003 Public admin endpoint

Impact: critical.

Controls:
- auth required,
- rate limit,
- no debug mode,
- security review before deploy.

### RISK-004 Customer data exposure through prompts

Impact: high.

Controls:
- anonymize data,
- mask secrets,
- no raw customer data in prompts unless necessary,
- log minimization.

### RISK-005 Supply chain dependency compromise

Impact: high.

Controls:
- dependency review,
- lockfiles,
- Dependabot,
- package source review,
- minimal dependencies.

### RISK-006 Prompt injection via external text

Impact: high.

Controls:
- treat external content as data,
- tools enforce permissions,
- no untrusted text can override system/repo rules,
- human review for high-risk actions.

### RISK-007 Broken auth / access control

Impact: high.

Controls:
- RBAC,
- auth tests,
- deny by default,
- audit logs,
- session expiration.

### RISK-008 Data loss

Impact: high.

Controls:
- backups,
- migrations reviewed,
- destructive command approval,
- rollback plan.

### RISK-009 Payment/order manipulation

Impact: high.

Controls:
- CFO + Security review,
- idempotency,
- server-side validation,
- audit logs.

### RISK-010 Overexposed marketplace data

Impact: medium/high.

Controls:
- data classification,
- endpoint filtering,
- seller-level permissions,
- no internal cost/supplier leak.

## Security review checklist

For every significant change ask:

1. Does it touch secrets?
2. Does it touch auth?
3. Does it touch customer data?
4. Does it create public endpoint?
5. Does it change pricing/payment/order logic?
6. Does it allow AI agent to take action?
7. Does it add dependency?
8. Does it affect deploy?
9. Does it expose internal maps/routes/entities?
10. Is there rollback?

## Final rule

Threat model must be updated whenever new product, integration, public endpoint, payment flow, marketplace module or AI tool permission is added.
