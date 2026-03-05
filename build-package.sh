#!/usr/bin/env bash
# Dont edit or delete this file
# Termux App Store Official
# Developer: Djunekz
# https://github.com/djunekz/termux-app-store

set -euo pipefail

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

_section "Validating build.sh"

if [[ ! -s "$BUILD_SH" ]] || ! grep -qE '[^[:space:]]' "$BUILD_SH"; then
  _fatal "build.sh is empty"
  echo ""
  printf "  ${BRED}╭─ Error: Empty build script${R}\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}│${R}  ${WHITE}File ditemukan tapi tidak ada konten${R}\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}File:${R} $BUILD_SH\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}│${R}  ${BYELLOW}Minimal isi dengan:${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_HOMEPAGE=https://example.com${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_DESCRIPTION=\"My package\"${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_VERSION=1.0.0${R}\n"
  printf "  ${BRED}╰─${R}\n"
  echo ""
  exit 1
fi

_SYNTAX_ERR=$(bash -n "$BUILD_SH" 2>&1)
if [[ $? -ne 0 ]] || [[ -n "$_SYNTAX_ERR" ]]; then
  _fatal "Syntax error in build.sh"
  echo ""
  _ERR_LINE=$(echo "$_SYNTAX_ERR" | grep -oP '(?<=line )\d+' | head -1)
  _ERR_MSG=$(echo "$_SYNTAX_ERR" | sed "s|$BUILD_SH: ||g")
  printf "  ${BRED}╭─ Syntax Error${R}\n"
  printf "  ${BRED}│${R}\n"
  if [[ -n "$_ERR_LINE" ]]; then
    printf "  ${BRED}│${R}  ${GRAY}Line ${BYELLOW}$_ERR_LINE${R}:  ${WHITE}$_ERR_MSG${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Context (lines around error):${R}\n"
    printf "  ${BRED}│${R}\n"
    _START=$(( _ERR_LINE - 3 ))
    [[ $_START -lt 1 ]] && _START=1
    _END=$(( _ERR_LINE + 2 ))
    _LINENUM=$_START
    while IFS= read -r _L; do
      if [[ "$_LINENUM" -eq "$_ERR_LINE" ]]; then
        printf "  ${BRED}│${R}  ${BG_RED}${BLACK}${BOLD} %-4s ${R}  ${BRED}%s${R}\n" "$_LINENUM" "$_L"
      else
        printf "  ${BRED}│${R}  ${GRAY} %-4s ${R}  ${WHITE}%s${R}\n" "$_LINENUM" "$_L"
      fi
      (( _LINENUM++ ))
    done < <(sed -n "${_START},${_END}p" "$BUILD_SH")
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${BYELLOW}Tip:${R} Periksa tanda kutip, kurung kurawal, atau EOF yang tidak lengkap\n"
  else
    printf "  ${BRED}│${R}  ${WHITE}$_ERR_MSG${R}\n"
  fi
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}╰─ Fix in: ${BCYAN}nano $BUILD_SH${R}\n"
  echo ""
  exit 1
fi

_ok "Syntax OK"

source "$BUILD_SH"

_FIELD_ERRORS=()
_FIELD_WARNS=()

[[ -z "${TERMUX_PKG_HOMEPAGE:-}"    ]] && _FIELD_ERRORS+=("TERMUX_PKG_HOMEPAGE   │  (empty)  — URL homepage paket")
[[ -z "${TERMUX_PKG_DESCRIPTION:-}" ]] && _FIELD_ERRORS+=("TERMUX_PKG_DESCRIPTION│  (empty)  — Deskripsi singkat paket")
[[ -z "${TERMUX_PKG_LICENSE:-}"     ]] && _FIELD_ERRORS+=("TERMUX_PKG_LICENSE    │  (empty)  — Lisensi (MIT, GPL-3.0, dll)")
[[ -z "${TERMUX_PKG_VERSION:-}"     ]] && _FIELD_ERRORS+=("TERMUX_PKG_VERSION    │  (empty)  — Versi paket (harus mulai angka)")

[[ -z "${TERMUX_PKG_MAINTAINER:-}"  ]] && _FIELD_WARNS+=("TERMUX_PKG_MAINTAINER │  (empty)  — Nama/handle maintainer")

if [[ ${#_FIELD_ERRORS[@]} -gt 0 ]] || [[ ${#_FIELD_WARNS[@]} -gt 0 ]]; then
  echo ""
  if [[ ${#_FIELD_ERRORS[@]} -gt 0 ]]; then
    _fatal "Missing required fields in build.sh"
    echo ""
    printf "  ${BRED}╭─ Field Validation Failed${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${WHITE}Field berikut wajib diisi:${R}\n"
    printf "  ${BRED}│${R}\n"
    for _fe in "${_FIELD_ERRORS[@]}"; do
      _fname=$(echo "$_fe" | cut -d'│' -f1 | xargs)
      _fdesc=$(echo "$_fe" | cut -d'│' -f2- | xargs)
      printf "  ${BRED}│${R}  ${BRED}✗${R}  ${BOLD}${BYELLOW}%-28s${R}  ${GRAY}%s${R}\n" "$_fname" "$_fdesc"
    done
    if [[ ${#_FIELD_WARNS[@]} -gt 0 ]]; then
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${WHITE}Field berikut disarankan diisi:${R}\n"
      printf "  ${BRED}│${R}\n"
      for _fw in "${_FIELD_WARNS[@]}"; do
        _fname=$(echo "$_fw" | cut -d'│' -f1 | xargs)
        _fdesc=$(echo "$_fw" | cut -d'│' -f2- | xargs)
        printf "  ${BRED}│${R}  ${BYELLOW}⚠${R}  ${BOLD}${GRAY}%-28s${R}  ${GRAY}%s${R}\n" "$_fname" "$_fdesc"
      done
    fi
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Contoh build.sh minimal yang valid:${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_HOMEPAGE=https://github.com/user/pkg${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_DESCRIPTION=\"A cool package\"${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_LICENSE=\"MIT\"${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_MAINTAINER=\"@username\"${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_VERSION=1.0.0${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}╰─ Fix in: ${BCYAN}nano $BUILD_SH${R}\n"
    echo ""
    exit 1
  else
    printf "  ${BYELLOW}╭─ Field Warnings${R}\n"
    printf "  ${BYELLOW}│${R}\n"
    for _fw in "${_FIELD_WARNS[@]}"; do
      _fname=$(echo "$_fw" | cut -d'│' -f1 | xargs)
      _fdesc=$(echo "$_fw" | cut -d'│' -f2- | xargs)
      printf "  ${BYELLOW}│${R}  ${BYELLOW}⚠${R}  ${BOLD}${GRAY}%-28s${R}  ${GRAY}%s${R}\n" "$_fname" "$_fdesc"
    done
    printf "  ${BYELLOW}│${R}\n"
    printf "  ${BYELLOW}╰─ Build dilanjutkan (warnings tidak memblokir build)${R}\n"
    echo ""
  fi
fi

_ok "Fields validated"

if [[ -z "${TERMUX_PKG_NAME:-}" ]]; then
  TERMUX_PKG_NAME="$PACKAGE"
fi

PKG_NAME_ORIGINAL="$TERMUX_PKG_NAME"
PKG_NAME_SANITIZED=$(echo "$PKG_NAME_ORIGINAL" | tr '_' '-')

if [[ "$PKG_NAME_ORIGINAL" != "$PKG_NAME_SANITIZED" ]]; then
  TERMUX_PKG_NAME="$PKG_NAME_SANITIZED"
fi

PKG_NAME="$PKG_NAME_SANITIZED"

PACKAGE="$PKG_NAME"

if ! [[ "$PKG_NAME_SANITIZED" =~ ^[a-z0-9+.-]+$ ]]; then
  echo ""
  _fatal "Invalid package name format"
  echo ""
  printf "  ${BRED}╭─ Validation Error${R}\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}│${R}  ${WHITE}Package name contains invalid characters${R}\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}Found:${R}      ${BYELLOW}$PKG_NAME_ORIGINAL${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}Sanitized:${R}  ${BCYAN}$PKG_NAME_SANITIZED${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}Policy:${R}     Only lowercase letters, digits, and ${GREEN}-${R} ${GREEN}+${R} ${GREEN}.${R}\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}╰─ Fix in: ${BCYAN}$BUILD_SH${R}\n"
  echo ""
  printf "  ${GRAY}Valid examples:${R}\n"
  printf "    ${GREEN}✓${R} aircrack-ng\n"
  printf "    ${GREEN}✓${R} python3.11\n"
  printf "    ${GREEN}✓${R} lib++-dev\n"
  echo ""
  printf "  ${GRAY}Invalid examples:${R}\n"
  printf "    ${BRED}✗${R} aliens_eye    ${GRAY}(use: aliens-eye)${R}\n"
  printf "    ${BRED}✗${R} My-Tool       ${GRAY}(uppercase not allowed)${R}\n"
  printf "    ${BRED}✗${R} app@latest    ${GRAY}(@ not allowed)${R}\n"
  echo ""
  exit 1
fi

if [[ -n "${TERMUX_PKG_VERSION:-}" ]]; then
  if ! [[ "$TERMUX_PKG_VERSION" =~ ^[0-9] ]]; then
    echo ""
    _fatal "Invalid TERMUX_PKG_VERSION format"
    echo ""
    printf "  ${BRED}╭─ Validation Error${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${WHITE}Package version must start with a digit${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Found:${R}      ${BYELLOW}TERMUX_PKG_VERSION=$TERMUX_PKG_VERSION${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Required:${R}   Must match pattern: ${GREEN}^[0-9]${R} (e.g., 1.0, 2.3.4, 0.1-beta)\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}╰─ Fix in: ${BCYAN}$BUILD_SH${R}\n"
    echo ""
    printf "  ${GRAY}Examples of valid versions:${R}\n"
    printf "    ${GREEN}✓${R} 1.7\n"
    printf "    ${GREEN}✓${R} 2.0.3\n"
    printf "    ${GREEN}✓${R} 0.1-alpha\n"
    printf "    ${GREEN}✓${R} 3.1.4-rc2\n"
    echo ""
    printf "  ${GRAY}Invalid versions:${R}\n"
    printf "    ${BRED}✗${R} Aircrack-ng_termux  ${GRAY}(starts with letter)${R}\n"
    printf "    ${BRED}✗${R} v1.2.3             ${GRAY}(starts with 'v')${R}\n"
    printf "    ${BRED}✗${R} latest             ${GRAY}(no version number)${R}\n"
    echo ""
    exit 1
  fi
fi

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

_section "Dependencies"

if [[ -n "${TERMUX_PKG_DEPENDS:-}" ]]; then
  _progress "Installing dependencies..."
  IFS=',' read -ra _DEPS <<< "$TERMUX_PKG_DEPENDS"
  for dep in "${_DEPS[@]}"; do
    dep="$(echo "$dep" | tr -d ' ')"
    printf "      ${GRAY}+${R} ${WHITE}%s${R}\n" "$dep"
  done

  _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  _spin_i=0
  _PKG_LOG=$(mktemp)
  pkg install -y $(tr ',' ' ' <<<"$TERMUX_PKG_DEPENDS") > "$_PKG_LOG" 2>&1 &
  _PKG_PID=$!
  while kill -0 "$_PKG_PID" 2>/dev/null; do
    _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
    printf "\r  ${BCYAN}[  %s  ]${R}  Installing dependencies..." "$_sc"
    sleep 0.1
    (( _spin_i++ )) || true
  done
  wait "$_PKG_PID" || true
  printf "\r%*s\r" "$(tput cols)" ""
  rm -f "$_PKG_LOG"

  _ok "Dependencies installed"
else
  _skip "No dependencies required"
fi


_check_rust_env() {
  local needs_rust=0
  echo "${TERMUX_PKG_DEPENDS:-}" | grep -qi "rust" && needs_rust=1
  declare -f termux_step_make > /dev/null 2>&1 && command -v cargo &>/dev/null && needs_rust=1

  [[ "$needs_rust" -eq 0 ]] && return 0

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

  if [[ "$rustc_ver" != "$cargo_ver" ]]; then
    _warn "rustc ($rustc_ver) dan cargo ($cargo_ver) versi berbeda"
    mismatch=1
  fi

  local _tmpdir; _tmpdir=$(mktemp -d)
  printf 'fn main() {}\n' > "$_tmpdir/check.rs"
  if ! (rustc "$_tmpdir/check.rs" -o "$_tmpdir/check_bin" 2>/dev/null); then
    _warn "rustc compile test gagal — kemungkinan stale cache"
    mismatch=1
  fi
  rm -rf "$_tmpdir"

  if [[ "$mismatch" -eq 1 ]]; then
    echo ""
    printf "  ${BYELLOW}[  !!  ]${R}  ${BOLD}Rust mismatch terdeteksi — update & bersihkan otomatis...${R}\n"
    echo ""

    _progress "Mengupdate rust (pkg upgrade rust)..."
    if pkg upgrade -y rust 2>&1 | grep -v "^$"; then
      _ok "Rust diupdate"
    else
      _warn "pkg upgrade rust gagal, melanjutkan dengan versi saat ini"
    fi

    if [[ -d "$HOME/.cargo/registry/src" ]]; then
      _progress "Menghapus registry/src cache yang stale..."
      rm -rf "$HOME/.cargo/registry/src/"
      _ok "registry/src dibersihkan"
    fi

    rm -f "$HOME/.cargo/.package-cache" 2>/dev/null || true

    if [[ -d "$ROOT_DIR/build/$PACKAGE" ]]; then
      find "$ROOT_DIR/build/$PACKAGE" -name "Cargo.toml" -maxdepth 3 2>/dev/null \
        | while read -r _ct; do
        local _pd; _pd=$(dirname "$_ct")
        if [[ -d "$_pd/target" ]]; then
          _progress "cargo clean: $(basename "$_pd")..."
          (cd "$_pd" && cargo clean 2>/dev/null) || true
        fi
      done
    fi

    local rustc_ver_new
    rustc_ver_new=$(rustc --version 2>/dev/null | awk '{print $2}' || echo "unknown")
    _ok "Rust environment bersih (rustc $rustc_ver_new)"

    echo ""
    printf "  ${BCYAN}[  >>  ]${R}  ${BOLD}Restarting build...${R}\n"
    echo ""
    exec "$0" "$@"
  else
    _ok "Rust environment OK  (rustc $rustc_ver)"
  fi
}

_check_rust_env

_section "Preparing Build Environment"

_progress "Cleaning previous build..."
rm -rf "$WORK_DIR"
_progress "Creating directories..."
mkdir -p "$WORK_DIR/src" "$WORK_DIR/pkg" "$DEB_DIR"
_ok "Build environment ready"
_detail "Work dir:"   "$WORK_DIR"
_detail "Output dir:" "$DEB_DIR"

SRC_FILE="$WORK_DIR/source"
PREBUILT_DEB=""
PREBUILT_BIN=""
SRC_ROOT="$WORK_DIR/src"
_HAS_SOURCE=0

if [[ -n "${TERMUX_PKG_SRCURL:-}" ]]; then
  _section "Downloading Source"
  _progress "Fetching source..."
  _detail "URL:" "${TERMUX_PKG_SRCURL}"

  _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  _spin_i=0
  curl -fL --silent --retry 3 --retry-delay 2 --connect-timeout 30 "$TERMUX_PKG_SRCURL" -o "$SRC_FILE" &
  _CURL_PID=$!
  while kill -0 "$_CURL_PID" 2>/dev/null; do
    _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
    _SIZE=$(du -sh "$SRC_FILE" 2>/dev/null | awk '{print $1}' || echo "...")
    printf "\r  ${BCYAN}[  %s  ]${R}  Downloading... ${GRAY}%s${R}%-10s" "$_sc" "$_SIZE" " "
    sleep 0.2
    (( _spin_i++ )) || true
  done
  wait "$_CURL_PID"
  _CURL_EXIT=$?
  printf "\r%*s\r" "$(tput cols)" ""
  if [[ $_CURL_EXIT -ne 0 ]]; then
    _fatal "Download failed (curl exit $_CURL_EXIT)"
    exit 1
  fi

  _ok "Download complete"
  _HAS_SOURCE=1

  if [[ -z "${TERMUX_PKG_SHA256:-}" ]]; then
    _CALC=$(sha256sum "$SRC_FILE" | awk '{print $1}')
    echo ""
    _fatal "TERMUX_PKG_SHA256 is empty"
    echo ""
    printf "  ${BRED}╭─ Security Error${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${WHITE}SHA256 wajib diisi untuk verifikasi integritas file${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}File yang didownload:${R} $(du -sh "$SRC_FILE" | awk '{print $1}')\n"
    printf "  ${BRED}│${R}  ${GRAY}SHA256:${R}  ${BGREEN}$_CALC${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${BYELLOW}Tambahkan baris berikut ke build.sh:${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_SHA256=%s${R}\n" "$_CALC"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}╰─ Fix in: ${BCYAN}$BUILD_SH${R}\n"
    echo ""
    exit 1
  fi

  if [[ "${TERMUX_PKG_SHA256:-}" == "SKIP" ]]; then
    _section "Integrity Check (SHA256)"
    _skip "SHA256=SKIP — checksum verification bypassed (trusted source)"
  elif [[ -n "${TERMUX_PKG_SHA256:-}" ]]; then
    _section "Integrity Check (SHA256)"
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

  _section "Extracting Source"

  _detect_filetype() {
    local f="$1"
    local url="${TERMUX_PKG_SRCURL:-}"
    local b2; b2=$(od -A n -N 2 -t x1 "$f" 2>/dev/null | tr -d ' \n')
    local b4; b4=$(od -A n -N 4 -t x1 "$f" 2>/dev/null | tr -d ' \n')
    local b8; b8=$(od -A n -N 8 -t x1 "$f" 2>/dev/null | tr -d ' \n')
    if   [[ "$b4" == "7f454c46" ]];         then echo "elf"
    elif [[ "$b2" == "1f8b" ]];             then echo "tar.gz"
    elif [[ "$b4" == "fd377a58" ]];         then echo "xz"
    elif [[ "$b4" == "425a6839" ]];         then echo "bz2"
    elif [[ "$b4" == "504b0304" ]];         then echo "zip"
    elif [[ "$b8" == "213c617263683e0a" ]]; then echo "deb"
    elif [[ "$b4" == "213c6172" ]];         then echo "deb"
    else
      if   [[ "$url" == *.tar.gz || "$url" == *.tgz ]]; then echo "tar.gz"
      elif [[ "$url" == *.tar.xz ]];  then echo "xz"
      elif [[ "$url" == *.tar.bz2 ]]; then echo "bz2"
      elif [[ "$url" == *.zip ]];     then echo "zip"
      elif [[ "$url" == *.deb ]];     then echo "deb"
      else echo "unknown"
      fi
    fi
  }

  _smart_extract() {
    local src="$1" dst="$2"
    if   (tar -xzf "$src" -C "$dst") 2>/dev/null; then echo "tar.gz"
    elif (tar -xJf "$src" -C "$dst") 2>/dev/null; then echo "xz"
    elif (tar -xjf "$src" -C "$dst") 2>/dev/null; then echo "bz2"
    elif (tar -xf  "$src" -C "$dst") 2>/dev/null; then echo "tar"
    elif (unzip -q "$src" -d "$dst") 2>/dev/null; then echo "zip"
    else echo "fail"
    fi
  }

  FILETYPE=$(_detect_filetype "$SRC_FILE")
  _detail "File type:" "$FILETYPE"

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

else
  _section "Downloading Source"
  _skip "No TERMUX_PKG_SRCURL defined — skipping download & extract"
fi

export TERMUX_PKG_SRCDIR="$SRC_ROOT"

if [[ -n "$PREBUILT_DEB" ]]; then
  _section "Analyzing Prebuilt Package"

  _progress "Extracting package metadata..."
  CONTROL_DATA=$(dpkg-deb -f "$PREBUILT_DEB" 2>/dev/null || true)

  if [[ -n "$CONTROL_DATA" ]]; then
    DEB_DEPENDS=$(echo "$CONTROL_DATA" | grep "^Depends:" | sed 's/^Depends: *//' || true)

    if [[ -n "$DEB_DEPENDS" ]]; then
      _detail "Found deps:" "$DEB_DEPENDS"

      if [[ -n "${TERMUX_PKG_DEPENDS:-}" ]]; then
        COMBINED_DEPS="$TERMUX_PKG_DEPENDS,$DEB_DEPENDS"
      else
        COMBINED_DEPS="$DEB_DEPENDS"
      fi

      CLEANED_DEPS=$(echo "$COMBINED_DEPS" | sed -e 's/([^)]*)//g' -e 's/|/,/g' -e 's/  */ /g' | tr -d ' ')

      # Install dependencies yang belum ada
      _progress "Installing missing dependencies from .deb..."
      IFS=',' read -ra _AUTO_DEPS <<< "$CLEANED_DEPS"

      _need_install=()
      for dep in "${_AUTO_DEPS[@]}"; do
        dep=$(echo "$dep" | tr -d ' ')
        [[ -z "$dep" ]] && continue

        if ! dpkg -l "$dep" 2>/dev/null | grep -q "^ii"; then
          _need_install+=("$dep")
          printf "      ${GRAY}+${R} ${WHITE}%s${R} ${YELLOW}(auto-detected)${R}\n" "$dep"
        fi
      done

      if [[ ${#_need_install[@]} -gt 0 ]]; then
        pkg install -y "${_need_install[@]}" 2>&1 | grep -v "^$" || true
        _ok "Auto-detected dependencies installed"
      else
        _ok "All dependencies already satisfied"
      fi
    else
      _skip "No dependencies found in .deb metadata"
    fi
  else
    _warn "Could not read .deb metadata (dpkg-deb -f failed)"
  fi
fi

if declare -f termux_step_make > /dev/null 2>&1; then
  _section "Building Source"
  _step "Custom termux_step_make() found, running..."
  export TERMUX_PREFIX="$PREFIX"
  export TERMUX_PKG_SRCDIR="$SRC_ROOT"
  if [[ "${TERMUX_PKG_BUILD_IN_SRC:-false}" == "true" ]]; then
    cd "$TERMUX_PKG_SRCDIR"
  fi

  _MAKE_LOG=$(mktemp)
  _MAKE_EXIT=0

  # Spinner saat build
  _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  _spin_i=0
  termux_step_make > "$_MAKE_LOG" 2>&1 &
  _MAKE_PID=$!
  while kill -0 "$_MAKE_PID" 2>/dev/null; do
    _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
    printf "\r  ${BCYAN}[  %s  ]${R}  Building..." "$_sc"
    sleep 0.1
    (( _spin_i++ )) || true
  done
  wait "$_MAKE_PID" || _MAKE_EXIT=$?
  printf "\r%*s\r" "$(tput cols)" ""

  _MAKE_OUTPUT=$(cat "$_MAKE_LOG")
  rm -f "$_MAKE_LOG"

  if [[ $_MAKE_EXIT -ne 0 ]]; then
    echo ""
    _fatal "termux_step_make() failed (exit $_MAKE_EXIT)"
    echo ""
    printf "  ${BRED}╭─ Build error (last 10 lines):${R}\n"
    echo "$_MAKE_OUTPUT" | tail -10 | while IFS= read -r line; do
      printf "  ${BRED}│${R}  %s\n" "$line"
    done
    printf "  ${BRED}╰─ Fix: periksa ${BCYAN}$BUILD_SH${R}\n"
    echo ""
    cd "$ROOT_DIR"
    exit 1
  fi

  cd "$ROOT_DIR"
  _ok "Build completed"
fi

_section "Installing Files (DESTDIR)"

if [[ -n "$PREBUILT_BIN" ]]; then
  _step "Mode: ELF binary"
  mkdir -p "$WORK_DIR/pkg/$PREFIX/bin"
  install -Dm755 "$PREBUILT_BIN" "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE"
  _ok "Binary staged"
  _detail "Bin:" "$PREFIX/bin/$PACKAGE"

elif [[ -n "$PREBUILT_DEB" ]]; then
  _step "Mode: Prebuilt .deb"
  _progress "Extracting .deb contents..."
  dpkg -x "$PREBUILT_DEB" "$WORK_DIR/pkg"

  # Cari binary/script di dalam .deb — cek bin/ dulu, lalu fallback ke file apapun
  BIN_FILE="$(find "$WORK_DIR/pkg" -type f -name "$PACKAGE*" -executable | head -n1 || true)"

  # Fallback 1: ada file di bin/ walaupun tidak executable
  [[ -z "$BIN_FILE" ]] &&     BIN_FILE="$(find "$WORK_DIR/pkg" -type f -path "*/bin/$PACKAGE" | head -n1 || true)"

  # Fallback 2: ada wrapper script di bin/ dengan nama apapun
  [[ -z "$BIN_FILE" ]] &&     BIN_FILE="$(find "$WORK_DIR/pkg" -type f -path "*/bin/*" | head -n1 || true)"

  # Fallback 3: ada .py atau .sh di lib/
  [[ -z "$BIN_FILE" ]] &&     BIN_FILE="$(find "$WORK_DIR/pkg" -type f \( -name "*.py" -o -name "*.sh" \) | head -n1 || true)"

  # Fallback 4: file apapun yang ada
  [[ -z "$BIN_FILE" ]] &&     BIN_FILE="$(find "$WORK_DIR/pkg" -type f -not -path "*/DEBIAN/*" | head -n1 || true)"

  if [[ -n "$BIN_FILE" ]]; then
    mkdir -p "$PREFIX/lib/$PACKAGE"

    # Deteksi tipe file untuk tentukan cara install
    _BIN_EXT="${BIN_FILE##*.}"
    _IS_SCRIPT=0
    _SCRIPT_INTERPRETER=""

    if [[ "$_BIN_EXT" == "py" ]]; then
      _IS_SCRIPT=1
      _SCRIPT_INTERPRETER="python3"
    elif [[ "$_BIN_EXT" == "sh" ]]; then
      _IS_SCRIPT=1
      _SCRIPT_INTERPRETER="bash"
    else
      # Cek shebang
      _SHEBANG=$(head -c 512 "$BIN_FILE" 2>/dev/null | head -n1 || true)
      if echo "$_SHEBANG" | grep -q "python"; then
        _IS_SCRIPT=1
        _SCRIPT_INTERPRETER="python3"
      elif echo "$_SHEBANG" | grep -q "bash\|sh"; then
        _IS_SCRIPT=1
        _SCRIPT_INTERPRETER="bash"
      fi
    fi

    if [[ "$_IS_SCRIPT" -eq 1 ]]; then
      # Script — copy ke lib/ dan buat wrapper langsung tanpa perlu cek libpython
      cp "$BIN_FILE" "$PREFIX/lib/$PACKAGE/$(basename $BIN_FILE)"
      chmod 644 "$PREFIX/lib/$PACKAGE/$(basename $BIN_FILE)"
      mkdir -p "$PREFIX/bin"
      cat > "$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec $_SCRIPT_INTERPRETER "$PREFIX/lib/$PACKAGE/$(basename $BIN_FILE)" "\$@"
EOF
      chmod +x "$PREFIX/bin/$PACKAGE"
      _ok "Script installed"
      _detail "Script:" "$PREFIX/lib/$PACKAGE/$(basename $BIN_FILE)"
      _detail "Interpreter:" "$_SCRIPT_INTERPRETER"
      _detail "Bin:" "$PREFIX/bin/$PACKAGE"
    else
      mv "$BIN_FILE" "$PREFIX/lib/$PACKAGE/$PACKAGE"
      chmod +x "$PREFIX/lib/$PACKAGE/$PACKAGE"

    # Cek apakah binary ini linked ke libpython versi spesifik
    # Kalau iya, jangan exec langsung — buat wrapper python3 supaya
    # tidak terikat ke versi Python tertentu (misal libpython3.12.so)
    _LINKED_PYTHON=""
    if command -v readelf &>/dev/null; then
      _LINKED_PYTHON=$(readelf -d "$PREFIX/lib/$PACKAGE/$PACKAGE" 2>/dev/null         | grep -oP "libpython[0-9]+\.[0-9]+[^]]*" | head -n1 || true)
    elif command -v objdump &>/dev/null; then
      _LINKED_PYTHON=$(objdump -p "$PREFIX/lib/$PACKAGE/$PACKAGE" 2>/dev/null         | grep -oP "libpython[0-9]+\.[0-9]+[^[:space:]]*" | head -n1 || true)
    fi

    if [[ -n "$_LINKED_PYTHON" ]]; then
      # Binary linked ke libpython versi spesifik.
      # Solusi: buat symlink dari libpython yang terinstall saat ini
      # ke nama yang dibutuhkan binary. Ini cara paling reliable dan permanen
      # karena Python di Termux selalu ada satu versi aktif.

      _PY_VER=$(echo "$_LINKED_PYTHON" | grep -oP "[0-9]+\.[0-9]+" | head -n1 || true)

      # Cek apakah libpython yang dibutuhkan sudah ada
      _LIB_NEEDED="$PREFIX/lib/libpython${_PY_VER}.so.1.0"
      _LIB_EXISTS=0
      find "$PREFIX/lib" -name "libpython${_PY_VER}*.so*" 2>/dev/null | grep -q . && _LIB_EXISTS=1

      if [[ "$_LIB_EXISTS" -eq 0 && -n "$_PY_VER" ]]; then
        # Cari libpython versi lain yang terinstall (misal libpython3.13.so.1.0)
        _INSTALLED_LIBPY=$(find "$PREFIX/lib" -maxdepth 1 -name "libpython*.so.1.0" \
          2>/dev/null | head -n1 || true)

        if [[ -n "$_INSTALLED_LIBPY" ]]; then
          # Buat symlink: libpython3.12.so.1.0 → libpython3.13.so.1.0 (atau versi apapun)
          ln -sf "$_INSTALLED_LIBPY" "$_LIB_NEEDED" 2>/dev/null && {
            _ok "Symlinked: libpython${_PY_VER}.so.1.0 → $(basename $_INSTALLED_LIBPY)"
          } || {
            _warn "Could not create libpython symlink"
          }
        else
          _warn "No installed libpython found to symlink from"
        fi
      else
        [[ "$_LIB_EXISTS" -eq 1 ]] && _ok "libpython${_PY_VER} already present"
      fi

      cat > "$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec "$PREFIX/lib/$PACKAGE/$PACKAGE" "\$@"
EOF
      _detail "Linked Python:" "$_LINKED_PYTHON"
    else
      # Binary normal, tidak ada dependency libpython
      cat > "$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec "$PREFIX/lib/$PACKAGE/$PACKAGE" "\$@"
EOF
    fi

    chmod +x "$PREFIX/bin/$PACKAGE"
    _ok "Binary installed"
    _detail "Bin:" "$PREFIX/bin/$PACKAGE"
    fi  # end if _IS_SCRIPT
  fi

elif declare -f termux_step_make_install > /dev/null 2>&1; then
  _step "Mode: Custom termux_step_make_install()"
  export TERMUX_PREFIX="$PREFIX"
  export TERMUX_PKG_SRCDIR="$SRC_ROOT"
  _install_dir="$SRC_ROOT"
  [[ -d "$_install_dir" ]] || _install_dir="$SRC_ROOT"
  cd "$_install_dir"
  _detail "Install dir:" "$_install_dir"

  _INSTALL_LOG=$(mktemp)
  _INSTALL_EXIT=0

  _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  _spin_i=0
  termux_step_make_install > "$_INSTALL_LOG" 2>&1 &
  _INSTALL_PID=$!
  while kill -0 "$_INSTALL_PID" 2>/dev/null; do
    _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
    _last_line=$(tail -n1 "$_INSTALL_LOG" 2>/dev/null | tr -d '\r\n' | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-40)
    if [[ -n "$_last_line" ]]; then
      printf "\r  ${BCYAN}[  %s  ]${R}  ${GRAY}%s${R}%-20s" "$_sc" "$_last_line" " "
    else
      printf "\r  ${BCYAN}[  %s  ]${R}  Running install...%-20s" "$_sc" " "
    fi
    sleep 0.15
    (( _spin_i++ )) || true
  done
  wait "$_INSTALL_PID" || _INSTALL_EXIT=$?
  printf "\r%*s\r" "$(tput cols)" ""

  _INSTALL_OUTPUT=$(cat "$_INSTALL_LOG")
  rm -f "$_INSTALL_LOG"

  if [[ $_INSTALL_EXIT -ne 0 ]]; then
    echo ""
    _fatal "termux_step_make_install() failed (exit $_INSTALL_EXIT)"
    echo ""

    if echo "$_INSTALL_OUTPUT" | grep -q "ENOENT.*package.json"; then
      printf "  ${BRED}╭─ Error: package.json not found${R}\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${WHITE}npm tidak bisa menemukan package.json di source dir${R}\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}Source dir:${R} $_install_dir\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}Isi direktori source:${R}\n"
      find "$_install_dir" -maxdepth 3 -not -path "*/node_modules/*" \
        | sed "s|$_install_dir||" \
        | sed 's/^/  │    /' \
        | while IFS= read -r line; do printf "  ${BRED}│${R}${GRAY}%s${R}\n" "$line"; done
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${BYELLOW}Kemungkinan penyebab:${R}\n"
      printf "  ${BRED}│${R}  • package.json tidak ada di root repo — cek struktur repo di GitHub\n"
      printf "  ${BRED}│${R}  • TERMUX_PKG_SRCURL mengarah ke tarball yang salah\n"
      printf "  ${BRED}│${R}  • Paket ini bukan Node.js package standar\n"
      printf "  ${BRED}╰─ Fix: periksa ${BCYAN}$BUILD_SH${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -q "Cannot find module\|MODULE_NOT_FOUND"; then
      printf "  ${BRED}╭─ Error: npm module not found${R}\n"
      printf "  ${BRED}│${R}  Missing dependency saat install\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${BYELLOW}Coba tambahkan ke TERMUX_PKG_DEPENDS di build.sh:${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_DEPENDS=\"nodejs\"${R}\n"
      printf "  ${BRED}╰─ Fix: periksa ${BCYAN}$BUILD_SH${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -q "EACCES\|permission denied"; then
      printf "  ${BRED}╭─ Error: Permission denied${R}\n"
      printf "  ${BRED}│${R}  npm tidak punya akses tulis ke PREFIX\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}PREFIX:${R} $PREFIX\n"
      printf "  ${BRED}╰─ Cek permission direktori PREFIX${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -q "ENOTFOUND\|network\|ETIMEDOUT"; then
      printf "  ${BRED}╭─ Error: Network issue${R}\n"
      printf "  ${BRED}│${R}  npm tidak bisa connect ke registry\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}Cek koneksi internet dan coba lagi${R}\n"
      printf "  ${BRED}╰─ Atau set npm registry: npm config set registry https://registry.npmjs.org${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -qE "^make.*Error|CMake Error|gcc.*error:|undefined reference"; then
      printf "  ${BRED}╭─ Error: Build/Compile failed${R}\n"
      printf "  ${BRED}│${R}\n"
      _ERR_LINES=$(echo "$_INSTALL_OUTPUT" | grep -E "error:|Error" | head -5)
      while IFS= read -r line; do
        printf "  ${BRED}│${R}  ${BYELLOW}%s${R}\n" "$line"
      done <<< "$_ERR_LINES"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${BYELLOW}Pastikan build tools terinstall:${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}pkg install build-essential cmake${R}\n"
      printf "  ${BRED}╰─ Fix: periksa ${BCYAN}$BUILD_SH${R}\n"

    else
      printf "  ${BRED}╭─ Install output (last 10 lines):${R}\n"
      echo "$_INSTALL_OUTPUT" | tail -10 | while IFS= read -r line; do
        printf "  ${BRED}│${R}  %s\n" "$line"
      done
      printf "  ${BRED}╰─${R}\n"
    fi

    echo ""
    cd "$ROOT_DIR"
    exit 1
  fi

  cd "$ROOT_DIR"

  _progress "Staging installed files..."
  mkdir -p "$WORK_DIR/pkg$PREFIX/bin" "$WORK_DIR/pkg$PREFIX/lib"

  [[ -f "$PREFIX/bin/$PACKAGE" ]] && \
    install -Dm755 "$PREFIX/bin/$PACKAGE" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"

  _PY_SITE_TMP=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null || true)
  if [[ -n "$_PY_SITE_TMP" ]]; then
    _EP_FILE=$(find "$_PY_SITE_TMP" -maxdepth 2 -iname "entry_points.txt" -path "*${PACKAGE}*" 2>/dev/null | head -1 || true)
    if [[ -n "$_EP_FILE" ]]; then
      grep -A50 "\[console_scripts\]" "$_EP_FILE" 2>/dev/null | grep "=" | while IFS='=' read -r _ep_name _; do
        _ep_name=$(echo "$_ep_name" | tr -d ' ')
        [[ -f "$PREFIX/bin/$_ep_name" ]] && \
          install -Dm755 "$PREFIX/bin/$_ep_name" "$WORK_DIR/pkg$PREFIX/bin/$_ep_name" && \
          _detail "Staged bin:" "$PREFIX/bin/$_ep_name"
      done
    fi
  fi

  if [[ -d "$PREFIX/lib/$PACKAGE" ]]; then
    cp -r "$PREFIX/lib/$PACKAGE" "$WORK_DIR/pkg$PREFIX/lib/"
    _detail "Staged lib:" "$PREFIX/lib/$PACKAGE"
  fi

  if [[ -d "$PREFIX/lib/node_modules/$PACKAGE" ]]; then
    mkdir -p "$WORK_DIR/pkg$PREFIX/lib/node_modules"
    cp -r "$PREFIX/lib/node_modules/$PACKAGE" "$WORK_DIR/pkg$PREFIX/lib/node_modules/"
    _detail "Staged npm:" "$PREFIX/lib/node_modules/$PACKAGE"
  fi

  _PY_SITE=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null || true)
  if [[ -n "$_PY_SITE" ]]; then
    _PY_PKG=$(find "$_PY_SITE" -maxdepth 1 -iname "${PACKAGE}" -o \
                               -maxdepth 1 -iname "${PACKAGE}-*.dist-info" 2>/dev/null | \
              grep -v "dist-info" | head -1 || true)
    if [[ -n "$_PY_PKG" ]]; then
      _PY_SITE_DEST="$WORK_DIR/pkg$_PY_SITE"
      mkdir -p "$_PY_SITE_DEST"
      cp -r "$_PY_PKG" "$_PY_SITE_DEST/"
      find "$_PY_SITE" -maxdepth 1 -iname "${PACKAGE}-*.dist-info" -exec cp -r {} "$_PY_SITE_DEST/" \; 2>/dev/null || true
      _detail "Staged pip:" "$_PY_PKG"
    fi
  fi

  [[ -d "$PREFIX/share/doc/$PACKAGE" ]] && \
    mkdir -p "$WORK_DIR/pkg$PREFIX/share/doc" && \
    cp -r "$PREFIX/share/doc/$PACKAGE" "$WORK_DIR/pkg$PREFIX/share/doc/"

  _ok "Custom install completed"

else
  _NODE_PKG_JSON=$(find "$SRC_ROOT" -maxdepth 3 -name "package.json" -not -path "*/node_modules/*" | head -n1 || true)

  if [[ -n "$_NODE_PKG_JSON" ]]; then
    _step "Mode: Node.js package (auto-detected)"
    _NODE_SRC_DIR="$(dirname "$_NODE_PKG_JSON")"
    _detail "package.json:" "$_NODE_PKG_JSON"
    _detail "Install dir:"  "$_NODE_SRC_DIR"

    if ! command -v npm &>/dev/null; then
      _fatal "npm not found — install nodejs first"
      printf "  ${BRED}╭─ Fix${R}\n"
      printf "  ${BRED}│${R}  Tambahkan ke build.sh:\n"
      printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_DEPENDS=\"nodejs\"${R}\n"
      printf "  ${BRED}╰─${R}\n"
      exit 1
    fi

    _progress "Running npm install -g..."
    _NPM_LOG=$(mktemp)
    _NPM_EXIT=0

    _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    _spin_i=0
    npm install -g --prefix "$PREFIX" "$_NODE_SRC_DIR" > "$_NPM_LOG" 2>&1 &
    _NPM_PID=$!
    while kill -0 "$_NPM_PID" 2>/dev/null; do
      _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
      printf "\r  ${BCYAN}[  %s  ]${R}  Installing packages..." "$_sc"
      sleep 0.1
      (( _spin_i++ )) || true
    done
    wait "$_NPM_PID" || _NPM_EXIT=$?
    printf "\r%*s\r" "$(tput cols)" ""

    _NPM_OUTPUT=$(cat "$_NPM_LOG")
    rm -f "$_NPM_LOG"

    if [[ $_NPM_EXIT -ne 0 ]]; then
      echo ""
      _fatal "npm install failed (exit $_NPM_EXIT)"
      echo ""
      printf "  ${BRED}╭─ npm output (last 10 lines):${R}\n"
      echo "$_NPM_OUTPUT" | tail -10 | while IFS= read -r line; do
        printf "  ${BRED}│${R}  %s\n" "$line"
      done
      printf "  ${BRED}╰─${R}\n"
      echo ""
      exit 1
    fi

    _ok "npm install completed"

    _NPM_BIN=$(find "$PREFIX/bin" -name "$PACKAGE" -o -name "${PACKAGE}.js" 2>/dev/null | head -n1 || true)
    if [[ -n "$_NPM_BIN" ]]; then
      mkdir -p "$WORK_DIR/pkg/$PREFIX/bin"
      install -Dm755 "$_NPM_BIN" "$WORK_DIR/pkg/$PREFIX/bin/$(basename "$_NPM_BIN")"
      _detail "Binary:" "$_NPM_BIN"
    fi

    _NPM_LIB="$PREFIX/lib/node_modules/$PACKAGE"
    if [[ -d "$_NPM_LIB" ]]; then
      mkdir -p "$WORK_DIR/pkg/$PREFIX/lib/node_modules"
      cp -r "$_NPM_LIB" "$WORK_DIR/pkg/$PREFIX/lib/node_modules/"
      _detail "Lib:" "$_NPM_LIB"
    fi

  else

  _step "Mode: Auto-detect main file"

  EXTRACT_ROOT="$WORK_DIR/src"
  MAIN_FILE=""
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "$PACKAGE.py"         | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "$PACKAGE" -perm /111 | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -perm /111                  | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "*.py"                | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 1 -type f -name "*.sh"                | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$SRC_ROOT"     -maxdepth 2 -type f -name "$PACKAGE.py"         | head -n1 || true)"
  [[ -z "$MAIN_FILE" ]] && MAIN_FILE="$(find "$EXTRACT_ROOT" -maxdepth 2 -type f -name "$PACKAGE"            | head -n1 || true)"

  if [[ -n "$MAIN_FILE" ]]; then
    BASENAME="$(basename "$MAIN_FILE")"

    mkdir -p "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE"
    cp -r "$SRC_ROOT"/. "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE/"
    _detail "Staged:"  "$PREFIX/lib/$PACKAGE/ (full repo)"

    MAIN_REL="${MAIN_FILE#$SRC_ROOT/}"

    chmod +x "$WORK_DIR/pkg/$PREFIX/lib/$PACKAGE/$MAIN_REL"

    _file_magic=$(file -b "$MAIN_FILE" 2>/dev/null || echo "unknown")
    _is_elf=0
    if echo "$_file_magic" | grep -qi "ELF.*executable"; then
      _is_elf=1
    fi

    if [[ $_is_elf -eq 1 ]]; then
      mkdir -p "$WORK_DIR/pkg/$PREFIX/bin"
      ln -sf "$PREFIX/lib/$PACKAGE/$MAIN_REL" "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE"

      _ok "Main file detected"
      _detail "File:"    "$MAIN_FILE"
      _detail "Type:"    "ELF binary"
      _detail "Symlink:" "$PREFIX/bin/$PACKAGE → lib/$PACKAGE/$MAIN_REL"
    else
      FIRST_LINE="$(head -n1 "$MAIN_FILE" 2>/dev/null || true)"
      if [[ "$FIRST_LINE" =~ ^#! ]]; then
        INTERPRETER=$(echo "$FIRST_LINE" | sed 's|^#!||' | awk '{print $1}')
        if [[ "$INTERPRETER" == */env ]]; then
          INTERPRETER=$(echo "$FIRST_LINE" | awk '{print $2}')
        fi
      elif [[ "$MAIN_FILE" == *.py ]]; then
        INTERPRETER="python3"
      elif [[ "$MAIN_FILE" == *.sh ]]; then
        INTERPRETER="bash"
      else
        INTERPRETER="bash"
      fi

      mkdir -p "$WORK_DIR/pkg/$PREFIX/bin"
      cat > "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec $INTERPRETER "$PREFIX/lib/$PACKAGE/$MAIN_REL" "\$@"
EOF
      chmod +x "$WORK_DIR/pkg/$PREFIX/bin/$PACKAGE"

      _ok "Main file detected"
      _detail "File:"        "$MAIN_FILE"
      _detail "Interpreter:" "$INTERPRETER"
      _detail "Wrapper:"     "$PREFIX/bin/$PACKAGE"
    fi
  else
    _warn "No executable/main file found in $SRC_ROOT"
    _skip "Skipping install step"
  fi

  fi
fi

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

_section "Building .deb Package"

DEB_FILE="$DEB_DIR/${TERMUX_PKG_NAME:-$PACKAGE}_${TERMUX_PKG_VERSION:-0.0.1}_${ARCH}.deb"
_progress "Running dpkg-deb..."
_detail "Output:" "$(basename "$DEB_FILE")"

DPKG_LOG=$(mktemp)
if dpkg-deb --build "$WORK_DIR/pkg" "$DEB_FILE" 2>&1 | tee "$DPKG_LOG"; then
  DPKG_EXIT=0
else
  DPKG_EXIT=$?
fi
DPKG_OUTPUT=$(cat "$DPKG_LOG")
rm -f "$DPKG_LOG"

if [[ $DPKG_EXIT -ne 0 ]]; then
  echo ""
  _fatal "Failed to build .deb package"
  echo ""

  if echo "$DPKG_OUTPUT" | grep -q "version number does not start with digit"; then
    printf "  ${BRED}╭─ Error Details${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${WHITE}Invalid version format in TERMUX_PKG_VERSION${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Current value:${R}  ${BYELLOW}${TERMUX_PKG_VERSION}${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Problem:${R}       Version must start with a digit (e.g., 1.0, 2.3.4)\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}╰─ Recommended Fix${R}\n"
    echo ""
    printf "  ${BCYAN}1.${R} Open the build script:\n"
    printf "     ${GRAY}$ nano $BUILD_SH${R}\n"
    echo ""
    printf "  ${BCYAN}2.${R} Change ${BYELLOW}TERMUX_PKG_VERSION${R} to a valid format:\n"
    printf "     ${GRAY}TERMUX_PKG_VERSION=1.7${R}  ${GREEN}← Extract version number from filename/tag${R}\n"
    echo ""
    printf "  ${BCYAN}3.${R} Re-run the build:\n"
    printf "     ${GRAY}$ ./build-package.sh $PACKAGE${R}\n"
    echo ""
  elif echo "$DPKG_OUTPUT" | grep -q "control.*Permission denied"; then
    printf "  ${BRED}╭─ Error Details${R}\n"
    printf "  ${BRED}│${R}  Permission error when creating control file\n"
    printf "  ${BRED}╰─ Fix: Run with appropriate permissions or check WORK_DIR ownership${R}\n"
    echo ""
  else
    printf "  ${BRED}╭─ dpkg-deb output:${R}\n"
    echo "$DPKG_OUTPUT" | sed 's/^/  │  /'
    printf "  ${BRED}╰─${R}\n"
    echo ""
  fi

  exit 1
fi

_ok "Package built successfully"

_section "Installing Package"

_progress "Running dpkg -i..."
dpkg -i "$DEB_FILE"

if apt-mark hold "$PACKAGE" > /dev/null 2>&1; then
  _ok "Package held — protected from 'pkg upgrade' overwrite"
else
  _warn "Could not hold package — may be overwritten by 'pkg upgrade'"
fi

if apt-cache show "$PACKAGE" > /dev/null 2>&1; then
  _warn "Package '$PACKAGE' also exists in official Termux repo"
  _detail "Note:" "Package is held — official version will be skipped on upgrade"
fi

_section "Validating Installation"

_BIN_PATH=$(command -v "$PACKAGE" 2>/dev/null || true)

if [[ -n "$_BIN_PATH" ]]; then
  _ok "Binary found: $_BIN_PATH"
else
  if [[ -f "$PREFIX/bin/$PACKAGE" ]]; then
    _ok "Binary found: $PREFIX/bin/$PACKAGE"
    _BIN_PATH="$PREFIX/bin/$PACKAGE"
  else
    echo ""
    _warn "Binary '$PACKAGE' tidak ditemukan di PATH setelah install"
    echo ""
    printf "  ${BYELLOW}╭─ Warning: Package installed but command not found${R}\n"
    printf "  ${BYELLOW}│${R}\n"
    printf "  ${BYELLOW}│${R}  .deb berhasil dibuat dan diinstall, tapi command ${BOLD}$PACKAGE${R} tidak tersedia.\n"
    printf "  ${BYELLOW}│${R}\n"
    printf "  ${BYELLOW}│${R}  ${GRAY}Kemungkinan penyebab:${R}\n"
    printf "  ${BYELLOW}│${R}  • Package adalah library (bukan CLI tool)\n"
    printf "  ${BYELLOW}│${R}  • Nama binary berbeda dari nama package\n"
    printf "  ${BYELLOW}│${R}  • Install mode tidak meletakkan binary di bin/\n"
    printf "  ${BYELLOW}│${R}\n"
    printf "  ${BYELLOW}│${R}  ${GRAY}Cek isi .deb:${R}\n"
    printf "  ${BYELLOW}│${R}  ${GRAY}$ dpkg -L $PACKAGE${R}\n"
    printf "  ${BYELLOW}╰─${R}\n"
    echo ""
  fi
fi

echo ""
_line_heavy
printf "  ${BG_GREEN}${BLACK}${BOLD}  DONE  ${R}  "
printf "${BGREEN}${BOLD}%s${R}" "${TERMUX_PKG_NAME:-$PACKAGE}"
printf "${GRAY}  v${TERMUX_PKG_VERSION:-0.0.1}  [${ARCH}]${R}"
printf "${GREEN}  installed successfully${R}\n"
_line_heavy
echo ""
if [[ -n "$_BIN_PATH" ]]; then
  printf "  ${GRAY}Run with:${R}  ${BCYAN}${BOLD}${TERMUX_PKG_NAME:-$PACKAGE}${R}\n"
else
  printf "  ${GRAY}Check files:${R}  ${BCYAN}${BOLD}dpkg -L ${TERMUX_PKG_NAME:-$PACKAGE}${R}\n"
fi
echo ""
