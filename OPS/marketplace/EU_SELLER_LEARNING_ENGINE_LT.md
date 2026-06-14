# EU Seller Learning Engine — ne kopijavimo, o rinkos taisyklių mokymosi sistema

Date: 2026-06-14
Owner: CEO-A Parts OS General Manager + CI-1 Market Spy Chief + JUDGE-1 Release Gate Judge
Status: active
Linked tasks: OPS-003, OPS-019, OPS-022

## Tikslas

Išanalizuoti EU naudotų autodalių pardavėjus ir marketplace’us tam, kad Parts Seller OS išmoktų bendras rinkos taisykles:

- kaip struktūruojamas dalių katalogas,
- kaip pirkėjas ieško dalies,
- kokie duomenys būtini listingui,
- kaip formuojamas pasitikėjimas,
- kaip veikia grąžinimas/garantija,
- kaip pristatymas ir šalis keičia kainą,
- kaip pardavėjas turi paruošti dalį pardavimui,
- kokios listing klaidos mažina konversiją,
- kokie UI šablonai kartojasi per skirtingas platformas.

Sistema **nesiekia kopijuoti** svetainių, katalogų, nuotraukų, dizaino, tekstų ar duomenų bazių. Sistema mokosi abstrakčias taisykles ir verčia jas į mūsų produkto logiką.

## Pagrindinis principas

Ne kopijuojam RRR, Ovoko, Opisto, B-Parts, Autoparts24, eBay, Allegro ar kitus pardavėjus.

Mokomės jų bendrą veikimo mechaniką:

`buyer intent -> vehicle/part identification -> listing quality -> price confidence -> trust -> delivery -> return/warranty -> seller workflow`

## Ką agentai privalo rinkti iš kiekvieno EU seller/platformos

| Learning field | Ką reiškia | Parts Seller OS panaudojimas |
|---|---|---|
| Search pattern | VIN/plate, brand/model/year, OEM code, part name, category | paieškos UI ir listing title taisyklės |
| Required listing fields | part name, code, side, position, condition, photos, donor car, mileage | listing readiness score |
| Fitment logic | model generation, year range, engine, gearbox, body, LHD/RHD | compatibility confidence |
| Price display | VAT, delivery, currency, discount, seller price, marketplace fee hints | pricing confidence/floor |
| Trust signals | warranty, returns, seller rating, tested, verified seller, secure payment | seller trust score |
| Delivery rules | EU delivery, local pickup, country selector, courier options | shipping readiness |
| Return/warranty terms | 14 days, 3 months, 1 year selected parts, seller warranty | buyer protection model |
| Category taxonomy | top categories, subcategories, synonyms, side/position values | canonical category tree |
| Bad listing patterns | vague title, missing side, missing OEM, no condition, poor category | QA block rules |
| Seller workflow hints | publish, reserve, pack, ship, refund, relist, dead-stock | one-seller workflow engine |
| Monetization hints | marketplace fee, pro account, B2B discount, subscription, seller onboarding | future marketplace business model |

## Seller/platform archetypes

### 1. Large EU multi-seller marketplace

Examples to study: RRR/Ovoko, Opisto, B-Parts, Autoparts24, eBay Motors EU, Allegro automotive.

Learning target:

- marketplace trust layer,
- seller onboarding,
- centralized search,
- multi-country delivery,
- buyer protection,
- category normalization.

### 2. National dismantler network

Examples to study: French, Dutch, Polish, German, Baltic and Nordic dismantler networks.

Learning target:

- how yards expose stock,
- how part request forms work,
- how seller identity is shown,
- how warranty and delivery are handled per seller.

### 3. Individual professional dismantler/e-shop

Examples to study: independent dismantlers with their own shops and stock exports.

Learning target:

- practical inventory structure,
- local warehouse logic,
- photo quality and title formats,
- weak points that our OS can fix.

### 4. New/aftermarket parts platforms

Examples to study only for UI/commercial logic: AUTODOC, Oscaro and similar.

Learning target:

- category UX,
- fitment logic,
- product filtering,
- trust and delivery presentation.

