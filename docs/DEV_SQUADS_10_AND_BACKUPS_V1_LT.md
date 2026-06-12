# Dev Squads 10 and Backup OS v1 LT

Tikslas: sukurti 10 kodavimo ir techninio vykdymo komandu, kurios greitina AI Business Factory produktus, bet nekuria chaoso. Kiekvienas squad turi owneri, misija, agentus, output, testus, done proof ir backup atsakomybe.

## Globalios dev taisykles

1. Kiekvienas squad dirba tik su taskais, kurie turi revenue, product, delivery, automation arba risk reason.
2. Kiekvienas pakeitimas turi test, review arba aišku done proof.
3. Kiekvienas squad turi tureti rollback planą.
4. Kiekvienas squad turi pildyti Memory Ledger, kai sprendimas svarbus.
5. Nera release be QA, backup ir restore kelio.
6. Nera naujos funkcijos be ownerio ir acceptance criteria.
7. Visi squad'ai masto kaip CTO + CEO: greitis, pinigai, rizika, vartotojas, support kaina.

---

# 1. Core Platform Squad

Misija: pastatyti pagrindine platforma, kurioje veikia agentai, taskai, vartotojai, produktai ir darbo srautai.

Vadovai:
- Platform Tech Lead.
- Backend Architect.
- System Design Reviewer.

Agentai:
1. API Developer.
2. Database Developer.
3. Auth and Roles Developer.
4. Workflow Developer.
5. Platform Refactor Agent.

Pirmi darbai:
- agent registry schema;
- task queue schema;
- roles and permissions;
- audit log;
- platform health endpoint.

Done proof:
- veikia basic API;
- yra DB schema;
- yra health check;
- yra smoke test;
- yra rollback notes.

---

# 2. Agent Runtime and Orchestration Squad

Misija: padaryti, kad 100 vadovu ir 240 agentu veiktu kaip protinga sistema, o ne kaip triuksmas.

Vadovai:
- AI Orchestration Lead.
- Worker Runtime Lead.
- Decision Logic Reviewer.

Agentai:
1. Orchestrator Developer.
2. Worker Queue Developer.
3. Prompt Contract Agent.
4. Agent Score Agent.
5. Kill Criteria Agent.

Pirmi darbai:
- agent registry MVP;
- worker queue MVP;
- priority rules;
- task assignment logic;
- agent performance log.

Done proof:
- orchestrator parenka darba;
- worker ivykdo darba;
- judge patikrina darba;
- memory atnaujinama;
- nenaudingas taskas atmetamas.

---

# 3. Revenue Ops and CRM Squad

Misija: sukurti sistema, kuri stumia lead -> reply -> demo -> paid pilot -> delivery -> maintenance.

Vadovai:
- Revenue Systems Lead.
- CRM Architect.
- Funnel QA Reviewer.

Agentai:
1. Lead Pipeline Developer.
2. Outreach Log Developer.
3. Proposal Flow Developer.
4. Invoice State Developer.
5. Follow Up Automation Agent.

Pirmi darbai:
- lead table;
- lead status flow;
- outreach log;
- demo tracker;
- paid pilot tracker.

Done proof:
- matosi kiek leadu;
- matosi kiek contacted;
- matosi kiek replied;
- matosi kiek demo;
- matosi kiek paid;
- yra daily revenue report.

---

# 4. Product UI and Conversion Squad

Misija: padaryti, kad musu puslapiai atrodytu patikimai, aiskiai ir parduotu.

Vadovai:
- Frontend Lead.
- UX Conversion Lead.
- Visual QA Reviewer.

Agentai:
1. Landing Developer.
2. Dashboard Frontend Developer.
3. Form UX Developer.
4. Mobile QA Agent.
5. Trust Block Agent.

Pirmi darbai:
- hero section improvement;
- pricing section;
- trust blocks;
- lead form;
- mobile pass.

Done proof:
- desktop vaizdas tvarkingas;
- mobile vaizdas tvarkingas;
- CTA matomas;
- lead forma veikia;
- conversion review atliktas.

---

# 5. Delivery and Client Portal Squad

Misija: uztikrinti, kad parduotas produktas butu pristatomas greitai, aiskiai ir be chaoso.

Vadovai:
- Delivery Systems Lead.
- Client Portal Lead.
- Support Flow Reviewer.

Agentai:
1. Intake Form Developer.
2. Delivery Checklist Developer.
3. Handoff Page Developer.
4. Support Ticket Developer.
5. Maintenance Flow Agent.

Pirmi darbai:
- client intake;
- delivery checklist;
- acceptance checklist;
- handoff page;
- maintenance offer flow.

Done proof:
- klientas turi intake;
- komanda turi scope;
- yra checklist;
- yra handoff;
- yra support ir maintenance next step.

---

# 6. Data and Pricing Intelligence Squad

Misija: duomenys, kainodara, konkurentu kainos, likvidumas ir sprendimai pagal skaicius.

Vadovai:
- Data Lead.
- Pricing Intelligence Lead.
- Data Quality Reviewer.

Agentai:
1. Data Model Developer.
2. Price Observation Developer.
3. Liquidity Score Developer.
4. Competitor Data Developer.
5. Data Quality Agent.

Pirmi darbai:
- competitor price table;
- price source fields;
- liquidity score v1;
- data completeness score;
- pricing recommendation v1.

Done proof:
- price observations saugomi;
- dalis gauna pricing note;
- matomas source;
- matomas confidence;
- blogi duomenys blokuojami.

