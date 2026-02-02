#!/usr/bin/env bash
set -e

PACKAGE="$1"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGES_DIR="$ROOT_DIR/packages"
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BUILD_DIR="$PACKAGES_DIR/$PACKAGE"
WORK_DIR="$ROOT_DIR/build/$PACKAGE"
DEB_DIR="$ROOT_DIR/output"
CACHE_DIR="$ROOT_DIR/cache"

if [[ -z "$PACKAGE" ]]; then
    echo "Usage: $0 <package-name>"
    exit 1
fi

BUILD_SH="$BUILD_DIR/build.sh"
[[ -f "$BUILD_SH" ]] || { echo "build.sh not found"; exit 1; }

# ---------------- LOAD METADATA ----------------
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
mkdir -p "$WORK_DIR/src" "$WORK_DIR/pkg" "$DEB_DIR" "$CACHE_DIR"

# ---------------- DOWNLOAD ----------------
echo "==> Downloading source..."
SRC_FILE="$CACHE_DIR/${PACKAGE}_$(basename "$TERMUX_PKG_SRCURL")"
if [[ ! -f "$SRC_FILE" ]]; then
    curl -fL "$TERMUX_PKG_SRCURL" -o "$SRC_FILE"
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
SRC_DEST="$WORK_DIR/src"

if [[ "$SRC_FILE" == *.deb ]]; then
    echo "[*] Source is a .deb package, skipping extraction."
elif [[ "$SRC_FILE" == *.zip ]]; then
    unzip -q "$SRC_FILE" -d "$SRC_DEST"
else
    tar -xf "$SRC_FILE" -C "$SRC_DEST"
fi

# Tentukan SRC_ROOT
SRC_ROOT_CANDIDATES=( $(find "$SRC_DEST" -mindepth 1 -maxdepth 1 -type d) )
if [[ ${#SRC_ROOT_CANDIDATES[@]} -eq 1 ]]; then
    SRC_ROOT="${SRC_ROOT_CANDIDATES[0]}"
else
    SRC_ROOT="$SRC_DEST"
fi

export TERMUX_PKG_SRCDIR="$SRC_ROOT"
echo "[*] Source root: $TERMUX_PKG_SRCDIR"

# ---------------- ENV ----------------
export TERMUX_PREFIX="$PREFIX"
DESTDIR="$WORK_DIR/pkg"

# ---------------- INSTALL ----------------
if [[ "$SRC_FILE" == *.deb ]]; then
    echo "[*] Installing binary from .deb..."
    dpkg -x "$SRC_FILE" "$DESTDIR"
elif [[ -f "$SRC_ROOT/Cargo.toml" ]]; then
    echo "[*] Rust project detected, building with cargo..."
    cargo build --release
    BIN_NAME="${PACKAGE}"  # bisa diubah jika nama binary beda
    mkdir -p "$DESTDIR/bin"
    install -Dm700 "target/release/$BIN_NAME" "$DESTDIR/bin/$BIN_NAME"
else
    if declare -f termux_step_make_install >/dev/null 2>&1; then
        echo "==> Running install (DESTDIR)..."
        termux_step_make_install
    else
        echo "[!] No install method found, skipping."
    fi
fi

# ---------------- CONTROL ----------------
CONTROL_DIR="$DESTDIR/DEBIAN"
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
dpkg-deb --build "$DESTDIR" "$DEB_FILE"

# ---------------- INSTALL ----------------
echo "==> Installing package..."
dpkg -i "$DEB_FILE"

echo "==> DONE: $PACKAGE installed"
