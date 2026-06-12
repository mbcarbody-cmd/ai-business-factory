import http from 'node:http';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PORT = Number(process.env.PORT || 3060);
const DATA_DIR = path.join(__dirname, 'data');
const DB_PATH = path.join(DATA_DIR, 'demo-db.json');
const PUBLIC_DIR = path.join(__dirname, 'public');

function id(prefix) {
  return `${prefix}_${crypto.randomBytes(6).toString('hex')}`;
}

function now() {
  return new Date().toISOString();
}

function partVolumeLitres(part) {
  const l = Number(part.length_cm || 0);
  const w = Number(part.width_cm || 0);
  const h = Number(part.height_cm || 0);
  if (!l || !w || !h) return 0;
  return Math.round((l * w * h) / 1000 * 100) / 100;
}

function initialState() {
  const sellerId = 'seller_demo';
  return {
    meta: {
      product: 'Parts Business OS',
      version: '0.1.0',
      created_at: now(),
      updated_at: now()
    },
    sellers: [
      {
        id: sellerId,
        company_name: 'Demo Parts Seller',
        vat_mode: 'vat_payer',
        vat_code: 'LT000000000',
        status: 'approved',
        created_at: now(),
        updated_at: now()
      }
    ],
    users: [
      {
        id: 'user_admin',
        seller_id: sellerId,
        email: 'admin@example.test',
        role: 'seller_admin',
        status: 'active',
        created_at: now(),
        updated_at: now()
      }
    ],
    donor_assets: [],
    locations: [
      { id: 'loc_A1_01', seller_id: sellerId, zone: 'A', row_code: '1', shelf: '01', bin: 'LEFT', barcode: 'A1-01-LEFT', max_volume_l: 120, max_weight_kg: 80, occupied_volume_l: 0, occupied_weight_kg: 0, state: 'free', created_at: now(), updated_at: now() },
      { id: 'loc_A1_02', seller_id: sellerId, zone: 'A', row_code: '1', shelf: '02', bin: 'RIGHT', barcode: 'A1-02-RIGHT', max_volume_l: 220, max_weight_kg: 120, occupied_volume_l: 0, occupied_weight_kg: 0, state: 'free', created_at: now(), updated_at: now() },
      { id: 'loc_B2_01', seller_id: sellerId, zone: 'B', row_code: '2', shelf: '01', bin: 'FLOOR', barcode: 'B2-01-FLOOR', max_volume_l: 900, max_weight_kg: 300, occupied_volume_l: 0, occupied_weight_kg: 0, state: 'free', created_at: now(), updated_at: now() }
    ],
    parts: [],
    worker_tasks: [],
    reservations: [],
    orders: [],
    shipments: [],
    audit_logs: []
  };
}

async function ensureDb() {
  await mkdir(DATA_DIR, { recursive: true });
  if (!existsSync(DB_PATH)) {
    await writeFile(DB_PATH, JSON.stringify(initialState(), null, 2));
  }
}

async function loadState() {
  await ensureDb();
  return JSON.parse(await readFile(DB_PATH, 'utf8'));
}

async function saveState(state) {
  state.meta.updated_at = now();
  await writeFile(DB_PATH, JSON.stringify(state, null, 2));
}

function audit(state, entity_type, entity_id, action, before = null, after = null) {
  state.audit_logs.push({
    id: id('audit'),
    seller_id: after?.seller_id || before?.seller_id || 'seller_demo',
    user_id: 'user_admin',
    entity_type,
    entity_id,
    action,
    before_json: before ? JSON.stringify(before) : null,
    after_json: after ? JSON.stringify(after) : null,
    created_at: now()
  });
}

