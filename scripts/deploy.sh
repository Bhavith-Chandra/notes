#!/usr/bin/env bash
# Build the site and publish it to the gh-pages branch.
#
# Usage:  npm run deploy
#
# This exists because the `gh` OAuth token on this machine lacks the `workflow`
# scope, so .github/workflows/deploy.yml cannot be pushed and GitHub Actions
# cannot run the deploy. Everything below is what that workflow would have done.
#
# To switch to automatic deploys instead:
#   gh auth refresh -s workflow
#   git add -f .github && git commit -m "Add deploy workflow" && git push
#   then set Settings -> Pages -> Source to "GitHub Actions"

set -euo pipefail

REPO_URL="https://github.com/Bhavith-Chandra/notes.git"
BRANCH="gh-pages"

# macOS ships an ancient git (2.15) that fails these pushes with an opaque
# HTTP 400, and a Node too old for Astro 7. Prefer the Homebrew versions.
export PATH="/opt/homebrew/bin:/opt/homebrew/opt/node@23/bin:$PATH"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> git  $(git --version | awk '{print $3}')"
echo "==> node $(node -v)"

echo "==> Building"
# Structural invariants first — a build that ships with a broken curriculum
# order is worse than one that fails here.
npm run check:order

npm run build

echo "==> Publishing dist/ to $BRANCH"
cd dist
rm -rf .git
git init -q -b "$BRANCH"
git add -A
git -c user.email="bhavith-chandra@users.noreply.github.com" \
    -c user.name="Bhavith-Chandra" \
    commit -q -m "Deploy site $(date -u '+%Y-%m-%d %H:%M UTC')"
git push -q --force "$REPO_URL" "$BRANCH:$BRANCH"
rm -rf .git

echo "==> Done. Live in ~1 min at https://bhavith-chandra.github.io/notes/"
