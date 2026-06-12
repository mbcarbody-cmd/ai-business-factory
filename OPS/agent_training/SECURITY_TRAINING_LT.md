# Security Training LT

Date: 2026-06-12
Owner: Agent Academy + CISO / Security Judge
Purpose: apmokinti visus agentus dirbti saugiai su kodu, duomenimis, AI tools, secrets, deploy ir klientu informacija.

## Training modules

### Module 1 — No Secrets

Agentas turi zinoti:
- kas yra secret,
- kur secret laikomas,
- kodel secret negalima deti i repo, promptus, logs ar screenshots,
- ka daryti aptikus secret.

Proof:
- agentas gali paaiskinti revoke/rotate procesa.

### Module 2 — Least Privilege

Agentas turi zinoti:
- naudoti maziausias teises,
- atskirti dev/staging/prod,
- neprasyti admin teisiu be reikalo.

Proof:
- taskuose nurodo permission level.

### Module 3 — AI Agent Safety

Agentas turi zinoti:
- prompt injection,
- excessive agency,
- untrusted input,
- tool permission boundaries.

Proof:
- pries tool use nurodo rizika ir approval poreiki.

### Module 4 — Secure PR

Agentas turi zinoti:
- PR checklist,
- tests/no-test reason,
- security note,
- rollback note.

Proof:
- PR summary atitinka template.

### Module 5 — Data Classification

Agentas turi zinoti:
- public,
- internal,
- confidential,
- restricted.

Proof:
- gali klasifikuoti lead/customer/secret/pricing/roadmap data.

### Module 6 — Incident Response

Agentas turi zinoti:
- stop,
- revoke,
- rotate,
- isolate,
- audit,
- document.

Proof:
- gali uzpildyti incident log.

## Graduation rule

Agentas negali savarankiskai keisti kodo ar integraciju, kol nepraeina:

- No Secrets,
- AI Agent Safety,
- Secure PR,
- Data Classification.

## Weekly drill

Karta per savaite simuliuoti viena scenariju:

- leaked token,
- public admin route,
- risky dependency,
- AI agent destructive command,
- customer data in prompt,
- failed security workflow.

## Final rule

Security training yra privalomas layer, ne pasirenkamas kursas.
