#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COLORS_FILE="$ROOT/tools/colors.sh"
PKG_DIR="$ROOT/packages"

if [[ -f "$COLORS_FILE" ]]; then
  source "$COLORS_FILE"
else
  BOLD_RED=""
  BOLD_GREEN=""
  BOLD_CYAN=""
  CYAN=""
  YELLOW=""
  MAGENTA=""
  RESET=""
fi

PKG="${1:-}"

if [[ -z "$PKG" ]]; then
  echo -e "${BOLD_RED}❌ Usage: termux-build suggest <package>${RESET}"
  exit 1
fi

FILE="$PKG_DIR/$PKG/build.sh"

if [[ ! -f "$FILE" ]]; then
  echo -e "${BOLD_RED}❌ build.sh not found for package: $PKG${RESET}"
  exit 1
fi

# Load variables safely (avoid script execution side effects)
set +e
source "$FILE"
set -e

echo -e "${BOLD_CYAN}💡 Suggestions for $PKG${RESET}"
echo -e "${CYAN}=======================${RESET}"

SUGGESTIONS=0

suggest_missing() {
  local var="$1"
  if [[ -z "${!var:-}" ]]; then
    echo -e "${YELLOW}- add ${var}=\"...\"${RESET}"
    SUGGESTIONS=1
  fi
}

suggest_quality() {
  local var="$1"
  local val="${!var:-}"
  if [[ -n "$val" && ${#val} -lt 10 ]]; then
    echo -e "${MAGENTA}- consider improving ${var} (too short)${RESET}"
    SUGGESTIONS=1
  fi
}

# Required fields
suggest_missing TERMUX_PKG_HOMEPAGE
suggest_missing TERMUX_PKG_DESCRIPTION
suggest_missing TERMUX_PKG_LICENSE
suggest_missing TERMUX_PKG_MAINTAINER
suggest_missing TERMUX_PKG_VERSION
suggest_missing TERMUX_PKG_SRCURL
suggest_missing TERMUX_PKG_SHA256

# Quality hints
suggest_quality TERMUX_PKG_DESCRIPTION
suggest_quality TERMUX_PKG_HOMEPAGE

echo
if [[ $SUGGESTIONS -eq 0 ]]; then
  echo -e "${BOLD_GREEN}✔ No suggestions — build.sh already looks solid${RESET}"
fi
