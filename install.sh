#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

# =========================================================
# Termux App Store — Installer
# =========================================================

APP_NAME="termux-app-store"
REPO="djunekz/termux-app-store"
VERSION="latest"
INSTALL_DIR="$PREFIX/lib/.tas"
BIN_DIR="$PREFIX/bin"

# ---------------- UTIL ----------------
die() {
  echo "[!] $*" >&2
  exit 1
}

info() {
  echo "[*] $*"
}

ok() {
  echo "[✓] $*"
}

warn() {
  echo "[!] $*"
}

# ---------------- PRECHECK ----------------
info "Preparing environment"

if ! command -v pkg >/dev/null 2>&1; then
  die "This installer must be run inside Termux"
fi

# curl
if command -v curl >/dev/null 2>&1; then
  ok "Dependency satisfied: curl"
else
  info "Installing dependency: curl"
  pkg install -y curl || die "Failed to install curl"
  ok "curl installed"
fi

# file
if command -v file >/dev/null 2>&1; then
  ok "Dependency satisfied: file"
else
  info "Installing dependency: file"
  pkg install -y file || die "Failed to install file"
  ok "file installed"
fi

# ---------------- ARCH DETECTION ----------------
ARCH="$(uname -m)"
case "$ARCH" in
  aarch64) BIN="termux-app-store-aarch64" ;;
  armv7l|armv8l) BIN="termux-app-store-arm" ;;
  x86_64) BIN="termux-app-store-x86_64" ;;
  i686) BIN="termux-app-store-i686" ;;
  *)
    die "Unsupported architecture: $ARCH"
    ;;
esac
ok "Architecture detected: $ARCH"

# ---------------- RUNTIME NOTES ----------------
echo
info "Runtime information"
echo "  • This installation uses a prebuilt binary"
echo "  • Python/Textual are NOT required to run"
echo "  • Python is only needed for development or source builds"

# ---------------- OPTIONAL DEV DEP CHECK ----------------
echo
info "Optional development environment check"

# Python
if command -v python3 >/dev/null 2>&1 || command -v python >/dev/null 2>&1; then
  PY_VER="$(python3 --version 2>/dev/null || python --version)"
  ok "Python detected: $PY_VER"
else
  warn "Python not found (skipped — not required)"
fi

# Textual
if python3 - <<'EOF' >/dev/null 2>&1
import textual
EOF
then
  TXT_VER="$(python3 - <<'EOF'
import textual
print(textual.__version__)
EOF
)"
  ok "Textual detected: v$TXT_VER"
else
  warn "Textual not found (skipped — not required)"
fi

# ---------------- INSTALL ----------------
mkdir -p "$INSTALL_DIR"

URL="https://github.com/$REPO/releases/$VERSION/download/$BIN"
TARGET="$INSTALL_DIR/$APP_NAME"

echo
info "Downloading Termux App Store binary"
echo "  → $URL"

curl -fL --retry 3 --retry-delay 2 "$URL" -o "$TARGET" \
  || die "Download failed"

# ---------------- VALIDATION ----------------
if file "$TARGET" | grep -q ELF; then
  ok "Binary validation passed (ELF)"
else
  die "Downloaded file is not a valid ELF binary"
fi

chmod +x "$TARGET"
ln -sf "$TARGET" "$BIN_DIR/$APP_NAME"

ok "Binary installed successfully"

# ---------------- POST INSTALL ----------------
echo
ok "Installation completed!"
echo "→ Run with: $APP_NAME"

echo
info "Usage notes"
echo "  • Re-run this installer to update"
echo "  • For development mode:"
echo "      pkg install python"
echo "      pip install textual"
