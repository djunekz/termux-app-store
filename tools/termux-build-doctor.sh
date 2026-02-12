#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COLORS_FILE="$ROOT/tools/colors.sh"

# Safe color loader (CI friendly)
if [[ -f "$COLORS_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$COLORS_FILE"
else
  BOLD_GREEN=""
  BOLD_YELLOW=""
  BOLD_RED=""
  CYAN=""
  WHITE=""
  RESET=""
fi

echo -e "${CYAN}🩺 termux-build doctor${RESET}"
echo -e "${CYAN}======================${RESET}"

ok()   { echo -e "${BOLD_GREEN}✔ $1${RESET}"; }
warn() { echo -e "${BOLD_YELLOW}⚠ $1${RESET}"; }
fail() { echo -e "${BOLD_RED}❌ $1${RESET}"; }

command -v pkg      &>/dev/null && ok "pkg available"      || fail "pkg not found"
command -v dpkg-deb &>/dev/null && ok "dpkg-deb available" || warn "dpkg-deb missing"
command -v curl     &>/dev/null && ok "curl available"     || fail "curl missing"
command -v git      &>/dev/null && ok "git available"      || warn "git missing"

echo
echo -e "${CYAN}Architecture : ${WHITE}$(uname -m)${RESET}"
echo -e "${CYAN}PREFIX       : ${WHITE}${PREFIX:-/data/data/com.termux/files/usr}${RESET}"

echo
echo -e "${CYAN}Doctor check finished (no changes made).${RESET}"
