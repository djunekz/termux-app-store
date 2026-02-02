#!/usr/bin/env bash
set -euo pipefail

PACKAGE="$1"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGES_DIR="$ROOT_DIR/packages"
CACHE_DIR="$ROOT_DIR/cache"
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BUILD_DIR="$PACKAGES_DIR/$PACKAGE"
WORK_DIR="$ROOT_DIR/build/$PACKAGE"
DEB_DIR="$ROOT_DIR/output"
TMP_DIR="$HOME/tmp"

mkdir -p "$TMP_DIR" "$CACHE_DIR"

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
SRC_FILE="$CACHE_DIR/${PACKAGE}_$(basename $TERMUX_PKG_SRCURL)"
if [[ ! -f "$SRC_FILE" ]]; then
    curl -fL --progress-bar "$TERMUX_PKG_SRCURL" -o "$SRC_FILE"
else
    echo "[*] Using cached source: $SRC_FILE"
fi

# ---------------- SHA256 ----------------
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
if [[ "$TERMUX_PKG_SRCURL" == *.deb ]]; then
    echo "[*] Source is .deb, skipping extraction."
    SRC_ROOT="$SRC_FILE"
else
    mkdir -p "$WORK_DIR/src"
    if [[ "$TERMUX_PKG_SRCURL" == *.zip ]]; then
        unzip -q "$SRC_FILE" -d "$WORK_DIR/src"
    else
        tar -xf "$SRC_FILE" -C "$WORK_DIR/src"
    fi

    # Tentukan SRC_ROOT
    FOLDER_COUNT=$(find "$WORK_DIR/src" -mindepth 1 -maxdepth 1 -type d | wc -l)
    if [[ "$FOLDER_COUNT" -eq 1 ]]; then
        SRC_ROOT="$(find "$WORK_DIR/src" -mindepth 1 -maxdepth 1 -type d | head -n1)"
        mv "$SRC_ROOT" "$WORK_DIR/src/root"
        SRC_ROOT="$WORK_DIR/src/root"
    else
        # Bisa jadi tar hanya file tunggal
        SRC_FILE_ONLY=$(find "$WORK_DIR/src" -mindepth 1 -maxdepth 1 ! -type d | head -n1)
        if [[ -n "$SRC_FILE_ONLY" ]]; then
            mkdir -p "$WORK_DIR/src/root"
            mv "$SRC_FILE_ONLY" "$WORK_DIR/src/root/"
            SRC_ROOT="$WORK_DIR/src/root"
        else
            # fallback: ambil semua isi src
            SRC_ROOT="$WORK_DIR/src"
        fi
    fi
fi

# ---------------- ENV ----------------
export TERMUX_PREFIX="$PREFIX"
export TERMUX_PKG_SRCDIR="$WORK_DIR/src/root"
export DESTDIR="$WORK_DIR/pkg"

# ---------------- INSTALL ----------------
if [[ "$TERMUX_PKG_SRCURL" == *.deb ]]; then
    echo "[*] Installing binary from .deb..."
    TMP_EXTRACT="$TMP_DIR/debcheck_$PACKAGE"
    rm -rf "$TMP_EXTRACT"
    mkdir -p "$TMP_EXTRACT"
    dpkg-deb -x "$SRC_FILE" "$TMP_EXTRACT"

    # Copy binaries
    BIN_DIR="$TMP_EXTRACT/data/data/com.termux/files/usr/bin"
    if [[ -d "$BIN_DIR" ]]; then
        for BIN in "$BIN_DIR"/*; do
            cp "$BIN" "$PREFIX/bin/"
            chmod +x "$PREFIX/bin/$(basename "$BIN")"
            echo "[✔] Installed binary: $PREFIX/bin/$(basename "$BIN")"
        done
    else
        echo "[!] Warning: No binaries directory found in .deb"
    fi

    # Copy Python libs
    PY_LIB_DIR="$TMP_EXTRACT/data/data/com.termux/files/usr/lib/python3.12"
    if [[ -d "$PY_LIB_DIR" ]]; then
        mkdir -p "$PREFIX/lib/python3.12"
        cp -r "$PY_LIB_DIR/"* "$PREFIX/lib/python3.12/"
        echo "[✔] Installed Python libraries"
    fi

else
    echo "==> Running install (DESTDIR)..."
    termux_step_make_install
fi

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
echo "[*] Cached sources: $SRC_FILE"
echo "==> DONE: $PACKAGE installed"
