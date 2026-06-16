# Overnight Revenue Runtime

This directory turns the static Content Hook Factory demo into an always-on, auditable order and fulfillment service.

## What is implemented

- PostgreSQL source of truth for prospects, outreach drafts, payments, jobs, deliveries and immutable audit events.
- Public intake endpoint and payment-link handoff.
- Stripe webhook verification and idempotent paid-order creation.
- Manual B2B payment endpoint protected by an admin token.
- Persistent worker with retries, QA gate and deterministic fallback output.
- Nightly prospect-draft cycle with legal-basis fields, approval state and daily cap.
- Outreach is `draft` by default and cannot send until both `OUTREACH_MODE=send` and the kill switch are explicitly disabled.
- SMTP delivery, metrics, health endpoint and emergency kill switch.
- Docker Compose, PostgreSQL initialization and Caddy HTTPS reverse proxy.

## Server installation

```bash
cd runtime
cp .env.example .env
chmod 600 .env
# Edit .env directly on the server. Never paste secrets into chat or commit them.
docker compose config
docker compose up -d --build
docker compose ps
curl -fsS https://YOUR_RUNTIME_DOMAIN/health
```

Keep `KILL_SWITCH=true` during the first boot. After health, payment-webhook and delivery tests pass, change it to `false` and restart only the runtime service:

```bash
docker compose up -d --no-deps runtime
```

## Required external configuration

1. Point the runtime subdomain DNS A/AAAA record to the server.
2. Enter the domain in `RUNTIME_DOMAIN` and `PUBLIC_BASE_URL`.
3. Create a long random `POSTGRES_PASSWORD` and `ADMIN_TOKEN`.
4. Add one limited AI API key and provider-side spending cap.
5. Create a payment link and webhook to `https://DOMAIN/webhooks/stripe`.
6. Put bank payout details only in the payment provider's verified dashboard. They do not belong in this repo, `.env.example`, issues or chat.
7. Configure a separate authenticated business mailbox and SPF, DKIM and DMARC before enabling outreach.

## Checkout flow

1. Website posts the customer brief to `POST /api/intake`.
2. Response returns `intake_id` and `payment_url`.
3. Checkout Session metadata must include the same `intake_id`.
4. The signed `checkout.session.completed` webhook records cash and queues a job.
5. Worker generates the content pack, applies QA, stores delivery and emails it when SMTP is configured.

## Safe operational defaults

- `KILL_SWITCH=true`
- `OUTREACH_MODE=draft`
- `DAILY_SEND_CAP=10`
- no payment, AI or SMTP secrets in the repository
- no automatic scraping or sending to contacts without a recorded legal basis

## Admin endpoints

Send `X-Admin-Token: <ADMIN_TOKEN>`.

- `POST /api/prospects`
- `POST /api/manual-payment`
- `GET /api/metrics`
- `POST /api/kill-switch/on`
- `POST /api/kill-switch/off`

## Backup

At minimum, schedule an encrypted daily PostgreSQL dump outside this directory and test restore regularly. Never store unencrypted production dumps in GitHub.
