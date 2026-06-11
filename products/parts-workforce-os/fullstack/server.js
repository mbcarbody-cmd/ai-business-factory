const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PORT = process.env.PORT || 8110;
const DATA_DIR = path.join(__dirname, 'data');
const PUBLIC_DIR = path.join(__dirname, 'public');
const DB_FILE = path.join(DATA_DIR, 'db.json');
fs.mkdirSync(DATA_DIR, { recursive: true });
fs.mkdirSync(path.join(DATA_DIR, 'photos'), { recursive: true });

function seed() {
  return {
    workers: [
      { id: 'w1', name: 'Worker 1', role: 'Dismantling', active: true },
      { id: 'w2', name: 'Worker 2', role: 'Photo', active: true }
    ],
    shifts: [],
    parts: [],
    tasks: [],
    photos: [],
    labels: []
  };
}
function load() {
  if (!fs.existsSync(DB_FILE)) fs.writeFileSync(DB_FILE, JSON.stringify(seed(), null, 2));
  return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
}
function save(db) { fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2)); }
function json(res, code, body) {
  const data = JSON.stringify(body);
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8', 'Content-Length': Buffer.byteLength(data), 'Cache-Control': 'no-store' });
  res.end(data);
}
function readBody(req) {
  return new Promise((resolve, reject) => {
    let chunks = [];
    req.on('data', c => chunks.push(c));
    req.on('end', () => {
      const raw = Buffer.concat(chunks).toString('utf8');
      if (!raw) return resolve({});
      try { resolve(JSON.parse(raw)); } catch(e) { reject(e); }
    });
  });
}
function id(prefix) { return prefix + crypto.randomBytes(6).toString('hex'); }
function now() { return new Date().toISOString(); }
function nextPartId(db) {
  const n = db.parts.length + 1;
  return 'P-' + String(n).padStart(6, '0');
}
function csvEscape(v) { return '"' + String(v ?? '').replace(/"/g, '""') + '"'; }
function csv(rows) { return rows.map(r => r.map(csvEscape).join(',')).join('\n'); }

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, 'http://localhost');
    if (req.method === 'GET' && url.pathname === '/') {
      const p = path.join(PUBLIC_DIR, 'index.html');
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      return res.end(fs.readFileSync(p));
    }
    if (req.method === 'GET' && url.pathname.startsWith('/public/')) {
      const safe = path.normalize(url.pathname.replace('/public/', '')).replace(/^\.\.[/\\]/, '');
      const p = path.join(PUBLIC_DIR, safe);
      if (!fs.existsSync(p)) { res.writeHead(404); return res.end('not found'); }
      const type = p.endsWith('.css') ? 'text/css' : p.endsWith('.js') ? 'text/javascript' : 'text/plain';
      res.writeHead(200, { 'Content-Type': type + '; charset=utf-8' });
      return res.end(fs.readFileSync(p));
    }
    if (req.method === 'GET' && url.pathname.startsWith('/photos/')) {
      const safe = path.basename(url.pathname);
      const p = path.join(DATA_DIR, 'photos', safe);
      if (!fs.existsSync(p)) { res.writeHead(404); return res.end('not found'); }
      res.writeHead(200, { 'Content-Type': 'image/jpeg' });
      return res.end(fs.readFileSync(p));
    }

    if (url.pathname === '/api/state' && req.method === 'GET') return json(res, 200, load());

    if (url.pathname === '/api/workers' && req.method === 'POST') {
      const db = load(); const b = await readBody(req);
      const worker = { id: id('w_'), name: b.name || 'Worker', role: b.role || 'Worker', active: true, createdAt: now() };
      db.workers.push(worker); save(db); return json(res, 200, worker);
    }
    if (url.pathname === '/api/shift/start' && req.method === 'POST') {
      const db = load(); const b = await readBody(req);
      const shift = { id: id('s_'), workerId: b.workerId, start: now(), end: null };
      db.shifts.push(shift); save(db); return json(res, 200, shift);
    }
    if (url.pathname === '/api/shift/stop' && req.method === 'POST') {
      const db = load(); const b = await readBody(req);
      const shift = db.shifts.find(s => s.id === b.shiftId && !s.end);
      if (!shift) return json(res, 404, { error: 'shift not found' });
      shift.end = now(); save(db); return json(res, 200, shift);
    }
    if (url.pathname === '/api/parts' && req.method === 'POST') {
      const db = load(); const b = await readBody(req);
      const part = { id: id('part_'), partId: b.partId || nextPartId(db), oem: b.oem || '', vehicle: b.vehicle || '', vin: b.vin || '', category: b.category || '', side: b.side || '', condition: b.condition || 'unknown', shelf: b.shelf || '', status: b.status || 'created', createdAt: now(), updatedAt: now() };
      db.parts.push(part); save(db); return json(res, 200, part);
    }
    if (url.pathname === '/api/tasks' && req.method === 'POST') {
      const db = load(); const b = await readBody(req);
      const task = { id: id('t_'), workerId: b.workerId, partId: b.partId, type: b.type, notes: b.notes || '', startedAt: b.startedAt || now(), endedAt: b.endedAt || now(), minutes: Number(b.minutes || 0), createdAt: now() };
      db.tasks.push(task);
      const part = db.parts.find(p => p.partId === b.partId || p.id === b.partId);
      if (part) { part.status = b.type || part.status; part.updatedAt = now(); }
      save(db); return json(res, 200, task);
    }
    if (url.pathname === '/api/photos' && req.method === 'POST') {
      const db = load(); const b = await readBody(req);
      const photo = { id: id('ph_'), partId: b.partId, workerId: b.workerId, checklist: b.checklist || {}, status: b.status || 'uploaded', notes: b.notes || '', createdAt: now() };
      if (b.dataUrl && String(b.dataUrl).startsWith('data:image/')) {
        const base64 = String(b.dataUrl).split(',')[1];
        const file = photo.id + '.jpg';
        fs.writeFileSync(path.join(DATA_DIR, 'photos', file), Buffer.from(base64, 'base64'));
        photo.file = '/photos/' + file;
      }
      db.photos.push(photo); save(db); return json(res, 200, photo);
    }
    if (url.pathname === '/api/labels' && req.method === 'POST') {
      const db = load(); const b = await readBody(req);
      const part = db.parts.find(p => p.partId === b.partId || p.id === b.partId);
      if (!part) return json(res, 404, { error: 'part not found' });
      const label = { id: id('l_'), partId: part.partId, oem: part.oem, vehicle: part.vehicle, shelf: part.shelf, condition: part.condition, createdAt: now() };
      db.labels.push(label); save(db); return json(res, 200, label);
    }
    if (url.pathname === '/api/export/tasks.csv' && req.method === 'GET') {
      const db = load();
      const header = ['time','worker','role','partId','task','minutes','oem','vehicle','shelf','notes'];
      const rows = [header];
      db.tasks.forEach(t => {
        const w = db.workers.find(x => x.id === t.workerId) || {};
        const p = db.parts.find(x => x.partId === t.partId || x.id === t.partId) || {};
        rows.push([t.createdAt, w.name, w.role, t.partId, t.type, t.minutes, p.oem, p.vehicle, p.shelf, t.notes]);
      });
      const data = csv(rows);
      res.writeHead(200, { 'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': 'attachment; filename="parts_workforce_tasks.csv"' });
      return res.end(data);
    }
    if (url.pathname === '/api/export/parts.csv' && req.method === 'GET') {
      const db = load();
      const rows = [['partId','oem','vehicle','vin','category','side','condition','shelf','status','createdAt','updatedAt']];
      db.parts.forEach(p => rows.push([p.partId,p.oem,p.vehicle,p.vin,p.category,p.side,p.condition,p.shelf,p.status,p.createdAt,p.updatedAt]));
      const data = csv(rows);
      res.writeHead(200, { 'Content-Type': 'text/csv; charset=utf-8', 'Content-Disposition': 'attachment; filename="parts.csv"' });
      return res.end(data);
    }
    if (url.pathname === '/api/reset' && req.method === 'POST') { save(seed()); return json(res, 200, { ok: true }); }

    res.writeHead(404); res.end('not found');
  } catch (e) { json(res, 500, { error: String(e.stack || e) }); }
});

server.listen(PORT, '0.0.0.0', () => console.log('Parts Workforce OS running on 0.0.0.0:' + PORT));
