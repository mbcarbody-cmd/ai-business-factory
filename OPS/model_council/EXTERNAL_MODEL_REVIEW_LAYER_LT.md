# External Model Review Layer LT

Date: 2026-06-12
Owner: CTO-1 Product Factory Architect + JUDGE-1 Release Gate Judge
Purpose: naudoti Claude ar kitus stiprius modelius kaip kontroliuojamą antrą nuomonę, o ne kaip chaotišką papildomą kanalą.

## Pagrindinė pozicija

Kiti modeliai neturi pakeisti mūsų operating system. Jie turi padėti geriau tikrinti, lyginti, rašyti alternatyvas ir gerinti architektūrą.

## Kodėl Claude verta naudoti

Claude Code oficialiai aprašomas kaip įrankis, kuris gali skaityti codebase, redaguoti failus, vykdyti komandas ir integruotis su development tools. Tai naudinga repo review, testų, dokumentacijos, refactor ir PR analizės darbams.

MCP yra atviras standartas AI aplikacijoms jungtis prie duomenų, įrankių ir workflow. Todėl mūsų OS turi būti projektuojamas taip, kad ateityje galėtų turėti vieną saugų data/tool sluoksnį keliems modeliams.

## Rolės

### 1. Codebase Reviewer

Tikrina:
- ar logika aiški,
- ar trūksta testų,
- ar yra pasikartojimų,
- ar architektūra nesusipainiojusi,
- ar pakeitimas turi aiškų outputą.

Output:
- review notes,
- improvement tasks,
- test suggestions,
- architecture notes.

### 2. Long Context Auditor

Tikrina:
- ar dokumentai neprieštarauja vieni kitiems,
- ar task board atitinka roles,
- ar product gates atitinka revenue, CFO, QA ir delivery,
- ar nėra tuščių strategijos vietų.

Output:
- inconsistency report,
- missing link report,
- cleanup task list.

### 3. Alternative Strategist

Tikrina:
- 3-5 alternatyvius kelius,
- kiekvieno kelio kainą,
- greitį,
- riziką,
- revenue potencialą,
- delivery sudėtingumą.

Output:
- alternative matrix,
- recommended path,
- stop criteria.

### 4. Product Critic

Tikrina:
- ar klientas pirktų,
- ar offer aiškus,
- ar pažadas nėra per platus,
- ar delivery realus,
- ar yra QA ir CFO logika.

Output:
- product risk note,
- needed fixes,
- Judge recommendation.

### 5. Tooling Advisor

Padeda:
- projektuoti MCP-compatible data/tool sluoksnį,
- aprašyti tool schemas,
- suderinti GitHub, task board, memory, revenue pipeline ir marketplace data.

Output:
- tool architecture note,
- schema proposal,
- integration task list.

## Ko mokytis iš Claude ekosistemos

1. Project instruction file: vienas aiškus repo instruction/memory failas.
2. Skills: pasikartojančius workflow paversti reusable agent skills.
3. Hooks: po veiksmų automatiškai paleisti format, test, QA ar task update.
4. MCP: data/tool jungtis daryti standartizuotai.
5. Multi-agent sessions: dideles užduotis skaidyti į mažas roles su aiškiais outputais.
6. Permission modes: agentų veiksmus riboti pagal riziką.
7. Diff review: svarbius pakeitimus tikrinti per diff ir proof.

## Kada naudoti external model review

Naudoti kai:
- reikia antros nuomonės,
- reikia code review,
- reikia ilgo dokumento auditavimo,
- reikia alternatyvų matricos,
- produktas eina į sell-ready,
- planuojamas naujas marketplace/workflow modulis,
- norime patikrinti ar architektūra neper sudėtinga.

## Kada nenaudoti

Nenaudoti kai:
- nėra aiškaus klausimo,
- nėra output formato,
- užtenka paprasto task update,
- nėra planuojamo review,
- užduotis per daug smulki.

## Output contract

Kiekvienas external model review turi grąžinti:

1. Top issues.
2. Top opportunities.
3. Recommended task board updates.
4. Product gate risks.
5. CFO/revenue impact.
6. Next 3 repo actions.

## Multi-model council

- ChatGPT: CEO reasoning, architecture, business strategy, marketplace design.
- Claude: codebase audit, long-context review, alternative plans, PR review.
- Smaller models: repetitive extraction, classification, data cleanup.

## Final rule

External models yra patarėjai ir auditoriai. Galutinė kontrolė lieka mūsų repo OPS: task board, product gates, QA, CFO, revenue ir delivery sluoksniai.
