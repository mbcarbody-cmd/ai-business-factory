-- Parts Business OS: Core Production Spine v1
-- PostgreSQL 16+
-- Every seller-owned row is tenant-isolated and every material action is auditable.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

CREATE TYPE organization_status AS ENUM ('application','review','approved','active','suspended','closed');
CREATE TYPE user_status AS ENUM ('invited','active','disabled','suspended','archived');
CREATE TYPE part_status AS ENUM ('received','measured','photo_required','stored','ready_for_pricing','ready_for_publish','published','reserved','picked','packed','shipped','sold','quarantine','written_off');
CREATE TYPE order_status AS ENUM ('draft','pending_payment','paid','processing','packed','shipped','delivered','cancelled','returned','refunded');
CREATE TYPE payment_status AS ENUM ('created','pending','paid','failed','cancelled','refunded','partially_refunded');
CREATE TYPE subscription_status AS ENUM ('trial','active','past_due','paused','cancelled');

CREATE TABLE tenants (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  legal_name text NOT NULL,
  display_name text NOT NULL,
  country_code char(2) NOT NULL,
  vat_number text,
  vat_mode text NOT NULL CHECK (vat_mode IN ('vat_payer','non_vat')),
  status organization_status NOT NULL DEFAULT 'application',
  currency char(3) NOT NULL DEFAULT 'EUR',
  timezone text NOT NULL DEFAULT 'Europe/Vilnius',
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  email citext UNIQUE NOT NULL,
  full_name text,
  password_hash text,
  status user_status NOT NULL DEFAULT 'invited',
  mfa_enabled boolean NOT NULL DEFAULT false,
  last_login_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE roles (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code text UNIQUE NOT NULL,
  name text NOT NULL,
  scope text NOT NULL CHECK (scope IN ('platform','tenant','customer')),
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE permissions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  code text UNIQUE NOT NULL,
  description text NOT NULL
);

CREATE TABLE role_permissions (
  role_id uuid NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
  permission_id uuid NOT NULL REFERENCES permissions(id) ON DELETE CASCADE,
  PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE tenant_memberships (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role_id uuid NOT NULL REFERENCES roles(id),
  status user_status NOT NULL DEFAULT 'invited',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, user_id)
);

CREATE TABLE warehouses (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  code text NOT NULL,
  name text NOT NULL,
  address jsonb NOT NULL DEFAULT '{}'::jsonb,
  status text NOT NULL DEFAULT 'active',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, code)
);

CREATE TABLE warehouse_locations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  warehouse_id uuid NOT NULL REFERENCES warehouses(id) ON DELETE CASCADE,
  code text NOT NULL,
  zone text NOT NULL,
  location_type text NOT NULL,
  length_cm numeric(10,2),
  width_cm numeric(10,2),
  height_cm numeric(10,2),
  max_weight_kg numeric(10,2),
  occupied_volume_pct numeric(5,2) NOT NULL DEFAULT 0 CHECK (occupied_volume_pct BETWEEN 0 AND 100),
  occupied_weight_kg numeric(10,2) NOT NULL DEFAULT 0,
  allowed_categories text[] NOT NULL DEFAULT '{}',
  security_level smallint NOT NULL DEFAULT 1 CHECK (security_level BETWEEN 1 AND 5),
  status text NOT NULL DEFAULT 'open',
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, code)
);

CREATE TABLE parts (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  internal_code text NOT NULL,
  oem_code text,
  normalized_oem_code text,
  title text NOT NULL,
  category text NOT NULL,
  make text,
  model text,
  model_year_from integer,
  model_year_to integer,
  condition_grade text,
  length_cm numeric(10,2),
  width_cm numeric(10,2),
  height_cm numeric(10,2),
  weight_kg numeric(10,2),
  fragile boolean NOT NULL DEFAULT false,
  hazardous boolean NOT NULL DEFAULT false,
  quantity integer NOT NULL DEFAULT 1 CHECK (quantity >= 0),
  reserved_quantity integer NOT NULL DEFAULT 0 CHECK (reserved_quantity >= 0),
  location_id uuid REFERENCES warehouse_locations(id),
  cost_net numeric(12,2),
  price_net numeric(12,2),
  price_gross numeric(12,2),
  currency char(3) NOT NULL DEFAULT 'EUR',
  status part_status NOT NULL DEFAULT 'received',
  version integer NOT NULL DEFAULT 1,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, internal_code),
  CHECK (reserved_quantity <= quantity)
);

CREATE INDEX parts_tenant_oem_idx ON parts (tenant_id, normalized_oem_code);
CREATE INDEX parts_tenant_status_idx ON parts (tenant_id, status);
CREATE INDEX parts_tenant_location_idx ON parts (tenant_id, location_id);

CREATE TABLE stock_movements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  part_id uuid NOT NULL REFERENCES parts(id) ON DELETE CASCADE,
  movement_type text NOT NULL,
  from_location_id uuid REFERENCES warehouse_locations(id),
  to_location_id uuid REFERENCES warehouse_locations(id),
  quantity integer NOT NULL CHECK (quantity > 0),
  reason text,
  actor_user_id uuid REFERENCES users(id),
  idempotency_key text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, idempotency_key)
);

