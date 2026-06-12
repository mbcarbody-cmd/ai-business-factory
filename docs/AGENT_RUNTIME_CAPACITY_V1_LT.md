# Agent Runtime Capacity v1 LT

Tikslas: 100 vadovu ir 240 agentu sistema turi veikti protingai, o ne deginti serveri tusciais procesais.

## Pagrindine taisykle

Agentas nera nuolat veikiantis procesas. Agentas yra role, taisykles, atmintis, teises, uzduociu tipai ir output kriterijai.

Serveris turi vykdyti ne visus agentus vienu metu, o tik aktyvias uzduotis eileje.

## Runtime modelis

1. Orchestrator: parenka prioritetus ir paskirsto uzduotis.
2. Queue: laiko laukiamas uzduotis.
3. Worker pool: vykdo tik ribota kieki uzduociu vienu metu.
4. Memory: saugo sprendimus, klaidas ir pamokas.
5. Judge: tikrina kokybe ir pinigu logika.
6. Scheduler: paleidzia periodines uzduotis.
7. Budget guard: stabdo brangius arba nenaudingus veiksmus.

## Rekomenduojamas startas

Pradziai paleisti:
- 1 orchestrator;
- 2-4 workeriai;
- 1 scheduler;
- 1 DB;
- 1 log ir monitoring sluoksnis.

Vadovu ir agentu gali buti daug dokumentuose, bet vienu metu veikia tik uzduociu vykdytojai.

## Protingumo taisykles

Kiekvienas agentas privalo tureti:
- domain;
- decision rights;
- money logic;
- risk logic;
- done proof;
- kill criteria;
- memory update.

Be situ lauku agentas laikomas neveikianciu.

## Serverio pakopos

Small VPS:
- tinka dokumentams, task board, API, basic workers, scheduler.
- netinka daug vietinio AI modeliu darbo.

Medium VPS:
- tinka keliems workers, DB, monitoring, basic rendering.
- geras pirmam production etapui.

Large server:
- reikia tik kai bus daug klientu, daug video rendering arba daug lokaliu modeliu.

## Svarbiausia

240 agentu nereiskia 240 serverio procesu.
240 agentu reiskia 240 specializuotu sprendimu roliu, kurias orkestratorius kviecia tada, kai reikia.

## Done criteria

Sistema paruosta, kai yra:
- agent registry;
- task queue;
- worker pool;
- memory ledger;
- judge gate;
- cost guard;
- runtime dashboard;
- weekly agent performance review.
