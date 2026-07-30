#!/usr/bin/env bash
# Do not edit or delete this file
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

_cleanup_on_interrupt() {
  printf "\r%*s\r" "$(tput cols 2>/dev/null || echo 60)" ""
  echo ""
  printf "  ${BYELLOW}╭─ Interrupted${R}\n"
  printf "  ${BYELLOW}│${R}\n"
  printf "  ${BYELLOW}│${R}  Build was cancelled by user (Ctrl+C)\n"
  printf "  ${BYELLOW}│${R}\n"
  jobs -p | xargs -r kill 2>/dev/null || true
  [[ -n "${_MAKE_LOG:-}"    ]] && rm -f "$_MAKE_LOG"
  [[ -n "${_INSTALL_LOG:-}" ]] && rm -f "$_INSTALL_LOG"
  [[ -n "${_PKG_LOG:-}"     ]] && rm -f "$_PKG_LOG"
  printf "  ${BYELLOW}╰─ Exited cleanly.${R}\n"
  echo ""
  exit 130
}
trap '_cleanup_on_interrupt' INT TERM

_width() {
  local w; w=$(tput cols 2>/dev/null)
  [[ "$w" =~ ^[0-9]+$ ]] && echo "$w" || echo 60
}

_line_heavy() {
  local w; w=$(_width)
  printf "${CYAN}"
  printf '%.0s─' $(seq 1 $w)
  printf "${R}\n"
}

_line_thin() {
  :
}

_banner() {
  local w; w=$(_width)
  local _l; _l=$(printf '%.0s─' $(seq 1 $w))
  echo ""
  printf "${CYAN}${_l}${R}\n"
  printf "${BOLD}${CYAN}"
  printf "%*s" $(( (w + 24) / 2 )) "Termux App Store Builder"
  printf "${R}\n"
  printf "${GRAY}"
  printf "%*s" $(( (w + 36) / 2 )) "github.com/djunekz/termux-app-store"
  printf "${R}\n"
  printf "${CYAN}${_l}${R}\n"
  echo ""
}

_section() {
  echo ""
  printf "${BYELLOW}— %s —${R}\n" "$1"
}

_ok()       { printf "${BGREEN}[${GREEN}✓${BGREEN}]${R}  %s\n"      "$*"; }
_info()     { printf "${BGREEN}[${BCYAN}INFO${BGREEN}]${R}  %s\n"       "$*"; }
_warn()     { printf "${BGREEN}[${BYELLOW}!${BGREEN}]${R}  %s\n"     "$*"; }
_skip()     { printf "${BGREEN}[${GRAY}-${BGREEN}]${R}  %s${R}\n"        "$*"; }
_step()     { printf "${BGREEN}[${BCYAN}>${BGREEN}]${R}  ${BOLD}%s${R}\n" "$*"; }
_progress() { printf "${BGREEN}[${YELLOW}*${BGREEN}]${R}  %s\n"      "$*"; }
_fatal()    { printf "\n ${BG_RED}${BLACK}${BOLD} FATAL ${R} ${BRED}${BOLD}%s${R}\n\n" "$*"; }
_detail()   { printf "${GRAY}%-14s${R} ${DIM}%s${R}\n" "$1" "$2"; }
_badge()    { printf "${GRAY}%-12s${R} ${BOLD}${WHITE}%s${R}\n" "$1" "$2"; }

PACKAGE="${1:-}"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PACKAGES_DIR="$ROOT_DIR/packages"
PREFIX="${PREFIX:-/data/data/com.termux/files/usr}"
BUILD_DIR="$PACKAGES_DIR/$PACKAGE"
WORK_DIR="$ROOT_DIR/build/$PACKAGE"
DEB_DIR="$ROOT_DIR/output"

