// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeBaseLinks from './src/plugins/rehype-base-links.mjs';

// Deployment target: https://bhavith-chandra.github.io/notes
//
// `site` is the origin only; `base` is the subpath the repo is served from and
// must match the repository name exactly. If you later move this to a custom
// domain or rename the repo to `bhavith-chandra.github.io`, set base to '/'
// (or delete the line) — every internal link follows automatically, because
// they all route through BASE (see rehype-base-links.mjs).
const SITE = 'https://bhavith-chandra.github.io';
const BASE = '/notes';

export default defineConfig({
  site: SITE,
  base: BASE,

  // Emit `/notes/page/` rather than `/notes/page` so GitHub Pages' static
  // file serving resolves directory index.html without a redirect hop.
  trailingSlash: 'always',
  build: { format: 'directory' },

  // Pages that have moved. AI Safety was originally under Foundations; it reads
  // correctly only after Post-Training, so it now lives in Training. Keep the
  // old URL alive — it has been linked externally.
  //
  // NOTE: Astro applies `base` to the redirect KEY but writes the VALUE into the
  // meta-refresh verbatim, so the destination must include BASE explicitly.
  redirects: {
    '/foundations/ai-safety/': `${BASE}/training/ai-safety/`,
  },

  // KaTeX math support. Astro 7 replaced `markdown.remarkPlugins` /
  // `markdown.rehypePlugins` with this `unified()` processor hook.
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [
        [
          rehypeKatex,
          {
            // Don't kill the build on a malformed expression — render it in
            // red so it's obvious in review instead.
            throwOnError: false,
            strict: false,
          },
        ],
        // Must run after KaTeX. Rewrites hand-written root-relative links in
        // Markdown so they resolve under BASE instead of the domain root.
        [rehypeBaseLinks, { base: BASE }],
      ],
    }),
  },

  integrations: [
    starlight({
      title: 'ML Atlas',
      description:
        'Machine learning and AI research concepts explained from first principles through to the research frontier.',
      tagline: 'From first principles to the research frontier.',

      // Nerfies-inspired styling lives here. Order matters: ours loads last.
      customCss: ['katex/dist/katex.min.css', './src/styles/nerfies.css'],

      // Show the "Edit this page" link — useful once this is in a repo.
      // editLink: { baseUrl: 'https://github.com/<you>/ml-atlas/edit/main/' },

      social: [
        // { icon: 'github', label: 'GitHub', href: 'https://github.com/<you>/ml-atlas' },
      ],

      // Right-hand "On this page" rail. Nerfies pages are long, so go deep.
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },

      sidebar: [
        // SIDEBAR ORDER IS THE CURRICULUM.
        //
        // Groups are listed in prerequisite order: nothing in a group should
        // depend on a group below it. Within a group, `sidebar.order` in each
        // page's frontmatter does the same job — index pages are always 0, and
        // no two pages in a directory may share an order (Starlight resolves
        // ties by filename, which is not a curriculum).
        //
        // If you add a page, place it by asking "what must the reader already
        // know?", not by topic affinity. /curriculum mirrors this order and
        // must be updated alongside it.
        //
        // NOTE: since Starlight v0.39, `autogenerate` must live inside a
        // group's `items` array — a labelled autogenerate object at the top
        // level is no longer valid config.
        {
          label: 'Start here',
          items: [
            { label: 'What this is', slug: 'index' },
            { label: 'How to read a page', slug: 'how-to-read' },
            { label: 'Reading order', slug: 'curriculum' },
          ],
        },
        {
          label: '1 · Foundations',
          collapsed: false,
          items: [{ autogenerate: { directory: 'foundations' } }],
        },
        {
          label: '2 · Encoders',
          collapsed: false,
          items: [{ autogenerate: { directory: 'encoders' } }],
        },
        {
          label: '3 · Architectures',
          collapsed: true,
          items: [{ autogenerate: { directory: 'architectures' } }],
        },
        {
          label: '4 · Embeddings',
          collapsed: true,
          items: [{ autogenerate: { directory: 'embeddings' } }],
        },
        {
          label: '5 · Training & Objectives',
          collapsed: true,
          items: [{ autogenerate: { directory: 'training' } }],
        },
        {
          label: '6 · World Models & Planning',
          collapsed: true,
          items: [{ autogenerate: { directory: 'world-models' } }],
        },
        {
          label: '7 · Domains',
          collapsed: true,
          items: [{ autogenerate: { directory: 'domains' } }],
        },
        {
          label: '8 · Systems',
          collapsed: true,
          items: [{ autogenerate: { directory: 'systems' } }],
        },
        {
          label: '9 · Hardware & Compute',
          collapsed: true,
          items: [{ autogenerate: { directory: 'hardware' } }],
        },
        {
          label: 'Reference',
          collapsed: true,
          items: [{ autogenerate: { directory: 'reference' } }],
        },
      ],

      // Starlight ships Pagefind search at build time — nothing to configure.
      pagefind: true,

      lastUpdated: true,
      credits: false,
    }),
  ],
});
