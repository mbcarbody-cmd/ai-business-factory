# Parts Seller OS Build Contract

## Non-negotiable direction

This product is not a generic AI agent setup, lead page, consulting funnel or presentation site.

It is a used auto parts seller operating system.

The system must help one seller do the daily work of selling used auto parts:

1. Receive or input a part.
2. Identify category, side, position and storage profile.
3. Estimate price, floor price, confidence and manual-review need.
4. Assign warehouse location or pending-location queue.
5. Decide listing readiness.
6. Generate marketplace feed/draft.
7. Track reservation, sold state, margin and next action.

## MVP acceptance criteria

The MVP is only acceptable when a user can:

- enter OEM code, part name, vehicle, condition, cost, comparable prices and photo status;
- see suggested category and storage profile;
- see price, floor price, confidence, reason and review warnings;
- see suggested warehouse location;
- see listing status and next action;
- view an inventory table;
- export marketplace feed as JSON or CSV;
- reserve at least one ready-to-publish part;
- understand from the UI what is still blocked before production.

## Current implementation

The first static prototype is implemented in:

```text
website/index.html
```

It uses browser `localStorage` and no backend. That is acceptable for the first proof only.

## Next production build sequence

1. Split static prototype into real frontend modules.
2. Add persistent database schema: vehicles, parts, locations, listings, orders, channels, price history.
3. Add import pipeline for seller inventory data.
4. Add marketplace export adapters.
5. Add photo intake and quality checks.
6. Add role-based workflows: pricing agent, warehouse agent, listing agent, CFO agent, QA critic.
7. Add smoke tests and seed data.
8. Add public demo health check.

## Agent rule

Any agent that proposes generic lead generation, broad AI setup, agency services or unrelated landing pages for this product is off-task.

Correct next action is always the highest-value executable step that makes used auto parts selling more automated, measurable and profitable.
