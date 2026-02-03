#!/usr/bin/env bash
set -eo pipefail

FILE="$1"

if [[ -z "${FILE:-}" ]]; then
    echo "Usage: validate-build.sh <path/to/build.sh>"
    exit 2
fi

if [[ ! -f "$FILE" ]]; then
    echo "❌ ERROR: File not found: $FILE"
    exit 2
fi

echo "🔎 Validating build.sh → $FILE"
echo "================================================="

FAIL=0

# ---------- helper ----------
check_var() {
    local var="$1"
    if ! grep -Eq "^${var}=" "$FILE"; then
        echo "❌ FAIL : $var is missing"
        FAIL=1
    else
        echo "✅ OK   : $var"
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
    echo "⚠️  WARN : build.sh contains 'dpkg -i' (not allowed in Termux build)"
fi

if grep -q "sudo " "$FILE"; then
    echo "❌ FAIL : sudo usage detected"
    FAIL=1
fi

if grep -q "apt install" "$FILE"; then
    echo "⚠️  WARN : apt install found (use pkg install instead)"
fi

# ---------- RESULT ----------
echo "-------------------------------------------------"

if [[ "$FAIL" -eq 1 ]]; then
    echo "❌ VALIDATION FAILED"
    exit 1
else
    echo "✅ VALIDATION PASSED"
    exit 0
fi
