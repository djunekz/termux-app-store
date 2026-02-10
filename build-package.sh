#!/usr/bin/env bash
# Dont edit or delete this file
# Termux App Store Official
# Developer: Djunekz
# https://github.com/djunekz/termux-app-store

set -euo pipefail

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
[[ -f "$BUILD_SH" ]] || { echo "[FATAL] build.sh not found for $PACKAGE"; exit 1; }

# ---------------- LOAD METADATA ----------------
source "$BUILD_SH"

# ---------------- ARCH ----------------
case "$(uname -m)" in
    aarch64) ARCH="aarch64" ;;
    armv7l)  ARCH="arm" ;;
    x86_64)  ARCH="x86_64" ;;
    i686)    ARCH="i686" ;;
    *) echo "[FATAL] Unsupported arch"; exit 1 ;;
esac
echo "==> Architecture detected: $ARCH"

# ---------------- DEPS ----------------
echo "==> Installing dependencies..."
[[ -n "${TERMUX_PKG_DEPENDS:-}" ]] && pkg install -y $(tr ',' ' ' <<<"$TERMUX_PKG_DEPENDS")

# ---------------- CLEAN / DIRS ----------------
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR/src" "$WORK_DIR/pkg" "$DEB_DIR"

# ---------------- DOWNLOAD ----------------
echo "==> Downloading source..."
SRC_FILE="$WORK_DIR/source"
curl -fL "$TERMUX_PKG_SRCURL" -o "$SRC_FILE"

# ---------------- SHA256 ----------------
if [[ -n "${TERMUX_PKG_SHA256:-}" ]]; then
    echo "==> Verifying SHA256..."
    CALC_SHA256="$(sha256sum "$SRC_FILE" | awk '{print $1}')"
    if [[ "$CALC_SHA256" != "$TERMUX_PKG_SHA256" ]]; then
        echo "[FATAL] SHA256 mismatch!"
        exit 1
    fi
    echo "[✔] SHA256 valid"
fi

# ---------------- EXTRACT ----------------
echo "==> Extracting source..."
PREBUILT_DEB=""
SRC_ROOT="$WORK_DIR/src"

if [[ "$TERMUX_PKG_SRCURL" == *.deb ]]; then
    echo "[*] Prebuilt .deb detected, skipping extraction."
    PREBUILT_DEB="$SRC_FILE"
elif [[ "$TERMUX_PKG_SRCURL" == *.zip ]]; then
    unzip -q "$SRC_FILE" -d "$SRC_ROOT"
else
    tar -xf "$SRC_FILE" -C "$SRC_ROOT"
fi

# ---------------- FLATTEN ----------------
SUBDIR="$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d | head -n1)"
[[ -n "$SUBDIR" ]] && SRC_ROOT="$SUBDIR"
echo "[*] Source root: $SRC_ROOT"

# ---------------- ENV ----------------
export TERMUX_PREFIX="$PREFIX"
export TERMUX_PKG_SRCDIR="$SRC_ROOT"
export DESTDIR="$WORK_DIR/pkg"

# ---------------- INSTALL ----------------
echo "==> Running install (DESTDIR)..."

if [[ -n "$PREBUILT_DEB" ]]; then
    echo "[*] Installing prebuilt .deb..."
    dpkg -x "$PREBUILT_DEB" "$WORK_DIR/pkg"
    BIN_FILE="$(find "$WORK_DIR/pkg" -type f -name "$PACKAGE*" -executable | head -n1 || true)"
    if [[ -n "$BIN_FILE" ]]; then
        mkdir -p "$PREFIX/lib/$PACKAGE"
        mv "$BIN_FILE" "$PREFIX/lib/$PACKAGE/$PACKAGE"
        chmod +x "$PREFIX/lib/$PACKAGE/$PACKAGE"

        cat > "$PREFIX/bin/$PACKAGE" <<EOF
#!/usr/bin/env bash
exec "$PREFIX/lib/$PACKAGE/$PACKAGE" "\$@"
EOF
        chmod +x "$PREFIX/bin/$PACKAGE"
        echo "[✔] $PACKAGE installed and executable at $PREFIX/bin/$PACKAGE"
    fi

elif [[ -f "$SRC_ROOT/Cargo.toml" ]]; then
    echo "[*] Rust source detected, building..."
    case "$ARCH" in
        aarch64) RUST_TARGET="aarch64-linux-android" ;;
        arm)     RUST_TARGET="armv7-linux-androideabi" ;;
        x86_64)  RUST_TARGET="x86_64-linux-android" ;;
        i686)    RUST_TARGET="i686-linux-android" ;;
    esac
    cargo build --release --target "$RUST_TARGET" --manifest-path "$SRC_ROOT/Cargo.toml"
    BIN_PATH="$SRC_ROOT/target/$RUST_TARGET/release/$PACKAGE"
    [[ -f "$BIN_PATH" ]] || { echo "[FATAL] Binary not found: $BIN_PATH"; exit 1; }
    install -Dm755 "$BIN_PATH" "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE"

else
    # ---------------- AUTO LANGUAGE DETECTION ----------------
    MAIN_FILE="$(find "$SRC_ROOT" -maxdepth 1 -type f -perm /111 | head -n1 || true)"

    # if no executable, check for Python
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT" -maxdepth 1 -type f -name '*.py' | head -n1 || true)"

    if [[ -n "$MAIN_FILE" ]]; then
        BASENAME="$(basename "$MAIN_FILE")"
        mkdir -p "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE"
        cp "$SRC_ROOT"/* "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE/" 2>/dev/null || true
        chmod +x "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE/$BASENAME"

        mkdir -p "$WORK_DIR/pkg/$PREFIX/bin"
        # detect interpreter
        FIRST_LINE="$(head -n1 "$MAIN_FILE")"
        if [[ "$FIRST_LINE" =~ ^#! ]]; then
            INTERPRETER=$(awk '{print $1}' <<<"$FIRST_LINE" | sed 's|#!||')
        elif [[ "$MAIN_FILE" == *.py ]]; then
            INTERPRETER="python3"
        else
            INTERPRETER="bash"
        fi

        cat > "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE" <<EOF
#!/usr/bin/env bash
exec $INTERPRETER "$PREFIX/lib/$PACKAGE/$BASENAME" "\$@"
EOF
        chmod +x "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE"
        echo "[✔] Wrapper created: $PREFIX/bin/$PACKAGE -> $INTERPRETER"
    else
        echo "[!] No executable/main file found in $SRC_ROOT, skipping install."
    fi
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

# ---------------- INSTALL DEB ----------------
echo "==> Installing package..."
dpkg -i "$DEB_FILE"

echo "==> DONE: $PACKAGE installed"
