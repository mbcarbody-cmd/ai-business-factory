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

## Mandatory shared learning core

Every agent, CEO cell, reviewer, builder, researcher and future worker must read and obey:

- `OPS/learning/GLOBAL_KNOWLEDGE_CORE_LT.md`
- `OPS/learning/AI_BUSINESS_FACTORY_LEARNING_ACADEMY_LT.md`
- `OPS/learning/worker_exam_matrix.json`
- `OPS/learning/knowledge_sync_bus.json`
- `OPS/org/TEN_THOUSAND_LEARNING_WORKFORCE_2026_06_14.json`

Specialists may know more in their domain, but no worker may contradict the shared core.

A worker cannot mark work complete, teach other workers or change product rules unless the required exam modules in `OPS/learning/worker_exam_matrix.json` are passed or explicitly marked as pending with QA review.

## Before changing code

1. Read `OPS/task_board.json`.
2. Read `OPS/learning/GLOBAL_KNOWLEDGE_CORE_LT.md`.
3. Identify the task ID or create a new task proposal.
4. Read the relevant OPS layer file.
5. Read `OPS/security/SECURITY_FORTRESS_LT.md` if code, config, deploy, auth, data, AI tools or integrations are touched.
6. State files to change.
7. State risk.
8. Make the smallest useful change.
9. Run or propose tests.
10. Update proof path.
11. Record reusable lessons in `OPS/learning/knowledge_sync_bus.json` when the change teaches more than one project.

## 10 000 learning workforce routing rule

The 10 000-unit learning directive is `OPS/org/TEN_THOUSAND_LEARNING_WORKFORCE_2026_06_14.json` and the learning task manifest is `OPS/TASK_BOARD/learning_scale_tasks_2026_06_14.json`.

These are virtual learning capacity units, not independent human employees. They are not allowed to create duplicate work. Every unit must attach to a tracked task, a single owner, a canonical output path and proof.

Learning capacity must become one of:

- reusable rule extraction,
- proof review,
- QA testing,
- data provenance verification,
- EU seller learning,
- Parts Seller OS workflow training,
- revenue/CFO/delivery training,
- design/conversion review,
- dedupe/normalization,
- blocked-task fallback support.

## Mass scale routing rule

The mass-scale directive is `OPS/org/mass_agent_scale_directive_2026_06_14.json` and the scale task manifest is `OPS/TASK_BOARD/mass_scale_tasks_2026_06_14.json`.

Mass capacity units are not allowed to create parallel duplicate work. Each unit must attach to a tracked task, a single accountable owner, a canonical output path and proof. Extra units must become reviewers, testers, health checkers, researchers, documentation helpers or fallback workers.

Revenue-related units may prepare verified public business records, offer drafts and pilot tracking only after review. They must not perform automated bulk messaging, private-data collection, consent bypass, platform-rule bypass or unreviewed claims.

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
- AI agent permission policy,
- Global Knowledge Core,
- worker exam matrix,
- knowledge sync bus.

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
- Do not copy catalogues, protected data, images, branding, layout or text from EU sellers/marketplaces.
- Do not treat seed targets as real leads.
- Do not treat search snippets as price proof.

## Security rules

Every significant PR must include:

- task ID,
- changed files,
- tests or no-test reason,
- security note,
- risk and rollback note,
- proof path,
- learning impact note when the change teaches another project.

A PR is blocked if:

- secret or credential is present,
- security workflow fails,
- auth/data/deploy/payment changes lack review,
- AI agent made broad changes without scope,
- public endpoint lacks auth/rate-limit review,
- public data lacks source_url, checked_at, confidence and allowed_use,
- worker output violates Global Knowledge Core.

## Preferred execution style

- Small commits.
- Clear proof.
- Tests or explicit no-test reason.
- PR-ready summary.
- No vague strategy without output.
- Security first when unsure.
- Learn once, sync everywhere.
- Build Parts Seller OS proof before expanding optional projects.

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
- `OPS/marketplace/EU_SELLER_LEARNING_ENGINE_LT.md`
- `OPS/marketplace/category_learning_map.json`
- `OPS/marketplace/trust_signal_rules.json`
- `OPS/org/mass_agent_scale_directive_2026_06_14.json`
- `OPS/org/TEN_THOUSAND_LEARNING_WORKFORCE_2026_06_14.json`
- `OPS/TASK_BOARD/mass_scale_tasks_2026_06_14.json`
- `OPS/TASK_BOARD/learning_scale_tasks_2026_06_14.json`
- `OPS/learning/GLOBAL_KNOWLEDGE_CORE_LT.md`
- `OPS/learning/AI_BUSINESS_FACTORY_LEARNING_ACADEMY_LT.md`
- `OPS/learning/worker_exam_matrix.json`
- `OPS/learning/knowledge_sync_bus.json`
- `OPS/learning/parts_seller_os_training_matrix.json`
- `OPS/learning/learning_metrics_2026_06_14.json`
- `OPS/model_council/CURSOR_INTEGRATION_PLAYBOOK_LT.md`
- `OPS/security/SECURITY_FORTRESS_LT.md`
- `OPS/security/AI_AGENT_SECURITY_POLICY_LT.md`
- `OPS/security/THREAT_MODEL_LT.md`
- `OPS/security/INCIDENT_RESPONSE_PLAYBOOK_LT.md`

## Final rule

Act like an owner: protect revenue, margin, customer trust, code quality, security, system memory and shared learning.
