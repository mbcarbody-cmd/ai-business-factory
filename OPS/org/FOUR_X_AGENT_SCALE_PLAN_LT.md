# 4x Agentu ir CEO grupiu ispletimo planas

Date: 2026-06-13
Owner: CEO / Master Agent + COO-1 Execution Architect
Status: ACTIVE / GOVERNANCE

## Tikslas

Padidinti AI organizacijos pajeguma 4 kartus, bet ne chaotiskai. Nauji projektai negali strigti, taciau pagrindinis P0 darbas negali buti isblaskytas.

Taisykle: daugiau agentu turi reiksti daugiau proof output, ne daugiau dokumentu.

## 4 CEO cell modelis

1. CEO-A Parts Seller OS — pagrindine autodaliu OS kryptis.
2. CEO-B Revenue & Delivery — pardavimai, leadai, outbound, 72h delivery ir pilotai.
3. CEO-C Build & Deploy Factory — UI, prototipai, deploy loop, QA, public demo.
4. CEO-D Opportunity Lab — nauji projektai, bet izoliuotai, be teises stabdyti P0.

Kiekvienas CEO turi savo agentu komanda, savo task board lane, savo proof path ir savo blokatoriu eskalacija.

## CEO-A Parts Seller OS komanda

Misija: padaryti veikiancia autodaliu OS nuo dalies ivedimo iki pardavimo.

R roles:
- CEO-A / Parts OS General Manager
- Product PM-A1 / Parts Intake PM
- Taxonomy Agent-A2 / Parts Category Tree Owner
- Warehouse Agent-A3 / Location and Capacity Logic Owner
- Pricing Agent-A4 / Used Parts Pricing Logic Owner
- Listing Agent-A5 / Listing Readiness Owner
- Fitment Agent-A6 / Vehicle Compatibility Owner
- QA Agent-A7 / Real Part Workflow Tester
- Data Agent-A8 / Sample Data and Import Mapping Owner
- CFO Agent-A9 / Unit Economics Owner
- Delivery Agent-A10 / Seller Onboarding Owner

## CEO-B Revenue & Delivery komanda

Misija: paversti produktus i pinigus ir pirmus pilotus.

R roles:
- CEO-B / Revenue General Manager
- CRO-B1 / Pipeline Commander
- Lead Research Agent-B2 / Exact Company Finder
- Outbound Agent-B3 / Message and Follow-up Operator
- Offer Agent-B4 / Offer Packaging Owner
- Deal Desk Agent-B5 / Scope and Proposal Owner
- Delivery Captain-B6 / 72h Pilot Execution Owner
- Customer Success Agent-B7 / Handoff and Feedback Owner
- CFO Agent-B8 / Pilot Margin Controller
- CRM Agent-B9 / Lead State Owner
- Proof Agent-B10 / Case Study Owner

## CEO-C Build & Deploy Factory komanda

Misija: daryti prototipus, ne tik planus.

R roles:
- CEO-C / Build Factory General Manager
- CTO-C1 / Architecture Owner
- Frontend Agent-C2 / UI and Cockpit Builder
- Backend Agent-C3 / Data Flow Owner
- DevOps Agent-C4 / Hosting, Smoke Test and Rollback Owner
- QA Critic-C5 / Break-Test Owner
- Security Agent-C6 / Safe Data and Permissions Owner
- Docs Agent-C7 / Runbook and Handoff Owner
- Test Agent-C8 / Fixtures and Test Cases Owner
- Bugfix Agent-C9 / Fix Queue Owner
- Design Agent-C10 / Visual Trust and Conversion Owner

## CEO-D Opportunity Lab komanda

Misija: ieskoti ir paruošti naujas kryptis, bet ne stabdyti P0.

R roles:
- CEO-D / Opportunity Lab General Manager
- Market Radar Agent-D1 / New Opportunities Scout
- Competitor Agent-D2 / Competitive Gap Analyst
- Product Scout-D3 / New Product Candidate PM
- Validation Agent-D4 / Pain and Buyer Proof Owner
- CFO Agent-D5 / Value Case and Risk Owner
- Risk Agent-D6 / Compliance Filter
- Prototype Scout-D7 / Tiny Demo Feasibility Owner
- Backlog Agent-D8 / Opportunity Parking Owner
- Stop Agent-D9 / Stop Weak Ideas Owner
- Handoff Agent-D10 / Move Proven Ideas to P0 Review

## Izoliacijos taisykle

CEO-D gali ruosti naujas kryptis, bet negali naudoti CEO-A build resursu, kol Parts Seller OS foundation incomplete.

Naujas projektas gali tapti aktyviu build tik jei turi:
- pirkeja,
- problema,
- 72h MVP,
- pinigu kelia,
- proof path,
- CFO value case,
- aisku poveiki P0 resursams.

Jei sito nera, projektas lieka backlog.

## Bendras komandų darbo rezimas

Kiekviena CEO grupe privalo kiekviename cikle tureti:
- viena pagrindini tiksla,
- viena proof output path,
- blokatoriu sarasa,
- fallback veiksma,
- CFO pastaba,
- QA kritika,
- kita konkretu veiksma.

## P0 apsauga

Kol Parts Seller OS neturi veikiancio vieno pardavejo prototipo:
- CEO-A gauna pirma build prioriteta.
- CEO-C gauna antra prioriteta, kai stato CEO-A reikalinga prototipa.
- CEO-B dirba paraleliai su lead, offer ir delivery.
- CEO-D dirba validation/backlog rezimu ir nestabdo P0.

## Sekmes matas

4x padidinimas laikomas sekmingu tik jei dideja:
- veikianciu proof output skaicius,
- uzdarytu foundation failu skaicius,
- exact lead/contact path skaicius,
- demo/prototipu skaicius,
- paid pilot galimybes,
- tasku su fallback kokybe.

## Draudziama

- Kurti nauja aktyvu projekta be CEO savininko.
- Kurti projekta be proof path.
- Judinti ideja i build be CFO value case.
- Rasyti done be failo, demo arba patikrinamo proof.
- Leisti opportunity krypciai stabdyti Parts Seller OS P0.
