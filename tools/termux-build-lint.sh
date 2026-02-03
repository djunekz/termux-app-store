#!/usr/bin/env bash
set -eo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT_DIR/tools/validate-build.sh"
PKG_DIR="$ROOT_DIR/packages"

TARGET="${1:-}"

if [[ -z "$TARGET" ]]; then
    echo "Usage:"
    echo "  termux-build lint packages/foo/build.sh"
    echo "  termux-build lint foo"
    echo "  termux-build lint all"
    exit 2
fi

if [[ "$TARGET" == "all" ]]; then
    FAIL=0
    for BUILD in "$PKG_DIR"/*/build.sh; do
        echo
        if ! bash "$VALIDATOR" "$BUILD"; then
            FAIL=1
        fi
    done
    exit $FAIL
fi

# ---------- by package name ----------
if [[ -d "$PKG_DIR/$TARGET" ]]; then
    exec bash "$VALIDATOR" "$PKG_DIR/$TARGET/build.sh"
fi

# ---------- by direct path ----------
if [[ -f "$TARGET" ]]; then
    exec bash "$VALIDATOR" "$TARGET"
fi

echo "❌ ERROR: Invalid target: $TARGET"
exit 2
