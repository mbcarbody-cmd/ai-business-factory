-- Parts Business OS core schema v0.1
-- Goal: provide a stable operational skeleton for sellers, assets, parts, locations, tasks, reservations, orders and audit logs.

CREATE TABLE sellers (
  id TEXT PRIMARY KEY,
  company_name TEXT NOT NULL,
  vat_mode TEXT NOT NULL CHECK (vat_mode IN ('vat_payer', 'non_vat')),
  vat_code TEXT,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'suspended')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
  id TEXT PRIMARY KEY,
  seller_id TEXT REFERENCES sellers(id),
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('invited', 'active', 'disabled')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE user_roles (
  user_id TEXT NOT NULL REFERENCES users(id),
  role_id TEXT NOT NULL REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);

CREATE TABLE donor_assets (
  id TEXT PRIMARY KEY,
  seller_id TEXT NOT NULL REFERENCES sellers(id),
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  vin_or_identifier TEXT,
  purchase_price_net REAL DEFAULT 0,
  transport_cost_net REAL DEFAULT 0,
  dismantling_cost_net REAL DEFAULT 0,
  storage_cost_net REAL DEFAULT 0,
  other_cost_net REAL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('draft', 'active', 'closed', 'archived')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE locations (
  id TEXT PRIMARY KEY,
  seller_id TEXT NOT NULL REFERENCES sellers(id),
  zone TEXT NOT NULL,
  row_code TEXT,
  shelf TEXT,
  bin TEXT,
  barcode TEXT UNIQUE,
  max_volume_l REAL,
  max_weight_kg REAL,
  occupied_volume_l REAL DEFAULT 0,
  occupied_weight_kg REAL DEFAULT 0,
  state TEXT NOT NULL DEFAULT 'free' CHECK (state IN ('free', 'partial', 'full', 'blocked')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parts (
  id TEXT PRIMARY KEY,
  seller_id TEXT NOT NULL REFERENCES sellers(id),
  donor_asset_id TEXT NOT NULL REFERENCES donor_assets(id),
  location_id TEXT REFERENCES locations(id),
  internal_part_id TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  oem_codes TEXT,
  condition_grade TEXT CHECK (condition_grade IN ('new_other', 'excellent', 'good', 'used', 'damaged', 'unknown')),
  defect_description TEXT,
  length_cm REAL,
  width_cm REAL,
  height_cm REAL,
  weight_kg REAL,
  price_net REAL,
  price_gross REAL,
  pricing_status TEXT NOT NULL DEFAULT 'price_missing' CHECK (pricing_status IN ('price_missing', 'price_review', 'price_ready')),
  listing_status TEXT NOT NULL DEFAULT 'draft' CHECK (listing_status IN ('draft', 'ready', 'listed', 'hidden')),
  stock_status TEXT NOT NULL DEFAULT 'draft' CHECK (stock_status IN ('draft', 'in_warehouse', 'reserved', 'sold', 'returned', 'written_off')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE part_photos (
  id TEXT PRIMARY KEY,
  part_id TEXT NOT NULL REFERENCES parts(id),
  file_path TEXT NOT NULL,
  is_main INTEGER NOT NULL DEFAULT 0,
  is_internal_only INTEGER NOT NULL DEFAULT 0,
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE worker_tasks (
  id TEXT PRIMARY KEY,
  seller_id TEXT NOT NULL REFERENCES sellers(id),
  assigned_user_id TEXT REFERENCES users(id),
  linked_type TEXT NOT NULL CHECK (linked_type IN ('donor_asset', 'part', 'order', 'shipment', 'general')),
  linked_id TEXT,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'assigned', 'doing', 'blocked', 'done', 'cancelled')),
  requires_proof_photo INTEGER NOT NULL DEFAULT 0,
  started_at TEXT,
  completed_at TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
  id TEXT PRIMARY KEY,
  seller_id TEXT NOT NULL REFERENCES sellers(id),
  customer_name TEXT,
  customer_type TEXT CHECK (customer_type IN ('retail', 'business', 'internal')),
  status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'expired', 'cancelled', 'converted')),
  reserved_until TEXT NOT NULL,
  cancel_reason TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservation_parts (
  reservation_id TEXT NOT NULL REFERENCES reservations(id),
  part_id TEXT NOT NULL REFERENCES parts(id),
  PRIMARY KEY (reservation_id, part_id)
);

CREATE TABLE orders (
  id TEXT PRIMARY KEY,
  seller_id TEXT NOT NULL REFERENCES sellers(id),
  reservation_id TEXT REFERENCES reservations(id),
  customer_name TEXT,
  order_status TEXT NOT NULL DEFAULT 'new' CHECK (order_status IN ('new', 'confirmed', 'picking', 'packed', 'shipped', 'completed', 'cancelled', 'returned')),
  payment_status TEXT NOT NULL DEFAULT 'unpaid' CHECK (payment_status IN ('unpaid', 'partial', 'paid', 'refunded')),
  invoice_status TEXT NOT NULL DEFAULT 'not_required' CHECK (invoice_status IN ('not_required', 'needed', 'issued')),
  total_net REAL DEFAULT 0,
  total_gross REAL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_parts (
  order_id TEXT NOT NULL REFERENCES orders(id),
  part_id TEXT NOT NULL REFERENCES parts(id),
  sold_price_net REAL NOT NULL DEFAULT 0,
  sold_price_gross REAL NOT NULL DEFAULT 0,
  PRIMARY KEY (order_id, part_id)
);

CREATE TABLE shipments (
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL REFERENCES orders(id),
  carrier TEXT,
  package_size TEXT,
  weight_kg REAL,
  tracking_number TEXT,
  label_status TEXT NOT NULL DEFAULT 'not_created' CHECK (label_status IN ('not_created', 'created', 'printed', 'void')),
  shipment_status TEXT NOT NULL DEFAULT 'pending' CHECK (shipment_status IN ('pending', 'packed', 'handed_to_carrier', 'in_transit', 'delivered', 'problem')),
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE competitor_price_observations (
  id TEXT PRIMARY KEY,
  part_id TEXT REFERENCES parts(id),
  source TEXT NOT NULL,
  observed_title TEXT,
  observed_price_gross REAL,
  observed_currency TEXT DEFAULT 'EUR',
  observed_url TEXT,
  confidence INTEGER DEFAULT 0 CHECK (confidence BETWEEN 0 AND 100),
  observed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
  id TEXT PRIMARY KEY,
  seller_id TEXT REFERENCES sellers(id),
  user_id TEXT REFERENCES users(id),
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  action TEXT NOT NULL,
  before_json TEXT,
  after_json TEXT,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_parts_seller_status ON parts(seller_id, stock_status, listing_status, pricing_status);
CREATE INDEX idx_parts_location ON parts(location_id);
CREATE INDEX idx_tasks_seller_status ON worker_tasks(seller_id, status);
CREATE INDEX idx_orders_seller_status ON orders(seller_id, order_status, payment_status);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
