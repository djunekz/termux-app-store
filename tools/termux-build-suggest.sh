#!/usr/bin/env bash
set -euo pipefail

PKG="$1"
FILE="packages/$PKG/build.sh"

[[ -f "$FILE" ]] || { echo "❌ build.sh not found"; exit 1; }

source "$FILE" || true

echo "💡 Suggestions for $PKG"
echo "======================="

suggest() {
  [[ -z "${!1:-}" ]] && echo "- add $1=\"...\""
}

suggest TERMUX_PKG_HOMEPAGE
suggest TERMUX_PKG_DESCRIPTION
suggest TERMUX_PKG_LICENSE
suggest TERMUX_PKG_MAINTAINER
suggest TERMUX_PKG_VERSION
suggest TERMUX_PKG_SRCURL
suggest TERMUX_PKG_SHA256

echo
echo "(No files were modified)"
