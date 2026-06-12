# QA Critic Checklist

Owner: CTO-3 Systems Reliability Breaker

## Purpose

Break the product before a client does.

## Critic questions

1. Can a new user understand the product in 10 seconds?
2. Can the main workflow be completed without help?
3. What happens with empty, wrong or messy inputs?
4. What breaks on mobile?
5. What breaks if an API key or env var is missing?
6. What breaks if there is no internet or slow loading?
7. Can data be lost?
8. Can private client data leak?
9. Is the offer promising more than the product does?
10. Can support explain the handoff in simple words?

## Release blocker levels

- Critical: blocks sale/deploy.
- High: blocks delivery unless explicitly accepted.
- Medium: can ship if documented.
- Low: backlog.

## Required proof before sell-ready

- Critical paths tested.
- Mobile checked.
- Known bugs entered in bug board.
- No critical open bugs.
- Judge sign-off recorded in product gates.
