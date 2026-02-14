#!/usr/bin/env bash
# Dont edit or delete this file
# Termux App Store Official
# Developer: Djunekz
# https://github.com/djunekz/termux-app-store

set -euo pipefail

# =============================================
#  COLORS
# =============================================
R="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"
GRAY="\033[90m"
WHITE="\033[97m"
GREEN="\033[32m"
BGREEN="\033[92m"
YELLOW="\033[33m"
BYELLOW="\033[93m"
CYAN="\033[36m"
BCYAN="\033[96m"
BRED="\033[91m"
BG_GREEN="\033[42m"
BG_RED="\033[41m"
BLACK="\033[30m"

# =============================================
#  LINE HELPERS  (warna seragam: GRAY)
# =============================================
_width() {
  local w; w=$(tput cols 2>/dev/null)
  [[ "$w" =~ ^[0-9]+$ ]] && echo "$w" || echo 60
}

_line_heavy() {
  local w; w=$(_width)
  printf "${GRAY}"
  printf '%*s' "$w" '' | tr ' ' '='
  printf "${R}\n"
}

_line_thin() {
  local w; w=$(_width)
  printf "${GRAY}"
  printf '%*s' "$w" '' | tr ' ' '-'
  printf "${R}\n"
}

# =============================================
#  OUTPUT HELPERS
# =============================================
_banner() {
  local w; w=$(_width)
  echo ""
  _line_heavy
  printf "${BOLD}${BCYAN}"
  printf "%*s" $(( (w + 26) / 2 )) "Termux App Store Builder"
  printf "${R}\n"
  printf "${GRAY}"
  printf "%*s" $(( (w + 36) / 2 )) "github.com/djunekz/termux-app-store"
  printf "${R}\n"
  _line_heavy
  echo ""
}

_section() {
  echo ""
  printf "  ${BOLD}${WHITE}:: %s${R}\n" "$1"
  _line_thin
}

_ok()       { printf "  ${BGREEN}[  OK  ]${R}  %s\n"           "$*"; }
_info()     { printf "  ${BCYAN}[ INFO ]${R}  %s\n"            "$*"; }
_warn()     { printf "  ${BYELLOW}[ WARN ]${R}  %s\n"          "$*"; }
_skip()     { printf "  ${GRAY}[ SKIP ]  %s${R}\n"             "$*"; }
_step()     { printf "  ${BCYAN}[  >>  ]${R}  ${BOLD}%s${R}\n" "$*"; }
_progress() { printf "  ${YELLOW}[  ..  ]${R}  %s\n"           "$*"; }
_fatal()    { printf "\n  ${BG_RED}${BLACK}${BOLD} FATAL ${R}  ${BRED}${BOLD}%s${R}\n\n" "$*"; }
_detail()   { printf "      ${GRAY}%-14s${R}  ${WHITE}%s${R}\n" "$1" "$2"; }
_badge()    { printf "  ${GRAY}%-12s${R}  ${BOLD}${WHITE}%s${R}\n" "$1" "$2"; }

# =============================================
#  ARGS & PATHS
# =============================================
PACKAGE="${1:-}"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGES_DIR="$ROOT_DIR/packages"
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BUILD_DIR="$PACKAGES_DIR/$PACKAGE"
WORK_DIR="$ROOT_DIR/build/$PACKAGE"
DEB_DIR="$ROOT_DIR/output"

_banner

if [[ -z "$PACKAGE" ]]; then
  _fatal "No package specified"
  printf "  Usage:  $0 ${BOLD}<package-name>${R}\n\n"
  exit 1
fi

BUILD_SH="$BUILD_DIR/build.sh"
if [[ ! -f "$BUILD_SH" ]]; then
  _fatal "build.sh not found for package '${PACKAGE}'"
  _detail "Looked in:" "$BUILD_SH"
  exit 1
fi

source "$BUILD_SH"

# =============================================
#  ARCH
# =============================================
_section "System & Architecture"

case "$(uname -m)" in
  aarch64) ARCH="aarch64" ;;
  armv7l)  ARCH="arm"     ;;
  x86_64)  ARCH="x86_64"  ;;
  i686)    ARCH="i686"    ;;
  *)
    _fatal "Unsupported architecture: $(uname -m)"
    exit 1
    ;;
