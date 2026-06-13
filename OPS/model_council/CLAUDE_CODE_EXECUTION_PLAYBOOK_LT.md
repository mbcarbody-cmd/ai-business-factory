# Claude Code Execution Playbook LT

Date: 2026-06-13
Owner: CTO-1 Product Factory Architect + CISO / Security Judge
Status: active
Purpose: use Claude Code as a repo execution worker without losing control, security or proof discipline.

## Why Claude Code belongs in this project

Claude Code can read the repo, edit files, run commands, create commits/PRs, connect to tools through MCP, use repo instructions, use skills, use hooks and run through GitHub Actions or routines. In this project it should act as a disciplined coding operator, not as an uncontrolled CEO.

## Required repo controls

Claude Code must follow:

- `AGENTS.md`
- `CLAUDE.md`
- `.claude/settings.json`
- `OPS/task_board.json`
- `OPS/task_board_v2.json`
- `OPS/security/AI_AGENT_SECURITY_POLICY_LT.md`
- `OPS/data_intelligence/PUBLIC_DATA_COLLECTION_PLAYBOOK.md`
- `OPS/qa/bug_board.json`

## Best use cases for this repo

### P0 use cases

1. Build local OPS audit script.
2. Build CEO Cockpit dynamic JSON loading.
3. Build Parts Seller OS one-seller prototype.
4. Add tests and smoke checks.
5. Convert roadmap/data model into working UI or local app.
6. Open PR-ready changes with proof path and rollback note.

### P1 use cases

1. Refactor website for trust and conversion.
2. Create delivery templates and intake forms.
3. Add sample data and validation fixtures.
4. Improve CFO cost-per-task tracking.
5. Generate marketplace workflow diagrams.

### Not allowed without human approval

- production deploy,
- outbound customer email,
- payment/order logic,
- auth/security changes,
- deleting data,
- using secrets,
- login-gated data access,
- public scraping without permission checklist.

## Recommended Claude Code setup

1. Install Claude Code locally.
2. Open repo root.
3. Run `/status` and confirm `CLAUDE.md` and `.claude/settings.json` are loaded.
4. Run in default or plan mode for exploration.
5. Use feature branches for code changes.
6. Run `/ops-audit` skill after every meaningful change.
7. Never use bypass permissions outside an isolated disposable environment.

## First commands to run in this repo

```bash
claude
/status
/permissions
```

Then prompt:

```text
Read AGENTS.md, CLAUDE.md and OPS/task_board.json. Pick the highest-value P0 task that can be advanced safely. Make the smallest useful proof-producing change. Update the relevant OPS proof path. Do not touch secrets, production, payment, auth or customer data.
```

## Claude Code work packets

### Packet 1 — OPS audit guardrail

Task: `OPS-018`
Output:

- `scripts/ops_audit.py`
- audit result in terminal
- bug board update if audit fails

Prompt:

```text
Build a local Python OPS audit script that validates required OPS files exist, task board rows have owner/status/next_action/output_path/done_proof, and high/critical bugs are visible. Do not change business logic. Add no-test reason if only docs/script validation exists.
```

### Packet 2 — CEO Cockpit dynamic data

Task: `OPS-017`
Output:

- `products/ceo-cockpit/` dynamic JSON loading
- local smoke test note
- deploy SOP update

Prompt:

```text
Make CEO Cockpit load OPS JSON files dynamically where browser security allows it, keep a static fallback, add local smoke-test instructions and update deploy proof. No public hosting claim until a URL exists.
```

### Packet 3 — Parts Seller OS prototype

Task: `OPS-010`
Output:

- one-seller prototype from `OPS/marketplace/parts_os_mvp_data_model.json`
- sample data
- first KPI cards

Prompt:

```text
Build the smallest Parts Seller OS prototype using the existing data model: add part, suggested location, price/floor, listing status, reservation state and ageing/dead-stock signal. Use sample data only. No external marketplace integration.
```

### Packet 4 — Public data verification

Task: `OPS-019`
Output:

- `OPS/data_intelligence/source_registry.json` updates
- competitor validation updates
- lead rows only from public company pages

Prompt:

```text
Use only public, permitted business pages and the public data permission checklist. Verify competitor pricing/CTA and record source URL/date. Do not use login-gated pages, cookies, personal data or automated outbound.
```

## GitHub Actions use

Claude Code GitHub Actions should be enabled only after:

1. repo settings are committed,
2. `ANTHROPIC_API_KEY` is stored as a GitHub secret,
3. workflow has limited triggers,
4. branch protection or human review is used,
5. output must be PR, not direct main push.

Recommended first action: mention-based issue/PR helper, not automatic merge.

## MCP use

MCP should be added gradually:

1. GitHub MCP/read PRs and issues.
2. Local filesystem within repo only.
3. Optional Google Drive docs after data boundaries are clear.
4. No Gmail/customer outbound MCP until revenue workflow and approval policy are written.
5. No database MCP with production credentials.

## Skills to add

- `/ops-audit` — validate core OPS state.
- `/public-data-verify` — verify public data safely.
- `/parts-os-build` — build one-seller seller OS slice.
- `/qa-critic` — break-test before release.

## Done definition

Claude Code integration is useful only when it produces merged repo artifacts, passing audit, QA notes and proof paths. Merely installing the tool is not progress.