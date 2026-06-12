const BASE_URL = process.env.BASE_URL || 'http://localhost:3060';

async function api(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'content-type': 'application/json',
      ...(options.headers || {})
    }
  });

  const data = await response.json();
  return { ok: response.ok, status: response.status, data };
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function expectOk(path, options, message) {
  const result = await api(path, options);
  assert(result.ok, `${message}: ${result.status} ${JSON.stringify(result.data)}`);
  return result.data;
}

async function expectStatus(path, options, expectedStatus, message) {
  const result = await api(path, options);
  assert(result.status === expectedStatus, `${message}: expected ${expectedStatus}, got ${result.status} ${JSON.stringify(result.data)}`);
  return result.data;
}

async function run() {
  const health = await expectOk('/health', {}, 'health must pass');
  assert(health.status === 'ok', 'health status must be ok');

  await expectStatus('/api/donor-assets', {
    method: 'POST',
    body: JSON.stringify({ category: 'cars' })
  }, 400, 'donor asset without title must be rejected');

  await expectStatus('/api/parts', {
    method: 'POST',
    body: JSON.stringify({ title: 'Invalid orphan part', category: 'lighting' })
  }, 400, 'part without donor_asset_id must be rejected');

  const asset = await expectOk('/api/donor-assets', {
    method: 'POST',
    body: JSON.stringify({
      title: `P0 donor ${Date.now()}`,
      category: 'cars',
      purchase_price_net: 1500,
      transport_cost_net: 120
    })
  }, 'asset creation must work');

  const part = await expectOk('/api/parts', {
    method: 'POST',
    body: JSON.stringify({
      donor_asset_id: asset.id,
      title: `P0 part ${Date.now()}`,
      category: 'lighting',
      condition_grade: 'good',
      length_cm: 40,
      width_cm: 30,
      height_cm: 20,
      weight_kg: 3.5,
      price_net: 200,
      price_gross: 242
    })
  }, 'part creation must work');

  assert(part.internal_part_id, 'part must receive internal id');
  assert(part.recommended_location, 'part must receive location recommendation');

  const assigned = await expectOk('/api/assign-location', {
    method: 'POST',
    body: JSON.stringify({ part_id: part.id })
  }, 'assign location must work');

  assert(assigned.part.stock_status === 'in_warehouse', 'assigned part must become in_warehouse');
  assert(assigned.location.state === 'partial' || assigned.location.state === 'full', 'location state must update after assignment');

  const reservation = await expectOk('/api/reservations', {
    method: 'POST',
    body: JSON.stringify({
      part_id: part.id,
      customer_name: 'P0 buyer',
      customer_type: 'business',
      reserved_until: new Date(Date.now() + 86400000).toISOString()
    })
  }, 'first reservation must work');

  await expectStatus('/api/reservations', {
    method: 'POST',
    body: JSON.stringify({
      part_id: part.id,
      customer_name: 'Second buyer must fail',
      customer_type: 'business',
      reserved_until: new Date(Date.now() + 86400000).toISOString()
    })
  }, 409, 'double reservation must be blocked');

  const order = await expectOk('/api/orders/from-reservation', {
    method: 'POST',
    body: JSON.stringify({ reservation_id: reservation.id })
  }, 'reservation must convert to order');

  assert(order.order_status === 'confirmed', 'order must be confirmed');
  assert(order.part_ids.includes(part.id), 'order must include reserved part');

  await expectStatus('/api/reservations', {
    method: 'POST',
    body: JSON.stringify({
      part_id: part.id,
      customer_name: 'Buyer after sale must fail',
      customer_type: 'business',
      reserved_until: new Date(Date.now() + 86400000).toISOString()
    })
  }, 409, 'sold part reservation must be blocked');

  const state = await expectOk('/api/state', {}, 'state must be readable');
  const partAuditRows = state.audit_logs.filter((row) => row.entity_id === part.id);
  assert(partAuditRows.length >= 3, 'part create, assign, reserve/sell actions must be audited');

  console.log('P0 API tests passed:', {
    asset: asset.id,
    part: part.internal_part_id,
    reservation: reservation.id,
    order: order.id,
    partAuditRows: partAuditRows.length
  });
}

run().catch((error) => {
  console.error('P0 API tests failed:', error.message);
  process.exit(1);
});
