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
  if (!response.ok) {
    throw new Error(`${path} failed: ${data.error || response.statusText}`);
  }
  return data;
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function run() {
  const health = await api('/health');
  assert(health.status === 'ok', 'health endpoint must return ok');

  const asset = await api('/api/donor-assets', {
    method: 'POST',
    body: JSON.stringify({ title: 'Smoke donor asset', category: 'cars', purchase_price_net: 1000 })
  });
  assert(asset.id, 'asset must have id');

  const part = await api('/api/parts', {
    method: 'POST',
    body: JSON.stringify({
      donor_asset_id: asset.id,
      title: 'Smoke test part',
      category: 'lighting',
      condition_grade: 'good',
      length_cm: 50,
      width_cm: 30,
      height_cm: 25,
      weight_kg: 4,
      price_net: 100,
      price_gross: 121
    })
  });
  assert(part.id, 'part must have id');
  assert(part.internal_part_id, 'part must have internal id');

  const recommendation = await api(`/api/location-recommendation?part_id=${part.id}`);
  assert(recommendation.recommended_location, 'part must receive location recommendation');

  const assigned = await api('/api/assign-location', {
    method: 'POST',
    body: JSON.stringify({ part_id: part.id })
  });
  assert(assigned.part.location_id, 'part must be assigned to location');
  assert(assigned.part.stock_status === 'in_warehouse', 'part must become in_warehouse');

  const task = await api('/api/worker-tasks', {
    method: 'POST',
    body: JSON.stringify({ title: 'Smoke task', linked_type: 'part', linked_id: part.id })
  });
  assert(task.id, 'task must have id');

  const reservation = await api('/api/reservations', {
    method: 'POST',
    body: JSON.stringify({ part_id: part.id, reserved_until: new Date(Date.now() + 86400000).toISOString() })
  });
  assert(reservation.id, 'reservation must have id');

  const order = await api('/api/orders/from-reservation', {
    method: 'POST',
    body: JSON.stringify({ reservation_id: reservation.id })
  });
  assert(order.id, 'order must have id');
  assert(order.order_status === 'confirmed', 'order must be confirmed');

  const state = await api('/api/state');
  assert(state.audit_logs.length >= 6, 'audit logs must be created');

  console.log('Smoke test passed:', {
    asset: asset.id,
    part: part.internal_part_id,
    location: assigned.location.barcode,
    task: task.id,
    reservation: reservation.id,
    order: order.id
  });
}

run().catch((error) => {
  console.error('Smoke test failed:', error.message);
  process.exit(1);
});