esac

_badge "  Package :" "${TERMUX_PKG_NAME:-$PACKAGE}"
_badge "  Version :" "${TERMUX_PKG_VERSION:-unknown}"
_badge "  Arch    :" "$ARCH"
_badge "  Prefix  :" "$PREFIX"

# =============================================
#  DEPS
# =============================================
_section "Dependencies"

if [[ -n "${TERMUX_PKG_DEPENDS:-}" ]]; then
  _progress "Installing dependencies..."
  IFS=',' read -ra _DEPS <<< "$TERMUX_PKG_DEPENDS"
  for dep in "${_DEPS[@]}"; do
    dep="$(echo "$dep" | tr -d ' ')"
    printf "      ${GRAY}+${R} ${WHITE}%s${R}\n" "$dep"
  done
  pkg install -y $(tr ',' ' ' <<<"$TERMUX_PKG_DEPENDS")
  _ok "Dependencies installed"
else
  _skip "No dependencies required"
fi


# =============================================
#  RUST VERSION CHECK (jika paket butuh rust)
# =============================================
_check_rust_env() {
  # Apakah paket ini butuh rust?
  local needs_rust=0
  echo "${TERMUX_PKG_DEPENDS:-}" | grep -qi "rust" && needs_rust=1
  declare -f termux_step_make > /dev/null 2>&1 && command -v cargo &>/dev/null && needs_rust=1

  [[ "$needs_rust" -eq 0 ]] && return 0

  # Rust terinstall?
  if ! command -v rustc &>/dev/null || ! command -v cargo &>/dev/null; then
    _skip "Rust/Cargo not found, skipping rust check"
    return 0
  fi

  _section "Rust Environment Check"

  local rustc_ver cargo_ver mismatch=0
  rustc_ver=$(rustc --version 2>/dev/null | awk '{print $2}' || echo "unknown")
  cargo_ver=$(cargo  --version 2>/dev/null | awk '{print $2}' || echo "unknown")

  _detail "rustc version:" "$rustc_ver"
  _detail "cargo version:" "$cargo_ver"

  # Cek 1: rustc vs cargo harus versi sama
  if [[ "$rustc_ver" != "$cargo_ver" ]]; then
    _warn "rustc ($rustc_ver) dan cargo ($cargo_ver) versi berbeda"
    mismatch=1
  fi

  # Cek 2: Compile dummy — deteksi E0514 stale cache paling akurat
  local _tmpdir; _tmpdir=$(mktemp -d)
  printf 'fn main() {}\n' > "$_tmpdir/check.rs"
  if ! (rustc "$_tmpdir/check.rs" -o "$_tmpdir/check_bin" 2>/dev/null); then
    _warn "rustc compile test gagal — kemungkinan stale cache"
    mismatch=1
  fi
  rm -rf "$_tmpdir"

  # Auto-upgrade jika ada masalah
  if [[ "$mismatch" -eq 1 ]]; then
    echo ""
    printf "  ${BYELLOW}[  !!  ]${R}  ${BOLD}Rust mismatch terdeteksi — memulai auto-upgrade...${R}\n"
    echo ""

    # Step 1: Clean cache dulu
    if [[ -d "$HOME/.cargo/registry/src" ]]; then
      _progress "Menghapus registry/src cache yang stale..."
      rm -rf "$HOME/.cargo/registry/src/"
      _ok "registry/src dibersihkan"
    fi

    rm -f "$HOME/.cargo/.package-cache" 2>/dev/null || true

    # cargo clean jika ada sisa build sebelumnya
    if [[ -d "$ROOT_DIR/build/$PACKAGE" ]]; then
      find "$ROOT_DIR/build/$PACKAGE" -name "Cargo.toml" -maxdepth 3 2>/dev/null | while read -r _ct; do
        local _pd; _pd=$(dirname "$_ct")
        if [[ -d "$_pd/target" ]]; then
          _progress "cargo clean: $(basename "$_pd")..."
          (cd "$_pd" && cargo clean 2>/dev/null) || true
        fi
      done
    fi

    # Step 2: Upgrade Rust via pkg
    echo ""
    _section "Upgrading Rust"
    _progress "Running pkg upgrade rust..."
    
    if pkg upgrade -y rust 2>&1 | tee /tmp/rust_upgrade.log; then
      _ok "Rust upgrade completed"
    else
      _warn "Upgrade command completed with warnings (check /tmp/rust_upgrade.log)"
    fi

    # Step 3: Verifikasi upgrade berhasil
    echo ""
    _section "Verifying Rust Installation"
    
    # Reload environment untuk memastikan binary terbaru
    hash -r 2>/dev/null || true
    
    if ! command -v rustc &>/dev/null || ! command -v cargo &>/dev/null; then
      _fatal "Rust/Cargo tidak ditemukan setelah upgrade!"
      _detail "Hint:" "Coba restart Termux atau jalankan 'source \$PREFIX/etc/profile'"
      exit 1
    fi

    rustc_ver=$(rustc --version 2>/dev/null | awk '{print $2}' || echo "unknown")
    cargo_ver=$(cargo --version 2>/dev/null | awk '{print $2}' || echo "unknown")

    _detail "rustc version:" "$rustc_ver"
    _detail "cargo version:" "$cargo_ver"

    if [[ "$rustc_ver" != "$cargo_ver" ]]; then
      _fatal "Versi masih berbeda setelah upgrade!"
      _detail "rustc:" "$rustc_ver"
      _detail "cargo:" "$cargo_ver"
      _detail "Hint:" "Coba jalankan: pkg reinstall rust"
      exit 1
    fi

    # Test compile lagi
    _tmpdir=$(mktemp -d)
    printf 'fn main() {}\n' > "$_tmpdir/check.rs"
    if ! (rustc "$_tmpdir/check.rs" -o "$_tmpdir/check_bin" 2>/dev/null); then
      _fatal "Compile test masih gagal setelah upgrade!"
      rm -rf "$_tmpdir"
      exit 1
    fi
    rm -rf "$_tmpdir"

    _ok "Rust environment verified — ready to build with rustc $rustc_ver"
    echo ""
    _info "Melanjutkan instalasi paket..."
  else
    _ok "Rust environment OK  (rustc $rustc_ver)"
  fi
}

