# Production Spine Execution Note

Canonical task board: `OPS/TASK_BOARD/production_business_spine_2026_06_17.json`

Canonical database migration: `products/parts-business-os/server/db/001_core_production_spine.sql`

Canonical API contract: `products/parts-business-os/server/openapi/core_v1.yaml`

Canonical local infrastructure: `products/parts-business-os/server/docker-compose.yml`

P0 stop rule: do not create more generic management layers while authentication, tenant isolation tests, monitoring, backup restore, billing path and one working connector remain unfinished.
