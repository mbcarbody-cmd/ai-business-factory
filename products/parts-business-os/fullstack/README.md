# Parts Business OS Fullstack Demo

This is the first runnable technical skeleton for Parts Business OS.

It proves the core operational workflow:

```text
seller -> donor asset -> part -> warehouse location -> worker task -> reservation -> order -> audit log
```

## Why this exists

The project needs more than agent role documents. This folder gives agents a concrete product surface to build, test and improve.

## Requirements

- Node.js 20+
- No external npm dependencies are required for this skeleton

## Run

```bash
cd products/parts-business-os/fullstack
npm start
```

Open:

```text
http://localhost:3060
```

Health check:

```text
http://localhost:3060/health
```

## Smoke test

Start the server in one terminal:

```bash
npm start
```

Run the smoke test in another terminal:

```bash
npm run smoke
```

## Current implemented flows

- Health endpoint
- Demo data store in `data/demo-db.json`
- Create donor asset
- Create part from donor asset
- Generate internal part ID
- Recommend warehouse location by volume and weight
- Assign part to location
- Create worker task
- Reserve part
- Convert reservation to order
- Write audit logs
- Demo frontend with one-click full workflow

## Not production-ready yet

This skeleton intentionally uses a local JSON data file for fast execution.

Next production steps:

1. Replace JSON storage with the SQL schema in `../schema/001_core_schema.sql`
2. Add real auth and role middleware
3. Add migrations
4. Add API validation tests
5. Add deploy script and systemd/docker service
6. Add backup and restore test
7. Add CI release gate

## Agent ownership

- Principal Architect: keep workflow coherent
- Backend Engineer: API and state transitions
- Database Engineer: migrate from JSON to SQL
- Warehouse Math Agent: improve location recommendation
- QA Automation Engineer: expand smoke test into E2E suite
- DevOps Engineer: make deploy executable
- UX / Website Design Agent: improve public and operator screens

## Done gate for next iteration

The next iteration is done only when:

- SQL-backed storage works
- `/health` checks DB access
- role permission middleware exists
- automated tests cover double-reservation prevention
- deploy script exists
