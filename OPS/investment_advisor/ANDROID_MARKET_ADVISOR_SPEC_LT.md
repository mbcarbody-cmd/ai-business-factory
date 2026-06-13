# Android Market Advisor App Spec LT

Date: 2026-06-13
Owner: PRODUCT-INVEST-1 Market Intelligence PM + CTO-1 Product Factory Architect + JUDGE-1 Release Gate Judge
Status: P0 product candidate / internal-first MVP

## Tikslas

Sukurti Android appsa, kuris stebi rinkas, daro izvalgas, sudaro investavimo scenarijus ir siuncia rizikos bei galimybiu pranesimus apie auksa, ETF, nafta, indeksus, technologijas, valiutas ir kitus instrumentus.

Pirmas variantas nera brokeris ir nevykdo pavedimu. Jis yra sprendimu pagalbininkas:

- stebi rinką;
- rodo trendą, riziką, momentum ir sentimentą;
- rodo stebėjimo zonas ir rizikos zonas;
- kuria scenarijus pagal vartotojo riziką;
- siunčia pranešimus;
- veda portfelio žurnalą;
- leidžia tikrinti istorines taisykles;
- paaiškina, kodėl atsirado perspėjimas.

## Kodėl ne nuo automatinio investuotojo

Automatinis investuotojas, kuris pats vykdo pavedimus arba duoda personalizuotas rekomendacijas kitiems vartotojams, gali tapti reguliuojama finansine paslauga. Todėl MVP darome kaip:

1. private/internal decision-support;
2. educational market alert app;
3. no order execution;
4. no guaranteed returns;
5. no hidden leverage/CFD push;
6. every alert has risk explanation;
7. user makes final decision.

## Pirmi stebimi aktyvai

### Commodities

- XAU / gold spot;
- WTI crude;
- Brent crude;
- silver optional later;
- natural gas optional later.

### ETF / funds

- S&P 500 ETF variants;
- Nasdaq / technology ETF;
- semiconductor ETF;
- world ETF;
- dividend ETF;
- bond/cash-like ETF later.

### Macro / risk indicators

- DXY / USD index;
- US 10Y yield;
- EUR/USD;
- VIX;
- inflation / CPI dates;
- central bank decisions;
- oil inventory events;
- earnings/calendar for major tech.

## MVP funkcijos

### 1. Watchlist

Vartotojas prideda aktyvus:
- symbol;
- name;
- asset class;
- currency;
- exchange/source;
- investment thesis;
- max allocation;
- alert thresholds.

### 2. Market dashboard

Kiekvienam aktyvui:
- current or delayed price;
- 1d / 1w / 1m / 6m / 1y return;
- trend state;
- momentum state;
- volatility state;
- risk state;
- alert state;
- next review action.

### 3. Market regime engine

Režimai:
- WATCHLIST IDEA: įdomu, bet sąlygų dar nėra;
- ENTRY REVIEW ZONE: sąlygos vertos peržiūros, bet reikia risk check;
- HOLD / NO ACTION: nėra stipraus pokyčio;
- PROFIT REVIEW ZONE: verta peržiūrėti pozicijos dydį ir riziką;
- RISK REVIEW ZONE: reikia peržiūrėti neigiamą scenarijų;
- NO CLEAR EDGE: rinka neaiški.

### 4. Investment scenario builder

Planui reikia:
- kapitalo suma;
- timeframe;
- risk level;
- max drawdown comfort;
- existing holdings;
- monthly contribution;
- forbidden assets;
- target allocation.

Output:
- allocation scenario;
- staged entry scenario;
- invalidation/risk condition;
- rebalance date;
- reasons;
- risks.

### 5. Notifications

Pranešimai:
- price crosses target;
- trend change;
- momentum extreme;
- drawdown opportunity;
- macro event tomorrow/today;
- ETF reaches planned review zone;
- portfolio allocation drift;
- high-risk warning.

Notification text must avoid blind commands:
- use "Market alert: ENTRY REVIEW ZONE. Check risk and plan before action.";
- every alert links to reasoning page.

### 6. Portfolio journal

Kiekvienas sprendimas:
- date;
- asset;
- planned action;
- actual action;
- price;
- amount;
- thesis;
- emotion note;
- alert state at the time;
- result after 1w/1m/3m.

### 7. Garage module

"Garazas" yra idėjų parkingas:
- asset idea;
- why interesting;
- current risk;
- review conditions;
- evidence;
- wait trigger;
- kill trigger.

Tikslas: nepirkti iš emocijos. Idėja pirmiausia statoma į garazą, tada market engine ją tikrina.

### 8. History test / paper mode

Prieš realius sprendimus:
- test strategy on past data;
- paper decision log;
- compare against passive benchmark;
- show max drawdown;
- show false alerts;
- show missed opportunities.

## Signalų logika MVP

Pirmas MVP naudoja taisyklių variklį, ne black-box AI.

Inputs:
- price trend: 20/50/200 MA;
- momentum: RSI, MACD optional;
- volatility: ATR / rolling volatility;
- drawdown from 52w high;
- support/resistance zones;
- macro event proximity;
- news/sentiment later;
- portfolio allocation drift.

AI naudojamas paaiškinimui ir santraukai, bet ne vienintelis režimų šaltinis.

## Data sources

MVP data source priority:

1. official/broker export for user's own holdings;
2. paid/licensed market data provider if needed;
3. free delayed data only for prototype;
4. public macro calendars;
5. news APIs only if allowed by license;
6. no scraping behind login/paywall/captcha.

Every market data point must include:
- symbol;
- source;
- timestamp;
- delay status;
- currency;
- confidence.

## Android architecture

Recommended MVP stack:

- Kotlin + Jetpack Compose;
- local Room DB;
- WorkManager for scheduled sync;
- Firebase Cloud Messaging or local notifications;
- backend later: FastAPI/Node + Postgres;
- first prototype can be local-first JSON data;
- charts: MPAndroidChart or Compose chart library;
- no broker API integration in MVP.

## Screens

1. Home dashboard.
2. Asset detail page.
3. Alert reasoning page.
4. Watchlist.
5. Portfolio.
6. Garazas.
7. Alerts.
8. Journal.
9. Settings / risk profile.
10. Data source status.

## Risk profile

Fields:
- time horizon optional;
- capital size;
- monthly contribution;
- max loss tolerated;
- max single asset allocation;
- leverage allowed: default no;
- CFD allowed: default no;
- crypto allowed: optional;
- review discipline preference;
- tax/currency note.

## Guardrails

The app must never:
- guarantee profit;
- hide risk;
- encourage leverage by default;
- execute trades without explicit licensed broker integration and legal approval;
- generate alert without data timestamp;
- send alert without reasoning;
- use stale price as current;
- confuse educational market alert with regulated advice for public users.

## First MVP slice

Smallest useful build:

1. Watchlist with 8 instruments.
2. Manual/current CSV or mock data ingestion.
3. Rule-based market regime engine.
4. Asset dashboard.
5. Alert rules.
6. Portfolio journal.
7. Garazas module.
8. Android UI prototype.
9. History-test placeholder.
10. Legal/risk disclaimer screen.

## Done proof

MVP is done when:

- app opens on Android emulator;
- watchlist loads sample assets;
- each asset has market regime state;
- alert has reasoning;
- user can add target alert;
- user can add idea to Garazas;
- user can log a decision;
- no execution/trading API exists;
- QA verifies stale-data warning;
- CFO estimates data/tool costs.