_check_rust_env

# =============================================
#  DIRS
# =============================================
_section "Preparing Build Environment"

_progress "Cleaning previous build..."
rm -rf "$WORK_DIR"
_progress "Creating directories..."
mkdir -p "$WORK_DIR/src" "$WORK_DIR/pkg" "$DEB_DIR"
_ok "Build environment ready"
_detail "Work dir:"   "$WORK_DIR"
_detail "Output dir:" "$DEB_DIR"

# =============================================
#  DOWNLOAD
# =============================================
_section "Downloading Source"

SRC_FILE="$WORK_DIR/source"
_progress "Fetching source..."
_detail "URL:" "${TERMUX_PKG_SRCURL}"
curl -fL --progress-bar "$TERMUX_PKG_SRCURL" -o "$SRC_FILE"
echo ""
_ok "Download complete"

# =============================================
#  SHA256
# =============================================
if [[ -n "${TERMUX_PKG_SHA256:-}" ]]; then
  _section "Integrity Check (SHA256)"

  if [[ ! -f "$SRC_FILE" ]]; then
    _fatal "Source file not found: $SRC_FILE"
    exit 1
  fi

  _progress "Computing checksum..."
  CALC_SHA256="$(sha256sum "$SRC_FILE" | awk '{print $1}')"

  _detail "Expected:" "${TERMUX_PKG_SHA256}"
  _detail "Got:"      "${CALC_SHA256}"

  if [[ "$CALC_SHA256" != "$TERMUX_PKG_SHA256" ]]; then
    _fatal "SHA256 mismatch! File may be corrupted or tampered."
    exit 1
  fi

  _ok "Checksum verified"
fi

# =============================================
#  EXTRACT
# =============================================
_section "Extracting Source"

PREBUILT_DEB=""
PREBUILT_BIN=""
SRC_ROOT="$WORK_DIR/src"

