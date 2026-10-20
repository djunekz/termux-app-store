#!/usr/bin/env bash
set -euo pipefail

PAGES_DIR="${1:?usage: sign_release.sh <gh-pages-dir>}"
RELEASE="$PAGES_DIR/dists/termux/Release"
EXPECTED_KEY_FPR="${EXPECTED_KEY_FPR:-D39134A177717A5BEBEEAE7105D70CDBB6D80295}"

if [ ! -f "$RELEASE" ]; then
  echo "::error::Release file not found: $RELEASE"
  exit 1
fi

if [ -z "${GPG_PRIVATE_KEY:-}" ]; then
  echo "::error::Secret GPG_PRIVATE_KEY is not set - refusing to publish an unsigned repository"
  exit 1
fi

GNUPGHOME="$(mktemp -d)"
export GNUPGHOME
chmod 700 "$GNUPGHOME"
VERIFY_HOME="$(mktemp -d)"
chmod 700 "$VERIFY_HOME"

cleanup() {
  gpgconf --kill gpg-agent 2>/dev/null || true
  rm -rf "$GNUPGHOME" "$VERIFY_HOME"
}
trap cleanup EXIT

printf '%s\n' "$GPG_PRIVATE_KEY" | gpg --batch --quiet --import

KEY_FPR="$(gpg --batch --list-secret-keys --with-colons \
  | awk -F: '/^sec:/ {s=1; next} s && /^fpr:/ {print $10; exit}')"

if [ -z "$KEY_FPR" ]; then
  echo "::error::No secret key found after import"
  exit 1
fi

if [ "$KEY_FPR" != "$EXPECTED_KEY_FPR" ]; then
  echo "::error::Signing key $KEY_FPR does not match the pinned key $EXPECTED_KEY_FPR - clients would reject this repository"
  exit 1
fi

GPG_ARGS=(--batch --yes --pinentry-mode loopback --local-user "$KEY_FPR" --digest-algo SHA256)
if [ -n "${GPG_PASSPHRASE:-}" ]; then
  PASSFILE="$GNUPGHOME/pass"
  ( umask 077; printf '%s' "$GPG_PASSPHRASE" > "$PASSFILE" )
  GPG_ARGS+=(--passphrase-file "$PASSFILE")
fi

rm -f "$PAGES_DIR/dists/termux/InRelease" "$PAGES_DIR/dists/termux/Release.gpg"
gpg "${GPG_ARGS[@]}" --clearsign   -o "$PAGES_DIR/dists/termux/InRelease"   "$RELEASE"
gpg "${GPG_ARGS[@]}" --detach-sign -o "$PAGES_DIR/dists/termux/Release.gpg" "$RELEASE"

gpg --batch --export "$KEY_FPR"         > "$PAGES_DIR/termux-app-store.gpg"
gpg --batch --armor --export "$KEY_FPR" > "$PAGES_DIR/termux-app-store.asc"

gpgv --homedir "$VERIFY_HOME" --keyring "$PWD/$PAGES_DIR/termux-app-store.gpg" \
  "$PAGES_DIR/dists/termux/Release.gpg" "$RELEASE"
gpgv --homedir "$VERIFY_HOME" --keyring "$PWD/$PAGES_DIR/termux-app-store.gpg" \
  "$PAGES_DIR/dists/termux/InRelease"

echo "Signed Release with key $KEY_FPR"
