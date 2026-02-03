#!/usr/bin/env bash
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT/tools/validate-build.sh"

FAIL=0

echo "🔍 Checking all packages..."
echo "================================"

for BUILD in "$ROOT/packages"/*/build.sh; do
    PKG="$(basename "$(dirname "$BUILD")")"
    echo
    echo "📦 $PKG"
    if ! bash "$VALIDATOR" "$BUILD"; then
        FAIL=1
    fi
done

if [[ $FAIL -eq 0 ]]; then
    echo
    echo "✅ PR looks good"
else
    echo
    echo "❌ PR has issues"
fi

exit $FAIL