# Deteksi tipe file: magic bytes DULU, lalu fallback ekstensi URL
_detect_filetype() {
  local f="$1"
  local url="${TERMUX_PKG_SRCURL:-}"

  # Baca 2 byte pertama untuk gzip (lebih reliable dari 4 byte)
  local b2
  b2=$(od -A n -N 2 -t x1 "$f" 2>/dev/null | tr -d ' \n')

  # Baca 4 byte untuk format lain
  local b4
  b4=$(od -A n -N 4 -t x1 "$f" 2>/dev/null | tr -d ' \n')

  # Baca 8 byte untuk deb
  local b8
  b8=$(od -A n -N 8 -t x1 "$f" 2>/dev/null | tr -d ' \n')

  if   [[ "$b4"  == "7f454c46" ]];            then echo "elf"    # ELF binary
  elif [[ "$b2"  == "1f8b" ]];                then echo "tar.gz" # gzip (semua varian)
  elif [[ "$b4"  == "fd377a58" ]];            then echo "xz"     # xz
  elif [[ "$b4"  == "425a6839" ]];            then echo "bz2"    # bzip2
  elif [[ "$b4"  == "504b0304" ]];            then echo "zip"    # ZIP
  elif [[ "$b8"  == "213c617263683e0a" ]];    then echo "deb"    # .deb (ar archive)
  elif [[ "$b4"  == "213c6172" ]];            then echo "deb"    # .deb fallback
  else
    # Tidak cocok magic bytes — fallback ke ekstensi URL
    if   [[ "$url" == *.tar.gz || "$url" == *.tgz ]]; then echo "tar.gz"
    elif [[ "$url" == *.tar.xz ]];                    then echo "xz"
    elif [[ "$url" == *.tar.bz2 ]];                   then echo "bz2"
    elif [[ "$url" == *.zip ]];                       then echo "zip"
    elif [[ "$url" == *.deb ]];                       then echo "deb"
    else echo "unknown"
    fi
  fi
}

FILETYPE=$(_detect_filetype "$SRC_FILE")
_detail "File type:" "$FILETYPE"

# _smart_extract: coba semua format, tidak exit jika satu gagal
_smart_extract() {
  local src="$1" dst="$2"
  # Urutan: xzf → xjf → xzf(gz) → xf → unzip
  # Masing-masing dibungkus subshell agar error tidak kena set -e
  if   (tar -xzf "$src" -C "$dst") 2>/dev/null; then
    echo "tar.gz"
  elif (tar -xJf "$src" -C "$dst") 2>/dev/null; then
    echo "xz"
  elif (tar -xjf "$src" -C "$dst") 2>/dev/null; then
    echo "bz2"
  elif (tar -xf  "$src" -C "$dst") 2>/dev/null; then
    echo "tar"
  elif (unzip -q "$src" -d "$dst") 2>/dev/null; then
    echo "zip"
  else
    echo "fail"
  fi
}

case "$FILETYPE" in
  elf)
    _skip "ELF binary detected — no extraction needed"
    PREBUILT_BIN="$SRC_FILE"
    chmod +x "$PREBUILT_BIN"
    _ok "Binary marked executable"
    ;;
  deb)
    _skip "Prebuilt .deb detected — skipping extraction"
    PREBUILT_DEB="$SRC_FILE"
    ;;
  *)
    # Untuk semua tipe archive (tar.gz, xz, bz2, zip, unknown)
    # Gunakan smart extract yang coba semua format
    case "$FILETYPE" in
      zip)    _progress "Unzipping archive..." ;;
      xz)     _progress "Extracting xz tarball..." ;;
      bz2)    _progress "Extracting bzip2 tarball..." ;;
      tar.gz) _progress "Extracting gzip tarball..." ;;
      *)      _progress "Detecting and extracting archive..." ;;
    esac

    _EXTRACT_RESULT=$(_smart_extract "$SRC_FILE" "$SRC_ROOT")

    if [[ "$_EXTRACT_RESULT" == "fail" ]]; then
      _warn "All extraction methods failed — treating as raw binary"
      PREBUILT_BIN="$SRC_FILE"
      chmod +x "$PREBUILT_BIN"
      _ok "Binary marked executable"
    else
      _ok "Extraction complete (format: $_EXTRACT_RESULT)"
    fi
    ;;