CREATE TABLE customers (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  customer_type text NOT NULL CHECK (customer_type IN ('individual','business')),
  name text NOT NULL,
  email citext,
  phone text,
  vat_number text,
  billing_address jsonb NOT NULL DEFAULT '{}'::jsonb,
  shipping_address jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE orders (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  order_number text NOT NULL,
  customer_id uuid REFERENCES customers(id),
  status order_status NOT NULL DEFAULT 'draft',
  currency char(3) NOT NULL DEFAULT 'EUR',
  subtotal_net numeric(12,2) NOT NULL DEFAULT 0,
  vat_amount numeric(12,2) NOT NULL DEFAULT 0,
  shipping_amount numeric(12,2) NOT NULL DEFAULT 0,
  total_gross numeric(12,2) NOT NULL DEFAULT 0,
  sales_channel text,
  external_order_id text,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, order_number)
);

CREATE TABLE order_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  order_id uuid NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  part_id uuid NOT NULL REFERENCES parts(id),
  quantity integer NOT NULL CHECK (quantity > 0),
  unit_price_net numeric(12,2) NOT NULL,
  vat_rate numeric(5,2) NOT NULL DEFAULT 0,
  unit_price_gross numeric(12,2) NOT NULL,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE payments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  order_id uuid REFERENCES orders(id) ON DELETE SET NULL,
  provider text NOT NULL,
  provider_payment_id text,
  status payment_status NOT NULL DEFAULT 'created',
  amount numeric(12,2) NOT NULL CHECK (amount >= 0),
  currency char(3) NOT NULL DEFAULT 'EUR',
  idempotency_key text NOT NULL,
  failure_reason text,
  paid_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, idempotency_key)
);

CREATE TABLE invoices (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  order_id uuid REFERENCES orders(id) ON DELETE SET NULL,
  invoice_number text NOT NULL,
  issue_date date NOT NULL,
  due_date date,
  status text NOT NULL DEFAULT 'draft',
  total_gross numeric(12,2) NOT NULL DEFAULT 0,
  pdf_storage_key text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, invoice_number)
);

CREATE TABLE subscriptions (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid NOT NULL UNIQUE REFERENCES tenants(id) ON DELETE CASCADE,
  plan_code text NOT NULL,
  status subscription_status NOT NULL DEFAULT 'trial',
  billing_provider text,
  external_customer_id text,
  external_subscription_id text,
  monthly_price numeric(12,2) NOT NULL DEFAULT 0,
  currency char(3) NOT NULL DEFAULT 'EUR',
  current_period_start timestamptz,
  current_period_end timestamptz,
  cancel_at_period_end boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE audit_events (
  id bigserial PRIMARY KEY,
  tenant_id uuid REFERENCES tenants(id) ON DELETE SET NULL,
  actor_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
  event_type text NOT NULL,
  object_type text NOT NULL,
  object_id text,
  request_id text,
  source_ip inet,
  user_agent text,
  before_state jsonb,
  after_state jsonb,
  reason text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX audit_events_tenant_time_idx ON audit_events (tenant_id, created_at DESC);
CREATE INDEX audit_events_object_idx ON audit_events (object_type, object_id);

CREATE TABLE background_jobs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id uuid REFERENCES tenants(id) ON DELETE CASCADE,
  job_type text NOT NULL,
  payload jsonb NOT NULL DEFAULT '{}'::jsonb,
  status text NOT NULL DEFAULT 'queued',
  attempts integer NOT NULL DEFAULT 0,
  max_attempts integer NOT NULL DEFAULT 5,
  scheduled_at timestamptz NOT NULL DEFAULT now(),
  started_at timestamptz,
  finished_at timestamptz,
  last_error text,
  idempotency_key text,
  created_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, idempotency_key)
);

CREATE TABLE webhook_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  provider text NOT NULL,
  provider_event_id text NOT NULL,
  event_type text NOT NULL,
  payload jsonb NOT NULL,
  signature_valid boolean NOT NULL DEFAULT false,
  processed_at timestamptz,
  processing_error text,
  received_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE (provider, provider_event_id)
);

-- Row-level tenant isolation. Application sets: SET LOCAL app.current_tenant_id = '<uuid>';
DO $$
DECLARE t text;
BEGIN
  FOREACH t IN ARRAY ARRAY[
    'tenant_memberships','warehouses','warehouse_locations','parts','stock_movements',
    'customers','orders','order_items','payments','invoices','subscriptions','audit_events','background_jobs'
  ] LOOP
    EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', t);
    EXECUTE format(
      'CREATE POLICY %I_tenant_isolation ON %I USING (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid) WITH CHECK (tenant_id = current_setting(''app.current_tenant_id'', true)::uuid)',
      t, t
    );
  END LOOP;
END $$;

-- Seed core roles.
INSERT INTO roles (code,name,scope) VALUES
('platform_owner','Platform Owner','platform'),
('platform_admin','Platform Admin','platform'),
('seller_owner','Seller Owner','tenant'),
('seller_admin','Seller Admin','tenant'),
('manager','Manager','tenant'),
('pricing_specialist','Pricing Specialist','tenant'),
('warehouse_worker','Warehouse Worker','tenant'),
('packing_worker','Packing Worker','tenant'),
('finance_user','Finance User','tenant'),
('readonly_auditor','Readonly Auditor','tenant')
ON CONFLICT (code) DO NOTHING;
