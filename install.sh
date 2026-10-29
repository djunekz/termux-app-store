#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

readonly OFFICIAL_REPO="djunekz/termux-app-store"
readonly OFFICIAL_API="https://api.github.com/repos/djunekz/termux-app-store/releases/latest"
readonly OFFICIAL_RELEASE_BASE="https://github.com/djunekz/termux-app-store/releases/download"
readonly OFFICIAL_URL="https://github.com/djunekz/termux-app-store"

APP_NAME="termux-app-store"
CURL_SEC=(--proto '=https' --tlsv1.2)
ALLOW_NO_CHECKSUM="${TAS_ALLOW_NO_CHECKSUM:-0}"
TMP_DIR=""
STAGE_DIR=""
BACKUP_DIR=""
SWAPPED=0
DONE=0
INSTALL_DIR="$PREFIX/lib/.tas"
BIN_DIR="$PREFIX/bin"

R=$'\033[0m'
B=$'\033[1m'
DIM=$'\033[2m'
RED=$'\033[31m'
BRED=$'\033[91m'
BGREEN=$'\033[92m'
BYELLOW=$'\033[93m'
BCYAN=$'\033[96m'

die()  { printf "\n %s[✗]%s %b\n\n" "$BRED$B" "$R" "$*" >&2; exit 1; }
info() { printf " %s[*]%s %s\n" "$BCYAN$B" "$R" "$*"; }
ok()   { printf " %s[✓]%s %s\n" "$BGREEN$B" "$R" "$*"; }
warn() { printf " %s[!]%s %s\n" "$BYELLOW$B" "$R" "$*"; }

show_banner() {
  printf "\n%s╔═════════════════════════════════════════════╗%s\n" "$BCYAN$B" "$R"
  printf   "%s║         Termux App Store Installer          ║%s\n" "$BCYAN$B" "$R"
  printf   "%s║ https://github.com/djunekz/termux-app-store ║%s\n" "$BCYAN$B" "$R"
  printf   "%s║               by @djunekz                   ║%s\n" "$BCYAN$B" "$R"
  printf   "%s╚═════════════════════════════════════════════╝%s\n\n" "$BCYAN$B" "$R"
}

verify_official_release() {
  info "Verifying official release source..."

  local api_full_name
  api_full_name=$(curl "${CURL_SEC[@]}" -fsSL --max-time 15 \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/$OFFICIAL_REPO" 2>/dev/null \
    | grep '"full_name"' \
    | head -1 \
    | sed 's/.*"full_name": *"\([^"]*\)".*/\1/' || true)

  if [[ -z "$api_full_name" ]]; then
    warn "Could not reach GitHub API (offline or rate-limited) — continuing"
    return 0
  fi

  if [[ "${api_full_name,,}" != "${OFFICIAL_REPO,,}" ]]; then
    printf "\n%s INSTALLATION BLOCKED — UNOFFICIAL SOURCE%s\n" "$BRED$B" "$R"
    printf "  Expected : %s\n  Got      : %s\n\n" "$OFFICIAL_REPO" "$api_full_name"
    printf "%sInstall from the official source:%s\n\n" "$BRED$B" "$R"
    printf "%s curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/install.sh | bash %s\n\n" "$BGREEN$B" "$R"
    exit 1
  fi

  ok "Official source verified: ${B}github.com/$OFFICIAL_REPO${R}"
}

check_termux() {
  [[ -n "${PREFIX:-}" ]] && command -v pkg >/dev/null 2>&1 \
    || die "This installer must be run inside Termux"
  ok "Termux environment detected"
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
    aarch64)        ARCH="aarch64" ;;
    armv7l|armv8l)  ARCH="arm"     ;;
    x86_64)         ARCH="x86_64"  ;;
    i686)           ARCH="i686"    ;;
    *) die "Unsupported architecture: $arch" ;;
  esac
  ok "Architecture: ${B}$arch${R}"
}

check_existing() {
  [[ -f "$BIN_DIR/$APP_NAME" ]] || [[ -d "$INSTALL_DIR" ]] || return 0

  warn "Existing installation found"
  local current=""
  [[ -f "$INSTALL_DIR/.installed" ]] && \
    current=$(grep '^version=' "$INSTALL_DIR/.installed" 2>/dev/null | cut -d= -f2 || true)
  [[ -n "$current" ]] && printf "  Installed version : %sv%s%s\n" "$B" "$current" "$R"

  if ! [ -t 0 ]; then
    warn "Running via pipe — auto-overwriting existing installation"
    return 0
  fi

  printf "  Overwrite? [Y/n]: "
  read -r resp </dev/tty
  case "${resp:-Y}" in
    [nN]|[nN][oO]) die "Installation cancelled" ;;
  esac
}