esac

# Flatten single-subdir (hanya untuk archive, bukan binary)
if [[ -z "$PREBUILT_BIN" && -z "$PREBUILT_DEB" ]]; then
  _SUBDIRS=$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
  _TOPFILES=$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type f 2>/dev/null | wc -l)
  if [[ "$_SUBDIRS" -eq 1 && "$_TOPFILES" -eq 0 ]]; then
    SUBDIR="$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d | head -n1)"
    SRC_ROOT="$SUBDIR"
    _info "Source root flattened to: $(basename "$SUBDIR")"
  fi
  _detail "Source root:" "$SRC_ROOT"
fi

export TERMUX_PREFIX="$PREFIX"
export TERMUX_PKG_SRCDIR="$SRC_ROOT"
export DESTDIR="$WORK_DIR/pkg"

# =============================================
#  BUILD STEP (opsional)
# =============================================
if declare -f termux_step_make > /dev/null 2>&1; then
  _section "Building Source"
  _step "Custom termux_step_make() found, running..."
  export TERMUX_PREFIX="$PREFIX"
  if [[ "${TERMUX_PKG_BUILD_IN_SRC:-false}" == "true" ]]; then
    cd "$TERMUX_PKG_SRCDIR"
  fi
  termux_step_make
  cd "$ROOT_DIR"
  _ok "Build completed"
fi

# =============================================
#  INSTALL
# =============================================
_section "Installing Files (DESTDIR)"

if [[ -n "$PREBUILT_BIN" ]]; then
  # ── Mode: ELF / Raw Binary ──
  _step "Mode: ELF binary"
  mkdir -p "$WORK_DIR/pkg/$PREFIX/bin"
  install -Dm755 "$PREBUILT_BIN" "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE"
  _ok "Binary staged"
  _detail "Bin:" "$PREFIX/bin/$PACKAGE"

elif [[ -n "$PREBUILT_DEB" ]]; then
  _step "Mode: Prebuilt .deb"
  _progress "Extracting .deb contents..."
  dpkg -x "$PREBUILT_DEB" "$WORK_DIR/pkg"

  BIN_FILE="$(find "$WORK_DIR/pkg" -type f -name "$PACKAGE*" -executable | head -n1 || true)"
  if [[ -n "$BIN_FILE" ]]; then
    mkdir -p "$PREFIX/lib/$PACKAGE"
    mv "$BIN_FILE" "$PREFIX/lib/$PACKAGE/$PACKAGE"
    chmod +x "$PREFIX/lib/$PACKAGE/$PACKAGE"
    cat > "$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec "$PREFIX/lib/$PACKAGE/$PACKAGE" "\$@"
EOF
    chmod +x "$PREFIX/bin/$PACKAGE"
    _ok "Binary installed"
    _detail "Bin:" "$PREFIX/bin/$PACKAGE"
  fi

elif declare -f termux_step_make_install > /dev/null 2>&1; then
  _step "Mode: Custom termux_step_make_install()"
  export TERMUX_PREFIX="$PREFIX"
  # Masuk ke direktori source yang aktual
  _install_dir="${TERMUX_PKG_SRCDIR:-$SRC_ROOT}"
  [[ -d "$_install_dir" ]] || _install_dir="$SRC_ROOT"
  cd "$_install_dir"
  _detail "Install dir:" "$_install_dir"
  termux_step_make_install
  cd "$ROOT_DIR"

  _progress "Staging installed files..."
  mkdir -p "$WORK_DIR/pkg$PREFIX/bin" "$WORK_DIR/pkg$PREFIX/lib"

  [[ -f "$PREFIX/bin/$PACKAGE" ]] && \
    install -Dm755 "$PREFIX/bin/$PACKAGE" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
  [[ -d "$PREFIX/lib/$PACKAGE" ]] && \
    cp -r "$PREFIX/lib/$PACKAGE" "$WORK_DIR/pkg$PREFIX/lib/"
  [[ -d "$PREFIX/share/doc/$PACKAGE" ]] && \
    mkdir -p "$WORK_DIR/pkg$PREFIX/share/doc" && \
    cp -r "$PREFIX/share/doc/$PACKAGE" "$WORK_DIR/pkg$PREFIX/share/doc/"

  _ok "Custom install completed"

