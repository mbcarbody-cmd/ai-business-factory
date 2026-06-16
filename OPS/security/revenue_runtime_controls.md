# Revenue Runtime Security Controls

## Hard rule

Any agent that reads untrusted websites, emails, social posts, PDFs, GitHub issues or user-submitted briefs is treated as influenceable. It must not also hold unrestricted secrets, production shell, payment admin or deletion rights.

## Controls to enforce before live money

1. Secrets are stored only in server `.env` or provider secret managers, never in repository files, prompts, exports or logs.
2. `ADMIN_TOKEN`, `N8N_ENCRYPTION_KEY` and payment webhook secrets are unique production values.
3. `KILL_SWITCH=true` until payment, email authentication and one test job pass.
4. Outreach uses a dedicated business mailbox only.
5. Daily sending cap starts at 20 or less.
6. Every prospect has source, legal basis/consent note, status and audit trail.
7. Every payment event has provider id, amount, status and raw event hash/summary.
8. Every job has status, QA score, delivery state and model cost estimate.
9. Production Stripe webhook must verify provider signature before marking a payment as paid.
10. Refunds, deletes, high-spend campaigns and production deploys require human approval.
11. GitHub Actions should pin external actions to commit SHA before production secrets are added.
12. Public repository must never contain private customer data.

## Agent permissions

- Research agent: internet read, no secrets, no sending.
- Draft agent: can write drafts, no direct send.
- Outreach agent: can send only approved templates, daily cap enforced.
- Payment agent: can read verified payment status, cannot refund.
- Fulfillment agent: can generate deliverables for paid jobs only.
- Judge agent: can score output, cannot change payment state.
- CEO controller: can prioritize tasks, but destructive actions still need approval.

## Runtime metrics

Dashboard must track:

- cash recorded;
- prospects created;
- messages drafted;
- messages sent;
- replies;
- paid jobs;
- delivered jobs;
- failed jobs;
- QA scores;
- estimated model cost;
- gross margin.