function json(res, status, payload) {
  res.writeHead(status, { 'content-type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(payload, null, 2));
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8');
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch {
    const err = new Error('Invalid JSON body');
    err.status = 400;
    throw err;
  }
}

function requireField(body, field) {
  if (body[field] === undefined || body[field] === null || body[field] === '') {
    const err = new Error(`Missing required field: ${field}`);
    err.status = 400;
    throw err;
  }
}

function recommendLocation(state, part) {
  const volume = partVolumeLitres(part);
  const weight = Number(part.weight_kg || 0);

  const candidates = state.locations
    .filter((loc) => loc.state !== 'blocked' && loc.state !== 'full')
    .map((loc) => {
      const freeVolume = Number(loc.max_volume_l || 0) - Number(loc.occupied_volume_l || 0);
      const freeWeight = Number(loc.max_weight_kg || 0) - Number(loc.occupied_weight_kg || 0);
      return { ...loc, freeVolume, freeWeight };
    })
    .filter((loc) => freeVolumeOk(loc, volume) && freeWeightOk(loc, weight))
    .sort((a, b) => a.freeVolume - b.freeVolume);

  return candidates[0] || null;
}

function freeVolumeOk(loc, volume) {
  if (!volume) return loc.freeVolume > 0;
  return loc.freeVolume >= volume;
}

function freeWeightOk(loc, weight) {
  if (!weight) return loc.freeWeight > 0;
  return loc.freeWeight >= weight;
}

function refreshLocationState(loc) {
  const volumeRatio = loc.max_volume_l ? loc.occupied_volume_l / loc.max_volume_l : 0;
  const weightRatio = loc.max_weight_kg ? loc.occupied_weight_kg / loc.max_weight_kg : 0;
  const ratio = Math.max(volumeRatio, weightRatio);
  if (ratio >= 0.95) loc.state = 'full';
  else if (ratio > 0) loc.state = 'partial';
  else loc.state = 'free';
  loc.updated_at = now();
}

async function handleApi(req, res, url) {
  const state = await loadState();

  if (req.method === 'GET' && url.pathname === '/health') {
    return json(res, 200, {
      status: 'ok',
      product: state.meta.product,
      version: state.meta.version,
      updated_at: state.meta.updated_at,
      counts: {
        sellers: state.sellers.length,
        donor_assets: state.donor_assets.length,
        parts: state.parts.length,
        locations: state.locations.length,
        worker_tasks: state.worker_tasks.length,
        reservations: state.reservations.length,
        orders: state.orders.length
      }
    });
  }

  if (req.method === 'GET' && url.pathname === '/api/state') {
    return json(res, 200, state);
  }

  if (req.method === 'POST' && url.pathname === '/api/donor-assets') {
    const body = await readBody(req);
    requireField(body, 'title');
    requireField(body, 'category');

    const asset = {
      id: id('asset'),
      seller_id: body.seller_id || 'seller_demo',
      title: body.title,
      category: body.category,
      vin_or_identifier: body.vin_or_identifier || null,
      purchase_price_net: Number(body.purchase_price_net || 0),
      transport_cost_net: Number(body.transport_cost_net || 0),
      dismantling_cost_net: Number(body.dismantling_cost_net || 0),
      storage_cost_net: Number(body.storage_cost_net || 0),
      other_cost_net: Number(body.other_cost_net || 0),
      status: 'active',
      created_at: now(),
      updated_at: now()
    };
    state.donor_assets.push(asset);
    audit(state, 'donor_asset', asset.id, 'create', null, asset);
    await saveState(state);
    return json(res, 201, asset);
  }

  if (req.method === 'POST' && url.pathname === '/api/parts') {
    const body = await readBody(req);
    requireField(body, 'donor_asset_id');
    requireField(body, 'title');
    requireField(body, 'category');

    const asset = state.donor_assets.find((item) => item.id === body.donor_asset_id);
    if (!asset) return json(res, 404, { error: 'Donor asset not found' });

    const part = {
      id: id('part'),
      seller_id: asset.seller_id,
      donor_asset_id: asset.id,
      location_id: null,
      internal_part_id: `P-${String(state.parts.length + 1).padStart(6, '0')}`,
      title: body.title,
      category: body.category,
      oem_codes: body.oem_codes || '',
      condition_grade: body.condition_grade || 'unknown',
      defect_description: body.defect_description || '',
      length_cm: Number(body.length_cm || 0),
      width_cm: Number(body.width_cm || 0),
      height_cm: Number(body.height_cm || 0),
      weight_kg: Number(body.weight_kg || 0),
      price_net: body.price_net === undefined ? null : Number(body.price_net),
      price_gross: body.price_gross === undefined ? null : Number(body.price_gross),
      pricing_status: body.price_net || body.price_gross ? 'price_review' : 'price_missing',
      listing_status: 'draft',
      stock_status: 'draft',
      created_at: now(),
      updated_at: now()
    };

    state.parts.push(part);
    audit(state, 'part', part.id, 'create', null, part);
    await saveState(state);
    return json(res, 201, { ...part, volume_l: partVolumeLitres(part), recommended_location: recommendLocation(state, part) });
  }

  if (req.method === 'GET' && url.pathname === '/api/location-recommendation') {
    const partId = url.searchParams.get('part_id');
    const part = state.parts.find((item) => item.id === partId);
    if (!part) return json(res, 404, { error: 'Part not found' });
    return json(res, 200, { part_id: part.id, volume_l: partVolumeLitres(part), recommended_location: recommendLocation(state, part) });
  }

  if (req.method === 'POST' && url.pathname === '/api/assign-location') {
    const body = await readBody(req);
    requireField(body, 'part_id');

    const part = state.parts.find((item) => item.id === body.part_id);
    if (!part) return json(res, 404, { error: 'Part not found' });

    const location = body.location_id
      ? state.locations.find((item) => item.id === body.location_id)
      : recommendLocation(state, part);

    if (!location) return json(res, 409, { error: 'No suitable location found' });
    if (location.state === 'blocked' || location.state === 'full') return json(res, 409, { error: 'Location is not available' });

    const before = { ...part };
    part.location_id = location.id;
    part.stock_status = 'in_warehouse';
    part.updated_at = now();
    location.occupied_volume_l += partVolumeLitres(part);
    location.occupied_weight_kg += Number(part.weight_kg || 0);
    refreshLocationState(location);
    audit(state, 'part', part.id, 'assign_location', before, part);
    await saveState(state);
    return json(res, 200, { part, location });
  }

  if (req.method === 'POST' && url.pathname === '/api/worker-tasks') {
    const body = await readBody(req);
    requireField(body, 'title');
    requireField(body, 'linked_type');

    const task = {
      id: id('task'),
      seller_id: body.seller_id || 'seller_demo',
      assigned_user_id: body.assigned_user_id || null,
      linked_type: body.linked_type,
      linked_id: body.linked_id || null,
      title: body.title,
      status: 'open',
      requires_proof_photo: Boolean(body.requires_proof_photo),
      started_at: null,
      completed_at: null,
      created_at: now(),
      updated_at: now()
    };
    state.worker_tasks.push(task);
    audit(state, 'worker_task', task.id, 'create', null, task);
    await saveState(state);
    return json(res, 201, task);
  }

  if (req.method === 'POST' && url.pathname === '/api/reservations') {
    const body = await readBody(req);
    requireField(body, 'part_id');
    requireField(body, 'reserved_until');

    const part = state.parts.find((item) => item.id === body.part_id);
    if (!part) return json(res, 404, { error: 'Part not found' });
    if (['reserved', 'sold'].includes(part.stock_status)) return json(res, 409, { error: 'Part is not available for reservation' });

    const before = { ...part };
    const reservation = {
      id: id('reservation'),
      seller_id: part.seller_id,
      customer_name: body.customer_name || 'Demo customer',
      customer_type: body.customer_type || 'retail',
      status: 'active',
      reserved_until: body.reserved_until,
      cancel_reason: null,
      part_ids: [part.id],
      created_at: now(),
      updated_at: now()
    };

    part.stock_status = 'reserved';
    part.updated_at = now();
    state.reservations.push(reservation);
    audit(state, 'part', part.id, 'reserve', before, part);
    audit(state, 'reservation', reservation.id, 'create', null, reservation);
    await saveState(state);
    return json(res, 201, reservation);
  }

  if (req.method === 'POST' && url.pathname === '/api/orders/from-reservation') {
    const body = await readBody(req);
    requireField(body, 'reservation_id');

    const reservation = state.reservations.find((item) => item.id === body.reservation_id);
    if (!reservation) return json(res, 404, { error: 'Reservation not found' });
    if (reservation.status !== 'active') return json(res, 409, { error: 'Reservation is not active' });

    const parts = reservation.part_ids.map((partId) => state.parts.find((item) => item.id === partId)).filter(Boolean);
    const totalNet = parts.reduce((sum, part) => sum + Number(part.price_net || 0), 0);
    const totalGross = parts.reduce((sum, part) => sum + Number(part.price_gross || part.price_net || 0), 0);

    const order = {
      id: id('order'),
      seller_id: reservation.seller_id,
      reservation_id: reservation.id,
      customer_name: reservation.customer_name,
      part_ids: parts.map((part) => part.id),
      order_status: 'confirmed',
      payment_status: 'unpaid',
      invoice_status: 'needed',
      total_net: totalNet,
      total_gross: totalGross,
      created_at: now(),
      updated_at: now()
    };

    reservation.status = 'converted';
    reservation.updated_at = now();
    for (const part of parts) {
      const before = { ...part };
      part.stock_status = 'sold';
      part.updated_at = now();
      audit(state, 'part', part.id, 'sell_from_reservation', before, part);
    }
    state.orders.push(order);
    audit(state, 'order', order.id, 'create_from_reservation', null, order);
    await saveState(state);
    return json(res, 201, order);
  }

  return json(res, 404, { error: 'API route not found' });
}

async function serveStatic(req, res, url) {
  const filePath = url.pathname === '/' ? path.join(PUBLIC_DIR, 'index.html') : path.join(PUBLIC_DIR, url.pathname);
  if (!filePath.startsWith(PUBLIC_DIR)) return json(res, 403, { error: 'Forbidden' });
  try {
    const content = await readFile(filePath);
    const ext = path.extname(filePath);
    const type = ext === '.html' ? 'text/html; charset=utf-8' : 'text/plain; charset=utf-8';
    res.writeHead(200, { 'content-type': type });
    res.end(content);
  } catch {
    json(res, 404, { error: 'File not found' });
  }
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://${req.headers.host}`);
    if (url.pathname === '/health' || url.pathname.startsWith('/api/')) {
      return await handleApi(req, res, url);
    }
    return await serveStatic(req, res, url);
  } catch (error) {
    json(res, error.status || 500, { error: error.message || 'Server error' });
  }
});

server.listen(PORT, () => {
  console.log(`Parts Business OS demo running on http://localhost:${PORT}`);
});
