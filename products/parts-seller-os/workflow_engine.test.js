const assert = require('assert');
const { runWorkflow } = require('./workflow_engine');

const rows = runWorkflow();

assert.strictEqual(rows.length, 2, 'two sample rows expected');

for (const row of rows) {
  assert.ok(row.item, 'item id required');
  assert.ok(row.title, 'title required');
  assert.ok(row.code, 'code required');
  assert.ok(row.category, 'category required');
  assert.ok(row.location, 'location required');
  assert.ok(Number.isFinite(row.value), 'numeric value required');
  assert.ok(Number.isFinite(row.floor), 'numeric floor required');
  assert.ok(row.floor < row.value, 'floor must be below suggested value');
  assert.ok(['ready', 'needs_photo', 'needs_review'].includes(row.listing_state), 'valid listing state required');
  assert.ok(['can_reserve', 'blocked_until_ready'].includes(row.reserve_state), 'valid reserve state required');
}

const ready = rows.find(row => row.listing_state === 'ready');
assert.ok(ready, 'at least one ready row expected');
assert.strictEqual(ready.reserve_state, 'can_reserve', 'ready row must be reservable');

const blocked = rows.find(row => row.listing_state !== 'ready');
assert.ok(blocked, 'at least one blocked row expected');
assert.strictEqual(blocked.reserve_state, 'blocked_until_ready', 'blocked row cannot be reserved');

console.log('Parts Seller OS workflow engine test PASS');
