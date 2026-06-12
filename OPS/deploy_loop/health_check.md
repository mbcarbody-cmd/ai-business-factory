# Health Check Registry

Owner: CTO-2 DevOps Commander

## Purpose

A product is not live unless it can be checked quickly.

## Health check types

- URL check: page/API returns success.
- Smoke workflow: main user flow works.
- Data check: required records exist and no migration break.
- Error check: logs do not show critical errors.

## Registry

| Product | Check type | Command/URL | Expected result | Status | Last checked |
|---|---|---|---|---|---|
| AI Agent Setup landing | URL check | pending | landing loads and CTA visible | pending | pending |
| AI Agent Setup lead capture | Smoke workflow | pending | lead can be submitted and recorded | pending | pending |
| AI Agent Setup outreach generator | Smoke workflow | pending | message generated from lead data | pending | pending |
| Parts Commerce OS | Architecture check | `OPS/marketplace/roadmap.md` | entities and MVP slice are defined | pending | pending |

## Rule

If no health check exists, product cannot be marked production-ready.
