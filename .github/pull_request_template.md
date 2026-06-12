# Pull Request Security Checklist

## Task link

- Task ID:
- Output/proof path:

## Change summary

What changed:

Why it changed:

## Security review

- [ ] No secrets, tokens, passwords, cookies, private keys or env values committed.
- [ ] No `.env` or credential files committed.
- [ ] No public admin/debug endpoint added.
- [ ] No auth/permission change without security note.
- [ ] No pricing/payment/order change without CFO + Security note.
- [ ] No customer/private data included in code, logs, prompts or tests.
- [ ] No new dependency without reason.
- [ ] No production deploy path changed without rollback note.
- [ ] No destructive script/command added.

## AI agent usage

- [ ] AI tool used: yes / no
- [ ] AI changes reviewed by human/Judge.
- [ ] AI did not bypass task board, QA, CFO, deploy or security gates.

## Tests

- [ ] Tests pass.
- [ ] No-test reason documented.

## Risk and rollback

Main risk:

Rollback plan:
