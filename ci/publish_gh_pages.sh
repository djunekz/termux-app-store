#!/usr/bin/env bash
set -euo pipefail

DIR="${1:?usage: publish_gh_pages.sh <directory> <message>}"
MSG="${2:?usage: publish_gh_pages.sh <directory> <message>}"

cd "$DIR"
git add -A

BASE=""
if git rev-parse --verify -q HEAD >/dev/null 2>&1; then
  BASE="$(git rev-parse HEAD)"
  if git diff --staged --quiet; then
    echo "Nothing to commit"
    exit 0
  fi
fi

git checkout --orphan publish-snapshot
git commit -m "$MSG"

if [[ -n "$BASE" ]]; then
  git push --force-with-lease="refs/heads/gh-pages:${BASE}" origin "publish-snapshot:refs/heads/gh-pages"
else
  git push origin "publish-snapshot:refs/heads/gh-pages"
fi
echo "Pushed: $MSG"
