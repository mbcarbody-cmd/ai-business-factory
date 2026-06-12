# Always On Revenue Runtime v1 LT

Tikslas: serveris turi dirbti 24/7 tik ten, kur yra aiskus kelias i pajamas, produkto verte arba automatizacijos nauda.

## Dabartinis principas

Vadovu ir agentu gali buti daug, bet serveris turi sukti tik aktyvias naudingas uzduotis.

Ne visi agentai veikia vienu metu. Orchestratorius parenka darba pagal prioriteta.

## Revenue first prioritetai

1. Lead list kurimas.
2. Outreach teksto paruosimas.
3. Landing page gerinimas.
4. Competitor intelligence.
5. Product demo gerinimas.
6. Delivery workflow gerinimas.
7. Marketplace ir parts OS funkcijos.
8. Pricing intelligence.
9. Content pack paruosimas.
10. Tech radar eksperimentai.

## 24/7 worker modelis

Pradzia:
- 1 orchestratorius;
- 4 workeriai;
- 1 scheduleris;
- 1 judge;
- 1 cost guard;
- 1 memory updater.

Jeigu serveris stabilus:
- didinti iki 6-8 workeriu.

Jeigu CPU virs 60 procentu arba RAM virs 70 procentu:
- mazinti workeriu skaiciu;
- stabdyti nebutinus darbus;
- palikti tik revenue ir production tasks.

## Darbu tipai pagal laika

Kas 15 min:
- patikrinti task queue;
- paimti viena auksciausio prioriteto darba;
- irasyti statusa.

Kas 1 val:
- competitor scan;
- lead list update;
- content idea update;
- bug and blocker check.

Kas 6 val:
- revenue pipeline review;
- product gate review;
- deploy status review.

Kas 24 val:
- daily report;
- top blockers;
- top money actions;
- next day plan.

## Naudos vartai

Darbas leidziamas tik jeigu bent vienas punktas tiesa:

- gali atvesti lead;
- gali pagerinti close rate;
- gali pagreitinti delivery;
- gali sumazinti rankini darba;
- gali pagerinti produkto kokybe;
- gali sumazinti rizika;
- gali duoti duomenu kainodarai.

Jeigu ne, darbas atmetamas.

## Serverio saugos ribos

Normalu:
- CPU iki 40 procentu;
- RAM iki 50 procentu;
- disk iki 70 procentu.

Atsargiai:
- CPU 40-60 procentu;
- RAM 50-70 procentu;
- disk 70-80 procentu.

Stabdyti ir mazinti:
- CPU virs 60 procentu ilgesni laika;
- RAM virs 70 procentu;
- disk virs 80 procentu;
- daug klaidu loguose.

## Pirma komanda

1. Revenue Worker.
2. Product Worker.
3. Content Worker.
4. Tech Radar Worker.
5. Judge Worker.
6. Memory Worker.

## Done criteria

Sistema veikia, kai yra:
- task queue;
- worker count config;
- scheduler;
- daily revenue report;
- blocker report;
- cost guard;
- memory update;
- weekly performance review.
