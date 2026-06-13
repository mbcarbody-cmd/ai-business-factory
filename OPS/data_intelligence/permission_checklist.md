# Public Data Permission Checklist LT

Date: 2026-06-13
Owner: CISO / Security Judge + CI-1 Market Spy Chief
Status: required before automated collection

## Naudojimas

Pries bet koki automatini public-data rinkima atsakyti i visus klausimus. Jei nors vienas critical atsakymas neigiamas arba neaiskus, taskas lieka blocked arba pereina i manual verification.

## 1. Source identity

- Domain:
- Exact URL pattern:
- Source owner / platform:
- Data type:
- Business purpose:
- Output path:
- Task ID:
- Owner:

## 2. Access permission

- Ar puslapis public be login?
- Ar nereikia apeiti paywall?
- Ar nereikia apeiti captcha?
- Ar nereikia naudoti cookies/session tokens?
- Ar yra oficialus API/feed? Jei taip, kodel nenaudojame?
- Ar robots.txt leidzia pasirinktus URL?
- Ar ToS nepriestarauja planuojamam rinkimui?
- Ar rate limit nustatytas?

Decision:
- allowed_api
- allowed_manual
- allowed_low_rate_public_fetch
- allowed_headless_public_render
- blocked

## 3. Personal data check

- Ar renkame asmens varda/pavarde?
- Ar renkame el. pasta?
- Ar renkame telefono numeri?
- Ar renkame social profile?
- Ar renkame nuotraukas su zmonemis?
- Ar renkame review/comment turini su asmens duomenimis?
- Ar duomenys reikalingi tikslui, ar galima ju nerinkti?

Decision:
- no_personal_data
- minimal_public_business_contact
- high_risk_requires_approval
- blocked

## 4. Copyright/content check

- Ar kopijuojame tik trumpus faktus, kainas, features, CTA?
- Ar nekopijuojame ilgu tekstu / straipsniu / aprasymu kaip savo turinio?
- Ar turime source_url ir attribution vidiniam auditui?
- Ar output bus transformuota analize, ne turinio vagyste?

Decision:
- facts_only
- short_excerpts_only
- transform_summary_allowed
- blocked

## 5. Technical safety

- Max requests per domain:
- Parallelism:
- User-agent:
- Timeout:
- Retry limit:
- Cache duration:
- Stop conditions:
- Error handling:

Blocked technical methods:
- captcha solving;
- anti-bot bypass;
- fingerprint evasion;
- fake login;
- credential stuffing;
- forced hidden endpoints;
- destructive requests.

## 6. Data quality

- Required fields:
- Optional fields:
- Dedupe key:
- Confidence rule:
- Manual spot check ratio:
- Second source required?
- Staleness limit:

## 7. Final approval

Approved method:
Risk level:
Allowed fields:
Blocked fields:
Rate limit:
Output path:
Review date:
Approver:

## Red flag auto-blocks

- Login required and no explicit permission.
- Captcha required.
- Paywall bypass required.
- ToS clearly forbids planned use.
- Personal data at scale without legal basis.
- Source owner sends stop request.
- Data can harm individual privacy.
- Agent cannot explain source, method and output path.
