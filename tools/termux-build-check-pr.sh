#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT/tools/validate-build.sh"

# Safe color loader (CI friendly)
COLORS_FILE="$ROOT/tools/colors.sh"
if [[ -f "$COLORS_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$COLORS_FILE"
else
  BLUE=""
  CYAN=""
  YELLOW=""
  BOLD_RED=""
  BOLD_GREEN=""
  RESET=""
fi

FAIL=0

# Ambil target package
TARGET="${1:-}"

# Kalau masih kebawa subcommand
if [[ "$TARGET" == "check-pr" ]]; then
    TARGET="${2:-}"
fi

echo -e "${BLUE}🔍 Checking packages...${RESET}"
echo -e "${CYAN}================================${RESET}"

if [[ -n "$TARGET" ]]; then
    BUILD="$ROOT/packages/$TARGET/build.sh"
    if [[ ! -f "$BUILD" ]]; then
        echo -e "${BOLD_RED}❌ Package not found: $TARGET${RESET}"
        exit 1
    fi

    echo
    echo -e "${YELLOW}📦 $TARGET${RESET}"
    bash "$VALIDATOR" "$BUILD" || FAIL=1
else
    for BUILD in "$ROOT/packages"/*/build.sh; do
        PKG="$(basename "$(dirname "$BUILD")")"
        echo
        echo -e "${YELLOW}📦 $PKG${RESET}"
        bash "$VALIDATOR" "$BUILD" || FAIL=1
    done
fi

if [[ $FAIL -eq 0 ]]; then
    echo
    echo -e "${BOLD_GREEN}✅ PR looks good${RESET}"
else
    echo
    echo -e "${BOLD_RED}❌ PR has issues${RESET}"
fi

exit $FAIL
