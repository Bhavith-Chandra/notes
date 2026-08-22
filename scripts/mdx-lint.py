#!/usr/bin/env python3
"""
mdx-lint.py — catch MDX mistakes that produce unhelpful build errors.

Two checks, both precise (zero false positives across the current 41 pages):

1. BRACES IN JSX CHILDREN.  MDX parses `{...}` as JavaScript, including inside
   JSX children such as SVG <text>. Writing `o_{t-k}` or a Unicode minus in a
   diagram label fails with an acorn error that names a line:column and gives
   no cause. Math and code are stripped first, since braces are legal there.

2. UNCLOSED PAIRED COMPONENTS.  A missing </Steps> reports the position of the
   OPENING tag without naming the file, which is unhelpful across 41 pages.

KNOWN GAP, recorded deliberately:
   Inline math reflowed across a line break can, in some circumstance not
   characterised here, push a brace group out of math and into JSX-expression
   position — producing a runtime "X is not defined" naming a variable absent
   from the source. One instance was hit and fixed in latent-spaces.mdx by
   joining the line. ~65 structurally similar cases elsewhere build fine, so
   the trigger is narrower than "math spans a line". A check for it was written
   and removed: at 65 false positives it would have been ignored, which is
   worse than no check. If it recurs, the fix is to join the wrapped inline
   math onto one line.
"""
import re
import sys
import glob

SKIP_PREFIX = ("import", "export", "{/*", "//", "*")
BRACE = re.compile(r"\{([^{}\n]{1,80})\}")
JSX_TEXT = re.compile(r"<\s*(text|tspan|title|desc)\b", re.I)
SAFE_EXPR = ("`", "frontmatter", "base", "/*")
PAIRED = ("Steps", "Tabs", "TabItem", "Aside", "Figure", "KeyPoints",
          "Abstract", "Card", "CardGrid", "FileTree")


def blank(m):
    """Replace a match with newlines so line numbers survive."""
    return "\n" * m.group(0).count("\n")


problems = 0
for path in sorted(glob.glob("src/content/docs/**/*.mdx", recursive=True)):
    raw = open(path, encoding="utf-8").read()

    body = re.sub(r"\$\$.*?\$\$", blank, raw, flags=re.S)
    body = re.sub(r"```.*?```", blank, body, flags=re.S)
    body = re.sub(r"\$[^$]*\$", blank, body, flags=re.S)
    body = re.sub(r"`[^`\n]*`", "", body)

    # --- 1. braces inside JSX children ------------------------------------
    for n, line in enumerate(body.split("\n"), 1):
        s = line.strip()
        if s.startswith(SKIP_PREFIX) or not JSX_TEXT.search(s):
            continue
        for m in BRACE.finditer(s):
            inner = m.group(1)
            if inner.startswith(SAFE_EXPR):
                continue
            print(f"  JSX-BRACE  {path}:{n}  {{{inner[:60]}}}")
            print(f"      {s[:100]}")
            problems += 1

    # --- 2. unclosed paired components ------------------------------------
    for tag in PAIRED:
        opens = len(re.findall(rf"<{tag}(?=[\s>])(?![^>]*/>)", raw, flags=re.S))
        closes = len(re.findall(rf"</{tag}>", raw))
        if opens != closes:
            print(f"  UNCLOSED   {path}  <{tag}> open={opens} close={closes}")
            problems += 1

print(f"\n  problems: {problems}")
sys.exit(1 if problems else 0)
