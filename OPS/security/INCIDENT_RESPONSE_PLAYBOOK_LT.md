# Incident Response Playbook LT

Date: 2026-06-12
Owner: CISO / Security Judge
Purpose: tureti aisku veiksmu plana nutikus secret leak, duomenu nutekejimui, production incidentui, supply chain rizikai arba AI agento klaidai.

## Severity levels

### SEV-1 Critical

Pavyzdziai:
- leaked production secret,
- exposed customer data,
- unauthorized production access,
- payment/order manipulation,
- destructive data change,
- public admin endpoint.

Response: immediate freeze, revoke, rotate, isolate, audit.

### SEV-2 High

Pavyzdziai:
- staging secret leak,
- auth bypass in non-production,
- vulnerable dependency with exploit path,
- agent attempted destructive command.

Response: fix before release, rotate if needed, add control.

### SEV-3 Medium

Pavyzdziai:
- missing rate limit,
- weak validation,
- incomplete logs,
- missing security note in PR.

Response: create task, fix before production.

### SEV-4 Low

Pavyzdziai:
- documentation gap,
- naming confusion,
- security checklist incomplete.

Response: backlog with owner.

## First 15 minutes

1. Stop risky activity.
2. Identify affected system.
3. Preserve evidence.
4. Revoke exposed token if any.
5. Rotate new credential.
6. Block deploys if production may be affected.
7. Assign incident owner.
8. Open incident log.

## Secret leak procedure

1. Revoke secret immediately.
2. Rotate secret immediately.
3. Check where it was exposed: code, issue, PR, log, screenshot, prompt, chat.
4. Search repo history.
5. Check access logs for use.
6. Replace with secure secret manager/GitHub secrets.
7. Add prevention control.
8. Record lesson.

Important: deleting the visible file is not enough. Assume copied until revoked.

## Production data issue

1. Freeze deploys.
2. Disable risky endpoint if needed.
3. Preserve logs.
4. Identify data scope.
5. Restore from backup only after root cause known.
6. Patch issue.
7. Review access logs.
8. Write postmortem.

## AI agent incident

1. Stop agent session.
2. Review commands and changed files.
3. Revert suspicious changes.
4. Check for secret exposure.
5. Check for destructive actions.
6. Reduce agent permission level.
7. Add new rule to AI Agent Security Policy.

## Supply chain incident

1. Identify package/action dependency.
2. Check version and source.
3. Remove or pin safe version.
4. Run tests and scans.
5. Check if secrets were exposed to CI.
6. Replace dependency if trust is weak.

## Incident log template

- Incident ID:
- Date/time:
- Severity:
- Owner:
- Detected by:
- Affected systems:
- What happened:
- Immediate actions:
- Secrets rotated:
- Data affected:
- Customer impact:
- Root cause:
- Fix:
- New prevention rule:
- Review date:

## Postmortem rules

Every SEV-1/SEV-2 incident must produce:

- root cause,
- fix,
- new control,
- task board update,
- memory lesson,
- security policy update if needed.

## Final rule

Fast response beats perfect response. For leaked secrets: revoke first, investigate second.
