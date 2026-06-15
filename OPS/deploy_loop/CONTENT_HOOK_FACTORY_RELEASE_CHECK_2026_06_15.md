# Content Hook Factory Release Check

Date: 2026-06-15
Owner: DevOps Agent-C4
Status: active

## Product

Content Hook Factory lightweight static app.

## Local check

Path:

- `website/index.html`

Required local smoke test:

1. Open `website/index.html`.
2. Press `Užkrauti demo`.
3. Confirm KPI cards update.
4. Open Hookai tab and confirm hooks render.
5. Open Postai tab and confirm posts render.
6. Open Video tab and confirm scripts render.
7. Open Landing / DM tab and confirm landing and DM copy render.
8. Open QA / eksportas tab and confirm Markdown output is shown.
9. Export JSON and confirm output is valid JSON-like data.

## Public URL check

Expected GitHub Pages URL:

```text
https://mbcarbody-cmd.github.io/ai-business-factory/
```

Direct path:

```text
https://mbcarbody-cmd.github.io/ai-business-factory/website/index.html
```

Public release can be claimed only when:

- URL opens;
- hero and CTA are visible;
- demo data can be loaded;
- tabs work;
- Markdown export renders;
- no critical runtime error is visible during basic use.

## Current deploy verdict

Local static app exists. Public URL still needs independent verification.

## Rollback

Rollback if:

- app does not load;
- tabs do not work;
- demo generation breaks;
- export breaks;
- mobile layout is unusable.
