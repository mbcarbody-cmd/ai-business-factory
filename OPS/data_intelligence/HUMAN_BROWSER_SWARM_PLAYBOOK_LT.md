# Human Browser Research Swarm

Date: 2026-06-14
Owner: CI-1 Market Spy Chief + CISO / Security Judge
Status: active

## Tikslas

Sukurti ne plepančius agentus, o viešos informacijos rinkimo sistemą, kuri imituoja atsargų žmogaus tyrimą: skirtingos užklausos, skirtingi šaltiniai, aiškūs URL, data, confidence, dedupe ir draudimas vadinti duomenis tiesa be šaltinio.

## Pagrindinė taisyklė

Agentas negali rašyti: „rasta internete“.

Agentas privalo rašyti:

- source_url,
- checked_at,
- query_used,
- extracted_fields,
- confidence,
- allowed_use,
- blocker_or_uncertainty,
- dedupe_key,
- next_action.

## Saugumo ir teisėtumo rėmai

Leidžiama:

- rankinė viešų puslapių peržiūra,
- viešų kainų/CTA/fitment signalų santrauka mažais kiekiais,
- šaltinio URL ir patikrinimo datos įrašymas,
- konkurentų kainodaros/pozicionavimo analizė,
- seller-owned duomenų importas, kai duomenis pateikia pats pardavėjas,
- API arba leidimu pagrįsta integracija.

Draudžiama:

- masinis katalogų kopijavimas,
- apsaugų apėjimas,
- agresyvus automatizuotas scrape,
- duomenų perpardavinėjimas kaip savo katalogo,
- naudoti eilutes be source_url ir confidence,
- siųsti automatizuotas masines žinutes be review.

## Swarm struktūra

| Cohort | Agentų tipas | Darbas | Output |
|---|---|---|---|
| HB-001 | RRR/Ovoko public signal researchers | Vieši brand/category/model signalai ir mažos pavyzdinės eilutės | `OPS/marketplace/rrr_public_seed_samples_2026_06_14.json` |
| HB-002 | Competitor price verifiers | Zapier/Make/n8n/Airtable/Ovoko/RRR/Partly kainos, CTA, silpnybės | `OPS/competitor_intelligence/competitors.json` |
| HB-003 | Lead company finders | Tikslios viešos LT/ES įmonės, kontaktiniai kanalai, pain hypothesis | `OPS/revenue_ops/lead_pipeline.json` |
| HB-004 | Parts fitment/query builders | OEM, modelių, kategorijų paieškos užklausų generavimas | `OPS/data_intelligence/browser_research_queue_2026_06_14.json` |
| HB-005 | QA provenance auditors | Tikrina, ar nėra eilučių be šaltinio, datos, confidence | `OPS/qa/bug_board.json` |

## 1000 agentų taisyklė

1000 virtualių browser agentų negali daryti 1000 vienodų paieškų.

Jie turi būti padalinti taip:

- 250 OEM/code price query agents,
- 200 model/category market signal agents,
- 150 competitor pricing agents,
- 150 lead-company agents,
- 100 compliance/provenance auditors,
- 100 dedupe/normalization agents,
- 50 QA critics.

Kiekvienas agentas gauna vieną query arba vieną šaltinį, bet nekuria atskiro produkto. Rezultatas eina į vieną canonical output path.

## RRR/Ovoko darbo būdas

1. Atidaryti viešą brand/category/model puslapį.
2. Neimti viso katalogo.
3. Paimti tik mažą seed signalą produkto logikai: part name, code, model, price, source URL, checked_at, confidence.
4. Eilutę naudoti tik kaip pricing/listing/category logic pavyzdį.
5. Produkcijai naudoti seller-owned export, API arba leidimą.

## Query šablonai

- `site:rrr.lt OEM_CODE`
- `site:rrr.lt "part name" "model"`
- `site:rrr.lt/naudotos-autodalys "brand" "model"`
- `site:ovoko.* OEM_CODE used part price`
- `"OEM_CODE" "used" "price" "Europe"`
- `"part name" "brand model" "used auto parts"`
- `"auto dismantler" Lithuania used parts email`
- `"naudotos auto dalys" "ardymas" "kontaktai"`

## Confidence modelis

- `public_page_verified` — matyta viešame puslapyje ir yra URL/data.
- `search_snippet_only` — tik paieškos snippet, negalima naudoti kainodaros sprendimui.
- `seller_owned` — pateikta vartotojo/savininko duomenų eksportu.
- `api_or_permissioned` — gauta per API arba su leidimu.
- `stale` — senas arba nepatvirtintas signalas.
- `blocked` — šaltinis neleidžia naudoti / nėra aiškaus leidimo / trūksta URL.

## Done proof

Swarm laikomas veikiančiu tik kai yra:

1. ne mažiau kaip 20 realių eilučių su source_url + checked_at + confidence,
2. bent 5 verified competitor rows,
3. bent 10 exact public company lead rows,
4. dedupe taisyklė,
5. QA bug board patikra,
6. viena Parts Seller OS demo lentelė, naudojanti realų seed failą.

## Pirma vykdoma komanda agentams

Nuo šiol kiekvienas market/data agentas pirmiausia tikrina, ar gali rasti viešą, leidžiamą, cituojamą šaltinį. Jeigu ne — rašo blocker ir pereina prie kito query. Nėra URL — nėra fakto.
