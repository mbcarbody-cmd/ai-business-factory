# Engineering Roles and Stack LT

Date: 2026-06-12
Owner: CTO-1 Product Factory Architect
Purpose: aiškiai nuspręsti kokių programuotojų reikia dabar, kokių vėliau, ir kada Java / Spring žmogus tampa būtinas.

## Dabartinis verdiktas

Java programuotojas dabar nėra pirmas kritinis hire. Dabartiniam AI Business Factory etapui svarbiausia greitai uždaryti revenue, delivery, QA, product gates, marketplace MVP ir automation workflows.

Java / Spring programuotojas reikalingas vėliau, kai sistema taps rimtu backend produktu su didesniu duomenų kiekiu, integracijomis, role-based access, audit logs, payments, warehouse API, mobile scan flows ir enterprise tipo stabilumu.

## Ar Java žmogus jau yra mūsų sistemoje?

Kaip role — ne atskirai. Dabartinėje architektūroje yra CTO / Product Factory, DevOps, QA/SRE, Marketplace, Data/Pricing ir WMS kryptys. Jos gali priimti Java developerį, bet Java role dar nėra atskirai aprašyta.

## Ko reikia dabar

### 1. Full-stack product builder

Prioritetas: P0

Kodėl: reikia greitai kurti landing, dashboard, forms, lead pipeline, simple API, admin UI, workflow tools.

Galimas stack: TypeScript / JavaScript, Node, Next.js arba paprastas web stack.

### 2. Automation / integration engineer

Prioritetas: P0

Kodėl: reikia jungti AI, scraping, emails, forms, marketplace data, CSV, APIs, Google Sheets, n8n/Make tipo workflow.

Galimas stack: Python, Node, n8n, Make, APIs.

### 3. Data / pricing engineer

Prioritetas: P0

Kodėl: naudotų dalių kainodara, competitor prices, floor price, liquidity score, duplicate detection, fitment data.

Galimas stack: Python, SQL, data pipelines.

### 4. Backend / API engineer

Prioritetas: P1

Kodėl: kai atsiranda realūs users, auth, roles, DB, audit logs, orders, warehouse/location API.

Galimas stack: Node/TypeScript pradžioje; Java/Spring arba Kotlin vėliau jei reikia enterprise stabilumo.

### 5. DevOps / reliability engineer

Prioritetas: P1

Kodėl: deploy, health checks, backups, monitoring, rollback, logs, security.

Galimas stack: Docker, Linux, GitHub Actions, cloud hosting.

### 6. Java / Spring engineer

Prioritetas: P2 dabar, P1 kai prasideda rimtas commerce backend.

Reikalingas kai:

- turime daug API ir DB transakcijų,
- reikia order/payment/reservation logikos,
- reikia RBAC ir audit logs,
- reikia patikimo warehouse/order backend,
- jungiamės prie enterprise sistemų,
- norime microservices arba didesnės backend disciplinos.

Ne pirmas pasirinkimas kai:

- dar testuojame offerius,
- dar nėra mokančių klientų,
- reikia greito MVP,
- workflow galima padaryti su Node/Python/no-code,
- svarbiau sales ir delivery nei enterprise architektūra.

## Kada Java tampa būtina

Java / Spring developeris tampa būtinas, jei bent 3 iš šių sąlygų yra true:

1. Turime realių mokančių klientų su daily usage.
2. Turime daugiau nei vieną seller/warehouse account.
3. Turime order/reservation/payment workflow.
4. Reikia role-based access ir audit logs.
5. Duomenų kiekis ir transakcijos tampa svarbios.
6. Reikia integracijų su išorinėmis enterprise/WMS/ERP sistemomis.
7. Node/no-code sprendimai pradeda lūžti arba tampa sunkiai prižiūrimi.

## Rekomenduojama seka

1. Dabar: Full-stack JS/TS + Python/data/automation.
2. Po pirmų paid pilots: backend/API discipline, DB schema, auth, deploy.
3. Po Parts Commerce OS MVP: nuspręsti Node/TypeScript ar Java/Spring pagal load, complexity ir hiring cost.
4. Kai atsiranda multi-seller marketplace: Java/Spring/Kotlin backend architect gali tapti labai vertingas.

## Java role aprašymas ateičiai

Role: Senior Java / Spring Backend Engineer

Atsakomybės:

- domain model: seller, warehouse, location, part, listing, reservation, order, shipment, return,
- REST/GraphQL APIs,
- PostgreSQL schema,
- transactions and concurrency,
- RBAC and audit logs,
- payments/order reliability,
- integrations,
- tests,
- performance and monitoring.

KPI:

- API stable,
- order/reservation workflow reliable,
- no data loss,
- tests pass,
- deploy and rollback documented,
- backend supports marketplace scaling.

## Final rule

Nesamdyti Java vien dėl to, kad Java rimtai skamba. Samdyti Java tada, kai turime backend problemą, kuri verta Java disciplinos. Dabar svarbiausia greitas MVP, mokantys klientai, duomenų kokybė, pricing, warehouse workflow ir delivery repeatability.
