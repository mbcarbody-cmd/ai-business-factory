# Cross-Project Knowledge Propagation Engine

Date: 2026-06-14
Owner: Chief Learning Officer + Cross-Project Knowledge Sync Operators + CEO / Master Agent
Status: active
Linked files:

- `OPS/learning/GLOBAL_KNOWLEDGE_CORE_LT.md`
- `OPS/learning/knowledge_sync_bus.json`
- `OPS/learning/project_learning_injection_map.json`
- `OPS/TASK_BOARD/learning_scale_tasks_2026_06_14.json`

## Tikslas

Žinios neturi likti tik viename projekte. Kiekviena naudinga pamoka turi greitai nueiti į visus projektus, kuriems ji gali padėti.

Tai nėra tik Parts Seller OS akademija. Tai visos AI Business Factory žinių kraujotaka.

## Pagrindinė taisyklė

Pamoka laikoma realiai įsisavinta tik tada, kai ji:

1. užfiksuota kaip lesson,
2. normalizuota į reusable rule,
3. priskirta affected_projects,
4. turi project-specific injection action,
5. turi ownerį,
6. turi proof path,
7. turi QA/Judge patikrą,
8. bent viename paveiktame projekte pakeičia elgesį, užduotį, rule, UI, offerį, delivery arba QA.

Jeigu pamoka tik įrašyta į dokumentą ir niekur nepanaudota — sistema dar neišmoko.

## Knowledge propagation loop

`observe -> lesson -> reusable rule -> affected projects -> injection task -> project artifact update -> QA -> sync_status=synced -> memory ledger`

## Greito paskirstymo SLA

Kai atsiranda P0 pamoka:

- per tą patį darbo ciklą ji turi patekti į `knowledge_sync_bus`,
- per tą patį darbo ciklą ji turi būti priskirta affected_projects,
- bent vienas projektas turi gauti konkrečią injection action,
- jei produktas negali būti keičiamas iš karto, sukuriamas fallback task su blocker ir next action.

## Projektų grupės

### P0 aktyvūs core projektai

- Parts Seller OS
- CEO Cockpit
- Public Data Intelligence / Safe Browser Crawler
- Revenue Operations
- CFO Layer
- QA/Judge Layer
- Delivery Layer
- Deploy Loop
- Marketplace Roadmap

### P1/P2 monetizavimo ir validacijos projektai

- AI Agent Setup 72h Pilot
- Data Intelligence Monitoring
- AI Ads Factory
- YouTube Content Engine
- Android Market Advisor / Investment Advisor App
- Opportunity Lab

### Universalūs sluoksniai, kurie turi gauti visas svarbias pamokas

- Task Board
- Product Gates
- Agent Memory
- Security / Data Permission
- Design / Conversion
- CFO / Pricing
- QA / Critic
- Revenue / Lead Pipeline
- Delivery / Customer Success

## Kokios pamokos kur turi keliauti

| Lesson type | Kur privalo nueiti |
|---|---|
| Market rule | Parts Seller OS, Marketplace Roadmap, Design, Revenue, QA |
| Data provenance rule | Data Intelligence, Public Crawler, Parts Seller OS, Competitor Intelligence, Revenue, QA |
| CFO/margin rule | CFO Layer, Pricing Rules, Offers, Delivery, Revenue, Product Gates |
| Revenue rule | Revenue Ops, Landing/Offer, Delivery, CFO, CEO Cockpit, Opportunity Lab |
| QA/proof rule | QA Board, Product Gates, Deploy Loop, Delivery, All product pages |
| Design/conversion rule | CEO Cockpit, Landing pages, AI Agent Setup, AI Ads Factory, Revenue Ops |
| Delivery rule | 72h Playbook, Revenue offers, Customer Success, Product Gates, CFO |
| Security/data rule | Security Fortress, Public Data Playbooks, Crawlers, Integrations, QA |
| Anti-duplication rule | Task Board, Opportunity Lab, Learning Workforce, All CEO cells |

## Privalomas project injection formatas

Kiekviena pamoka turi turėti:

- lesson_id,
- source_project,
- reusable_rule,
- target_project,
- injection_type,
- concrete_change,
- owner,
- output_path,
- status,
- proof_required,
- fallback_next_action.

## Injection types

- `rule_update`
- `ui_update`
- `offer_update`
- `qa_check`
- `cfo_check`
- `delivery_scope_update`
- `data_schema_update`
- `task_board_update`
- `security_review`
- `demo_test`
- `revenue_message_update`
- `opportunity_gate_update`

## Anti-chaos rule

Vienas lesson gali paveikti 10 projektų, bet negali sukurti 10 skirtingų interpretacijų. Jis turi vieną canonical reusable_rule ir daug project-specific injection actions.

## Pavyzdys

Lesson: `No source_url + checked_at + confidence means no price/product/revenue decision.`

Turi nueiti į:

- Parts Seller OS: price confidence logic,
- Public Data Crawler: provenance schema,
- Competitor Intelligence: competitor row validation,
- Revenue Ops: lead/source validation,
- CFO: no margin assumption without proof,
- QA: bug if row lacks provenance.

## Done proof

Šis propagation engine veikia tik tada, kai:

- yra project learning injection map,
- yra bent 20 injection actions,
- bent 5 projektai gauna tą pačią globalią pamoką skirtingais veiksmais,
- knowledge_sync_bus turi `synced` statusų, ne tik `queued_for_sync`,
- learning audit tikrina propagation failus,
- AGENTS.md reikalauja naudoti sync bus ir project injection map.
