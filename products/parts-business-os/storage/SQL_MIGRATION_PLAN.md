# SQL Migration Plan

Purpose: move Parts Business OS from demo JSON storage to production-grade database-backed storage.

## Current storage state

Current fullstack skeleton uses:

```text
products/parts-business-os/fullstack/data/demo-db.json
```

This is acceptable for internal alpha only.

It is not acceptable for production.

## Production storage target

Target database: SQL-backed storage using the schema in:

```text
products/parts-business-os/schema/001_core_schema.sql
```

The production system must have:

- migrations
- seed data
- transaction-safe state transitions
- indexes
- backup procedure
- restore test
- tenant isolation
- audit logs

## Migration phases

### Phase 1: Storage adapter boundary

Create a storage layer so business handlers do not directly read/write JSON.

Target files:

```text
products/parts-business-os/fullstack/src/storage/index.js
products/parts-business-os/fullstack/src/storage/json-store.js
products/parts-business-os/fullstack/src/storage/sql-store.js
```

Done when:

- API handlers call storage methods, not raw file operations
- JSON store remains available for local alpha
- SQL store interface is defined

### Phase 2: SQL migrations

Create migration runner.

Target files:

```text
products/parts-business-os/fullstack/scripts/migrate.js
products/parts-business-os/fullstack/migrations/001_core_schema.sql
```

Done when:

- migration command exists
- migration history table exists
- repeated migration does not corrupt database

### Phase 3: Business transactions

Move critical workflows into transaction-safe operations.

Critical operations:

- create part from donor asset
- assign location
- reserve part
- convert reservation to order
- update payment status
- update stock status

Done when:

- reserved/sold part cannot be sold twice
- failed order conversion does not half-update stock
- audit log is written in the same transaction as critical action

### Phase 4: Backup and restore

Create backup and restore commands.

Target files:

```text
products/parts-business-os/fullstack/scripts/backup.js
products/parts-business-os/fullstack/scripts/restore.js
```

Done when:

- backup can be created
- restore can rebuild working state
- restore test is documented and repeatable

## Data integrity rules

- every part belongs to one seller
- every part belongs to one donor asset
- every order belongs to one seller
- every reservation belongs to one seller
- part cannot be sold twice
- part cannot be reserved after sold
- location cannot exceed capacity without explicit override
- cross-seller access is blocked
- every money/stock/status mutation writes audit log

## Blocking issues before production

Production is blocked until:

- JSON direct writes are removed from business handlers
- SQL migration runner exists
- backup and restore are tested
- P0 data integrity tests pass

## Owner agents

- Database Engineer owns schema, migrations, indexes and backup
- Backend Engineer owns storage adapter and transactional operations
- QA Automation Engineer owns data integrity tests
- Security Reviewer owns tenant isolation checks

## Next implementation task

Refactor fullstack server into storage adapter boundary, then add migration runner.
