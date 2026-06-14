# AI Master Intake and Benchmark

Date: 2026-06-14
Owner: Model Council + CTO-1 AI Systems Architect + QA Critic-C5
Status: active_intake

## Kodėl sukurtas

Vartotojas nurodė, kad atsirado „AI Master“ tipo įrankis/modelis, kurį labai giria. Kadangi pavadinimas bendrinis ir be oficialios nuorodos nėra vienareikšmiškai identifikuotas, sistema turi jį išnaudoti per saugų benchmarką, o ne aklai prijungti prie duomenų, repo, klientų ar mokėjimų.

## Pagrindinis principas

Giriamas AI įrankis nėra automatiškai geras mūsų verslui.

Jis tampa naudingas tik tada, kai realiai pagerina bent vieną iš šių rodiklių:

- Parts Seller OS workflow sprendimą,
- EU seller learning rules extraction,
- public data provenance kokybę,
- revenue lead/offer kokybę,
- CFO/margin skaičiavimą,
- QA klaidų radimą,
- UI/conversion kokybę,
- deploy/delivery patikimumą,
- darbo greitį be proof kokybės kritimo.

## Saugumo statusas

Kol AI Master neidentifikuotas oficialiu URL / tiekėju / terms / data policy:

- negalima duoti privačių klientų duomenų,
- negalima duoti secrets, API keys, cookies, .env,
- negalima duoti full repo write access,
- negalima leisti automatinio bulk messaging,
- negalima leisti mokėjimų, deploy į production ar destruktyvių veiksmų,
- negalima naudoti kaip vienintelio sprendimo priėmėjo.

Leidžiama:

- naudoti kaip research / critique / second-opinion modelį,
- duoti anonimizuotus sample tasks,
- lyginti outputą su GPT, Claude, Gemini, Grok ar kitais modeliais,
- naudoti idėjų generavimui, QA kontrargumentams, UI copy variantams,
- naudoti tik per human/model council review.

## AI Master benchmark vartai

Įrankis pereina vartus tik jei:

1. Yra oficialus source URL arba vartotojo pateiktas screenshot/link.
2. Aiškūs data/privacy/terms signalai.
3. Yra testų rezultatai prieš bent 3 alternatyvas.
4. Output turi proof, ne vien gražų tekstą.
5. QA/Judge neranda hallucination ar unsafe automation rizikos.
6. CFO patvirtina kainą/naudą, jeigu įrankis mokamas.
7. Model Council priskiria leidžiamą rolę.

## Test suite

### Test 1 — Parts pricing reasoning

Input: viena reta naudota autodalis su OEM kodu, auto modeliu, naujos kainos signalu ir keliomis rinkos indikacijomis.

Vertinimas:

- ar randa, ko trūksta,
- ar nepateikia kainos kaip fakto be source,
- ar atskiria new/used/RHD/LHD/UK/EU,
- ar duoda floor/ask/manual review logiką,
- ar pažymi confidence.

### Test 2 — Parts Seller OS workflow

Input: 3 sample parts: low-value lamp/sensor, medium-value electrical part, rare expensive premium part.

Vertinimas:

- category,
- required fields,
- location suggestion,
- price confidence,
- listing readiness,
- QA block/manual review,
- CFO handling-cost signal.

### Test 3 — EU seller learning

Input: vieno seller/platformos vieši signalai.

Vertinimas:

- ar ištraukia reusable rules,
- ar nekopijuoja katalogo/dizaino/teksto,
- ar priskiria affected projects,
- ar duoda project injection actions.

### Test 4 — Revenue offer

Input: mažas autodalių pardavėjas su aiškiu skausmu.

Vertinimas:

- buyer pain,
- offer,
- price,
- narrow 72h deliverable,
- not-included list,
- message,
- CTA,
- maintenance upsell.

### Test 5 — QA/Judge critique

Input: mūsų pačių silpnas outputas arba generic AI landing copy.

Vertinimas:

- ar randa silpnumus,
- ar blokuoja neproofintas claims,
- ar reikalauja source/proof/test,
- ar duoda pataisymą.

### Test 6 — Code/repo review

Input: mažas PR arba failų pakeitimo planas.

Vertinimas:

- ar aptinka riziką,
- ar siūlo mažą commitą,
- ar neprašo nereikalingų refactorų,
- ar saugo secrets/security,
- ar duoda test/no-test reason.

## Scorecard

| Criterion | Weight |
|---|---:|
| Accuracy and factual discipline | 20 |
| Business usefulness | 20 |
| Proof/source discipline | 15 |
| Parts Seller OS domain fit | 15 |
| QA/risk detection | 10 |
| Speed/clarity | 10 |
| Cost/privacy/safety fit | 10 |

Passing score:

- 85+ — may join model council as specialist
- 75-84 — use only as secondary reviewer
- 60-74 — research only
- <60 — do not integrate

## Leidžiamos rolės po benchmark

| Role | Kada leidžiama |
|---|---|
| Research Scout | jei gerai ieško idėjų, bet reikia fact-check |
| QA Critic | jei gerai randa klaidas ir rizikas |
| Pricing Second Opinion | jei gerai struktūruoja kainodarą, bet reikalauja source check |
| UI Copy Variants | jei gerai rašo aiškias landing versijas |
| Revenue Message Critic | jei pagerina offer/message kokybę |
| Code Reviewer | tik jei saugiai veikia su mažais diffais |

## Draudžiamos rolės be papildomo patvirtinimo

- autonomous repo writer,
- customer data processor,
- payment operator,
- bulk email sender,
- production deployer,
- sole CFO/pricing authority,
- scraper without permission,
- legal/financial final advisor.

## Pirmas naudojimas mūsų sistemoje

Kol AI Master nėra pilnai identifikuotas, jis naudojamas taip:

1. Sukuriamas anonimizuotas test promptas.
2. Tas pats promptas duodamas GPT, Claude/Gemini/Grok ir AI Master.
3. Outputs lyginami per scorecard.
4. Geriausi rules įrašomi į knowledge_sync_bus.
5. Jei AI Master laimi konkrečioje srityje, jam priskiriama tik ta siaura rolė.

## Done proof

Šis intake laikomas aktyviai panaudotu tik kai yra:

- `OPS/model_council/ai_master_evaluation_queue.json`,
- bent 6 benchmark tasks,
- bent 1 realus output comparison row,
- QA/Judge verdict,
- CFO verdict jei mokamas,
- project injection actions, jeigu output gerina kitus projektus.
