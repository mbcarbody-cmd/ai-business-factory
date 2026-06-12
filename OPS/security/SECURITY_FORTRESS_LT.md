# Security Fortress LT

Date: 2026-06-12
Owner: CISO / Security Judge
Purpose: padaryti AI Business Factory sauguma rimtu bankinio lygio procesu: no secrets in repo, least privilege, strong review, AI-agent sandbox, incident response, secure deploy ir audit trail.

## Pagrindinis verdiktas

Vibe coding ir AI coding agentai be kontroles yra pavojingi. Didziausios rizikos:

- API raktai kode,
- `.env` failai repo,
- vieši endpointai be auth,
- per placios AI agentu teises,
- destructive shell commands,
- nepatikrinti dependency paketai,
- prompt injection,
- sensitive info disclosure,
- maps, routes, admin panels ir internal data leaks.

## Security operating law

1. No secret in repo.
2. No direct push to main.
3. No production deploy without security gate.
4. No AI agent with admin permission by default.
5. No public endpoint without auth/rate limit review.
6. No pricing/payment changes without CFO + Security review.
7. No customer data in prompts unless anonymized.
8. No destructive command without human approval.
9. No external integration without token scope review.
10. No release without rollback and incident plan.

## Security layers

### 1. Secrets protection

Rules:
- `.env`, tokens, private keys, API keys, cookies, sessions and service account files are never committed.
- Use GitHub secrets or secure secret manager.
- Rotate immediately if secret appears in repo, issue, prompt, screenshot or log.

Required controls:
- GitHub secret scanning and push protection.
- Local pre-commit secret scan.
- CI secret scan on pull request.
- `.gitignore` for env/key files.

### 2. Branch and PR protection

Rules:
- main branch protected.
- no direct push to main.
- required PR review for code changes.
- required security check pass before merge.
- required tests or no-test reason.

### 3. AI agent sandbox

Rules:
- AI coding tools can read repo and propose changes.
- AI agents cannot deploy production, delete data, change secrets, send customer emails, change payment logic or run destructive commands without approval.
- Every agent action must have task ID, scope, changed files and proof path.

### 4. Least privilege access

Rules:
- give the smallest permission needed.
- prefer read-only tokens.
- separate dev/staging/prod credentials.
- rotate tokens quarterly or after any suspicious event.
- no shared admin accounts.

### 5. Secure coding

Rules:
- validate all inputs.
- encode outputs.
- parameterize database queries.
- rate limit public endpoints.
- require auth for admin or sensitive APIs.
- log security events, not secrets.
- avoid exposing stack traces publicly.

### 6. Dependency and supply chain security

Rules:
- pin versions where practical.
- use Dependabot or equivalent.
- review new packages.
- no random copy-paste scripts from internet.
- no install/run unknown package without review.

### 7. Data protection

Rules:
- classify data: public, internal, confidential, restricted.
- customer data is confidential.
- credentials are restricted.
- logs must not contain secrets or personal/customer sensitive details.
- backups must be protected.

### 8. LLM and prompt security

Rules:
- never trust model output as authority.
- untrusted retrieved text can contain hostile instructions.
- tools must enforce permissions outside the model.
- LLM cannot decide to bypass security.
- sensitive data must be masked before prompt use.

### 9. Deploy and runtime security

Rules:
- deploy requires health check and rollback note.
- production env variables live outside repo.
- admin panels are not public without strong auth.
- debug mode off in production.
- CORS locked down.
- secrets not printed in logs.

### 10. Incident response

Rules:
- suspect breach = stop, isolate, rotate, audit, fix, document.
- leaked secret = revoke and rotate immediately.
- production data issue = freeze deploys until triage.
- every incident creates lesson and control improvement.

## Security gates before merge

A PR cannot merge if:

- secret scan fails,
- security workflow fails,
- code changes have no tests or no-test reason,
- auth/permission changes lack security note,
- payment/pricing changes lack CFO + Security note,
- public endpoint lacks auth/rate limit review,
- deploy path lacks rollback note,
- AI agent made broad unrelated changes.

## Security gates before production

Production release requires:

- product gate ready,
- QA pass,
- secret scan pass,
- dependency scan pass,
- security review pass,
- deploy SOP,
- health check,
- rollback plan,
- owner on call,
- incident response path.

## Access policy

Access levels:

- Viewer: read docs only.
- Contributor: branch/PR only.
- Maintainer: merge with review.
- Security Judge: can block release.
- Owner/Admin: rare, MFA required.

No agent gets Owner/Admin by default.

## Red flags

Immediate stop if:

- `.env` appears in repo,
- token appears in code/log/issue,
- private key appears anywhere,
- admin route is public,
- database URL is visible,
- AI agent asks to disable security,
- dependency asks strange install script,
- CI exposes secrets,
- prompt includes customer/private data unnecessarily.

## Security KPI

Track weekly:

- open critical findings,
- secret scan status,
- dependency alerts,
- PRs blocked by security,
- time to rotate leaked secret,
- production incidents,
- security training completed,
- high-risk AI agent actions.

## Final rule

Security is not optional polish. Security is a product feature, trust layer and survival rule. Faster build is worthless if it leaks keys, data or control.
