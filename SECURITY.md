# Security Policy

## Reporting security issues

Do not open public issues for vulnerabilities, leaked secrets, exposed tokens, authentication bypasses, data exposure, payment bugs, or production access problems.

Report privately to the repository owner or designated security contact.

## Immediate emergency rules

If a secret is exposed:

1. Revoke it immediately.
2. Rotate it immediately.
3. Search logs and repo history for use.
4. Remove the secret from current code.
5. Do not assume deleting a commit is enough.
6. Record the incident in `OPS/security/INCIDENT_RESPONSE_PLAYBOOK_LT.md`.

## Security expectations

All code changes must respect:

- no secrets in repository,
- least privilege,
- protected main branch,
- PR review before merge,
- tests or no-test reason,
- security scan pass,
- no destructive agent commands without approval,
- no production deploy without health check and rollback note.

## AI coding agent rules

AI agents and AI IDEs may propose code, docs and tests, but must not:

- deploy production,
- delete data,
- expose secrets,
- change payment or pricing logic,
- send customer emails,
- bypass security checks,
- run destructive commands without explicit approval.

## Security sources of truth

- `OPS/security/SECURITY_FORTRESS_LT.md`
- `OPS/security/AI_AGENT_SECURITY_POLICY_LT.md`
- `OPS/security/INCIDENT_RESPONSE_PLAYBOOK_LT.md`
- `.cursor/rules/security-and-permissions.mdc`
- `.github/pull_request_template.md`
