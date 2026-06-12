# RepoSell Seller OS MVP Brief v1 LT

Tikslas: sukurti pirma veikianti seller OS naudotu autodaliu pardavejams Europoje. RepoSell yra pardaveju puse. RepoBuy bus pirkeju puse, kai turesime supply, listingus ir pardaveju onboardinga.

## Product one-liner

RepoSell padeda naudotu autodaliu pardavejams greiciau sukelti, sutvarkyti, ikainoti, reklamuoti ir valdyti dalis vienoje sistemoje.

## Pirminis klientas

Naudotu autodaliu pardavejai Europoje:

- smulkus ardytojai;
- mazi sandeliai;
- e-commerce naudotu daliu pardavejai;
- pardavejai, kurie jau naudoja kelias platformas ir nori maziau rankinio darbo;
- pardavejai, kuriems reikia kainodaros, listing automation, lokaciju ir reklamos pagalbos.

## Skausmai

1. Per daug rankinio daliu sukelimo.
2. Bloga kainodara arba per pigiai parduodamos retos dalys.
3. Nera aiskaus sandelio lokaciju valdymo.
4. Dalis sunku rasti po menesio ar metu.
5. Listingai skirtingose platformose nesutvarkyti.
6. Truksta reklamos ir leadu.
7. Nera vieno dashboardo: kiek daliu, kur jos, kiek listing, kiek parduota.
8. Truksta konkurentu kainu matymo.

## MVP pazadas

Per pirma MVP RepoSell turi padeti pardavejui:

- suvesti dali;
- priskirti kategorija, koda, bukle ir lokacija;
- gauti kainos rekomendacija arba pricing note;
- matyti listing statusa;
- tureti paprasta lead arba uzsakymo statusa;
- tureti reklamos/content pasiulyma pasirinktoms dalims.

## MVP funkcijos

### 1. Part intake

Laukai:
- part title;
- category;
- brand;
- model;
- year range;
- OE / part number;
- side;
- condition;
- notes;
- photos status;
- source vehicle;
- seller;
- price;
- location;
- listing status.

### 2. Location system v1

- warehouse zone;
- shelf;
- box;
- large item location;
- pending location status;
- location notes.

### 3. Pricing note v1

- manual price;
- suggested price;
- source notes;
- confidence low / medium / high;
- competitor count;
- new part price if known;
- floor price;
- premium price.

### 4. Listing status v1

Statusai:
- draft;
- needs photo;
- needs price;
- ready;
- published;
- reserved;
- sold;
- archived.

### 5. Seller dashboard v1

Rodikliai:
- total parts;
- parts without price;
- parts without location;
- ready to publish;
- published;
- reserved;
- sold;
- high value parts;
- stale inventory.

### 6. Lead / order status v1

Statusai:
- new inquiry;
- waiting reply;
- offer sent;
- reserved;
- paid;
- shipped;
- closed lost.

### 7. Growth package v1

Kiekvienam pardavejui arba daliu grupei galima sugeneruoti:
- promotion angle;
- short post text;
- marketplace description improvement;
- 3 hooks;
- suggested channel;
- CTA.

## Kas nera MVP

Ne pirmoje versijoje:
- pilna buyer marketplace;
- automatiniai mokejimai;
- pilna shipping integracija;
- sudetingas fitment graph;
- pilnas video generatorius;
- mobile app;
- full ERP;
- dating portalas;
- dideli ads spend.

## Pirmas revenue model testas

Kol nera pilno marketplace, parduodami paketai:

1. Seller setup package.
2. Listing cleanup package.
3. Pricing assistance package.
4. Inventory and location setup package.
5. Promotion/content package.
6. Early seller onboarding package.

Kaina bus nustatyta po pirmo landing ir lead test, bet pradziai galima testuoti:

- low pilot: 99-199 EUR;
- standard setup: 299-499 EUR;
- monthly support: 99-299 EUR.

## Success metrics

Pirmas etapas laikomas sekmingu, jei:

- yra veikiantis seller intake flow;
- yra bent 50 demo daliu;
- bent 10 daliu turi pricing note;
- bent 10 daliu turi location;
- veikia seller dashboard;
- yra seller landing;
- yra 20 leadu sarasas;
- yra 5 outreach zinutes;
- yra bent 1 realus pokalbis su potencialiu selleriu;
- yra backup job.

## Squad ownership

Primary squads:

- Core Platform Squad.
- Marketplace and Parts Commerce Squad.
- Data and Pricing Intelligence Squad.
- Product UI and Conversion Squad.
- Revenue Ops and CRM Squad.
- Growth Agency.
- Media and Content Factory Squad.
- QA, DevOps, Security and Backup Squad.

## First build order

1. Data schema.
2. Part intake form.
3. Location fields.
4. Listing status.
5. Pricing note fields.
6. Seller dashboard.
7. Lead/waitlist form.
8. Landing copy.
9. Backup job.
10. Daily report.

## Risks

1. Per didelis scope.
2. Per anksti kurti buyer marketplace be seller supply.
3. Nepakankamas seller trust.
4. Blogi daliu duomenys.
5. Per mazai realiu selleriu feedback.
6. Per daug dokumentu, per mazai kodo.
7. Nera backup restore testo.

## Kill criteria

Jeigu per 30 dienu:

- nera jokio seller susidomejimo;
- nera bent 1 realaus demo pokalbio;
- niekas nenori net testuoti;
- MVP per sudetingas ir neduoda aiskaus skausmo sprendimo;

tada perziurimas offeris, auditorija arba product angle. Projektas nemarinamas automatiskai, bet keiciamas pozicionavimas.

## Next actions

1. Sukurti seller landing copy.
2. Sukurti waitlist / lead form schema.
3. Sukurti part intake schema.
4. Sukurti 50 seller segmentu sarasa.
5. Sukurti competitor map.
6. Sukurti 7 dienu content plan.
7. Sukurti backup job v1.
