import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

export class JsonStore {
  constructor({ dbPath, initialStateFactory }) {
    if (!dbPath) throw new Error('JsonStore requires dbPath');
    if (typeof initialStateFactory !== 'function') throw new Error('JsonStore requires initialStateFactory');

    this.dbPath = dbPath;
    this.initialStateFactory = initialStateFactory;
  }

  async ensure() {
    await mkdir(path.dirname(this.dbPath), { recursive: true });
    if (!existsSync(this.dbPath)) {
      await this.save(this.initialStateFactory());
    }
  }

  async load() {
    await this.ensure();
    return JSON.parse(await readFile(this.dbPath, 'utf8'));
  }

  async save(state) {
    if (!state || typeof state !== 'object') throw new Error('JsonStore.save requires state object');
    await mkdir(path.dirname(this.dbPath), { recursive: true });
    await writeFile(this.dbPath, JSON.stringify(state, null, 2));
  }

  async mutate(mutator) {
    if (typeof mutator !== 'function') throw new Error('JsonStore.mutate requires mutator function');
    const state = await this.load();
    const result = await mutator(state);
    await this.save(state);
    return result;
  }

  async snapshot() {
    return this.load();
  }
}
