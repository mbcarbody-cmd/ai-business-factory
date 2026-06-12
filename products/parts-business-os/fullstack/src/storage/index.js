import { JsonStore } from './json-store.js';

export function createStorage({ driver = process.env.STORAGE_DRIVER || 'json', dbPath, initialStateFactory }) {
  if (driver === 'json') {
    return new JsonStore({ dbPath, initialStateFactory });
  }

  if (driver === 'sql') {
    throw new Error('SQL storage driver is not implemented yet. This is the next RC-001 task.');
  }

  throw new Error(`Unsupported storage driver: ${driver}`);
}

export const STORAGE_DRIVERS = Object.freeze({
  JSON: 'json',
  SQL: 'sql'
});
