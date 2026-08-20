/**
 * rehype-base-links
 * -----------------
 * Prefixes root-relative internal links in Markdown/MDX with the site's `base`.
 *
 * Why this exists: when the site is served from a subpath (GitHub Pages at
 * `/notes`), Astro rewrites asset URLs and its own routing helpers, but it does
 * NOT touch raw `href="/foo/"` written by hand in Markdown. Those links resolve
 * against the domain root and 404.
 *
 * Rather than hand-prefixing every link — and remembering to do it in every
 * future page — this plugin rewrites them at build time. Write `/encoders/` in
 * your Markdown and it becomes `/notes/encoders/` in the output. Change `base`
 * in astro.config.mjs and every link follows automatically.
 *
 * NOTE: this operates on the HTML AST, so it only sees links written as
 * Markdown (`[text](/path/)`) or raw `<a href="/path/">`. Links passed as
 * *props* to a component (e.g. Starlight's `<LinkCard href="..." />`) are JSX
 * expressions and never reach this plugin — those must use
 * `import.meta.env.BASE_URL` explicitly.
 */

/** Attributes that hold a URL and should be rewritten. */
const URL_ATTRS = {
  a: 'href',
  area: 'href',
  img: 'src',
  video: 'src',
  audio: 'src',
  source: 'src',
};

/**
 * @param {{ base?: string }} options
 */
export default function rehypeBaseLinks(options = {}) {
  const raw = options.base ?? '/';
  // Normalise to a leading slash and no trailing slash: '/notes' or ''.
  const base = raw === '/' ? '' : `/${raw.replace(/^\/+|\/+$/g, '')}`;

  return (tree) => {
    // No base configured — nothing to do, so skip the walk entirely.
    if (!base) return;

    visit(tree);

    function visit(node) {
      if (node.type === 'element') {
        const attr = URL_ATTRS[node.tagName];
        if (attr) {
          const value = node.properties?.[attr];
          if (typeof value === 'string' && shouldRewrite(value)) {
            node.properties[attr] = base + value;
          }
        }
      }
      if (node.children) node.children.forEach(visit);
    }

    function shouldRewrite(url) {
      // Only root-relative paths.
      if (!url.startsWith('/')) return false;
      // Protocol-relative (//cdn.example.com) is external.
      if (url.startsWith('//')) return false;
      // Already prefixed — don't double up.
      if (url === base || url.startsWith(`${base}/`)) return false;
      return true;
    }
  };
}
