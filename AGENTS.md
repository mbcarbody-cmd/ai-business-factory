# AI Business Factory Agent Instructions

This repo is an execution operating system, not a note dump.

## Prime rule

No work is done unless it produces or updates a tracked artifact:

- task board update,
- decision memory entry,
- product gate update,
- QA/test/bug proof,
- deploy/health proof,
- revenue pipeline movement,
- CFO margin/cost check,
- delivery artifact,
- marketplace workflow/data model update,
- security review/proof when code, data, auth, deploy, AI tools or integrations are affected.

## Before changing code

1. Read `OPS/task_board.json`.
2. Identify the task ID or create a new task proposal.
3. Read the relevant OPS layer file.
4. Read `OPS/security/SECURITY_FORTRESS_LT.md` if code, config, deploy, auth, data, AI tools or integrations are touched.
5. State files to change.
6. State risk.
7. Make the smallest useful change.
8. Run or propose tests.
9. Update proof path.

## Hard gates

Do not bypass:

- product gates,
- QA critic layer,
- CFO layer,
- deploy loop,
- delivery intake,
- revenue tracking,
- marketplace data model rules,
- security fortress,
- AI agent permission policy.

## Do not do

- Do not push unrelated refactors.
- Do not change pricing without CFO logic.
- Do not change public sales promises without Judge review.
- Do not deploy production without deploy SOP and health check.
- Do not run destructive database, file or infrastructure commands.
- Do not delete data, backups, environment files or secrets.
- Do not commit `.env`, private keys, tokens, cookies, database URLs or service account files.
- Do not put customer/private data into prompts, logs, tests or screenshots unless anonymized and approved.
- Do not expose admin, debug, maps, internal routes or sensitive endpoints publicly.

## Security rules

Every significant PR must include:

- task ID,
- changed files,
- tests or no-test reason,
- security note,
- risk and rollback note,
- proof path.

A PR is blocked if:

- secret or credential is present,
- security workflow fails,
- auth/data/deploy/payment changes lack review,
- AI agent made broad changes without scope,
- public endpoint lacks auth/rate-limit review.

## Preferred execution style

- Small commits.
- Clear proof.
- Tests or explicit no-test reason.
- PR-ready summary.
- No vague strategy without output.
- Security first when unsure.

## Main OPS files

- `OPS/task_board.json`
- `OPS/CORE_OS_STATUS.md`
- `OPS/product_gates/product_stages.json`
- `OPS/product_gates/release_checklist.md`
- `OPS/qa/bug_board.json`
- `OPS/cfo/costs.json`
- `OPS/revenue_ops/lead_pipeline.json`
- `OPS/delivery/72h_delivery_playbook.md`
- `OPS/marketplace/roadmap.md`
- `OPS/model_council/CURSOR_INTEGRATION_PLAYBOOK_LT.md`
- `OPS/security/SECURITY_FORTRESS_LT.md`
- `OPS/security/AI_AGENT_SECURITY_POLICY_LT.md`
- `OPS/security/THREAT_MODEL_LT.md`
- `OPS/security/INCIDENT_RESPONSE_PLAYBOOK_LT.md`

## Final rule

Act like an owner: protect revenue, margin, customer trust, code quality, security and system memory.