cleanup_tmp() {
  [[ -n "$TMP_DIR" && -d "$TMP_DIR" ]] && rm -rf "$TMP_DIR"
  return 0
}

rollback() {
  [[ "$SWAPPED" == "1" && "$DONE" != "1" && -n "$BACKUP_DIR" ]] || return 0
  warn "Rolling back to previous installation..."
  rm -rf "$INSTALL_DIR"
  rm -f  "$BIN_DIR/$APP_NAME" "$BIN_DIR/tasctl"
  [[ -d "$BACKUP_DIR/lib"     ]] && mv "$BACKUP_DIR/lib" "$INSTALL_DIR"
  [[ -f "$BACKUP_DIR/app"     ]] && mv "$BACKUP_DIR/app" "$BIN_DIR/$APP_NAME"
  if [[ -e "$BACKUP_DIR/tasctl" || -L "$BACKUP_DIR/tasctl" ]]; then
    mv "$BACKUP_DIR/tasctl" "$BIN_DIR/tasctl"
  fi
  return 0
}

download_release() {
  install_dep curl

  info "Fetching latest release tag..."
  local tag
  tag=$(curl "${CURL_SEC[@]}" -fsSL --max-time 20 \
    -H "Accept: application/vnd.github+json" \
    "$OFFICIAL_API" 2>/dev/null \
    | grep '"tag_name"' \
    | head -1 \
    | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/' || true)

  [[ -n "$tag" ]] || die "Cannot fetch release info — check your internet connection"
  [[ "$tag" =~ ^[A-Za-z0-9._-]+$ ]] || die "Unexpected release tag format: $tag"
  VERSION="${tag#v}"
  TAG="$tag"
  ok "Latest release: ${B}$TAG${R}"

  local archive="termux-app-store-${TAG}.tar.gz"
  local url="${OFFICIAL_RELEASE_BASE}/${TAG}/${archive}"
  local sha256_url="${url}.sha256"

  TMP_DIR=$(mktemp -d)
  local tmp_archive="$TMP_DIR/$archive"
  STAGE_DIR="$TMP_DIR/stage"

  info "Downloading ${B}$archive${R}..."
  info "From: ${DIM}$url${R}"
  curl "${CURL_SEC[@]}" -fL --progress-bar --retry 3 --retry-delay 2 \
    "$url" -o "$tmp_archive" \
    || die "Download failed (your existing installation was not touched)"
  ok "Download complete"

  info "Verifying SHA256 checksum..."
  local expected actual
  expected=$(curl "${CURL_SEC[@]}" -fsSL --max-time 20 "$sha256_url" 2>/dev/null \
    | awk '{print $1}' | head -1 || true)

  if [[ "$expected" =~ ^[A-Fa-f0-9]{64}$ ]]; then
    actual=$(sha256sum "$tmp_archive" | awk '{print $1}')
    if [[ "${actual,,}" != "${expected,,}" ]]; then
      die "SHA256 mismatch — file may be corrupted or tampered\n  Expected : $expected\n  Got      : $actual\n  (your existing installation was not touched)"
    fi
    ok "Checksum verified"
  elif [[ "$ALLOW_NO_CHECKSUM" == "1" ]]; then
    warn "No valid SHA256 published — continuing because --insecure-skip-checksum was given"
  else
    die "No valid SHA256 checksum found at:\n  $sha256_url\n  Refusing to install an unverified archive.\n  (override at your own risk: --insecure-skip-checksum)"
  fi

  info "Extracting archive..."
  mkdir -p "$STAGE_DIR"
  tar -xzf "$tmp_archive" -C "$STAGE_DIR" || die "Extraction failed"
  [[ -f "$STAGE_DIR/termux_app_store/main.py" ]] \
    || die "Archive layout unexpected (termux_app_store/main.py missing)"
  ok "Extracted and staged"
}

swap_install() {
  info "Replacing installation..."
  BACKUP_DIR="$TMP_DIR/backup"
  mkdir -p "$BACKUP_DIR"

  [[ -d "$INSTALL_DIR" ]] && mv "$INSTALL_DIR" "$BACKUP_DIR/lib"
  [[ -f "$BIN_DIR/$APP_NAME" ]] && mv "$BIN_DIR/$APP_NAME" "$BACKUP_DIR/app"
  if [[ -e "$BIN_DIR/tasctl" || -L "$BIN_DIR/tasctl" ]]; then
    mv "$BIN_DIR/tasctl" "$BACKUP_DIR/tasctl"
  fi
  SWAPPED=1

  mkdir -p "$(dirname "$INSTALL_DIR")"
  mv "$STAGE_DIR" "$INSTALL_DIR"
  ok "Installed to $INSTALL_DIR"
}

install_python_deps() {
  if ! command -v python3 >/dev/null 2>&1; then
    info "Installing Python3..."
    pkg install -y python || die "Failed to install Python3"
  fi
  ok "Python: $(python3 --version 2>&1 | awk '{print $2}')"

  if ! python3 -m pip --version >/dev/null 2>&1; then
    info "Installing pip..."
    pkg install -y python-pip || die "Failed to install pip"
  fi
  ok "pip ready"

  if ! python3 -c "import textual" >/dev/null 2>&1; then
    info "Installing Textual..."
    python3 -m pip install textual --break-system-packages \
      || die "Failed to install Textual"
  fi
  ok "Textual: v$(python3 -c "import textual; print(textual.__version__)" 2>/dev/null)"
}

create_launcher() {
  info "Creating launcher..."
  cat > "$BIN_DIR/$APP_NAME" << WRAPPER
#!/data/data/com.termux/files/usr/bin/bash
export TERMUX_APP_STORE_VERSION="${VERSION}"
export TERMUX_APP_STORE_HOME="${INSTALL_DIR}"
exec python3 "${INSTALL_DIR}/termux_app_store/main.py" "\$@"
WRAPPER
  chmod +x "$BIN_DIR/$APP_NAME"
  ok "Launcher: $BIN_DIR/$APP_NAME"
}

setup_tasctl() {
  if [[ -f "$INSTALL_DIR/tasctl" ]]; then
    chmod +x "$INSTALL_DIR/tasctl"
    ln -sf "$INSTALL_DIR/tasctl" "$BIN_DIR/tasctl"
    ok "tasctl linked: $BIN_DIR/tasctl"
  fi
}

write_sentinel() {
  cat > "$INSTALL_DIR/.installed" << EOF
version=${VERSION}
tag=${TAG}
mode=release
source=github-official-release
repo=${OFFICIAL_REPO}
installed_at=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF
  ok "Install info saved"
}

show_done() {
  printf "\n"
  printf "%s╔═════════════════════════════════════════════╗%s\n" "$BGREEN$B" "$R"
  printf "%s║   Installation Completed Successfully!      ║%s\n" "$BGREEN$B" "$R"
  printf "%s╚═════════════════════════════════════════════╝%s\n" "$BGREEN$B" "$R"
  printf "\n%sDetails:%s\n" "$BCYAN$B" "$R"
  printf "  Version   : %sv%s%s\n"       "$B" "$VERSION" "$R"
  printf "  Source    : %sOfficial GitHub Release%s\n" "$B" "$R"
  printf "  Repo      : %s%s%s\n"        "$DIM" "$OFFICIAL_URL" "$R"
  printf "  Installed : %s%s/%s%s\n"     "$DIM" "$BIN_DIR" "$APP_NAME" "$R"
  printf "\n%sRun:%s\n" "$BCYAN$B" "$R"
  printf "  %s%s%s\n" "$B" "$APP_NAME" "$R"
  printf "\n%sManage with tasctl:%s\n" "$BCYAN$B" "$R"
  printf "  tasctl update    %s→ Update to latest release%s\n" "$DIM" "$R"
  printf "  tasctl uninstall %s→ Remove%s\n" "$DIM" "$R"
  printf "  tasctl doctor    %s→ Diagnose environment%s\n\n" "$DIM" "$R"
}

usage() {
  cat <<EOF
Usage: install.sh [options]

Options:
  --insecure-skip-checksum   Continue if no valid .sha256 is published (NOT recommended)
  -h, --help                 Show this help

Via pipe:  curl -fsSL <url>/install.sh | bash -s -- --insecure-skip-checksum
EOF
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --insecure-skip-checksum) ALLOW_NO_CHECKSUM=1 ;;
      -h|--help) usage; exit 0 ;;
      *) die "Unknown option: $1" ;;
    esac
    shift
  done
}

main() {
  parse_args "$@"
  show_banner
  check_termux
  verify_official_release
  detect_arch
  check_existing
  printf "\n"
  download_release
  install_python_deps
  swap_install
  write_sentinel
  create_launcher
  setup_tasctl
  DONE=1
  show_done
}

trap 'rc=$?; rollback; cleanup_tmp; exit $rc' EXIT
trap 'printf "\n"; die "Installation failed at line $LINENO"' ERR

main "$@"
