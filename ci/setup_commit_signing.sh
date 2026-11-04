#!/usr/bin/env bash
set -euo pipefail

if [ -z "${BOT_SIGNING_KEY:-}" ]; then
  echo "::notice::BOT_SIGNING_KEY is not set, commits made by this job will not be signed"
  exit 0
fi

dir="${RUNNER_TEMP:-${TMPDIR:-/tmp}}"
key="$dir/tas_commit_signing"

umask 077
printf '%s\n' "$BOT_SIGNING_KEY" > "$key"
chmod 600 "$key"

if ! printf 'signing check' | ssh-keygen -Y sign -f "$key" -n git >/dev/null 2>&1; then
  rm -f "$key"
  echo "::warning::BOT_SIGNING_KEY is not a usable unencrypted OpenSSH private key, commits made by this job will not be signed"
  exit 0
fi

git config --global gpg.format ssh
git config --global user.signingkey "$key"
git config --global commit.gpgsign true

echo "Commit signing enabled"
