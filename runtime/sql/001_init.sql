CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS system_config (
    key text PRIMARY KEY,
    value text NOT NULL,
    updated_at timestamptz NOT NULL DEFAULT now()
);

INSERT INTO system_config(key, value)
VALUES ('kill_switch', 'false')
ON CONFLICT (key) DO NOTHING;

CREATE TABLE IF NOT EXISTS intakes (
    id uuid PRIMARY KEY,
    email text NOT NULL,
    company text NOT NULL,
    payload jsonb NOT NULL,
    status text NOT NULL CHECK (status IN ('awaiting_payment','paid','cancelled')),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS prospects (
    id uuid PRIMARY KEY,
    company text NOT NULL,
    website text NOT NULL DEFAULT '',
    email text NOT NULL,
    legal_basis text NOT NULL CHECK (legal_basis IN ('consent','legitimate_interest','existing_customer')),
    notes text NOT NULL DEFAULT '',
    status text NOT NULL CHECK (status IN ('pending','approved','suppressed')) DEFAULT 'pending',
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS outreach_drafts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    prospect_id uuid NOT NULL REFERENCES prospects(id) ON DELETE CASCADE,
    subject text NOT NULL,
    body text NOT NULL,
    status text NOT NULL CHECK (status IN ('draft','approved','sent','cancelled')) DEFAULT 'draft',
    created_at timestamptz NOT NULL DEFAULT now(),
    sent_at timestamptz
);

CREATE TABLE IF NOT EXISTS jobs (
    id uuid PRIMARY KEY,
    job_type text NOT NULL,
    status text NOT NULL CHECK (status IN ('queued','running','delivered','failed','cancelled')),
    payload jsonb NOT NULL,
    result jsonb,
    attempts integer NOT NULL DEFAULT 0,
    max_attempts integer NOT NULL DEFAULT 3,
    run_after timestamptz NOT NULL DEFAULT now(),
    started_at timestamptz,
    completed_at timestamptz,
    last_error text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_jobs_ready
    ON jobs(status, run_after, created_at)
    WHERE status='queued';

CREATE TABLE IF NOT EXISTS payments (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    provider text NOT NULL,
    provider_payment_id text NOT NULL,
    amount_cents integer NOT NULL CHECK (amount_cents >= 0),
    currency text NOT NULL,
    customer_email text NOT NULL,
    status text NOT NULL CHECK (status IN ('pending','paid','refunded','failed')),
    job_id uuid REFERENCES jobs(id),
    raw_event jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (provider, provider_payment_id)
);

CREATE TABLE IF NOT EXISTS deliveries (
    id uuid PRIMARY KEY,
    job_id uuid NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    recipient_email text NOT NULL,
    status text NOT NULL CHECK (status IN ('pending','delivered','failed')),
    artifact jsonb NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (job_id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id bigserial PRIMARY KEY,
    event_type text NOT NULL,
    actor text NOT NULL,
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_created_at ON audit_log(created_at DESC);

REVOKE ALL ON SCHEMA public FROM PUBLIC;
