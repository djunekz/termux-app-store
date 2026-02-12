#!/usr/bin/env bash
set -eo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COLORS_FILE="$ROOT/tools/colors.sh"

if [[ -f "$COLORS_FILE" ]]; then
  source "$COLORS_FILE"
else
  BOLD_RED=""
  BOLD_GREEN=""
  BOLD_YELLOW=""
  CYAN=""
  RESET=""
fi

PKG="${1:-}"

if [[ -z "$PKG" ]]; then
  echo -e "${BOLD_RED}❌ Usage: termux-build explain <package>${RESET}"
  exit 1
fi

FILE="$ROOT/packages/$PKG/build.sh"

if [[ ! -f "$FILE" ]]; then
  echo -e "${BOLD_RED}❌ build.sh not found for package: $PKG${RESET}"
  exit 1
fi

(
  set +u +e
  source "$FILE"
  export TERMUX_PKG_SRCURL
  export TERMUX_PKG_SHA256
  export TERMUX_PKG_VERSION
  export TERMUX_PKG_LICENSE
  export TERMUX_PKG_HOMEPAGE
  export TERMUX_PKG_DESCRIPTION
) >/dev/null 2>&1 || true

TERMUX_PKG_SRCURL="${TERMUX_PKG_SRCURL:-}"
TERMUX_PKG_SHA256="${TERMUX_PKG_SHA256:-}"
TERMUX_PKG_VERSION="${TERMUX_PKG_VERSION:-}"
TERMUX_PKG_LICENSE="${TERMUX_PKG_LICENSE:-}"
TERMUX_PKG_HOMEPAGE="${TERMUX_PKG_HOMEPAGE:-}"
TERMUX_PKG_DESCRIPTION="${TERMUX_PKG_DESCRIPTION:-}"

echo -e "${CYAN}🧠 PR Risk Analysis: $PKG${RESET}"
echo -e "${CYAN}========================${RESET}"

RISK=0
WARN=0

fatal() {
  echo -e "${BOLD_RED}❌ FATAL : $1${RESET}"
  RISK=1
}

warn() {
  echo -e "${BOLD_YELLOW}⚠️  WARN  : $1${RESET}"
  WARN=1
}

ok() {
  echo -e "${BOLD_GREEN}✔ OK     : $1${RESET}"
}

[[ -z "$TERMUX_PKG_SRCURL"  ]] && fatal "TERMUX_PKG_SRCURL missing"  || ok "SRCURL present"
[[ -z "$TERMUX_PKG_SHA256"  ]] && fatal "TERMUX_PKG_SHA256 missing"  || ok "SHA256 present"
[[ -z "$TERMUX_PKG_VERSION" ]] && fatal "TERMUX_PKG_VERSION missing" || ok "VERSION present"
[[ -z "$TERMUX_PKG_LICENSE" ]] && fatal "TERMUX_PKG_LICENSE missing" || ok "LICENSE present"

[[ -z "$TERMUX_PKG_HOMEPAGE" ]] && warn "No homepage set (optional but recommended)"

if [[ -n "$TERMUX_PKG_DESCRIPTION" && ${#TERMUX_PKG_DESCRIPTION} -lt 15 ]]; then
  warn "Description is very short"
fi

echo
if [[ $RISK -eq 1 ]]; then
  echo -e "${BOLD_RED}🚫 High risk: PR likely to be rejected${RESET}"
elif [[ $WARN -eq 1 ]]; then
  echo -e "${BOLD_YELLOW}⚠️  Medium risk: PR may get reviewer comments${RESET}"
else
  echo -e "${BOLD_GREEN}🟢 Low risk: PR looks clean and review-friendly${RESET}"
fi

echo
echo -e "${CYAN}(Analysis only, no changes made)${RESET}"
