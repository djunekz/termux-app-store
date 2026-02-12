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
# Only flatten if there is exactly ONE subdir AND no files at top level.
# Handles tarballs like project-1.0/ (flatten ok).
# Keeps flat tarballs like impulse (impulse.py + tools/) as-is.
_SUBDIRS=$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d | wc -l)
_TOPFILES=$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type f | wc -l)
if [[ "$_SUBDIRS" -eq 1 && "$_TOPFILES" -eq 0 ]]; then
    SUBDIR="$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d | head -n1)"
    SRC_ROOT="$SUBDIR"
fi
echo "[*] Source root: $SRC_ROOT"

# ---------------- ENV ----------------
export TERMUX_PREFIX="$PREFIX"
export TERMUX_PKG_SRCDIR="$SRC_ROOT"
export DESTDIR="$WORK_DIR/pkg"

# ---------------- INSTALL ----------------
echo "==> Running install (DESTDIR)..."

if [[ -n "$PREBUILT_DEB" ]]; then
    # ── Prebuilt .deb ──
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
    # ── Rust source ──
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

elif declare -f termux_step_make_install > /dev/null 2>&1; then
    # ── Custom install function defined in build.sh ──
    echo "[*] Custom termux_step_make_install() found, running..."

    # Keep TERMUX_PREFIX as the REAL prefix.
    # Some functions embed it as a literal string inside generated wrapper
    # scripts (e.g. impulse), so overriding it would produce broken paths.
    # We install directly to real prefix, then mirror to staging for dpkg-deb.
    export TERMUX_PREFIX="$PREFIX"

    cd "$TERMUX_PKG_SRCDIR"
    termux_step_make_install
    cd "$ROOT_DIR"

    # Mirror installed files into staging dir for dpkg-deb
    echo "[*] Staging installed files..."
    mkdir -p "$WORK_DIR/pkg$PREFIX/bin" "$WORK_DIR/pkg$PREFIX/lib"
    [[ -f "$PREFIX/bin/$PACKAGE" ]] && \
        install -Dm755 "$PREFIX/bin/$PACKAGE" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
    [[ -d "$PREFIX/lib/$PACKAGE" ]] && \
        cp -r "$PREFIX/lib/$PACKAGE" "$WORK_DIR/pkg$PREFIX/lib/"
    [[ -d "$PREFIX/share/doc/$PACKAGE" ]] && \
        mkdir -p "$WORK_DIR/pkg$PREFIX/share/doc" && \
        cp -r "$PREFIX/share/doc/$PACKAGE" "$WORK_DIR/pkg$PREFIX/share/doc/"

    echo "[✔] Custom install completed."

else
    # ── Auto language detection (fallback) ──

    # Search order:
    # 1. File named exactly $PACKAGE (any extension) at SRC_ROOT level
    # 2. Executable file at SRC_ROOT level
    # 3. .py file at SRC_ROOT level
    # 4. .sh file at SRC_ROOT level
    # 5. File named $PACKAGE anywhere in the full src tree (handles
    #    flat tarballs where SRC_ROOT was NOT flattened, e.g. impulse
    #    has impulse.py at WORK_DIR/src alongside tools/)

    # The real extract root (one level above SRC_ROOT if it was flattened)
    EXTRACT_ROOT="$WORK_DIR/src"

    MAIN_FILE=""
    # Try SRC_ROOT first
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT" -maxdepth 1 -type f -name "$PACKAGE.py" | head -n1 || true)"
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT" -maxdepth 1 -type f -name "$PACKAGE" -perm /111 | head -n1 || true)"
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT" -maxdepth 1 -type f -perm /111 | head -n1 || true)"
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT" -maxdepth 1 -type f -name "*.py" | head -n1 || true)"
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT" -maxdepth 1 -type f -name "*.sh" | head -n1 || true)"
    # Widen search to full extract root (catches impulse.py sitting above tools/)
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$EXTRACT_ROOT" -maxdepth 2 -type f -name "$PACKAGE.py" | head -n1 || true)"
    [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$EXTRACT_ROOT" -maxdepth 2 -type f -name "$PACKAGE" | head -n1 || true)"

    if [[ -n "$MAIN_FILE" ]]; then
        BASENAME="$(basename "$MAIN_FILE")"
        # Copy from the directory that contains the entry file
        # so sibling files/dirs (e.g. tools/) are included
        COPY_ROOT="$(dirname "$MAIN_FILE")"

        mkdir -p "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE"
        cp -r "$COPY_ROOT"/. "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE/"

        mkdir -p "$WORK_DIR/pkg/$PREFIX/bin"
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
