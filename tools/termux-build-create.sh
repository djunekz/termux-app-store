#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COLORS_FILE="$ROOT/tools/colors.sh"

if [[ -f "$COLORS_FILE" ]]; then
  source "$COLORS_FILE"
else
  BOLD_RED=""
  BOLD_GREEN=""
  BOLD_YELLOW=""
  BOLD_CYAN=""
  CYAN=""
  RESET=""
fi

PKG="${1:-}"
PKG_DIR="$ROOT/packages"
TEMPLATE="$ROOT/template/build.sh"

die() {
  echo -e "${BOLD_RED}❌ $*${RESET}" >&2
  exit 1
}

info() {
  echo -e "${CYAN}ℹ $*${RESET}"
}

ok() {
  echo -e "${BOLD_GREEN}✔ $*${RESET}"
}

[[ -z "$PKG" ]] && die "Usage: ./termux-build create <package-name>"

if [[ ! "$PKG" =~ ^[a-z0-9._+-]+$ ]]; then
  die "Invalid package name: $PKG"
fi

TARGET="$PKG_DIR/$PKG"

[[ -d "$TARGET" ]] && die "Package already exists: $PKG"
[[ -f "$TEMPLATE" ]] || die "Template not found: template/build.sh"

info "Creating package: $PKG"

mkdir -p "$TARGET"
cp "$TEMPLATE" "$TARGET/build.sh"
chmod +x "$TARGET/build.sh"

ok "Package created:"
echo -e "  ${BOLD_YELLOW}→ packages/$PKG/build.sh${RESET}"

# ---------- Steps ----------
echo
echo -e "${BOLD_CYAN}=============================================${RESET}"
echo -e "${BOLD_CYAN}Next steps:${RESET}"
echo -e "  ${BOLD_CYAN}- Edit file build.sh: ${BOLD_GREEN}nano packages/$PKG/build.sh${RESET}"

echo -e "${BOLD_YELLOW}Step 1:${RESET}"
echo -e "  ${BOLD_YELLOW}Check installing your package:${RESET}"
echo -e "     - Run: ${BOLD_GREEN}bash build-packages.sh $PKG${RESET}"
echo -e "     - Run: ${BOLD_GREEN}$PKG${RESET}"

echo -e "${BOLD_YELLOW}Step 2:${RESET}"
echo -e "  ${BOLD_YELLOW}Validation:${RESET}"
echo -e "     - Run: ${BOLD_GREEN}./termux-build lint $PKG${RESET}"
echo -e "     - Run: ${BOLD_GREEN}./termux-build doctor${RESET}"

echo -e "${BOLD_CYAN}=============================================${RESET}"
