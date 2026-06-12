# Cursor Integration Playbook LT

Date: 2026-06-12
Owner: CTO-1 Product Factory Architect + JUDGE-1 Release Gate Judge
Purpose: naudoti Cursor kaip AI IDE ir coding execution sluoksnį, bet su OPS kontrole: task board, product gates, QA, CFO, deploy ir security ribomis.

## Pagrindinis verdiktas

Cursor verta naudoti. Jis neturi būti CEO ar strategas. Jo vieta: kodo rašymas, refactor, testai, PR review, frontend/dashboard kūrimas, greiti MVP pakeitimai ir repo navigacija.

## Kur Cursor mums naudingiausias

1. Greitas UI / dashboard / landing kūrimas.
2. Multi-file pakeitimai pagal aiškią užduotį.
3. Refactor ir kodo tvarkymas.
4. Testų generavimas ir bug fix.
5. PR review per Bugbot.
6. Repo onboarding: paaiškinti struktūrą ir rasti failus.
7. MCP tool jungtys prie mūsų OPS duomenų.
8. Skills / Rules kaip kartojami workflow.

## Ko mokytis iš Cursor

### 1. Rules

Cursor Rules leidžia repo viduje laikyti agento instrukcijas. Mums reikia `.cursor/rules` ir `AGENTS.md`, kad kiekvienas coding agentas laikytųsi mūsų OPS logikos.

### 2. Skills

Skills yra version-controlled workflow paketai. Mums reikia skillų:

- create-product-gate,
- run-qa-critic,
- update-task-board,
- create-revenue-offer,
- create-marketplace-entity,
- review-pr-before-merge,
- add-tests-for-backend-change.

### 3. MCP

Cursor MCP gali jungtis prie external tools ir data sources. Ateityje mūsų task board, product gates, revenue pipeline, CFO costs ir marketplace data turi būti pasiekiami per saugų MCP serverį.

### 4. Bugbot / PR review

Bugbot gali tikrinti PR diff, rasti bugus, security ir code quality problemas. Mums tai tinka kaip papildomas QA/Judge sluoksnis prieš merge.

### 5. Checkpoints

Cursor Agent daro checkpoints prieš reikšmingus pakeitimus. Tai naudinga eksperimentams, bet Git lieka pagrindinis version control.

## Kaip prijungti praktiškai

### Stage 1 — Manual Cursor use

Naudoti Cursor lokaliai su repo. Tikslas: greitai daryti mažus, aiškius taskus.

Allowed:
- read repo,
- edit docs,
- edit frontend/backend MVP,
- run tests,
- create PR branches.

Not allowed:
- production deploy be approval,
- delete DB/data,
- change pricing public pages without CFO/Judge,
- push directly to main,
- run destructive commands.

### Stage 2 — Add repo instructions

Sukurti:

- `AGENTS.md`,
- `.cursor/rules/ops-workflow.mdc`,
- `.cursor/rules/security-and-permissions.mdc`,
- `.cursor/BUGBOT.md`.

### Stage 3 — Add skills

Sukurti `.agents/skills/` workflow:

- task-board-update,
- product-gate-review,
- qa-critic-pass,
- revenue-offer-pack,
- marketplace-workflow-design.

### Stage 4 — PR review

Įjungti Cursor Bugbot arba bent manual review flow.

Rule: joks code PR negali merge be:

- tests arba no-test reason,
- QA note,
- product gate note,
- CFO impact jei keičia pricing/revenue,
- deploy/rollback note jei keičia production path.

### Stage 5 — MCP server v1

Kai OPS failai stabilūs, sukurti local MCP serverį, kuris Cursor gali duoti:

- task board read/update,
- product gates read/update,
- QA bug board update,
- CFO cost entry,
- revenue pipeline entry,
- marketplace entity read/update.

## Cursor role mūsų model council

Role: Cursor Coding Operator

Atsakomybė:
- konvertuoti task board užduotis į kodą,
- kurti mažus MVP increments,
- taisyti bugus,
- generuoti testus,
- ruošti PR,
- laikytis repo rules.

KPI:
- mažiau rankinio kodo darbo,
- daugiau uždarytų build taskų,
- mažiau bugų po QA,
- greitesnis MVP cycle,
- visi pakeitimai turi proof.

## Security rules

Cursor agentas negali:

- trinti production DB,
- trinti backups,
- keisti env secrets,
- deployinti production be approval,
- siųsti klientams laiškų,
- keisti mokėjimų logikos,
- daryti destructive shell commands be review.

Visi destructive veiksmai turi eiti per žmogaus/Judge approval.

## Cursor prompt template

You are the Cursor Coding Operator for this repo.

Before coding:
1. Read `OPS/task_board.json`.
2. Read related product gate or architecture doc.
3. State the exact files you will change.
4. State risks.
5. Make the smallest useful change.
6. Run or propose tests.
7. Update task board or proof path.
8. Do not change unrelated files.
9. Do not run destructive commands.
10. Prepare PR-ready summary.

## Best first Cursor tasks

1. Create `AGENTS.md` from OPS doctrine.
2. Create `.cursor/rules/ops-workflow.mdc`.
3. Create `.cursor/BUGBOT.md`.
4. Build first simple dashboard view for `OPS/task_board.json`.
5. Build first marketplace data model prototype.
6. Build AI cost-per-task tracker.

## Final rule

Cursor yra coding engine. OPS lieka control system. Cursor turi vykdyti taskus, bet ne apeiti task board, QA, CFO, product gates ar human approval.