mkdir -p "$PREFIX/tmp"
export TMPDIR="$PREFIX/tmp"

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
  printf "  ${BRED}│${R}  ${WHITE}File found but has no content${R}\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}File:${R} $BUILD_SH\n"
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}│${R}  ${BYELLOW}Minimum required fields:${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_HOMEPAGE=https://example.com${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_DESCRIPTION=\"My package\"${R}\n"
  printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_VERSION=1.0.0${R}\n"
  printf "  ${BRED}╰─${R}\n"
  echo ""
  exit 1
fi

_SYNTAX_ERR=$(bash -n "$BUILD_SH" 2>&1) || true
_SYNTAX_EXIT=$?
if [[ $_SYNTAX_EXIT -ne 0 ]] || [[ -n "$_SYNTAX_ERR" ]]; then
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
    printf "  ${BRED}│${R}  ${BYELLOW}Tip:${R} Check for unmatched quotes, braces, or incomplete EOF\n"
  else
    printf "  ${BRED}│${R}  ${WHITE}$_ERR_MSG${R}\n"
  fi
  printf "  ${BRED}│${R}\n"
  printf "  ${BRED}╰─ Fix in: ${BCYAN}nano $BUILD_SH${R}\n"
  echo ""
  exit 1
fi

_ok "Syntax OK"

export PATH="$PREFIX/bin:$PATH"

_BUILD_SH_SHA256="$(sha256sum "$BUILD_SH" | awk '{print $1}')"
_detail "build.sh SHA256:" "$_BUILD_SH_SHA256"
_warn "build.sh will now be sourced and executed with full user privileges — only build packages from sources you trust"

source "$BUILD_SH"

_FIELD_ERRORS=()
_FIELD_WARNS=()

[[ -z "${TERMUX_PKG_HOMEPAGE:-}"    ]] && _FIELD_ERRORS+=("TERMUX_PKG_HOMEPAGE   |  (empty)  — Package homepage URL")
[[ -z "${TERMUX_PKG_DESCRIPTION:-}" ]] && _FIELD_ERRORS+=("TERMUX_PKG_DESCRIPTION|  (empty)  — Short package description")
[[ -z "${TERMUX_PKG_LICENSE:-}"     ]] && _FIELD_ERRORS+=("TERMUX_PKG_LICENSE    |  (empty)  — License (MIT, GPL-3.0, etc.)")
[[ -z "${TERMUX_PKG_VERSION:-}"     ]] && _FIELD_ERRORS+=("TERMUX_PKG_VERSION    |  (empty)  — Package version (must start with digit)")

[[ -z "${TERMUX_PKG_MAINTAINER:-}"  ]] && _FIELD_WARNS+=("TERMUX_PKG_MAINTAINER |  (empty)  — Maintainer name/handle")

if [[ ${#_FIELD_ERRORS[@]} -gt 0 ]] || [[ ${#_FIELD_WARNS[@]} -gt 0 ]]; then
  echo ""
  if [[ ${#_FIELD_ERRORS[@]} -gt 0 ]]; then
    _fatal "Missing required fields in build.sh"
    echo ""
    printf "  ${BRED}╭─ Field Validation Failed${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${WHITE}The following fields are required:${R}\n"
    printf "  ${BRED}│${R}\n"
    for _fe in "${_FIELD_ERRORS[@]}"; do
      _fname=$(echo "$_fe" | cut -d'|' -f1 | xargs)
      _fdesc=$(echo "$_fe" | cut -d'|' -f2- | xargs)
      printf "  ${BRED}│${R}  ${BRED}✗${R}  ${BOLD}${BYELLOW}%-28s${R}  ${GRAY}%s${R}\n" "$_fname" "$_fdesc"
    done
    if [[ ${#_FIELD_WARNS[@]} -gt 0 ]]; then
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${WHITE}The following fields are recommended:${R}\n"
      printf "  ${BRED}│${R}\n"
      for _fw in "${_FIELD_WARNS[@]}"; do
        _fname=$(echo "$_fw" | cut -d'|' -f1 | xargs)
        _fdesc=$(echo "$_fw" | cut -d'|' -f2- | xargs)
        printf "  ${BRED}│${R}  ${BYELLOW}⚠${R}  ${BOLD}${GRAY}%-28s${R}  ${GRAY}%s${R}\n" "$_fname" "$_fdesc"
      done
    fi
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Example of a valid minimal build.sh:${R}\n"
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
      _fname=$(echo "$_fw" | cut -d'|' -f1 | xargs)
      _fdesc=$(echo "$_fw" | cut -d'|' -f2- | xargs)
      printf "  ${BYELLOW}│${R}  ${BYELLOW}⚠${R}  ${BOLD}${GRAY}%-28s${R}  ${GRAY}%s${R}\n" "$_fname" "$_fdesc"
    done
    printf "  ${BYELLOW}│${R}\n"
    printf "  ${BYELLOW}╰─ Build continuing (warnings do not block build)${R}\n"
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
  mapfile -t _DEPS_ARRAY < <(echo "$TERMUX_PKG_DEPENDS" | tr ',' '\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | grep -v '^$')
  for dep in "${_DEPS_ARRAY[@]}"; do
    printf "      ${GRAY}+${R} ${WHITE}%s${R}\n" "$dep"
  done

  _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  _spin_i=0
  _PKG_LOG=$(mktemp)
  pkg install -y "${_DEPS_ARRAY[@]}" > "$_PKG_LOG" 2>&1 &
  _PKG_PID=$!
  while kill -0 "$_PKG_PID" 2>/dev/null; do
    _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
    printf "\r ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} Installing dependencies..." "$_sc"
    sleep 0.1
    (( _spin_i++ )) || true
  done
  wait "$_PKG_PID" || true
  printf "\r%*s\r" "$(tput cols 2>/dev/null || echo 80)" ""
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
    _warn "rustc ($rustc_ver) and cargo ($cargo_ver) version mismatch"
    mismatch=1
  fi

  local _tmpdir; _tmpdir=$(mktemp -d)
  printf 'fn main() {}\n' > "$_tmpdir/check.rs"
  if ! (rustc "$_tmpdir/check.rs" -o "$_tmpdir/check_bin" 2>/dev/null); then
    _warn "rustc compile test failed — possibly stale cache"
    mismatch=1
  fi
  rm -rf "$_tmpdir"

  if [[ "$mismatch" -eq 1 ]]; then
    echo ""
    printf "  ${BYELLOW}[  !!  ]${R}  ${BOLD}Rust mismatch detected — updating & cleaning automatically...${R}\n"
    echo ""

    _progress "Updating rust (pkg upgrade rust)..."
    if pkg upgrade -y rust 2>&1 | grep -v "^$"; then
      _ok "Rust updated"
    else
      _warn "pkg upgrade rust failed, continuing with current version"
    fi

    if [[ -d "$HOME/.cargo/registry/src" ]]; then
      _progress "Removing stale registry/src cache..."
      rm -rf "$HOME/.cargo/registry/src/"
      _ok "registry/src cleaned"
    fi

    rm -f "$HOME/.cargo/.package-cache" 2>/dev/null || true

    if [[ -d "$ROOT_DIR/build/$PACKAGE" ]]; then
      find "$ROOT_DIR/build/$PACKAGE" -name "Cargo.toml" -maxdepth 3 2>/dev/null \
        | while read -r _ct; do
        _pd=$(dirname "$_ct")
        if [[ -d "$_pd/target" ]]; then
          _progress "cargo clean: $(basename "$_pd")..."
          (cd "$_pd" && cargo clean 2>/dev/null) || true
        fi
      done
    fi

    local rustc_ver_new
    rustc_ver_new=$(rustc --version 2>/dev/null | awk '{print $2}' || echo "unknown")
    _ok "Rust environment clean (rustc $rustc_ver_new)"

    echo ""
    printf "  ${BCYAN}[>>]${R}  ${BOLD}Restarting build...${R}\n"
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
_detail "Work dir  :" "$WORK_DIR"
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
    printf "\r ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} Downloading... ${GRAY}%s${R}%-10s" "$_sc" "$_SIZE" " "
    sleep 0.2
    (( _spin_i++ )) || true
  done
  wait "$_CURL_PID"
  _CURL_EXIT=$?
  printf "\r%*s\r" "$(tput cols 2>/dev/null || echo 80)" ""
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
    printf "  ${BRED}│${R}  ${WHITE}SHA256 is required to verify file integrity${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}Downloaded file:${R} $(du -sh "$SRC_FILE" | awk '{print $1}')\n"
    printf "  ${BRED}│${R}  ${GRAY}SHA256:${R}  ${BGREEN}$_CALC${R}\n"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}│${R}  ${BYELLOW}Add the following line to build.sh:${R}\n"
    printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_SHA256=%s${R}\n" "$_CALC"
    printf "  ${BRED}│${R}\n"
    printf "  ${BRED}╰─ Fix in: ${BCYAN}$BUILD_SH${R}\n"
    echo ""
    exit 1
  fi

  if [[ "${TERMUX_PKG_SHA256:-}" == "SKIP" ]]; then
    _section "Integrity Check (SHA256)"
    _warn "SHA256=SKIP — checksum verification bypassed for this source"
    _warn "The downloaded file's integrity/authenticity is NOT verified. Proceed only if you fully trust TERMUX_PKG_SRCURL"
  elif [[ -n "${TERMUX_PKG_SHA256:-}" ]]; then
    _section "Integrity Check (SHA256)"
    _progress "Computing checksum..."
    CALC_SHA256="$(sha256sum "$SRC_FILE" | awk '{print $1}')"
    _detail "Expected:" "${TERMUX_PKG_SHA256}"
    _detail "Got     :" "${CALC_SHA256}"
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
      if declare -f termux_step_make_install > /dev/null 2>&1; then
        _progress "Source is .deb with custom install — extracting contents with dpkg-deb..."
        mkdir -p "$SRC_ROOT"
        if dpkg-deb -x "$SRC_FILE" "$SRC_ROOT" 2>/dev/null; then
          _ok "Extracted .deb contents to SRC_ROOT"
          _detail "Source root:" "$SRC_ROOT"
          _SUBDIRS=$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
          _TOPFILES=$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type f 2>/dev/null | wc -l)
          if [[ "$_SUBDIRS" -eq 1 && "$_TOPFILES" -eq 0 ]]; then
            SUBDIR="$(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d | head -n1)"
            SRC_ROOT="$SUBDIR"
            _info "Source root flattened to: $(basename "$SUBDIR")"
          fi
        else
          _warn "dpkg-deb -x failed — falling back to prebuilt .deb mode"
          PREBUILT_DEB="$SRC_FILE"
        fi
      else
        _skip "Prebuilt .deb detected — skipping extraction"
        PREBUILT_DEB="$SRC_FILE"
      fi
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

if declare -f termux_step_pre_configure > /dev/null 2>&1; then
  _section "Pre-Configure"
  _step "Running termux_step_pre_configure()..."
  export TERMUX_PREFIX="$PREFIX"
  export TERMUX_PKG_SRCDIR="$SRC_ROOT"
  [[ -d "$SRC_ROOT" ]] && cd "$SRC_ROOT"
  termux_step_pre_configure
  cd "$ROOT_DIR"
  _ok "Pre-configure done"
fi

if declare -f termux_step_make > /dev/null 2>&1; then
  _section "Building Source"
  _step "Custom termux_step_make() found, running..."
  export TERMUX_PREFIX="$PREFIX"
  export TERMUX_PKG_SRCDIR="$SRC_ROOT"
  export PATH="$PREFIX/bin:$PATH"
  if [[ -d "$SRC_ROOT" ]]; then
    cd "$SRC_ROOT"
  fi

  _MAKE_LOG=$(mktemp)
  _MAKE_EXIT=0

  _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  _spin_i=0
  _MAKE_START=$(date +%s)
  ( export PATH="$PREFIX/bin:$PATH"; termux_step_make ) > "$_MAKE_LOG" 2>&1 &
  _MAKE_PID=$!
  while kill -0 "$_MAKE_PID" 2>/dev/null; do
    _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
    _elapsed=$(( $(date +%s) - _MAKE_START ))
    _elapsed_fmt=$(printf "%dm%02ds" $(( _elapsed / 60 )) $(( _elapsed % 60 )))
    _last_line=$(tail -n1 "$_MAKE_LOG" 2>/dev/null | tr -d '\r\n' \
      | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-45)
    if [[ -n "$_last_line" ]]; then
      printf "\r ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} ${GRAY}[%s]${R}  %s%-10s" \
        "$_sc" "$_elapsed_fmt" "$_last_line" " "
    else
      printf "\r ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} ${GRAY}[%s]${R}  Building...%-10s" \
        "$_sc" "$_elapsed_fmt" " "
    fi
    sleep 0.2
    (( _spin_i++ )) || true
  done
  wait "$_MAKE_PID" || _MAKE_EXIT=$?
  printf "\r%*s\r" "$(tput cols 2>/dev/null || echo 80)" ""
  _MAKE_ELAPSED=$(( $(date +%s) - _MAKE_START ))

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
    printf "  ${BRED}╰─ Fix: check ${BCYAN}$BUILD_SH${R}\n"
    echo ""
    cd "$ROOT_DIR"
    exit 1
  fi

  cd "$ROOT_DIR"
  _ok "Build completed  ($(printf "%dm%02ds" $(( _MAKE_ELAPSED / 60 )) $(( _MAKE_ELAPSED % 60 ))))"
fi

_section "Installing Files (DESTDIR)"

if [[ -n "$PREBUILT_BIN" ]]; then
  _step "Mode: ELF binary"
  mkdir -p "$WORK_DIR/pkg$PREFIX/bin"
  install -Dm755 "$PREBUILT_BIN" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
  _ok "Binary staged"
  _detail "Bin:" "$PREFIX/bin/$PACKAGE"

elif [[ -n "$PREBUILT_DEB" ]]; then
  if declare -f termux_step_make_install > /dev/null 2>&1; then
    _step "Mode: Prebuilt .deb + Custom termux_step_make_install()"
    _progress "Extracting .deb contents to SRC_ROOT for custom install..."
    mkdir -p "$SRC_ROOT"
    dpkg-deb -x "$PREBUILT_DEB" "$SRC_ROOT"
    export TERMUX_PREFIX="$PREFIX"
    export TERMUX_PKG_SRCDIR="$SRC_ROOT"
    _ok "Extracted .deb to SRC_ROOT"
    _detail "Install dir:" "$SRC_ROOT"

    _INSTALL_LOG=$(mktemp)
    _INSTALL_EXIT=0
    _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    _spin_i=0
    ( cd "$SRC_ROOT"; export PATH="$PREFIX/bin:$PATH"; termux_step_make_install ) > "$_INSTALL_LOG" 2>&1 &
    _INSTALL_PID=$!
    while kill -0 "$_INSTALL_PID" 2>/dev/null; do
      _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
      printf "
 ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} Running custom install...%-20s" "$_sc" " "
      sleep 0.15
      (( _spin_i++ )) || true
    done
    wait "$_INSTALL_PID" || _INSTALL_EXIT=$?
    printf "
%*s
" "$(tput cols 2>/dev/null || echo 80)" ""
    _INSTALL_OUTPUT=$(cat "$_INSTALL_LOG")
    rm -f "$_INSTALL_LOG"

    if [[ $_INSTALL_EXIT -ne 0 ]]; then
      _fatal "termux_step_make_install() failed (exit $_INSTALL_EXIT)"
      echo "$_INSTALL_OUTPUT" | tail -10 | while IFS= read -r line; do
        printf "  ${BRED}│${R}  %s
" "$line"
      done
      exit 1
    else
      [[ -n "$_INSTALL_OUTPUT" ]] && echo "$_INSTALL_OUTPUT"
      _ok "Custom install completed"
    fi

    _progress "Staging installed files..."
    _staged=0
    for _src_path in "$PREFIX/bin/$PACKAGE" "$PREFIX/lib/$PACKAGE"; do
      if [[ -e "$_src_path" ]]; then
        _dst="$WORK_DIR/pkg$_src_path"
        mkdir -p "$(dirname "$_dst")"
        cp -r "$_src_path" "$_dst"
        _staged=$(( _staged + 1 ))
        _detail "Staged:" "$_src_path"
      fi
    done
    find "$PREFIX/bin" -name "$PACKAGE" -type f 2>/dev/null | while read -r _f; do
      _dst="$WORK_DIR/pkg$_f"
      mkdir -p "$(dirname "$_dst")"
      cp "$_f" "$_dst" 2>/dev/null || true
    done
    find "$PREFIX/lib/$PACKAGE" -type f 2>/dev/null | while read -r _f; do
      _dst="$WORK_DIR/pkg$_f"
      mkdir -p "$(dirname "$_dst")"
      cp "$_f" "$_dst" 2>/dev/null || true
    done
    _detail "Files staged:" "$_staged"
    _ok "Custom install completed"
  else
  _step "Mode: Prebuilt .deb"
  _progress "Extracting .deb contents..."

  dpkg -x "$PREBUILT_DEB" "$WORK_DIR/pkg"
  dpkg -e "$PREBUILT_DEB" "$WORK_DIR/pkg/DEBIAN"

  _ORIG_BIN=$(find "$WORK_DIR/pkg" -type f -path "*/bin/$PACKAGE" ! -path "*/DEBIAN/*" | head -n1 || true)

  if [[ -n "$_ORIG_BIN" ]]; then
    chmod +x "$_ORIG_BIN"
    _ok "Binary staged into .deb"
    _detail "Bin:" "$PREFIX/bin/$PACKAGE"
  else
    BIN_FILE="$(find "$WORK_DIR/pkg" -type f -name "$PACKAGE" -executable ! -path "*/DEBIAN/*" | head -n1 || true)"
    [[ -z "$BIN_FILE" ]] && BIN_FILE="$(find "$WORK_DIR/pkg" -type f -path "*/bin/*" ! -path "*/DEBIAN/*" | head -n1 || true)"
    [[ -z "$BIN_FILE" ]] && BIN_FILE="$(find "$WORK_DIR/pkg" -type f \( -name "*.py" -o -name "*.sh" \) ! -path "*/DEBIAN/*" | head -n1 || true)"
    [[ -z "$BIN_FILE" ]] && BIN_FILE="$(find "$WORK_DIR/pkg" -type f ! -path "*/DEBIAN/*" | head -n1 || true)"

    if [[ -n "$BIN_FILE" ]]; then
      mkdir -p "$WORK_DIR/pkg$PREFIX/bin" "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE"
      _BIN_EXT="${BIN_FILE##*.}"
      _IS_SCRIPT=0
      _SCRIPT_INTERPRETER=""

      if [[ "$_BIN_EXT" == "py" ]]; then
        _IS_SCRIPT=1; _SCRIPT_INTERPRETER="python3"
      elif [[ "$_BIN_EXT" == "sh" ]]; then
        _IS_SCRIPT=1; _SCRIPT_INTERPRETER="bash"
      else
        _SHEBANG=$(head -c 512 "$BIN_FILE" 2>/dev/null | tr -d '\0' | head -n1 || true)
        if echo "$_SHEBANG" | grep -q "python"; then
          _IS_SCRIPT=1; _SCRIPT_INTERPRETER="python3"
        elif echo "$_SHEBANG" | grep -q "bash\|sh"; then
          _IS_SCRIPT=1; _SCRIPT_INTERPRETER="bash"
        fi
      fi

      cp "$BIN_FILE" "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$(basename "$BIN_FILE")"

      if [[ "$_IS_SCRIPT" -eq 1 ]]; then
        chmod 644 "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$(basename "$BIN_FILE")"
        if echo "$_SCRIPT_INTERPRETER" | grep -q "python"; then
          cat > "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
export PYTHONPATH="$PREFIX/lib/$PACKAGE\${PYTHONPATH:+:\$PYTHONPATH}"
exec $_SCRIPT_INTERPRETER "$PREFIX/lib/$PACKAGE/$(basename "$BIN_FILE")" "\$@"
EOF
        else
          cat > "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec $_SCRIPT_INTERPRETER "$PREFIX/lib/$PACKAGE/$(basename "$BIN_FILE")" "\$@"
EOF
        fi
        _ok "Script staged into .deb"
        _detail "Script:" "$PREFIX/lib/$PACKAGE/$(basename "$BIN_FILE")"
        _detail "Interpreter:" "$_SCRIPT_INTERPRETER"
      else
        chmod +x "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$PACKAGE"
        cat > "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec "$PREFIX/lib/$PACKAGE/$PACKAGE" "\$@"
EOF
        _ok "Binary staged into .deb"
      fi

      chmod +x "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
      _detail "Bin:" "$PREFIX/bin/$PACKAGE"
    else
      _warn "No binary found inside prebuilt .deb — package files preserved as-is"
    fi
  fi

  fi

elif declare -f termux_step_make_install > /dev/null 2>&1; then
  _step "Mode: Custom termux_step_make_install()"
  touch "$WORK_DIR/.pip_bin_before"
  export TERMUX_PREFIX="$PREFIX"
  export TERMUX_PKG_SRCDIR="$SRC_ROOT"
  export PATH="$PREFIX/bin:$PATH"
  _install_dir="$SRC_ROOT"
  [[ -d "$_install_dir" ]] || _install_dir="$SRC_ROOT"
  cd "$_install_dir"
  _detail "Install dir:" "$_install_dir"

  _INSTALL_LOG=$(mktemp)
  _INSTALL_EXIT=0

  _spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  _spin_i=0
  ( cd "$_install_dir"; export PATH="$PREFIX/bin:$PATH"; termux_step_make_install ) > "$_INSTALL_LOG" 2>&1 &
  _INSTALL_PID=$!
  while kill -0 "$_INSTALL_PID" 2>/dev/null; do
    _sc="${_spin_chars:$(( _spin_i % ${#_spin_chars} )):1}"
    _last_line=$(tail -n1 "$_INSTALL_LOG" 2>/dev/null | tr -d '\r\n' | sed 's/\x1b\[[0-9;]*m//g' | cut -c1-40)
    if [[ -n "$_last_line" ]]; then
      printf "\r ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} ${GRAY}%s${R}%-20s" "$_sc" "$_last_line" " "
    else
      printf "\r ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} Running install...%-20s" "$_sc" " "
    fi
    sleep 0.15
    (( _spin_i++ )) || true
  done
  wait "$_INSTALL_PID" || _INSTALL_EXIT=$?
  printf "\r%*s\r" "$(tput cols 2>/dev/null || echo 80)" ""

  _INSTALL_OUTPUT=$(cat "$_INSTALL_LOG")
  rm -f "$_INSTALL_LOG"

  if [[ $_INSTALL_EXIT -ne 0 ]]; then
    _PIP_OK=false
    echo "$_INSTALL_OUTPUT" | grep -qi "Successfully installed" && _PIP_OK=true
    [[ -f "$PREFIX/bin/$PACKAGE" ]] && _PIP_OK=true
    command -v "$PACKAGE" &>/dev/null && _PIP_OK=true

    if [[ "$_PIP_OK" == "false" ]] && echo "$_INSTALL_OUTPUT" | grep -q "npm"; then
      _NODE_PKG_JSON=$(find "$SRC_ROOT" -maxdepth 3 -name "package.json" ! -path "*/node_modules/*" | head -n1 || true)
      if [[ -n "$_NODE_PKG_JSON" ]]; then
        _NODE_SRC="$(dirname "$_NODE_PKG_JSON")"
        _NODE_MOD="$_NODE_SRC/node_modules"
        if [[ -d "$_NODE_MOD" ]]; then
          _warn "npm failed but node_modules found — using local node_modules"
          mkdir -p "$PREFIX/lib/node_modules/$PACKAGE"
          cp -r "$_NODE_SRC"/. "$PREFIX/lib/node_modules/$PACKAGE/"
          _MAIN_JS=$(find "$_NODE_SRC" -maxdepth 1 -name "*.js" | grep -E "index|main|app|$PACKAGE" | head -n1 || true)
          [[ -z "$_MAIN_JS" ]] && _MAIN_JS=$(find "$_NODE_SRC" -maxdepth 1 -name "*.js" | head -n1 || true)
          if [[ -n "$_MAIN_JS" ]]; then
            _MAIN_JS_REL="${_MAIN_JS#$_NODE_SRC/}"
            mkdir -p "$PREFIX/bin"
            printf "#!/data/data/com.termux/files/usr/bin/bash\nexec node \"$PREFIX/lib/node_modules/$PACKAGE/$_MAIN_JS_REL\" \"\$@\"\n" > "$PREFIX/bin/$PACKAGE"
            chmod +x "$PREFIX/bin/$PACKAGE"
            _PIP_OK=true
            _INSTALL_EXIT=0
            _ok "Installed via local node_modules fallback"
          fi
        else
          _warn "npm failed — retrying with --prefer-offline..."
          ( cd "$_NODE_SRC" && npm install --prefer-offline --no-audit --no-fund 2>&1 ) && {
            _PIP_OK=true; _INSTALL_EXIT=0
            _ok "npm --prefer-offline succeeded"
          } || true
        fi
      fi
    fi

    if [[ "$_PIP_OK" == "true" ]]; then
      _warn "termux_step_make_install() exited $_INSTALL_EXIT but package appears installed — continuing"
      _INSTALL_EXIT=0
    fi
  fi

  if [[ $_INSTALL_EXIT -ne 0 ]]; then
    echo ""
    _fatal "termux_step_make_install() failed (exit $_INSTALL_EXIT)"
    echo ""

    if echo "$_INSTALL_OUTPUT" | grep -q "Could not read package.json\|ENOENT.*package\.json.*no such file\|npm.*package\.json.*not found"; then
      printf "  ${BRED}╭─ Error: package.json not found${R}\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${WHITE}npm could not find package.json in source dir${R}\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}Source dir:${R} $_install_dir\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}Source directory contents:${R}\n"
      find "$_install_dir" -maxdepth 3 -not -path "*/node_modules/*" \
        | sed "s|$_install_dir||" \
        | sed 's/^/  │    /' \
        | while IFS= read -r line; do printf "  ${BRED}│${R}${GRAY}%s${R}\n" "$line"; done
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${BYELLOW}Possible causes:${R}\n"
      printf "  ${BRED}│${R}  • package.json not found in repo root — check repo structure on GitHub\n"
      printf "  ${BRED}│${R}  • TERMUX_PKG_SRCURL points to the wrong tarball\n"
      printf "  ${BRED}│${R}  • This package is not a standard Node.js package\n"
      printf "  ${BRED}╰─ Fix: check ${BCYAN}$BUILD_SH${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -q "Cannot find module\|MODULE_NOT_FOUND"; then
      printf "  ${BRED}╭─ Error: npm module not found${R}\n"
      printf "  ${BRED}│${R}  Missing dependency during install\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${BYELLOW}Try adding to TERMUX_PKG_DEPENDS in build.sh:${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}TERMUX_PKG_DEPENDS=\"nodejs\"${R}\n"
      printf "  ${BRED}╰─ Fix: check ${BCYAN}$BUILD_SH${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -q "EACCES\|permission denied"; then
      printf "  ${BRED}╭─ Error: Permission denied${R}\n"
      printf "  ${BRED}│${R}  npm does not have write access to PREFIX\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}PREFIX:${R} $PREFIX\n"
      printf "  ${BRED}╰─ Cek permission direktori PREFIX${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -q "ENOTFOUND\|network\|ETIMEDOUT"; then
      printf "  ${BRED}╭─ Error: Network issue${R}\n"
      printf "  ${BRED}│${R}  npm cannot connect to the registry\n"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}Check your internet connection and try again${R}\n"
      printf "  ${BRED}╰─ Or set the npm registry: npm config set registry https://registry.npmjs.org${R}\n"

    elif echo "$_INSTALL_OUTPUT" | grep -qE "^make.*Error|CMake Error|gcc.*error:|undefined reference"; then
      printf "  ${BRED}╭─ Error: Build/Compile failed${R}\n"
      printf "  ${BRED}│${R}\n"
      _ERR_LINES=$(echo "$_INSTALL_OUTPUT" | grep -E "error:|Error" | head -5)
      while IFS= read -r line; do
        printf "  ${BRED}│${R}  ${BYELLOW}%s${R}\n" "$line"
      done <<< "$_ERR_LINES"
      printf "  ${BRED}│${R}\n"
      printf "  ${BRED}│${R}  ${BYELLOW}Make sure build tools are installed:${R}\n"
      printf "  ${BRED}│${R}  ${GRAY}pkg install build-essential cmake${R}\n"
      printf "  ${BRED}╰─ Fix: check ${BCYAN}$BUILD_SH${R}\n"

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

  if [[ -f "$PREFIX/bin/$PACKAGE" ]]; then
    install -Dm755 "$PREFIX/bin/$PACKAGE" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
    _detail "Staged bin:" "$PREFIX/bin/$PACKAGE"
  fi

  if [[ -f "$WORK_DIR/.pip_bin_before" ]]; then
    while IFS= read -r _new_bin; do
      _bin_name=$(basename "$_new_bin")
      if [[ ! -f "$WORK_DIR/pkg$PREFIX/bin/$_bin_name" ]]; then
        install -Dm755 "$_new_bin" "$WORK_DIR/pkg$PREFIX/bin/$_bin_name"
        _detail "Staged new bin:" "$_new_bin"
      fi
    done < <(find "$PREFIX/bin" -type f -newer "$WORK_DIR/.pip_bin_before" 2>/dev/null || true)
  fi

  _PY_SITE_CANDIDATES=()
  _SYS_SITE=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null || true)
  [[ -n "$_SYS_SITE" ]] && _PY_SITE_CANDIDATES+=("$_SYS_SITE")
  while IFS= read -r _s; do
    _PY_SITE_CANDIDATES+=("$_s")
  done < <(find "$PREFIX/lib" -maxdepth 2 -type d -name "site-packages" 2>/dev/null)
  mapfile -t _PY_SITE_CANDIDATES < <(printf '%s\n' "${_PY_SITE_CANDIDATES[@]}" | sort -u)

  _STAGED_PY=false
  for _PY_SITE in "${_PY_SITE_CANDIDATES[@]}"; do
    [[ -d "$_PY_SITE" ]] || continue

    _EP_FILE=$(find "$_PY_SITE" -maxdepth 3 \
      \( -iname "entry_points.txt" -path "*${PACKAGE}*" \
         -o -iname "RECORD" -path "*${PACKAGE}*" \) \
      2>/dev/null | grep "entry_points" | head -1 || true)

    if [[ -n "$_EP_FILE" ]]; then
      grep -A50 "\[console_scripts\]" "$_EP_FILE" 2>/dev/null | grep "=" | \
      while IFS='=' read -r _ep_name _; do
        _ep_name=$(echo "$_ep_name" | tr -d ' ')
        [[ -z "$_ep_name" ]] && continue
        for _bdir in "$PREFIX/bin" "$(python3 -c 'import sys; print(sys.prefix)' 2>/dev/null)/bin"; do
          if [[ -f "$_bdir/$_ep_name" ]]; then
            install -Dm755 "$_bdir/$_ep_name" "$WORK_DIR/pkg$PREFIX/bin/$_ep_name"
            _detail "Staged script:" "$_bdir/$_ep_name"
            break
          fi
        done
      done
    fi

    _PY_PKG=$(find "$_PY_SITE" -maxdepth 1 -type d \
      \( -iname "${PACKAGE}" -o -iname "${PACKAGE}-*" \) 2>/dev/null | \
      grep -v "dist-info\|egg-info" | head -1 || true)

    if [[ -n "$_PY_PKG" && "$_STAGED_PY" == "false" ]]; then
      _PY_SITE_DEST="$WORK_DIR/pkg$_PY_SITE"
      mkdir -p "$_PY_SITE_DEST"
      cp -r "$_PY_PKG" "$_PY_SITE_DEST/"
      find "$_PY_SITE" -maxdepth 1 \
        \( -iname "${PACKAGE}-*.dist-info" -o -iname "${PACKAGE}-*.egg-info" \) \
        -exec cp -r {} "$_PY_SITE_DEST/" \; 2>/dev/null || true
      _detail "Staged pip pkg:" "$_PY_PKG"
      _STAGED_PY=true
    fi
  done

  if [[ "$_STAGED_PY" == "false" ]]; then
    _FALLBACK=$(find "$PREFIX/lib" -maxdepth 3 -type d -iname "${PACKAGE}" 2>/dev/null | \
      grep -v "dist-info\|egg-info" | head -1 || true)
    if [[ -n "$_FALLBACK" ]]; then
      _FALLBACK_PARENT=$(dirname "$_FALLBACK")
      _FALLBACK_DEST="$WORK_DIR/pkg$_FALLBACK_PARENT"
      mkdir -p "$_FALLBACK_DEST"
      cp -r "$_FALLBACK" "$_FALLBACK_DEST/"
      find "$_FALLBACK_PARENT" -maxdepth 1 \
        \( -iname "${PACKAGE}-*.dist-info" -o -iname "${PACKAGE}-*.egg-info" \) \
        -exec cp -r {} "$_FALLBACK_DEST/" \; 2>/dev/null || true
      _detail "Staged fallback pip:" "$_FALLBACK"
      _STAGED_PY=true
    fi
  fi

  if [[ -d "$PREFIX/lib/$PACKAGE" ]]; then
    cp -r "$PREFIX/lib/$PACKAGE" "$WORK_DIR/pkg$PREFIX/lib/"
    _detail "Staged lib:" "$PREFIX/lib/$PACKAGE"
  fi

  if [[ -n "${PKG_NAME_ORIGINAL:-}" && "$PKG_NAME_ORIGINAL" != "$PACKAGE" ]]; then
    if [[ -d "$PREFIX/lib/$PKG_NAME_ORIGINAL" ]]; then
      mkdir -p "$WORK_DIR/pkg$PREFIX/lib"
      cp -r "$PREFIX/lib/$PKG_NAME_ORIGINAL" "$WORK_DIR/pkg$PREFIX/lib/"
      _detail "Staged lib (original name):" "$PREFIX/lib/$PKG_NAME_ORIGINAL"
    fi
  fi

  if [[ -d "$PREFIX/lib/node_modules/$PACKAGE" ]]; then
    mkdir -p "$WORK_DIR/pkg$PREFIX/lib/node_modules"
    cp -r "$PREFIX/lib/node_modules/$PACKAGE" "$WORK_DIR/pkg$PREFIX/lib/node_modules/"
    _detail "Staged npm:" "$PREFIX/lib/node_modules/$PACKAGE"
  fi

  if [[ -d "$PREFIX/share/$PACKAGE" ]]; then
    mkdir -p "$WORK_DIR/pkg$PREFIX/share"
    cp -r "$PREFIX/share/$PACKAGE" "$WORK_DIR/pkg$PREFIX/share/"
    _detail "Staged share:" "$PREFIX/share/$PACKAGE"
  fi

  if [[ -d "$PREFIX/share/doc/$PACKAGE" ]]; then
    mkdir -p "$WORK_DIR/pkg$PREFIX/share/doc"
    cp -r "$PREFIX/share/doc/$PACKAGE" "$WORK_DIR/pkg$PREFIX/share/doc/"
  fi

  _STAGED_COUNT=$(find "$WORK_DIR/pkg$PREFIX" -type f 2>/dev/null | grep -v "DEBIAN" | wc -l)
  if [[ "$_STAGED_COUNT" -eq 0 ]]; then
    _warn "Staging found no files — attempting emergency capture from PREFIX"
    if [[ -f "$PREFIX/bin/$PACKAGE" ]]; then
      install -Dm755 "$PREFIX/bin/$PACKAGE" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
      _detail "Emergency bin:" "$PREFIX/bin/$PACKAGE"
    fi
    for _sp in "${_PY_SITE_CANDIDATES[@]:-}"; do
      [[ -d "$_sp" ]] || continue
      _epkg=$(find "$_sp" -maxdepth 1 -type d 2>/dev/null | \
        awk -F/ '{print $NF}' | grep -i "^${PACKAGE}" | grep -v "dist-info\|egg-info" | head -1 || true)
      if [[ -n "$_epkg" ]]; then
        _SP_DEST="$WORK_DIR/pkg$_sp"
        mkdir -p "$_SP_DEST"
        cp -r "$_sp/$_epkg" "$_SP_DEST/"
        find "$_sp" -maxdepth 1 \
          \( -iname "${_epkg}-*.dist-info" -o -iname "${_epkg}-*.egg-info" \) \
          -exec cp -r {} "$_SP_DEST/" \; 2>/dev/null || true
        _detail "Emergency pip:" "$_sp/$_epkg"
        break
      fi
    done
    _STAGED_COUNT=$(find "$WORK_DIR/pkg$PREFIX" -type f 2>/dev/null | grep -v "DEBIAN" | wc -l)
    if [[ "$_STAGED_COUNT" -gt 0 ]]; then
      _ok "Emergency capture succeeded ($_STAGED_COUNT file(s))"
    else
      _warn "Staging empty — .deb will contain no files (package may still be installed on device)"
    fi
  else
    _detail "Files staged:" "$_STAGED_COUNT"
  fi

  _LIB_PKG_DIR="$WORK_DIR/pkg$PREFIX/lib/$PACKAGE"
  _BIN_PKG="$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
  if [[ -d "$_LIB_PKG_DIR" && ! -f "$_BIN_PKG" ]]; then
    mkdir -p "$WORK_DIR/pkg$PREFIX/bin"

    _ENTRY=""
    _ENTRY_TYPE=""

    if [[ -f "$_LIB_PKG_DIR/$PACKAGE/__main__.py" ]]; then
      _ENTRY_TYPE="module"
    elif [[ -f "$_LIB_PKG_DIR/__main__.py" ]]; then
      _ENTRY="$PREFIX/lib/$PACKAGE/__main__.py"
      _ENTRY_TYPE="script"
    elif [[ -f "$_LIB_PKG_DIR/$PACKAGE/main.py" ]]; then
      _ENTRY="$PREFIX/lib/$PACKAGE/$PACKAGE/main.py"
      _ENTRY_TYPE="script"
    elif [[ -f "$_LIB_PKG_DIR/main.py" ]]; then
      _ENTRY="$PREFIX/lib/$PACKAGE/main.py"
      _ENTRY_TYPE="script"
    elif [[ -f "$_LIB_PKG_DIR/${PACKAGE}.py" ]]; then
      _ENTRY="$PREFIX/lib/$PACKAGE/${PACKAGE}.py"
      _ENTRY_TYPE="script"
    fi

    if [[ "$_ENTRY_TYPE" == "module" ]]; then
      cat > "$_BIN_PKG" <<LAUNCHEREOF
#!/data/data/com.termux/files/usr/bin/bash
cd "/data/data/com.termux/files/usr/lib/$PACKAGE"
exec python3 -m $PACKAGE "\$@"
LAUNCHEREOF
      chmod +x "$_BIN_PKG"
      _ok "Created Python module launcher: $PREFIX/bin/$PACKAGE → python3 -m $PACKAGE"
    elif [[ "$_ENTRY_TYPE" == "script" && -n "$_ENTRY" ]]; then
      cat > "$_BIN_PKG" <<LAUNCHEREOF
#!/data/data/com.termux/files/usr/bin/bash
cd "/data/data/com.termux/files/usr/lib/$PACKAGE"
exec python3 "${_ENTRY}" "\$@"
LAUNCHEREOF
      chmod +x "$_BIN_PKG"
      _ok "Created Python script launcher: $PREFIX/bin/$PACKAGE → ${_ENTRY}"
    fi
  fi

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
      printf "  ${BRED}│${R}  Add to build.sh:\n"
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
      printf "\r ${BGREEN}[${BCYAN} %s ${BGREEN}]${R} Installing packages..." "$_sc"
      sleep 0.1
      (( _spin_i++ )) || true
    done
    wait "$_NPM_PID" || _NPM_EXIT=$?
    printf "\r%*s\r" "$(tput cols 2>/dev/null || echo 80)" ""

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
      mkdir -p "$WORK_DIR/pkg$PREFIX/bin"
      install -Dm755 "$_NPM_BIN" "$WORK_DIR/pkg$PREFIX/bin/$(basename "$_NPM_BIN")"
      _detail "Binary:" "$_NPM_BIN"
    fi

    _NPM_LIB="$PREFIX/lib/node_modules/$PACKAGE"
    if [[ -d "$_NPM_LIB" ]]; then
      mkdir -p "$WORK_DIR/pkg$PREFIX/lib/node_modules"
      cp -r "$_NPM_LIB" "$WORK_DIR/pkg$PREFIX/lib/node_modules/"
      _detail "Lib:" "$_NPM_LIB"

      if [[ -d "$PREFIX/lib/node_modules" ]]; then
        _PKG_DEP_FILE="$_NPM_LIB/package.json"
        if [[ -f "$_PKG_DEP_FILE" ]]; then
          _PKG_DEPS=$(python3 -c "
import json, sys
try:
    d = json.load(open('$_PKG_DEP_FILE'))
    deps = list(d.get('dependencies', {}).keys())
    print(' '.join(deps))
except:
    print('')
" 2>/dev/null || echo "")
          if [[ -n "$_PKG_DEPS" ]]; then
            _progress "Staging npm peer dependencies..."
            for _dep in $_PKG_DEPS; do
              _dep_path="$PREFIX/lib/node_modules/$_dep"
              if [[ -d "$_dep_path" ]]; then
                cp -r "$_dep_path" "$WORK_DIR/pkg$PREFIX/lib/node_modules/" 2>/dev/null || true
                _detail "Staged dep:" "$_dep"
              fi
            done
            _ok "npm peer dependencies staged"
          fi
        fi
      fi
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

    _file_magic=$(file -b "$MAIN_FILE" 2>/dev/null || echo "unknown")
    _is_elf=0
    if echo "$_file_magic" | grep -qi "ELF"; then
      _is_elf=1
    fi

    if [[ $_is_elf -eq 1 ]]; then
      mkdir -p "$WORK_DIR/pkg$PREFIX/bin"
      install -m755 "$MAIN_FILE" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"

      _ok "Main file detected"
      _detail "File   :" "$MAIN_FILE"
      _detail "Type   :" "ELF binary"
      _detail "Install:" "$PREFIX/bin/$PACKAGE"
    else
      mkdir -p "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE"
      cp -r "$SRC_ROOT"/. "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/" 2>/dev/null || {
        find "$SRC_ROOT" -maxdepth 3 -type f | while read -r _f; do
          _rel="${_f#$SRC_ROOT/}"
          _dst="$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$_rel"
          mkdir -p "$(dirname "$_dst")"
          cp "$_f" "$_dst" 2>/dev/null || true
        done
      }
      _detail "Staged:" "$PREFIX/lib/$PACKAGE/ (full repo)"
      MAIN_REL="${MAIN_FILE#$SRC_ROOT/}"
      chmod +x "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$MAIN_REL" 2>/dev/null || true

      _staged_magic=$(file -b "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$MAIN_REL" 2>/dev/null || echo "")
      INTERPRETER=""
      if echo "$_staged_magic" | grep -qi "ELF"; then
        mkdir -p "$WORK_DIR/pkg$PREFIX/bin"
        install -m755 "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$MAIN_REL" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
        rm -f "$WORK_DIR/pkg$PREFIX/lib/$PACKAGE/$MAIN_REL"
        _ok "ELF binary staged to bin/"
        _detail "File   :" "$MAIN_FILE"
        _detail "Install:" "$PREFIX/bin/$PACKAGE"
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

        mkdir -p "$WORK_DIR/pkg$PREFIX/bin"
        if echo "$INTERPRETER" | grep -q "python"; then
          cat > "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
export PYTHONPATH="$PREFIX/lib/$PACKAGE\${PYTHONPATH:+:\$PYTHONPATH}"
exec $INTERPRETER "$PREFIX/lib/$PACKAGE/$MAIN_REL" "\$@"
EOF
        else
          cat > "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE" <<EOF
#!/data/data/com.termux/files/usr/bin/bash
exec $INTERPRETER "$PREFIX/lib/$PACKAGE/$MAIN_REL" "\$@"
EOF
        fi
        chmod +x "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"

        _ok "Main file detected"
        _detail "File:"        "$MAIN_FILE"
        _detail "Interpreter:" "$INTERPRETER"
        _detail "Wrapper:"     "$PREFIX/bin/$PACKAGE"
      fi
    fi
  else
    _warn "No executable/main file found in $SRC_ROOT"

    if [[ -f "$PREFIX/bin/$PACKAGE" ]]; then
      mkdir -p "$WORK_DIR/pkg$PREFIX/bin"
      install -Dm755 "$PREFIX/bin/$PACKAGE" "$WORK_DIR/pkg$PREFIX/bin/$PACKAGE"
      _ok "Fallback: binary found in \$PREFIX/bin — staged"
      _detail "Staged bin:" "$PREFIX/bin/$PACKAGE"

      _PY_SITE_FALLBACK=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null || true)
      if [[ -n "$_PY_SITE_FALLBACK" ]]; then
        _PY_PKG_DIR=$(find "$_PY_SITE_FALLBACK" -maxdepth 1 -type d \
          \( -iname "${PACKAGE}" -o -iname "${PACKAGE}-*" \) 2>/dev/null | \
          grep -v "dist-info\|egg-info" | head -1 || true)
        if [[ -n "$_PY_PKG_DIR" ]]; then
          _PY_SITE_DEST="$WORK_DIR/pkg$_PY_SITE_FALLBACK"
          mkdir -p "$_PY_SITE_DEST"
          cp -r "$_PY_PKG_DIR" "$_PY_SITE_DEST/"
          find "$_PY_SITE_FALLBACK" -maxdepth 1 \
            \( -iname "${PACKAGE}-*.dist-info" -o -iname "${PACKAGE}-*.egg-info" \) \
            -exec cp -r {} "$_PY_SITE_DEST/" \; 2>/dev/null || true
          _detail "Staged pip pkg:" "$_PY_PKG_DIR"
        fi
      fi
    else
      _skip "Skipping install step"
    fi
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

_ok "Control file written"
_detail "   Package   :" "${TERMUX_PKG_NAME:-$PACKAGE}"
_detail "   Version   :" "${TERMUX_PKG_VERSION:-0.0.1}"
_detail "   Arch      :" "$ARCH"
_detail "   Maintainer:" "${TERMUX_PKG_MAINTAINER:-unknown}"

_section "Building .deb Package"

DEB_FILE="$DEB_DIR/${TERMUX_PKG_NAME:-$PACKAGE}_${TERMUX_PKG_VERSION:-0.0.1}_${ARCH}.deb"
_progress "Running dpkg-deb..."
_detail "Output:" "$(basename "$DEB_FILE")"

DPKG_LOG=$(mktemp)
dpkg-deb --build "$WORK_DIR/pkg" "$DEB_FILE" > "$DPKG_LOG" 2>&1
DPKG_EXIT=$?
cat "$DPKG_LOG"
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
if ! dpkg -i "$DEB_FILE" 2>&1; then
  _warn "dpkg -i reported issues — retrying with --force-depends..."
  dpkg -i --force-depends "$DEB_FILE" 2>&1 || _warn "Install completed with warnings (dependency declarations ignored)"
fi

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
    _warn "Binary '$PACKAGE' not found in PATH after install"
    echo ""
    printf "  ${BYELLOW}╭─ Warning: Package installed but command not found${R}\n"
    printf "  ${BYELLOW}│${R}\n"
    printf "  ${BYELLOW}│${R}  .deb was built and installed, but command ${BOLD}$PACKAGE${R} is not available.\n"
    printf "  ${BYELLOW}│${R}\n"
    printf "  ${BYELLOW}│${R}  ${GRAY}Possible causes:${R}\n"
    printf "  ${BYELLOW}│${R}  • Package adalah library (bukan CLI tool)\n"
    printf "  ${BYELLOW}│${R}  • Nama binary berbeda dari nama package\n"
    printf "  ${BYELLOW}│${R}  • Install mode did not place binary in bin/\n"
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
