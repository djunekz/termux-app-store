#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
COLORS_FILE="$ROOT_DIR/tools/colors.sh"
VALIDATOR="$ROOT_DIR/tools/validate-build.sh"
PKG_DIR="$ROOT_DIR/packages"

if [[ -f "$COLORS_FILE" ]]; then
  source "$COLORS_FILE"
else
  RED=""
  GREEN=""
  BOLD_RED=""
  RESET=""
fi

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
    echo -e "${RED}Usage:${RESET}"
    echo -e "  ${GREEN}./termux-build lint packages/<package>/build.sh${RESET}"
    echo -e "  ${GREEN}./termux-build lint <package>${RESET}"
    echo -e "  ${GREEN}./termux-build lint all${RESET}"
    exit 2
fi

# ---------- Lint All ----------
if [[ "$TARGET" == "all" ]]; then
    FAIL=0
    FOUND=0

    for BUILD in "$PKG_DIR"/*/build.sh; do
        [[ -f "$BUILD" ]] || continue
        FOUND=1
        echo
        echo "🔍 Linting $(basename "$(dirname "$BUILD")")"
        if ! bash "$VALIDATOR" "$BUILD"; then
            FAIL=1
        fi
    done

    if [[ "$FOUND" -eq 0 ]]; then
        echo -e "${BOLD_RED}❌ No packages found${RESET}"
        exit 1
    fi

    exit $FAIL
fi

# ---------- Lint by package name ----------
if [[ -d "$PKG_DIR/$TARGET" ]]; then
    exec bash "$VALIDATOR" "$PKG_DIR/$TARGET/build.sh"
fi

# ---------- Lint by direct path ----------
if [[ -f "$TARGET" ]]; then
    exec bash "$VALIDATOR" "$TARGET"
fi

echo -e "${BOLD_RED}❌ ERROR: Invalid target: $TARGET${RESET}"
exit 2
