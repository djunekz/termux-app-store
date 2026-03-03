#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

APP_NAME="termux-app-store"
REPO="djunekz/termux-app-store"
VERSION="latest"
INSTALL_DIR="$PREFIX/lib/.tas"
BIN_DIR="$PREFIX/bin"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

R='\033[0m'
B='\033[1m'
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
DIM='\033[2m'

die()  { echo -e "${RED}[✗] $*${R}" >&2; exit 1; }
info() { echo -e "${CYAN}[*] $*${R}"; }
ok()   { echo -e "${GREEN}[✓] $*${R}"; }
warn() { echo -e "${YELLOW}[!] $*${R}"; }

strip_ansi() {
  echo "$1" | sed 's/\x1b\[[0-9;]*[mGKHf]//g'
}

export TERMUX_APP_STORE_MODE=local
export TERMUX_APP_STORE_HOME=$(pwd)
check_termux() {
  command -v pkg >/dev/null 2>&1 || die "This installer must be run inside Termux"
  ok "Running in Termux environment"
}

install_dep() {
  local dep="$1"
  if command -v "$dep" >/dev/null 2>&1; then
    ok "Dependency satisfied: $dep"
  else
    info "Installing: $dep"
    pkg install -y "$dep" || die "Failed to install $dep"
    ok "$dep installed"
  fi
}

detect_arch() {
  local arch; arch="$(uname -m)"
  case "$arch" in
    aarch64)       BIN_ARCH="aarch64" ;;
    armv7l|armv8l) BIN_ARCH="arm" ;;
    x86_64)        BIN_ARCH="x86_64" ;;
    i686)          BIN_ARCH="i686" ;;
    *) die "Unsupported architecture: $arch" ;;
  esac
  ok "Architecture: ${B}$arch${R}"
}

detect_mode() {
  if [[ -f "$SCRIPT_DIR/termux_app_store_cli.py" ]] && \
     [[ -f "$SCRIPT_DIR/termux_app_store.py" ]]    && \
     [[ -f "$SCRIPT_DIR/tools/package_manager.py" ]]; then
    INSTALL_MODE="source"
    ok "Installation mode: ${B}Source${R}"
  else
    INSTALL_MODE="binary"
    ok "Installation mode: ${B}Binary${R}"
  fi
}

detect_version() {
  local ver=""

  for f in "$INSTALL_DIR/termux_app_store_cli.py" "$INSTALL_DIR/termux_app_store.py" \
           "$SCRIPT_DIR/termux_app_store_cli.py" "$SCRIPT_DIR/termux_app_store.py"; do
    if [[ -f "$f" ]]; then
      ver=$(grep -oP 'APP_VERSION\s*=\s*"\K[0-9.]+' "$f" 2>/dev/null | head -1 || echo "")

      if [[ -z "$ver" ]]; then
        ver=$(awk -F'"' '/APP_VERSION.*=/{print $2; exit}' "$f" 2>/dev/null || echo "")
      fi

      if [[ -z "$ver" ]]; then
        ver=$(sed -n 's/.*APP_VERSION.*=.*"\([0-9.]*\)".*/\1/p' "$f" 2>/dev/null | head -1 || echo "")
      fi

      if [[ -n "$ver" ]] && [[ "$ver" != "unknown" ]]; then
        break
      fi
    fi
  done

  if [[ -z "$ver" ]] || [[ "$ver" == "unknown" ]]; then
    ver="0.1.4"
  fi

  echo "$ver"
}

check_existing() {
  [[ -f "$BIN_DIR/$APP_NAME" ]] || return 0

  warn "Existing installation found"

  local current
  current=$(detect_version)

  echo -e "  Current version : ${B}v$current${R}"

  echo -n "  Overwrite? [Y/n]: "
  read -r resp
  case "$resp" in
    [nN]|[nN][oO]) die "Installation cancelled" ;;
  esac
}

cleanup() {
  info "Cleaning up old installation..."
  rm -rf  "$INSTALL_DIR"
  rm -f   "$BIN_DIR/$APP_NAME"
}

install_source() {
  if ! command -v python3 >/dev/null 2>&1; then
    info "Installing Python3..."
    pkg install -y python || die "Failed to install Python3"
  fi
  ok "Python: $(python3 --version 2>&1 | awk '{print $2}')"

  if ! python3 -c "import textual" >/dev/null 2>&1; then
    info "Installing Textual..."
    pip install textual --break-system-packages || die "Failed to install Textual"
  fi
  ok "Textual: v$(python3 -c "import textual; print(textual.__version__)" 2>/dev/null)"

  info "Copying files to $INSTALL_DIR ..."
  mkdir -p "$INSTALL_DIR"
  cp "$SCRIPT_DIR/termux_app_store_cli.py"  "$INSTALL_DIR/"
  cp "$SCRIPT_DIR/termux_app_store.py"       "$INSTALL_DIR/"

  if [[ -d "$SCRIPT_DIR/packages" ]]; then
    cp -r "$SCRIPT_DIR/packages" "$INSTALL_DIR/"
    ok "Packages directory copied (local build mode enabled)"
  fi

  if [[ -f "$SCRIPT_DIR/build-package.sh" ]]; then
    cp "$SCRIPT_DIR/build-package.sh" "$INSTALL_DIR/"
  fi

  ok "Files copied"
}

