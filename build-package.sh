#!/usr/bin/env bash
set -e

PACKAGE="$1"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGES_DIR="$ROOT_DIR/packages"
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BUILD_DIR="$PACKAGES_DIR/$PACKAGE"
WORK_DIR="$ROOT_DIR/build/$PACKAGE"
DEB_DIR="$ROOT_DIR/output"

if [[ -z "$PACKAGE" ]]; then
    echo "Usage: $0 <package-name>"
    exit 1
fi

BUILD_SH="$BUILD_DIR/build.sh"
[[ -f "$BUILD_SH" ]] || { echo "build.sh not found"; exit 1; }

# ---------------- LOAD METADATA ----------------
# shellcheck disable=SC1090
source "$BUILD_SH"

# ---------------- ARCH ----------------
case "$(uname -m)" in
    aarch64) ARCH="aarch64" ;;
    armv7l)  ARCH="arm" ;;
    x86_64)  ARCH="x86_64" ;;
    i686)    ARCH="i686" ;;
    *) echo "Unsupported arch"; exit 1 ;;
esac
echo "==> Architecture detected: $ARCH"

# ---------------- DEPS ----------------
echo "==> Installing dependencies..."
[[ -n "${TERMUX_PKG_DEPENDS:-}" ]] && pkg install -y $(tr ',' ' ' <<<"$TERMUX_PKG_DEPENDS")

# ---------------- DIRS ----------------
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR/src" "$WORK_DIR/pkg" "$DEB_DIR"

# ---------------- DOWNLOAD ----------------
echo "==> Downloading source..."
SRC_FILE="$WORK_DIR/source"
curl -fL "$TERMUX_PKG_SRCURL" -o "$SRC_FILE"

# ---------------- SHA256 (STRICT VALIDATION) ----------------
if [[ -n "${TERMUX_PKG_SHA256:-}" ]]; then
    echo "==> Verifying SHA256..."
    CALC_SHA256="$(sha256sum "$SRC_FILE" | awk '{print $1}')"
    if [[ "$CALC_SHA256" != "$TERMUX_PKG_SHA256" ]]; then
        echo "[FATAL] SHA256 mismatch!"
        echo "Expected: $TERMUX_PKG_SHA256"
        echo "Got     : $CALC_SHA256"
        rm -f "$SRC_FILE"
        exit 1
    fi
    echo "[✔] SHA256 valid"
fi
# ---------------- EXTRACT ----------------
echo "==> Extracting source..."
if [[ "$TERMUX_PKG_SRCURL" == *.zip ]]; then
    unzip -q "$SRC_FILE" -d "$WORK_DIR/src"
else
    tar -xf "$SRC_FILE" -C "$WORK_DIR/src"
fi

SRC_ROOT="$(find "$WORK_DIR/src" -mindepth 1 -maxdepth 1 -type d | head -n1)"
mv "$SRC_ROOT" "$WORK_DIR/src/root"

# ---------------- ENV ----------------
export TERMUX_PREFIX="$PREFIX"
export TERMUX_PKG_SRCDIR="$WORK_DIR/src/root"
export DESTDIR="$WORK_DIR/pkg"

# ---------------- INSTALL ----------------
echo "==> Running install (DESTDIR)..."
termux_step_make_install

# ---------------- CONTROL ----------------
CONTROL_DIR="$WORK_DIR/pkg/DEBIAN"
mkdir -p "$CONTROL_DIR"
chmod 0755 "$CONTROL_DIR"

cat > "$CONTROL_DIR/control" <<EOF
Package: $PACKAGE
Version: $TERMUX_PKG_VERSION
Architecture: $ARCH
Maintainer: ${TERMUX_PKG_MAINTAINER:-unknown}
Depends: ${TERMUX_PKG_DEPENDS:-}
Description: ${TERMUX_PKG_DESCRIPTION:-No description}
Homepage: ${TERMUX_PKG_HOMEPAGE:-}
EOF

chmod 0644 "$CONTROL_DIR/control"

# ---------------- BUILD DEB ----------------
DEB_FILE="$DEB_DIR/${PACKAGE}_${TERMUX_PKG_VERSION}_${ARCH}.deb"
echo "==> Building deb: $(basename "$DEB_FILE")"
dpkg-deb --build "$WORK_DIR/pkg" "$DEB_FILE"

# ---------------- INSTALL ----------------
echo "==> Installing package..."
dpkg -i "$DEB_FILE"

echo "==> DONE: $PACKAGE installed"
