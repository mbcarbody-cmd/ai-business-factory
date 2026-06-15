# Product Factory Release Check

Updated: 2026-06-15  
Owner: PF10X-05-W01 Deploy Captain  
Status: active

## Purpose

Every product release needs either a public URL with release proof or an explicit NO URL blocker and fallback action.

## First target

Product: Parts Seller OS one-day MVP template.

Path:

- `products/_templates/parts-seller-os-one-day-mvp/index.html`

## Local release check

1. Open the HTML file locally.
2. Confirm the page renders.
3. Confirm hero, workflow, pricing and lead capture sections are visible.
4. Confirm CTA anchors point to existing sections.
5. Confirm mobile width remains readable.
6. Confirm payment path placeholder exists.
7. Confirm QA/CFO/revenue proof placeholders exist.

## Public release check

1. Choose GitHub Pages, Vercel, Netlify or Railway.
2. Deploy from the product folder or website path.
3. Record the public URL.
4. Run the release checklist against the public URL.
5. Record rollback path.
6. Update task board proof status.

## Current deploy verdict

Public URL is not independently verified yet. Local template exists and must be checked before any public claim.

## Next action

Create or verify public static hosting for the Parts Seller OS MVP page. If public hosting is blocked, keep NO URL blocker active and continue Revenue Ops, CFO and QA preparation.
