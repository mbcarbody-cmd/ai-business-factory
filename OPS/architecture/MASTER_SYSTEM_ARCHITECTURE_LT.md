# Master System Architecture LT

Date: 2026-06-12
Owner: CEO / Master Agent
Purpose: suderinti AI Business Factory architektūrą: agentų mokymą, sprendimų logiką, alternatyvas, idėjų filtravimą, produktų kūrimą, pardavimus, delivery, CFO, QA, marketplace ir augimą.

## Pagrindinė tezė

Sistema turi veikti kaip autonominis verslo fabrikas, o ne kaip dokumentų krūva. Kiekvienas sluoksnis turi įėjimą, sprendimo logiką, outputą, ownerį, proof ir mokymosi grįžtamąjį ryšį.

## Core loop

observe -> orient -> decide -> task -> build -> review -> deploy -> sell -> deliver -> learn -> improve

## 12 architektūros sluoksnių

### 1. CEO / Direction Layer

Atsako už kryptį, prioritetą, kapitalo paskirstymą, stop/continue sprendimus ir galutinę verslo logiką.

Output:
- strateginiai prioritetai,
- stop / continue sprendimai,
- capital allocation,
- produktų portfelio kryptis.

### 2. Agent Academy Layer

Atsako už tai, kad kiekvienas agentas mąstytų kaip savininkas, CFO, QA breaker, klientų tyrėjas ir operatorius.

Output:
- mokymų moduliai,
- agentų capability map,
- weekly training ritual,
- skill gate prieš savarankišką darbą.

### 3. Task Bus / Execution Layer

Atsako už užduočių gimimą, statusą, ownerius, next action ir proof.

Output:
- `OPS/task_board.json`,
- daily blockers,
- done proof,
- execution metrics.

### 4. Memory / Learning Layer

Atsako už sprendimų, klaidų, pamokų, competitor insight ir idėjų istoriją.

Output:
- decision memory,
- weak work memory,
- lessons learned,
- competitor findings,
- reusable playbooks.

### 5. Market / Competitor Intelligence Layer

Atsako už realybės patikrinimą: konkurentai, kainos, CTA, trust, delivery, silpnos vietos.

Output:
- competitor DB,
- gap map,
- pricing comparison,
- weekly opportunities,
- offer repositioning.

### 6. Product Gate / Judge Layer

Atsako už stage gates: idea, validated problem, build ready, demo ready, QA ready, deploy ready, sell ready, delivery ready.

Output:
- product stages,
- release checklist,
- sell-ready checklist,
- veto decisions.

### 7. Product / Build Layer

Atsako už realų produkto kūrimą, prototipus, DB, API, UI, automations ir integration logic.

Output:
- working product,
- run instructions,
- test output,
- deploy-ready artifact.

### 8. QA / Red Team Layer

Atsako už produkto patikrinimą prieš klientą: bugs, edge cases, security, mobile, data loss, usability.

Output:
- bug board,
- critic checklist,
- release blockers,
- incident lessons.

### 9. Deploy / Reliability Layer

Atsako už GitHub -> server / hosting -> health check -> rollback.

Output:
- deploy SOP,
- health checks,
- smoke tests,
- rollback notes,
- release status.

### 10. Revenue / Growth Layer

Atsako už leadus, outreach, ads, landing conversion, demo, proposals, follow-up, invoice.

Output:
- lead pipeline,
- campaign brief,
- outreach log,
- offer pack,
- paid pilots.

### 11. CFO / Economics Layer

Atsako už kainodarą, kaštus, maržą, break-even, ROI, riziką ir kapitalo prioritetus.

Output:
- cost log,
- pricing logic,
- margin checks,
- package economics,
- stop criteria.

### 12. Delivery / Customer Success Layer

Atsako už intake, scope, 72h delivery, handoff, support, maintenance, feedback.

Output:
- intake form,
- delivery brief,
- handoff doc,
- maintenance offer,
- feedback loop.

## Marketplace / Parts Commerce OS cross-layer

Marketplace nėra atskiras svajonių projektas. Jis turi kilti iš internal OS:

1. seller,
2. warehouse,
3. location,
4. part,
5. pricing,
6. listing,
7. reservation,
8. order,
9. shipment,
10. return,
11. learning.

Kiekviena dalis turi būti workflow objektas, ne tik prekė.

## Universal Growth / Ads cross-layer

Reklamos ir growth sistema turi būti universali visiems produktams. Ji negali būti pririšta prie vieno produkto. Kiekvienas naujas produktas gauna campaign brief, target segment, offer, message angle, creative angle, CTA, budget logic ir measurement plan.

## Decision law

Kiekvienas rimtas sprendimas turi atsakyti:

1. Kas pirkėjas?
2. Koks skausmas?
3. Kokia alternatyva?
4. Kodėl mes geresni?
5. Kiek tai kainuoja?
6. Kokia marža?
7. Kas gali nepavykti?
8. Ką testuojame pirmiausia?
9. Kada stabdome?
10. Koks proof, kad judame teisingai?

## Agent operating law

Agentas negali baigti darbo be bent vieno iš šių proof:

- task board update,
- decision memory entry,
- competitor profile,
- product gate update,
- test/bug proof,
- deploy/health proof,
- revenue pipeline movement,
- CFO margin check,
- delivery artifact,
- marketplace workflow/data model update.

## Architecture priority order

1. Revenue path visible.
2. Delivery path repeatable.
3. QA and risk controlled.
4. CFO economics known.
5. Product deployable.
6. Marketplace/internal OS mappable.
7. Ads/growth engine reusable.
8. Agent learning compounding.

## What must not happen

- More ideas without gates.
- More agents without owner/output.
- More products without sales path.
- More outreach without pipeline.
- More build without QA.
- More delivery without intake.
- More marketplace talk without data model.
- More strategy without proof.
