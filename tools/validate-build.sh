#!/usr/bin/env bash
set -Eeuo pipefail

# Safe color loader (CI friendly)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COLORS_FILE="$SCRIPT_DIR/colors.sh"

if [[ -f "$COLORS_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$COLORS_FILE"
else
  # fallback if colors.sh not found (prevent CI failure)
  BOLD_RED=""
  BOLD_GREEN=""
  BOLD_YELLOW=""
  BOLD_CYAN=""
  CYAN=""
  RESET=""
fi

FILE="${1:-}"

if [[ -z "$FILE" ]]; then
    echo -e "${BOLD_YELLOW}Usage:${RESET} validate-build.sh <path/to/build.sh>"
    exit 2
fi

if [[ ! -f "$FILE" ]]; then
    echo -e "${BOLD_RED}❌ ERROR:${RESET} File not found: $FILE"
    exit 2
fi

PACKAGE_NAME="$(basename "$(dirname "$FILE")")"

echo -e "${BOLD_CYAN}🔎 Validating build.sh → 📦$PACKAGE_NAME${RESET}"
echo -e "${CYAN}=================================================${RESET}"

FAIL=0

# ---------- helper ----------
check_var() {
    local var="$1"
    if ! grep -Eq "^${var}=" "$FILE"; then
        echo -e "${BOLD_RED}❌ FAIL :${RESET} $var is missing"
        FAIL=1
    else
        echo -e "${BOLD_GREEN}✅ OK   :${RESET} $var"
    fi
}

# ---------- REQUIRED FIELDS ----------
check_var "TERMUX_PKG_HOMEPAGE"
check_var "TERMUX_PKG_DESCRIPTION"
check_var "TERMUX_PKG_LICENSE"
check_var "TERMUX_PKG_MAINTAINER"
check_var "TERMUX_PKG_VERSION"
check_var "TERMUX_PKG_SRCURL"
check_var "TERMUX_PKG_SHA256"

# ---------- BASIC SANITY ----------
if grep -q "dpkg -i" "$FILE"; then
    echo -e "${BOLD_YELLOW}⚠️  WARN :${RESET} build.sh contains 'dpkg -i' (not allowed in Termux build)"
fi

if grep -q "sudo " "$FILE"; then
    echo -e "${BOLD_RED}❌ FAIL :${RESET} sudo usage detected"
    FAIL=1
fi

if grep -q "apt install" "$FILE"; then
    echo -e "${BOLD_YELLOW}⚠️  WARN :${RESET} apt install found (use pkg install instead)"
fi

# ---------- SOURCE SHA256 CHECK ----------
# shellcheck disable=SC1090
source "$FILE"
eval "SRCURL=\"$TERMUX_PKG_SRCURL\""
EXPECTED_SHA="${TERMUX_PKG_SHA256:-}"

if [[ -n "$SRCURL" && -n "$EXPECTED_SHA" ]]; then
    echo
    echo -e "${BOLD_CYAN}🔎 Verifying SHA256 of source package 📦 $PACKAGE_NAME...${RESET}"
    TMPFILE=$(mktemp)

    if ! curl -sL "$SRCURL" -o "$TMPFILE"; then
        echo -e "${BOLD_RED}❌ Failed to download source from $SRCURL${RESET}"
        FAIL=1
    else
        ACTUAL_SHA=$(sha256sum "$TMPFILE" | awk '{print $1}')
        rm -f "$TMPFILE"

        if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
            echo -e "${BOLD_RED}❌ SHA256 mismatch!${RESET}"
            echo -e "   Expected: ${BOLD_YELLOW}$EXPECTED_SHA${RESET}"
            echo -e "   Got     : ${BOLD_YELLOW}$ACTUAL_SHA${RESET}"
            FAIL=1
        else
            echo -e "${BOLD_GREEN}✅ SHA256 verified${RESET}"
        fi
    fi
fi

# ---------- RESULT ----------
echo -e "${CYAN}-------------------------------------------------${RESET}"

if [[ "$FAIL" -eq 1 ]]; then
    echo -e "${BOLD_RED}❌ VALIDATION FAILED${RESET}"
    exit 1
else
    echo -e "${BOLD_GREEN}✅ VALIDATION PASSED${RESET}"
    exit 0
fi
