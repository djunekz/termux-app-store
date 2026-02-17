#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

# =========================================================
# Termux App Store — Uninstaller
# =========================================================

APP_NAME="termux-app-store"
INSTALL_DIR="$PREFIX/lib/.tas"
BIN_DIR="$PREFIX/bin"

# Colors
R='\033[0m'
B='\033[1m'
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
CYAN='\033[36m'
DIM='\033[2m'

# ---------------- UTIL ----------------
info() {
  echo -e "${CYAN}[*] $*${R}"
}

ok() {
  echo -e "${GREEN}[✓] $*${R}"
}

warn() {
  echo -e "${YELLOW}[!] $*${R}"
}

# ---------------- CONFIRMATION ----------------
confirm_uninstall() {
  echo ""
  echo -e "${YELLOW}${B}╔══════════════════════════════════╗${R}"
  echo -e "${YELLOW}${B}║   Termux App Store Uninstaller   ║${R}"
  echo -e "${YELLOW}${B}╚══════════════════════════════════╝${R}"
  echo ""
  
  warn "This will remove:"
  echo "  • Binary/scripts in $BIN_DIR"
  echo "  • Installation directory: $INSTALL_DIR"
  echo "  • Environment variables from shell config"
  echo "  • Cache directory: ~/.cache/termux-app-store"
  echo ""
  
  echo -n "  Proceed with uninstallation? [y/N]: "
  read -r response
  case "$response" in
    [yY]|[yY][eE][sS])
      return 0
      ;;
    *)
      echo ""
      info "Uninstallation cancelled"
      exit 0
      ;;
  esac
}

# ---------------- REMOVAL ----------------
remove_binaries() {
  info "Removing binaries..."
  
  local removed=0
  
  if [[ -f "$BIN_DIR/$APP_NAME" ]]; then
    rm -f "$BIN_DIR/$APP_NAME"
    ok "Removed: $APP_NAME"
    ((removed++))
  fi
  
  if [[ -f "$BIN_DIR/$APP_NAME-cli" ]]; then
    rm -f "$BIN_DIR/$APP_NAME-cli"
    ok "Removed: $APP_NAME-cli"
    ((removed++))
  fi
  
  if [[ -f "$BIN_DIR/$APP_NAME-tui" ]]; then
    rm -f "$BIN_DIR/$APP_NAME-tui"
    ok "Removed: $APP_NAME-tui"
    ((removed++))
  fi
  
  if [[ $removed -eq 0 ]]; then
    warn "No binaries found"
  fi
}

remove_installation_dir() {
  info "Removing installation directory..."
  
  if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    ok "Removed: $INSTALL_DIR"
  else
    warn "Installation directory not found"
  fi
}

remove_cache() {
  info "Removing cache..."
  
  local cache_dir="$HOME/.cache/termux-app-store"
  if [[ -d "$cache_dir" ]]; then
    rm -rf "$cache_dir"
    ok "Removed cache: $cache_dir"
  else
    warn "Cache directory not found"
  fi
}

remove_env_vars() {
  info "Removing environment variables..."
  
  local removed=0
  
  # Remove from .bashrc
  if [[ -f "$HOME/.bashrc" ]]; then
    if grep -q "TERMUX_APP_STORE_HOME" "$HOME/.bashrc"; then
      sed -i '/# Termux App Store/d' "$HOME/.bashrc"
      sed -i '/TERMUX_APP_STORE_HOME/d' "$HOME/.bashrc"
      ok "Removed from: ~/.bashrc"
      ((removed++))
    fi
  fi
  
  # Remove from .zshrc
  if [[ -f "$HOME/.zshrc" ]]; then
    if grep -q "TERMUX_APP_STORE_HOME" "$HOME/.zshrc"; then
      sed -i '/# Termux App Store/d' "$HOME/.zshrc"
      sed -i '/TERMUX_APP_STORE_HOME/d' "$HOME/.zshrc"
      ok "Removed from: ~/.zshrc"
      ((removed++))
    fi
  fi
  
  # Remove from .profile
  if [[ -f "$HOME/.profile" ]]; then
    if grep -q "TERMUX_APP_STORE_HOME" "$HOME/.profile"; then
      sed -i '/# Termux App Store/d' "$HOME/.profile"
      sed -i '/TERMUX_APP_STORE_HOME/d' "$HOME/.profile"
      ok "Removed from: ~/.profile"
      ((removed++))
    fi
  fi
  
  if [[ $removed -eq 0 ]]; then
    warn "No environment variables found"
  fi
}

# ---------------- COMPLETION ----------------
show_completion() {
  echo ""
  echo -e "${GREEN}${B}╔════════════════════════════════════════════╗${R}"
  echo -e "${GREEN}${B}║   Uninstallation Completed Successfully!   ║${R}"
  echo -e "${GREEN}${B}╚════════════════════════════════════════════╝${R}"
  echo ""
  
  echo -e "${CYAN}Cleanup Summary:${R}"
  echo -e "  • Binaries removed"
  echo -e "  • Installation directory removed"
  echo -e "  • Cache cleaned"
  echo -e "  • Environment variables removed"
  echo ""
  
  echo -e "${YELLOW}Note:${R} Please restart your shell or run:"
  echo -e "  ${CYAN}exec \$SHELL${R}"
  echo ""
  
  echo -e "${DIM}Thank you for using Termux App Store!${R}"
  echo -e "${DIM}To reinstall: https://github.com/djunekz/termux-app-store${R}"
  echo ""
}

# ---------------- MAIN ----------------
main() {
  confirm_uninstall
  
  echo ""
  info "Starting uninstallation..."
  echo ""
  
  remove_binaries
  remove_installation_dir
  remove_cache
  remove_env_vars
  
  show_completion
}

# Run main
main "$@"