install_binary() {
  install_dep "curl"
  install_dep "file"

  mkdir -p "$INSTALL_DIR"

  local bin_name="termux-app-store-${BIN_ARCH}"
  local url="https://github.com/$REPO/releases/$VERSION/download/$bin_name"
  local target="$INSTALL_DIR/$APP_NAME.bin"

  info "Downloading ${B}$bin_name${R}..."

  curl -fL --progress-bar --retry 3 --retry-delay 2 "$url" -o "$target" 2>&1 || {
    warn "Binary download failed, falling back to source install"
    INSTALL_MODE="source"
    install_source
    return
  }

  file "$target" | grep -q ELF || die "Downloaded file is not a valid ELF binary"

  chmod +x "$target"
  ok "Binary downloaded and validated"
}


create_wrapper() {
  info "Creating wrapper script..."

  if [[ "$INSTALL_MODE" == "source" ]]; then
    CLI_SCRIPT="$INSTALL_DIR/termux_app_store_cli.py"
    TUI_SCRIPT="$INSTALL_DIR/termux_app_store.py"
  else
    CLI_SCRIPT="$INSTALL_DIR/$APP_NAME.bin"
    TUI_SCRIPT="$INSTALL_DIR/$APP_NAME.bin"
  fi

  local ver
  ver=$(detect_version)

  cat > "$BIN_DIR/$APP_NAME" << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# termux-app-store — auto-generated wrapper
# DO NOT EDIT — regenerated by install.sh

EOF

  echo "export TERMUX_APP_STORE_VERSION=\"$ver\"" >> "$BIN_DIR/$APP_NAME"
  echo "export TERMUX_APP_STORE_HOME=\"$INSTALL_DIR\"" >> "$BIN_DIR/$APP_NAME"
  echo "" >> "$BIN_DIR/$APP_NAME"

  if [[ "$INSTALL_MODE" == "source" ]]; then
    cat >> "$BIN_DIR/$APP_NAME" << EOF
if [ \$# -eq 0 ]; then
    exec python3 "$TUI_SCRIPT"
else
    exec python3 "$CLI_SCRIPT" "\$@"
fi
EOF
  else
    echo "exec \"$CLI_SCRIPT\" \"\$@\"" >> "$BIN_DIR/$APP_NAME"
  fi

  chmod +x "$BIN_DIR/$APP_NAME"
  ok "Wrapper created: $BIN_DIR/$APP_NAME"
}

show_done() {
  local ver
  ver=$(detect_version)

  echo ""
  echo -e "${GREEN}${B}╔══════════════════════════════════════════╗${R}"
  echo -e "${GREEN}${B}║   Installation Completed Successfully!   ║${R}"
  echo -e "${GREEN}${B}╚══════════════════════════════════════════╝${R}"
  echo ""
  echo -e "${CYAN}Details:${R}"
  echo -e "  Version   : ${B}v${ver}${R}"
  echo -e "  Mode      : ${B}${INSTALL_MODE}${R}"
  echo -e "  Installed : ${DIM}$BIN_DIR/$APP_NAME${R}"
  echo ""
  echo -e "${CYAN}Commands:${R}"
  echo -e "  ${B}$APP_NAME${R}                ${DIM}→ Open TUI${R}"
  echo -e "  ${B}$APP_NAME list${R}            ${DIM}→ List packages${R}"
  echo -e "  ${B}$APP_NAME install <pkg>${R}   ${DIM}→ Install a package${R}"
  echo -e "  ${B}$APP_NAME update${R}          ${DIM}→ Check for updates${R}"
  echo -e "  ${B}$APP_NAME upgrade${R}         ${DIM}→ Upgrade all${R}"
  echo -e "  ${B}$APP_NAME version${R}         ${DIM}→ Show version${R}"
  echo ""
}

main() {
  echo ""
  echo -e "${CYAN}${B}╔═════════════════════════════════════════════╗${R}"
  echo -e "${CYAN}${B}║         Termux App Store Installer          ║${R}"
  echo -e "${CYAN}${B}║ https://github.com/djunekz/termux-app-store ║${R}"
  echo -e "${CYAN}${B}║               by @djunekz                   ║${R}"
  echo -e "${CYAN}${B}╚═════════════════════════════════════════════╝${R}"
  echo ""

  check_termux
  detect_arch
  detect_mode
  check_existing
  echo ""
  cleanup

  if [[ "$INSTALL_MODE" == "source" ]]; then
    install_source
  else
    install_binary
  fi

  create_wrapper
  show_done
}

trap 'echo ""; die "Installation failed at line $LINENO"' ERR

main "$@"
