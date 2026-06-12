import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const root = path.resolve(path.dirname(__filename), '..');
const repoRoot = path.resolve(root, '../../..');

function has(relPath) {
  return existsSync(path.join(repoRoot, relPath));
}

function readJson(relPath) {
  return JSON.parse(readFileSync(path.join(repoRoot, relPath), 'utf8'));
}

const groups = [
  {
    id: 'RC-001 storage boundary',
    files: [
      'products/parts-business-os/fullstack/src/storage/index.js',
      'products/parts-business-os/fullstack/src/storage/json-store.js',
      'products/parts-business-os/storage/SQL_MIGRATION_PLAN.md',
      'products/parts-business-os/schema/001_core_schema.sql'
    ],
    next: 'Wire server.js to storage adapter and add SQL driver skeleton.'
  },
  {
    id: 'RC-002 auth and roles',
    files: [
      'products/parts-business-os/auth/ROLE_PERMISSION_MATRIX.md',
      'products/parts-business-os/fullstack/src/auth/permissions.js',
      'products/parts-business-os/fullstack/scripts/permission-model-test.js'
    ],
    next: 'Wire permission middleware into live API routes.'
  },
  {
    id: 'RC-005 QA automation',
    files: [
      'products/parts-business-os/fullstack/scripts/smoke-test.js',
      'products/parts-business-os/fullstack/scripts/p0-api-tests.js',
      'products/parts-business-os/qa/E2E_TEST_MATRIX.md'
    ],
    next: 'Add CI runner and API permission tests after middleware is wired.'
  },
  {
    id: 'RC-006 deploy loop',
    files: [
      'products/parts-business-os/fullstack/scripts/deploy-production.sh',
      'products/parts-business-os/fullstack/deploy/parts-business-os.service',
      'OPS/TECHNICAL_SPINE/DEPLOY_LOOP.md'
    ],
    next: 'Run deploy on server and record deploy result.'
  }
];

const packageJson = readJson('products/parts-business-os/fullstack/package.json');
const requiredScripts = ['smoke', 'test', 'test:p0', 'test:permissions'];

const result = {
  status: 'rc_status_report',
  rule: 'Do not rebuild existing files. Pick the next open action from this report.',
  groups: groups.map((group) => {
    const missing = group.files.filter((item) => !has(item));
    return {
      id: group.id,
      complete_artifacts: missing.length === 0,
      missing,
      next: group.next
    };
  }),
  package_scripts: requiredScripts.map((script) => ({
    script,
    present: Boolean(packageJson.scripts && packageJson.scripts[script])
  })),
  next_global_action: 'Wire storage adapter and permission middleware into live API routes.'
};

console.log(JSON.stringify(result, null, 2));
