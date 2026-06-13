# Public Data Collection Policy LT

Date: 2026-06-13
Owner: CI-1 Market Spy Chief + CISO / Security Judge + JUDGE-1 Release Gate Judge
Status: active P0 guardrail

## Tikslas

Leisti AI robotu fabrikui rinkti verslui naudinga informacija is interneto platybiu, bet tik taip, kad procesas butu legalus, saugus, pakartojamas, nedubliuotu darbu ir nesukurtu reputacines rizikos.

## Pagrindine taisykle

Public data intelligence nera laisvas scrapingas. Kiekvienas duomenu rinkimas turi tureti:

1. task ID;
2. source registry irasa;
3. leidziama metoda;
4. robots.txt / ToS / API patikra;
5. rate limit;
6. duomenu schema;
7. kokybes patikra;
8. output path;
9. owner;
10. done proof.

No source registry = no scrape.
No permission check = no automation.
Login-gated data = blocked unless explicit account/API permission.
Captcha bypass = blocked.
Paywall bypass = blocked.
Personal data collection = high risk and requires minimization + legal basis check.

## Leidziami metodai pagal prioriteta

### 1. Oficialus API arba data feed

Naudoti pirma, kai imanoma.

Pavyzdziai:
- marketplace API;
- affiliate/product feed;
- Google Sheets export su leidimu;
- RSS;
- sitemap;
- partnerio CSV/XML.

Status: lowest risk.

### 2. Manual verification + structured entry

Naudoti kai reikia kainu, CTA, competitor offeriu, leadu ar rinkos signalu ir nera API.

Status: safe start.

### 3. Low-rate public fetch

Naudoti tik kai:
- puslapis public;
- nera login;
- nera captcha;
- robots/terms nepriestarauja;
- rate limit mazas;
- renkama tik butina info.

Default rate:
- <= 1 request / 10-15 seconds / domain;
- no parallel crawl without approval;
- no full-site crawl unless explicit approved task.

### 4. Headless browser rendering

Naudoti tik public puslapiams, kai informacija atsiranda po JavaScript render.

Blocked:
- login simulation be leidimo;
- cookie/session reuse be leidimo;
- captcha solving;
- anti-bot bypass;
- fingerprint evasion;
- hidden endpoint abuse.

### 5. Third-party SERP/search/data providers

Naudoti kai kaina mazesne uz rizika ir kai laikomasi providerio taisykliu.

Status: CFO must approve paid providers.

## Draudziami veiksmai

AI agentams ir scraperiams draudziama:

- apeiti captcha;
- apeiti paywall;
- naudoti svetimus cookies/session tokens;
- bandyti password reset/login brute force;
- rinkti nebutinus asmens duomenis;
- rinkti private messages, account data, order data be leidimo;
- floodinti puslapius;
- ignoruoti disallow be Security Judge sprendimo;
- kopijuoti didelius teksto/content kiekius i musu produktus;
- pardavineti scraped copyrighted content kaip musu originalu turini;
- imituoti kita user-agent apgaules tikslu.

## Duomenu tipai ir rizika

### Low risk

- public plan prices;
- public CTA;
- public product feature list;
- public company name;
- public website URL;
- public business category;
- public product price visible without login.

### Medium risk

- public email/contact form;
- marketplace listing price history;
- seller names;
- large-scale repeated collection;
- pages with unclear ToS.

### High risk

- personal names + emails at scale;
- phone numbers;
- profile pages;
- social media scraping;
- reviews containing personal info;
- images of people;
- vehicle VIN tied to person;
- anything login-gated.

### Blocked unless explicit legal/owner approval

- special category personal data;
- private account/order data;
- payment data;
- medical/financial/legal client data;
- stolen/leaked datasets;
- bypassed or hacked data.

## Public data pipeline

1. Define question.
2. Check if data already exists in repo/memory.
3. Add source to `OPS/data_intelligence/source_registry.json`.
4. Run permission checklist.
5. Choose allowed method.
6. Collect smallest useful sample.
7. Normalize into schema.
8. Verify with at least one second source or manual spot check.
9. Write to output path.
10. Update task board, memory and downstream product/revenue tasks.

## Quality rules

Kiekvienas duomenu irasas turi tureti:

- source_url;
- collected_at;
- method;
- confidence;
- field-level uncertainty if needed;
- owner;
- next_action.

Confidence:
- high: official source or direct visible page verified today;
- medium: public page but uncertain currency/date/scope;
- low: third-party mention, old page, cached page, unclear source;
- rejected: unverifiable or not allowed.

## AI summarization rule

AI gali apibendrinti public data, bet negali:
- pateikti spėjimų kaip faktų;
- išgalvoti kainų, kontaktų ar funkcijų;
- priskirti asmeniui duomenų be šaltinio;
- kopijuoti ilgų originalių tekstų į mūsų produktus.

## Recommended stack

### MVP

- manual web search;
- browser + spreadsheet/JSON entry;
- Python requests + BeautifulSoup for allowed static pages;
- Playwright only for allowed JS rendering;
- SQLite/Postgres later;
- schema validation;
- duplicate detection;
- OPS audit.

### Scale

- source registry;
- fetch queue;
- rate limiter;
- robots/ToS check cache;
- content hash dedupe;
- extraction schema per source;
- provenance ledger;
- QA sampling;
- alerting when source changes.

## Done definition

Public Data Intelligence sluoksnis laikomas veikianciu tik kai:

1. source registry turi bent 20 verified sources;
2. permission checklist naudojamas pries automatizacija;
3. kiekvienas scrape/fetch turi rate limit;
4. kiekvienas data output turi provenance;
5. revenue pipeline turi exact public leads, ne seed placeholders;
6. competitor intelligence turi verified prices/CTA;
7. AI agents cannot run blocked methods;
8. QA Judge gali blokuoti data usage.
