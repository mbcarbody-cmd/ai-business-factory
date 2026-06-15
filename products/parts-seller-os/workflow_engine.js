const sampleItems = [
  { id: 'P-001', name: 'Front right headlight', code: 'SAMPLE-HEADLIGHT-RH', vehicle: 'Kia EV sample 2024', side: 'right', condition: 'used_good', photo: 'has_photo', base: 420 },
  { id: 'P-002', name: 'Door control module', code: 'SAMPLE-MODULE-01', vehicle: 'Aston sample 2024', side: 'left', condition: 'used_unknown', photo: 'needs_photo', base: 180 }
];

function category(item) {
  const n = item.name.toLowerCase();
  if (n.includes('headlight')) return { cat: 'lighting', sub: 'headlight', conf: 0.92 };
  if (n.includes('module')) return { cat: 'electronics', sub: 'control_module', conf: 0.8 };
  return { cat: 'review', sub: 'unknown', conf: 0.3 };
}

function location(c) {
  if (c.cat === 'lighting') return { zone: 'fragile-rack', profile: 'fragile_large' };
  if (c.cat === 'electronics') return { zone: 'small-electronics-bin', profile: 'small_protected' };
  return { zone: 'review-zone', profile: 'manual' };
}

function value(item, c) {
  const conf = Math.max(0.25, c.conf - (item.condition === 'used_unknown' ? 0.15 : 0));
  return { suggested: Math.round(item.base * (conf > 0.75 ? 1 : 0.85)), floor: Math.round(item.base * 0.72), confidence: Number(conf.toFixed(2)) };
}

function state(item, v) {
  if (item.photo !== 'has_photo') return 'needs_photo';
  if (v.confidence < 0.65) return 'needs_review';
  return 'ready';
}

function processItem(item) {
  const c = category(item);
  const l = location(c);
  const v = value(item, c);
  const s = state(item, v);
  return {
    item: item.id,
    title: `${item.vehicle} ${item.name} ${item.side}`,
    code: item.code,
    category: c.cat,
    subcategory: c.sub,
    location: l.zone,
    value: v.suggested,
    floor: v.floor,
    confidence: v.confidence,
    listing_state: s,
    reserve_state: s === 'ready' ? 'can_reserve' : 'blocked_until_ready'
  };
}

function runWorkflow(items = sampleItems) {
  return items.map(processItem);
}

module.exports = { sampleItems, category, location, value, state, processItem, runWorkflow };
