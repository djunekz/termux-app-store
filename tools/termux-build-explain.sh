#!/usr/bin/env bash
set -euo pipefail

PKG="$1"
FILE="packages/$PKG/build.sh"

[[ -f "$FILE" ]] || { echo "❌ build.sh not found"; exit 1; }

source "$FILE" || true

echo "🧠 PR Risk Analysis: $PKG"
echo "========================"

risk=0

check() {
  if [[ -z "${!1:-}" ]]; then
    echo "❌ Missing $1 → likely PR rejection"
    risk=1
  fi
}

check TERMUX_PKG_SRCURL
check TERMUX_PKG_SHA256
check TERMUX_PKG_VERSION
check TERMUX_PKG_LICENSE

[[ "$risk" -eq 0 ]] && echo "✔ No obvious policy violation detected"

echo
echo "(Analysis only, no changes made)"