Not target:

- copying aftermarket catalogues,
- using new-part pricing as direct used-part price without confidence label.

## Universal rules already visible from first verified sources

### Rule A — buyer starts with uncertainty

Buyers search by code, brand/model, category or visible part name. System must support all four.

Parts Seller OS action:

- every part needs `search_aliases`, `oem_codes`, `category_id`, `vehicle_fitment`, `side_position`.

### Rule B — trust must be visible before payment

Marketplaces show warranty/return/delivery/security signals near the buying path.

Parts Seller OS action:

- listing readiness must include warranty status, return status, tested/untested status, and shipping readiness.

### Rule C — category tree is not optional

EU sellers all converge around category trees: lighting, body, engine, electronics, interior, brake, cooling, doors, mirrors, etc.

Parts Seller OS action:

- every item must map to a canonical category before listing.

### Rule D — bad titles kill conversion

Vague titles like “other body part” are weak. They can exist in marketplaces, but our OS should block or warn.

Parts Seller OS action:

- QA critic blocks listing when title lacks clear part function, side, position or code when required.

### Rule E — warranty/return is not decoration, it changes price confidence

A tested part with warranty can support higher price than an untested/no-return part.

Parts Seller OS action:

- pricing rules must include condition, tested status, warranty status and return risk.

### Rule F — low-value parts need handling-cost logic

A 15–25 EUR part may not be worth manual listing, packing and support unless bundled, automated or high-demand.

Parts Seller OS action:

- CFO layer must flag low-margin parts for bundle/skip/auto-list only.

### Rule G — country and platform change selling logic

A part can be cheap locally but attractive cross-border if rare, code-specific or high new price.

Parts Seller OS action:

- pricing confidence must store country/platform/source and not collapse all prices into one average.

## Agent work split

| Agent group | Mission | Output path |
|---|---|---|
| EU Seller Scouts | find sellers/platforms by country and type | `OPS/data_intelligence/eu_seller_research_targets_2026_06_14.json` |
| Rule Extractors | convert seller observations into reusable rules | this file |
| Taxonomy Mappers | map external category labels to our canonical category tree | `OPS/marketplace/category_learning_map.json` |
| Trust/Warranty Analysts | normalize returns/warranty/tested signals | `OPS/marketplace/trust_signal_rules.json` |
| Pricing Pattern Analysts | identify price display, VAT, delivery, confidence patterns | `OPS/marketplace/pricing_rules.json` |
| QA Critics | block copying and weak unsourced claims | `OPS/qa/bug_board.json` |
| Product Builders | add learned rules to Parts Seller OS workflow | `products/parts-seller-os/` |

## EU seller analysis checklist

For every seller/platform row:

1. Country / language.
2. Platform type: marketplace, dismantler network, e-shop, classified, aftermarket reference.
3. Search methods: plate/VIN, brand/model, category, OEM code, text search.
4. Category structure depth.
5. Required listing fields.
6. Fitment details.
7. Price presentation.
8. Delivery presentation.
9. Returns/warranty/tested signals.
10. Seller trust signals.
11. Payment trust signals.
12. Listing weaknesses we can improve.
13. Product rule extracted.
14. Source URL.
15. Checked date.
16. Confidence.
17. Allowed use.

## Done proof

This engine is not complete until:

- at least 50 EU seller/platform rows exist with source URL and confidence,
- at least 15 countries are covered,
- at least 100 reusable rules/signals are extracted,
- at least 20 category mappings are added,
- at least 20 trust/warranty/delivery rules are added,
- Parts Seller OS UI shows learned rules in one-seller workflow,
- QA confirms no copied catalogue/design/text dependency.

## Immediate next action

Use the research target file to create verified rows for:

1. RRR/Ovoko,
2. Opisto,
3. B-Parts,
4. Autoparts24,
5. Allegro automotive,
6. eBay Motors EU,
7. Dutch dismantler network,
8. German dismantler/e-shop examples,
9. Polish dismantler/e-shop examples,
10. Baltic seller examples.

Then convert observations into product rules, not copied data.