---

# 7. Marketplace and Parts Commerce Squad

Misija: uzdaryti autodaliu commerce OS: seller, donor, part, location, listing, reservation, order, shipment.

Vadovai:
- Marketplace Tech Lead.
- Warehouse Systems Lead.
- Commerce Flow Reviewer.

Agentai:
1. Part Intake Developer.
2. Location Engine Developer.
3. Listing Publisher Developer.
4. Reservation Developer.
5. Order Flow Developer.

Pirmi darbai:
- part intake flow;
- location recommendation;
- location capacity;
- listing status;
- order and reservation flow.

Done proof:
- nauja dalis turi statusa;
- dalis turi lokacija arba pending location;
- matoma ar vietoje telpa;
- dalis gali buti rezervuota;
- order flow turi audit log.

---

# 8. Automation and Integration Squad

Misija: jungti isorines sistemas ir mazinti rankini darba.

Vadovai:
- Integration Lead.
- Automation Architect.
- Connector QA Reviewer.

Agentai:
1. API Connector Developer.
2. Import Export Developer.
3. Scheduler Developer.
4. Webhook Developer.
5. Error Handling Agent.

Pirmi darbai:
- integration registry;
- scheduler jobs;
- import/export format;
- retry rules;
- connector status log.

Done proof:
- integration turi owneri;
- yra status;
- yra klaidu logas;
- yra retry taisykle;
- yra manual fallback.

---

# 9. Media and Content Factory Squad

Misija: paruosti content, video scripts, calendar, assets ir publishing queue, kad savininkas nemontuotu kasdien rankomis.

Vadovai:
- Media Systems Lead.
- Content Pipeline Lead.
- Publishing QA Reviewer.

Agentai:
1. Content Calendar Developer.
2. Script Pack Developer.
3. Asset Library Developer.
4. Publishing Queue Developer.
5. Metrics Log Agent.

Pirmi darbai:
- campaign brief template;
- content calendar;
- script pack format;
- asset status flow;
- metrics log.

Done proof:
- kiekvienas produktas turi content brief;
- yra 7 dienu calendar;
- yra script pack;
- yra publish status;
- yra rezultatu logas.

---

# 10. QA, DevOps, Security and Backup Squad

Misija: neleisti prarasti darbo, neleisti blogo release ir uztikrinti restore kelia.

Vadovai:
- Reliability Lead.
- QA Automation Lead.
- Backup and Restore Lead.

Agentai:
1. CI Pipeline Developer.
2. Smoke Test Developer.
3. Monitoring Developer.
4. Backup Job Developer.
5. Restore Drill Agent.

Pirmi darbai:
- smoke test checklist;
- deploy checklist;
- monitoring dashboard;
- backup schedule;
- restore test schedule.

Done proof:
- testai paleidziami;
- deploy turi checklist;
- backup sukuriamas;
- restore isbandytas;
- incident log pildomas.

---

# Backup OS

Tikslas: neprarasti repo, DB, serverio konfigu, failu, klientu duomenu ir produktu dokumentacijos.

## 3-2-1 principas

- 3 kopijos: production, backup, offsite backup.
- 2 skirtingos laikmenos arba vietos.
- 1 kopija atskirai nuo pagrindinio serverio.

## Ka reikia saugoti

1. GitHub repo.
2. Database dump.
3. Uploads and assets.
4. Env example and config templates.
5. Deployment scripts.
6. Product docs.
7. Client delivery docs.
8. Logs needed for audit.
9. Pricing and competitor data.
10. Agent memory ledger.

## Backup daznis

Pradziai:
- repo: GitHub plus weekly mirror archive;
- DB: daily dump;
- uploads/assets: daily sync;
- configs: after every change;
- docs: GitHub is primary, weekly archive.

Veliau:
- DB hourly snapshot for active production;
- daily backup for 30 days;
- weekly backup for 12 weeks;
- monthly backup for 12 months.

## Restore tikslai

Pradziai:
- maksimalus duomenu praradimas: 24 valandos;
- atstatymo tikslas: 4 valandos.

Veliau:
- maksimalus duomenu praradimas: 1 valanda;
- atstatymo tikslas: 1 valanda.

## Backup owneriai

Primary owner: Backup and Restore Lead.

Supporting:
- DevOps Engineer;
- Database Developer;
- Security Engineer;
- Memory Keeper;
- CTO.

## Restore drill

Kas savaite:
- patikrinti ar backup failai egzistuoja;
- patikrinti backup dydzius;
- patikrinti ar backup ne tuscias.

Kas menesi:
- atstatyti testine kopija;
- paleisti smoke test;
- irasyti restore report.

Kas ketvirti:
- pilnas disaster recovery testas.

## Incident taisykle

Jeigu kas nors sugriuvo:

1. Stop destructive changes.
2. Snapshot current state.
3. Check latest backup.
4. Restore to staging.
5. Run smoke test.
6. Restore production only after judge approval.
7. Write incident report.

---

# Pirmi 10 techniniu tasku

1. Create dev squad registry.
2. Create agent registry schema.
3. Create task queue MVP.
4. Create worker runtime MVP.
5. Create revenue dashboard MVP.
6. Create lead pipeline tables.
7. Create competitor database v1.
8. Create backup job v1.
9. Create restore drill checklist.
10. Create smoke test checklist.

---

# Svarbiausias principas

Greitis be backup yra rizika. Backup be restore testo yra iliuzija. Squad be output proof yra tik pavadinimas.
