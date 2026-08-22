#!/usr/bin/env node
/**
 * Enforces the site's structural invariants. Run via `npm run check:order`.
 *
 * The sidebar order IS the curriculum, which only stays true if nothing drifts.
 * Four things are checked:
 *
 *   1. Every page has a numeric `sidebar.order`.
 *   2. No two pages in the same directory share an order — Starlight breaks
 *      ties by filename, which silently produces an arbitrary reading order.
 *   3. Every `index.mdx` is order 0.
 *   4. No page lists a prereq that lives in a LATER sidebar group. A forward
 *      prerequisite means the curriculum order is wrong, not the page.
 *
 * Exits non-zero on any violation so CI and the deploy script catch it.
 */
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const DOCS = join(ROOT, 'src/content/docs');

// Must match the `sidebar` array in astro.config.mjs, top to bottom.
const GROUP_ORDER = [
  'foundations',
  'encoders',
  'architectures',
  'embeddings',
  'training',
  'world-models',
  'domains',
  'systems',
  'hardware',
  'reference',
];

function walk(dir) {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) return walk(p);
    return name.endsWith('.mdx') && !name.startsWith('_') ? [p] : [];
  });
}

const problems = [];
const pages = [];

for (const file of walk(DOCS)) {
  const rel = relative(DOCS, file);
  const src = readFileSync(file, 'utf8');
  const fm = src.split('\n---\n')[0];
  const dir = rel.includes('/') ? rel.slice(0, rel.indexOf('/')) : '';

  const orderMatch = fm.match(/^sidebar:\n(?:[ \t]+\w+:.*\n)*?[ \t]+order:[ \t]*(\S+)/m);
  const prereqs = [...fm.matchAll(/slug:\s*"([^"]+)"/g)].map((m) => m[1]);

  // Root-level pages are listed explicitly in the sidebar, so they are exempt.
  if (!dir) continue;

  if (!orderMatch) {
    problems.push(`${rel}: no sidebar.order`);
    continue;
  }
  const order = Number(orderMatch[1]);
  if (Number.isNaN(order)) problems.push(`${rel}: sidebar.order is not a number`);

  if (rel.endsWith('index.mdx') && order !== 0) {
    problems.push(`${rel}: index pages must be order 0, found ${order}`);
  }

  pages.push({ rel, dir, order, prereqs });
}

// 2 — duplicate orders within a directory
const byDir = new Map();
for (const p of pages) {
  if (!byDir.has(p.dir)) byDir.set(p.dir, new Map());
  const seen = byDir.get(p.dir);
  if (seen.has(p.order)) {
    problems.push(`${p.dir}/: order ${p.order} used by both ${seen.get(p.order)} and ${p.rel}`);
  } else {
    seen.set(p.order, p.rel);
  }
}

// 4 — forward prerequisites
const groupIndex = (dir) => GROUP_ORDER.indexOf(dir);
for (const p of pages) {
  for (const slug of p.prereqs) {
    const target = slug.includes('/') ? slug.slice(0, slug.indexOf('/')) : slug;
    const a = groupIndex(p.dir);
    const b = groupIndex(target);
    if (a === -1) problems.push(`${p.rel}: directory "${p.dir}" is not in GROUP_ORDER`);
    if (b === -1) continue; // prereq points at a root page or an unknown group
    if (b > a) {
      problems.push(
        `${p.rel}: prereq "${slug}" is in group ${b + 1} (${target}) but this page is in group ${a + 1} (${p.dir}) — forward prerequisite`
      );
    }
  }
}

for (const dir of GROUP_ORDER) {
  const list = pages.filter((p) => p.dir === dir).sort((a, b) => a.order - b.order);
  if (list.length) {
    console.log(`  ${String(groupIndex(dir) + 1).padStart(2)}. ${dir.padEnd(14)} ${list.map((p) => p.order).join(' ')}`);
  }
}

console.log('');
if (problems.length) {
  console.error(`  ${problems.length} structural problem(s):\n`);
  for (const p of problems) console.error(`   - ${p}`);
  process.exit(1);
}
console.log(`  ${pages.length} pages, ${GROUP_ORDER.length} groups, order is consistent.\n`);
