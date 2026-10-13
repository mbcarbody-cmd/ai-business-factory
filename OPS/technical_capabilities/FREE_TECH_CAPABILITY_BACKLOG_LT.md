# Free Technical Capability Backlog LT

Date: 2026-06-13
Owner: CTO-1 Product Factory Architect + CTO-3 Systems Reliability Breaker
Purpose: nemokamomis priemonemis paversti repo is dokumentu valdymo i priverstini vykdymo, testavimo, saugumo ir deploy loop.

## Verdict

Repo jau turi geras OPS taisykles, bet truksta automatiniu vartų. Dauguma procesu egzistuoja kaip failai ir taisykles, taciau be CI/QA/deploy automatikos agentai vis dar gali palikti klaidas nepastebetas.

## P0 — idiegti pirmiausia

### 1. GitHub Actions OPS CI

Status: added in PR branch.
What it gives:
- runs `python3 scripts/ops_audit.py`,
- validates core JSON,
- checks demo files exist,
- serves static pages locally,
- performs smoke checks with `curl`,
- runs secret scan.

Money reason: maziau rankinio tikrinimo, maziau suluzusiu demo, daugiau pasitikejimo pries outreach.

### 2. GitHub Pages public demo

Status: recommended next.
What it gives:
- public CEO Cockpit URL,
- public landing/demo URL,
- public Parts Seller OS prototype URL,
- closes deploy-loop blocker.

Rule: public demo is not proof until URL is recorded in `OPS/deploy_loop/deploy_sop.md` and QA passes.

### 3. Gitleaks secret scan

Status: added to OPS CI workflow.
What it gives:
- blocks accidental secrets, tokens and keys in repo.

Rule: any secret hit blocks merge and requires rotation if real secret was exposed.

### 4. Dependabot

Status: already present in repo.
What it gives:
- weekly checks for GitHub Actions, npm and pip dependencies.

Rule: dependency PRs need security and test review before merge.

### 5. Branch protection + required checks

Status: must be enabled in GitHub settings.
Required checks:
- OPS audit,
- Static product smoke tests,
- Secret scan,
- CodeQL/security scan when available.

Rule: no direct push to `main`; PR must pass checks.

## P1 — next free upgrades

### 6. CodeQL / GitHub code scanning

Recommended because repo is public. Use it for JavaScript/Python once code grows beyond static prototypes.

### 7. Playwright smoke tests

Use for real browser tests after pages are deployed. Minimum tests:
- landing loads,
- CTA visible,
- CEO Cockpit cards visible,
- Parts Seller OS workflow cards visible,
- no console errors on demo pages.

### 8. Lighthouse CI

Use for landing page conversion/trust quality:
- performance,
- accessibility,
- SEO,
- best practices,
- regression prevention.

### 9. Pre-commit hooks

Use locally before commit:
- trailing whitespace,
- end-of-file fixer,
- JSON/YAML validation,
- secret pattern check.

### 10. Issue templates and PR template

Every PR must include:
- task ID,
- changed files,
- revenue or strategic reason,
- tests/no-test reason,
- security note,
- rollback note,
- proof path.

## P2 — later free upgrades

### 11. Public-source verification bot

A local script that checks every competitor/lead row has:
- source URL,
- checked date,
- confidence,
- permission status,
- next action.

### 12. CFO margin guard script

A local script that fails if a sellable offer lacks:
- price,
- estimated build hours,
- tool/model cost,
- gross margin,
- break-even logic.

### 13. Product gate verifier

A local script that fails if a product stage advances without required proof paths.

### 14. Revenue pipeline verifier

A local script that fails if outreach state is changed without exact company/contact/channel/follow-up date.

## Non-free or caution list

Avoid adding paid infrastructure until there is proof of demand or a paid pilot.
Avoid broad AI-agent write permissions until branch protection and secret scanning are active.
Avoid scraping or outbound automation without public data permission checklist and source provenance.

## Next repo actions

1. Merge OPS CI guardrails after review.
2. Enable branch protection and required checks in GitHub settings.
3. Enable GitHub Pages for public demo.
4. Record public URLs in deploy SOP.
5. Add Playwright only after a package manifest exists or after public pages need browser QA.
6. Add CodeQL workflow once codebase grows beyond mostly static HTML/JSON.