else
  _step "Mode: Auto-detect main file"

  EXTRACT_ROOT="$WORK_DIR/src"
  MAIN_FILE=""
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "$PACKAGE.py"         | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "$PACKAGE" -perm /111 | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -perm /111                  | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "*.py"                | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "*.sh"                | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$EXTRACT_ROOT" -maxdepth 2 -type f -name "$PACKAGE.py"         | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$EXTRACT_ROOT" -maxdepth 2 -type f -name "$PACKAGE"            | head -n1 || true)"

  if [[ -n "$MAIN_FILE" ]]; then
    BASENAME="$(basename "$MAIN_FILE")"
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
#!/data/data/com.termux/files/usr/bin/bash
exec $INTERPRETER "$PREFIX/lib/$PACKAGE/$BASENAME" "\$@"
EOF
    chmod +x "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE"

    _ok "Main file detected"
    _detail "File:"        "$MAIN_FILE"
    _detail "Interpreter:" "$INTERPRETER"
    _detail "Wrapper:"     "$PREFIX/bin/$PACKAGE"
  else
    _warn "No executable/main file found in $SRC_ROOT"
    _skip "Skipping install step"
  fi
fi

# =============================================
#  CONTROL FILE
# =============================================
_section "Generating Package Metadata"

CONTROL_DIR="$WORK_DIR/pkg/DEBIAN"
mkdir -p "$CONTROL_DIR"
chmod 0755 "$CONTROL_DIR"

cat > "$CONTROL_DIR/control" <<EOF
Package: ${TERMUX_PKG_NAME:-$PACKAGE}
Version: ${TERMUX_PKG_VERSION:-0.0.1}
Architecture: ${ARCH}
Maintainer: ${TERMUX_PKG_MAINTAINER:-unknown}
Description: ${TERMUX_PKG_DESCRIPTION:-No description}
EOF

if [[ -n "${TERMUX_PKG_DEPENDS:-}" ]]; then
  echo "Depends: ${TERMUX_PKG_DEPENDS}" >> "$CONTROL_DIR/control"
fi

_ok "control file written"
_detail "Package:"    "${TERMUX_PKG_NAME:-$PACKAGE}"
_detail "Version:"    "${TERMUX_PKG_VERSION:-0.0.1}"
_detail "Arch:"       "$ARCH"
_detail "Maintainer:" "${TERMUX_PKG_MAINTAINER:-unknown}"

# =============================================
#  BUILD DEB
# =============================================
_section "Building .deb Package"

DEB_FILE="$DEB_DIR/${TERMUX_PKG_NAME:-$PACKAGE}_${TERMUX_PKG_VERSION:-0.0.1}_${ARCH}.deb"
_progress "Running dpkg-deb..."
_detail "Output:" "$(basename "$DEB_FILE")"
dpkg-deb --build "$WORK_DIR/pkg" "$DEB_FILE"
_ok "Package built successfully"

# =============================================
#  INSTALL DEB
# =============================================
_section "Installing Package"

_progress "Running dpkg -i..."
dpkg -i "$DEB_FILE"

# =============================================
#  DONE
# =============================================
echo ""
_line_heavy
printf "  ${BG_GREEN}${BLACK}${BOLD}  DONE  ${R}  "
printf "${BGREEN}${BOLD}%s${R}" "${TERMUX_PKG_NAME:-$PACKAGE}"
printf "${GRAY}  v${TERMUX_PKG_VERSION:-0.0.1}  [${ARCH}]${R}"
printf "${GREEN}  installed successfully${R}\n"
_line_heavy
echo ""
printf "  ${GRAY}Run with:${R}  ${BCYAN}${BOLD}${TERMUX_PKG_NAME:-$PACKAGE}${R}\n"
echo ""
