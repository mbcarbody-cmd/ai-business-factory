# Overnight Revenue Runtime

This folder is the minimum always-on money loop for AI Business Factory.

## What this installs

- `revenue-api`: small FastAPI service with CRM, payment log, job queue, job runner, dashboard, audit log and kill switch.
- `n8n`: workflow orchestrator for schedules, approved outreach, webhook routing and follow-ups.
- persistent Docker volumes for runtime data.

## What it does not do by itself

It does not create a VPS, buy a domain, configure DNS, create a payment account, or place secrets into production. Those must be done in the real hosting/payment control panels.

## Server install

```bash
cd runtime
cp .env.example .env
# edit .env on the server only
mv revenue-api/Dockerfile.txt revenue-api/Dockerfile
docker compose up -d --build
```

Health check:

```bash
curl http://localhost:8080/health
```

Offer endpoint:

```bash
curl http://localhost:8080/offer
```

Admin dashboard:

```bash
curl -H "x-admin-token: $ADMIN_TOKEN" http://localhost:8080/dashboard
```

## First revenue flow

1. Put real secrets into `runtime/.env` on the server, not into GitHub.
2. Create one checkout/payment link for the 249 EUR Content Hook Factory Sprint.
3. Put that checkout URL into `STRIPE_PAYMENT_LINK` or the chosen payment field.
4. Configure the public landing page CTA to point to `/offer` or directly to checkout.
5. In n8n, create a nightly workflow:
   - trigger every night;
   - read eligible prospects from `revenue-api`;
   - enrich from public website/social data;
   - generate a short personalized sample;
   - send only through the approved business mailbox;
   - obey `DAILY_OUTREACH_LIMIT`;
   - write every send/reply to the audit log;
   - route interested prospects to checkout.
6. Payment webhook creates/updates a paid job.
7. Paid job is run through `/jobs/{job_id}/run`.
8. Delivery is sent after QA score passes.

## Manual paid job test

```bash
curl -X POST http://localhost:8080/jobs/manual-paid \
  -H "content-type: application/json" \
  -H "x-admin-token: $ADMIN_TOKEN" \
  -d '{"customer_email":"buyer@example.com","brief":"Business sells used auto parts and needs stronger social hooks for B2B buyers."}'
```

Then run returned job id:

```bash
curl -X POST http://localhost:8080/jobs/1/run -H "x-admin-token: $ADMIN_TOKEN"
```

## Safety rules

- Never put real API keys in GitHub.
- Keep `KILL_SWITCH=true` until DNS, email auth and payment tests pass.
- Start with `DAILY_OUTREACH_LIMIT=20` or lower.
- Use a dedicated sending mailbox, not a private personal inbox.
- Production Stripe webhook must verify `STRIPE_WEBHOOK_SECRET` before live payments.
- Destructive actions, refunds, large spend and production deploys need human approval.

## Minimum production checklist

- [ ] VPS online.
- [ ] Docker and Compose installed.
- [ ] Domain points to VPS.
- [ ] HTTPS reverse proxy configured.
- [ ] `runtime/.env` created on server.
- [ ] `ADMIN_TOKEN` changed.
- [ ] `N8N_ENCRYPTION_KEY` changed.
- [ ] Payment link created.
- [ ] Webhook secret configured.
- [ ] Business sending mailbox configured.
- [ ] SPF, DKIM, DMARC active.
- [ ] Test paid job created and delivered.
- [ ] Dashboard shows cash and job status.
