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
        {
          label: 'Start here',
          items: [
            { label: 'What this is', slug: 'index' },
            { label: 'How to read a page', slug: 'how-to-read' },
          ],
        },
        // NOTE: since Starlight v0.39, `autogenerate` must live inside a
        // group's `items` array — a labelled autogenerate object at the top
        // level is no longer valid config.
        {
          label: 'Encoders',
          collapsed: false,
          items: [{ autogenerate: { directory: 'encoders' } }],
        },
        {
          label: 'Foundations',
          collapsed: false,
          items: [{ autogenerate: { directory: 'foundations' } }],
        },
        {
          label: 'World Models & Planning',
          collapsed: false,
          items: [{ autogenerate: { directory: 'world-models' } }],
        },
        {
          label: 'Architectures',
          collapsed: true,
          items: [{ autogenerate: { directory: 'architectures' } }],
        },
        {
          label: 'Training & Objectives',
          collapsed: true,
          items: [{ autogenerate: { directory: 'training' } }],
        },
        {
          label: 'Systems',
          collapsed: true,
          items: [{ autogenerate: { directory: 'systems' } }],
        },
        {
          label: 'Hardware & Compute',
          collapsed: true,
          items: [{ autogenerate: { directory: 'hardware' } }],
        },
        {
          label: 'Domains',
          collapsed: true,
          items: [{ autogenerate: { directory: 'domains' } }],
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
