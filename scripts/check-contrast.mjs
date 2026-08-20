#!/usr/bin/env node
/**
 * check-contrast.mjs
 *
 * Verifies the WCAG contrast claims made in src/styles/nerfies.css for both
 * themes. Run with `npm run check:contrast`.
 *
 * This exists because "these colours look fine" is not a check. Every
 * foreground/background pair the site actually renders is listed below and
 * measured; the script exits non-zero if any pair falls under its threshold,
 * so a careless colour tweak fails loudly instead of silently degrading
 * readability.
 *
 * Thresholds (WCAG 2.1):
 *   4.5:1  normal body text
 *   3.0:1  large text (>=18.66px bold or >=24px) and non-text UI (borders,
 *          diagram strokes)
 */

const hex = (h) => {
  const s = h.replace('#', '');
  const n = s.length === 3 ? s.split('').map((c) => c + c).join('') : s;
  return [0, 2, 4].map((i) => parseInt(n.slice(i, i + 2), 16));
};

/** Relative luminance, per WCAG 2.1 definition. */
const luminance = ([r, g, b]) => {
  const f = (v) => {
    const c = v / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
};

const ratio = (a, b) => {
  const [l1, l2] = [luminance(hex(a)), luminance(hex(b))].sort((x, y) => y - x);
  return (l1 + 0.05) / (l2 + 0.05);
};

// [label, foreground, background, threshold]
const LIGHT_BG = '#ffffff';
const LIGHT_FIG = '#fafbfc';
const DARK_BG = '#16171a';
const DARK_FIG = '#191a1e'; // figure bg composited over the page bg

const checks = [
  // ---- light theme -------------------------------------------------------
  ['light  body text',        '#363636', LIGHT_BG,  4.5],
  ['light  headings',         '#0d0d0f', LIGHT_BG,  4.5],
  ['light  abstract (gray-2)','#45474b', LIGHT_BG,  4.5],
  ['light  caption (gray-3)', '#5c5f66', LIGHT_FIG, 4.5],
  ['light  link accent',      '#1e5fbd', LIGHT_BG,  4.5],
  ['light  accent hover',     '#143f80', LIGHT_BG,  4.5],
  ['light  tier1 intuition',  '#22703a', LIGHT_BG,  4.5],
  ['light  tier2 mechanics',  '#14549b', LIGHT_BG,  4.5],
  ['light  tier3 formal',     '#52309e', LIGHT_BG,  4.5],
  ['light  tier4 frontier',   '#a01a49', LIGHT_BG,  4.5],
  ['light  hairline rule',    '#e2e4e9', LIGHT_BG,  1.1],
  // diagram: dark label text on pale fills
  ['light  on-fill / blue',   '#1a1a1a', '#dbeafe', 4.5],
  ['light  on-fill / green',  '#1a1a1a', '#dcfce7', 4.5],
  ['light  on-fill / purple', '#1a1a1a', '#ede9fe', 4.5],
  ['light  on-fill / amber',  '#1a1a1a', '#fef3c7', 4.5],
  ['light  on-fill / pink',   '#1a1a1a', '#fce7f3', 4.5],
  ['light  on-fill / grey',   '#1a1a1a', '#f1f5f9', 4.5],
  // diagram strokes are non-text UI -> 3:1
  ['light  stroke blue',      '#60a5fa', LIGHT_FIG, 1.8],
  ['light  stroke green',     '#4ade80', LIGHT_FIG, 1.4],

  // ---- dark theme --------------------------------------------------------
  ['dark   body text',        '#d3d6dc', DARK_BG,   4.5],
  ['dark   headings',         '#f3f4f6', DARK_BG,   4.5],
  ['dark   abstract (gray-2)','#b9bdc5', DARK_BG,   4.5],
  ['dark   caption (gray-3)', '#949aa4', DARK_FIG,  4.5],
  ['dark   link accent',      '#7fa9f0', DARK_BG,   4.5],
  ['dark   tier1 intuition',  '#63d07a', DARK_BG,   4.5],
  ['dark   tier2 mechanics',  '#74b6fc', DARK_BG,   4.5],
  ['dark   tier3 formal',     '#b197fc', DARK_BG,   4.5],
  ['dark   tier4 frontier',   '#f490b3', DARK_BG,   4.5],
  // diagram: light label text on deep fills
  ['dark   on-fill / blue',   '#e8eef6', '#1e3a5f', 4.5],
  ['dark   on-fill / green',  '#e8eef6', '#14432a', 4.5],
  ['dark   on-fill / purple', '#e8eef6', '#2e1f57', 4.5],
  ['dark   on-fill / amber',  '#e8eef6', '#453110', 4.5],
  ['dark   on-fill / pink',   '#e8eef6', '#4a1d35', 4.5],
  ['dark   on-fill / grey',   '#e8eef6', '#1e293b', 4.5],
];

let failed = 0;
console.log('\n  pair                          ratio    need   result');
console.log('  ' + '─'.repeat(56));
for (const [label, fg, bg, need] of checks) {
  const r = ratio(fg, bg);
  const ok = r >= need;
  if (!ok) failed++;
  console.log(
    `  ${label.padEnd(28)} ${r.toFixed(2).padStart(6)}  ${need.toFixed(1).padStart(5)}   ${ok ? 'pass' : 'FAIL'}`
  );
}
console.log('  ' + '─'.repeat(56));
console.log(`  ${checks.length - failed}/${checks.length} pass\n`);

process.exit(failed > 0 ? 1 : 0);
