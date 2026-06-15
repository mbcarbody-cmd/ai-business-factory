# Daily Product Factory Loop

Updated: 2026-06-15  
Owner: Product Factory COO / Build Orchestrator  
Status: active

## Tikslas

Šitas loopas verčia sistemą kasdien judinti produktus iki realaus outputo: URL, demo, payment path, outreach, QA verdict arba CFO sprendimas. Tikslas nėra turėti daug agentų. Tikslas yra turėti daug agentų, kurie greitai stumia produktą į rinką.

## Gamybos linija

1. **Pick** — pasirinkti didžiausios vertės P0/P1 užduotį.
2. **Cut** — sumažinti scope iki vieno shippable output.
3. **Assign** — priskirti crew ir konkretų worker-agentą.
4. **Build** — sukurti artefaktą: file, page, demo, script, data model, outreach list.
5. **Deploy** — jeigu produktas ar page, turi būti URL arba aiškus NO URL blocker.
6. **QA** — techninis testas ir conversion/money testas.
7. **Revenue** — lead list, outreach, offer, quote, invoice arba payment path.
8. **CFO** — kaina, marža, break-even, continue/stop signalas.
9. **Record** — task board / proof path / blocker / fallback.
10. **Next** — pasirinkti kitą executable task, jei dabartinis blokuotas.

## Agentų routing taisyklė

- Boilerplate Crew gauna naują produkto karkasą.
- Idea To MVP Crew gauna žalią idėją.
- Build Orchestrator Crew gauna visus neaiškius build darbus.
- Component Library Crew gauna UI/copy reusable blokų darbus.
- Deploy Robot Crew gauna viską, kur reikia URL, health check arba smoke test.
- QA And Conversion Critic Crew gauna kiekvieną prieš-done darbą.
- Revenue Ops Crew gauna kiekvieną MVP, kuris turi būti parduotas.
- Competitor Intelligence Crew gauna konkurentų pavyzdžius ir paverčia į assets.
- CFO Gate Crew gauna kiekvieną kainos, maržos ir continue/stop klausimą.
- Product Stop/Pivot Crew gauna produktus be signalų, per ilgai stovinčius arba per brangius tęsti.

## Anti-stagnation taisyklė

Užblokuota užduotis negali stovėti be veiksmo. Kiekvienas blocker turi turėti:

- kas užblokavo;
- ką darome vietoje to;
- kas owneris;
- koks kitas executable output;
- kada reikia CFO/Judge/CEO sprendimo.

## P0 apsauga

Parts Seller OS yra protected primary build. Tai reiškia:

- revenue ir deploy pajėgumai pirmiausia aptarnauja Parts Seller OS;
- opportunity research negali sustabdyti P0 build;
- naujas produktas turi pereiti Product Gate, CFO Gate ir Stop/Pivot Gate prieš gaudamas P0 pajėgumus.

## Done proof taisyklė

Nėra proof — nėra done.

Priimtini proof tipai:

- repo file;
- public URL;
- deploy/smoke test output;
- QA verdict;
- conversion verdict;
- lead pipeline row;
- outreach sequence;
- quote/payment path;
- CFO verdict;
- client/revenue verification.

## Daily CEO cockpit report

Kiekvieno ciklo pabaigoje turi būti 7 eilutės:

1. Kas šiandien shipinta.
2. Kas priartino prie pinigų.
3. Kas užblokuota.
4. Koks fallback jau paleistas.
5. Ką QA atmetė.
6. Ką CFO rekomendavo tęsti/stabdyti.
7. Kitas vienas didžiausios vertės veiksmas.
