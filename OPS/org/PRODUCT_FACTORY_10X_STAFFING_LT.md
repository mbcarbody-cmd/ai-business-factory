# Product Factory 10x Staffing

Updated: 2026-06-15  
Owner: CEO / Master Agent + COO-1 Execution Architect  
Status: active

## Tikslas

Produktų gamyba turi veikti kaip konvejeris, ne kaip pavienių idėjų sąrašas. Dėl to įjungta 10 funkcijų × 10 darbuotojų struktūra: iš viso 100 specializuotų worker-agentų, kurie visi dirba per vieną įrodymų, pinigų ir deploy logiką.

Pagrindinė taisyklė: daugiau agentų leidžiama tik tada, kai jie turi aiškų input, output, KPI, ownerį ir fallback veiksmą. Jei kelias užblokuotas, darbuotojas ne laukia, o pereina prie fallback užduoties ir eskaluoja blockerį.

## Apsaugotas P0 fokusas

P0 produktas lieka Parts Seller OS. Naujos verslo galimybės turi eiti per Opportunity Lab ir negali atimti P0 build/revenue pajėgumų, kol nepraeina gate review.

## 10 gamybos funkcijų

1. Product Factory Boilerplate Crew — palaiko reusable produkto karkasą: landing, pricing, payment, dashboard, analytics, legal, deploy config.
2. Idea To MVP In One Day Crew — kiekvieną idėją priverčia turėti buyerį, problemą, offerį, demo scope, kainą, payment path ir pirmą outreach planą.
3. Build Orchestrator Crew — skaldo darbus į ticketus, priskiria ownerius, šalina blocker’ius, saugo nuo stagnacijos.
4. Reusable Component Library Crew — kuria UI/copy Lego blokelius: hero, pricing, forms, dashboard, product cards, emails.
5. Deploy Robot Crew — rūpinasi preview URL, GitHub Actions, hosting, health check, smoke test, rollback ir NO URL gate.
6. QA And Conversion Critic Crew — tikrina techniką ir pinigų logiką: forma, payment, mobile, CTA, trust, aiškumas.
7. Revenue Ops Autopilot Crew — gamina leadus, outbound žinutes, follow-up, CRM states, quote/invoice/payment flow.
8. Competitor Intelligence To Asset Factory Crew — konkurentų patternus paverčia hooks, landing copy, social posts, video scripts, SEO assets.
9. CFO Gate Crew — skaičiuoja kainą, savikainą, maržą, CAC effort, break-even ir continue/stop sprendimą.
10. Product Stop/Pivot Crew — neleidžia tempti silpnų produktų: continue, pivot, park arba stop su įrodymu.

## Kiekvienos funkcijos darbuotojų struktūra

Kiekviena iš 10 funkcijų turi 10 worker-agentų. Tiksli mašininė matrica saugoma faile:

`OPS/org/product_factory_10x_staffing.json`

Ten aprašyta:

- funkcijos ID;
- misija;
- KPI;
- input;
- output;
- 10 worker-agentų vardai;
- bendros daily output taisyklės.

## Daily factory ciklas

Kiekvieną darbo ciklą sistema turi judėti tokia tvarka:

1. Pick — paimti aukščiausios vertės P0/P1 užduotį.
2. Cut — nukirpti scope iki vieno shippable output.
3. Build — sukurti artefaktą.
4. Deploy — padaryti URL arba aiškų NO URL blockerį.
5. QA — techninis ir conversion patikrinimas.
6. Revenue — outreach, leadai, offeris arba payment path.
7. CFO — continue/stop signalas.
8. Record — įrašyti proof path, next_action ir blocker/fallback.

## Done taisyklė

Darbas laikomas padarytu tik tada, kai yra bent vienas iš šių proof tipų:

- repo file path;
- public URL;
- smoke test result;
- outreach/pipeline row;
- CFO verdict;
- QA verdict;
- user/client verified result;
- revenue verified result.

Be proof — ne done.

## Kodėl tai pagreitina produktus

Sena problema: daug idėjų, daug agentų, bet per mažai priverstinio konvejerio.

Naujas režimas: kiekviena idėja turi pereiti per tą pačią liniją:

Idea → MVP brief → boilerplate → build tickets → component assembly → deploy → QA → revenue ops → CFO gate → continue/pivot/park/stop.

Taip sistema nestovi vietoje ir kiekvienas agentas turi CEO lygio atsakomybę už pinigus, riziką, greitį ir įrodymą.
