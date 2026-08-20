# ML Atlas

A multi-page reference for ML/AI research concepts. Every topic page is written
in four cumulative depth tiers — **intuition → mechanics → formal → frontier** —
so the same page serves a complete beginner and someone who works on the topic.

Built with [Astro](https://astro.build) + [Starlight](https://starlight.astro.build),
styled after the [Nerfies](https://nerfies.github.io) academic project-page
template.

## Running it

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in dist/
npm run preview  # serve the built site
```

Node 18+ required. `npm run build` also generates a
[Pagefind](https://pagefind.app) search index automatically — no configuration.

## What's here

```
src/
  content/docs/
    _template.mdx          copy this to start a new page
    index.mdx              landing page
    how-to-read.mdx        the tier system + authoring rules — read this first
    world-models/
      index.mdx            ★ fully written; the reference for the format
      hierarchy.mdx        placeholder
      planning-and-mpc.mdx placeholder
    foundations/           placeholders
    architectures/         placeholders
    training/              placeholders
    reference/             placeholders
  components/
    Abstract.astro         serif summary block under the title
    KeyPoints.astro        the "Key Contributions" box
    Tier.astro             depth-tier divider band
    Figure.astro           centered figure + grey caption
    Papers.astro           numbered citations, rendered from frontmatter
  styles/
    nerfies.css            all visual styling, heavily commented
```

`src/content/docs/world-models/index.mdx` is the one page written end to end.
Use it as the worked example of the format; `_template.mdx` is the blank version.

## Adding a page

1. Copy `_template.mdx` into the right directory and rename it.
2. **Add one `../` to each component import** if you place it in a subdirectory.
3. Fill in frontmatter — `title`, `description`, `sidebar.order`, `papers`.
4. Delete `draft: true` when it's ready. Drafts show in `dev` but not in `build`.

The sidebar picks up new files automatically via `autogenerate`. To add a whole
new *section*, create the directory and add a group to the `sidebar` array in
`astro.config.mjs`.

## Gotchas worth knowing

These are the three things that will bite you, all discovered the hard way:

- **Never put a `<style>` block inside an inline `<svg>` in an `.mdx` file.**
  MDX parses the CSS braces as JSX expressions and the build fails with an
  unhelpful acorn error. Put diagram styles in `nerfies.css` under
  `.atlas-figure svg` instead — the `.bx` / `.lb` / `.sm` / `.ar` classes are
  already defined there.
- **Quote any frontmatter `description` containing a colon.** Otherwise YAML
  reads it as a nested mapping and the content sync fails.
- **`autogenerate` must sit inside a group's `items` array.** Labelled
  top-level `autogenerate` objects were removed in Starlight v0.39.

## Deploying to GitHub Pages

Configured for **https://bhavith-chandra.github.io/notes**. The repo must be
named `notes` — `base` in `astro.config.mjs` has to match the repository name
exactly, or every link 404s.

### First-time setup

> **Before anything else:** this folder contains a stale, broken `.git`
> directory left over from a failed init. Delete it first or git will refuse to
> run.

```bash
cd ml-atlas
rm -rf .git                 # remove the broken repo

git init -b main
git add -A
git commit -m "Initial commit"
git remote add origin git@github.com:bhavith-chandra/notes.git
git push -u origin main
```

Then, once: **repo → Settings → Pages → Build and deployment → Source →
GitHub Actions**. Not "Deploy from a branch" — the workflow uploads a Pages
artifact, which requires the Actions source.

The first build takes ~2 minutes. After that, every push to `main` redeploys
automatically via `.github/workflows/deploy.yml`.

### Changing the URL later

Everything routes through two constants at the top of `astro.config.mjs`:

```js
const SITE = 'https://bhavith-chandra.github.io';
const BASE = '/notes';
```

| Target | `SITE` | `BASE` |
|---|---|---|
| `bhavith-chandra.github.io/notes` | `https://bhavith-chandra.github.io` | `/notes` |
| `bhavith-chandra.github.io` (repo named `bhavith-chandra.github.io`) | same | `/` |
| custom domain | `https://yourdomain.com` | `/` |

Change those and internal links follow automatically — **except** the hero
`actions` links in `src/content/docs/index.mdx`, which are frontmatter and must
be edited by hand. They are the only ones.

### How links survive the base path

Astro rewrites its own asset URLs but not hand-written Markdown links, so a raw
`[text](/encoders/)` would resolve against the domain root and 404. Three
mechanisms cover the three places links appear:

| Link written as | Handled by |
|---|---|
| Markdown `[text](/path/)` or raw `<a href>` | `src/plugins/rehype-base-links.mjs`, automatically |
| Component prop, e.g. `<LinkCard href=...>` | `import.meta.env.BASE_URL` — see the top of `encoders/index.mdx` |
| Frontmatter `hero.actions[].link` | hardcoded, must include `/notes` |

Sidebar navigation, "next/previous" links, and Pagefind search are all generated
by Starlight and handle `base` on their own.

## Other hosts

Netlify, Vercel and Cloudflare Pages serve from the root, so set `BASE = '/'`
first. Build command `npm run build`, publish directory `dist`.

## Customising the look

Everything visual is in `src/styles/nerfies.css`, organised into eight commented
sections. The design tokens at the top (`:root`) control fonts, the accent
colour, the content width, and the four tier colours — start there before
touching anything else.
