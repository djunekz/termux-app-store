#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COLORS_FILE="$ROOT/tools/colors.sh"

# ---- Safe color loader (CI friendly) ----
if [[ -f "$COLORS_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$COLORS_FILE"
else
  BOLD_CYAN=""
  BOLD_YELLOW=""
  BOLD_GREEN=""
  RESET=""
fi

echo -e "${BOLD_CYAN}# build.sh template (Termux package)${RESET}"
echo

cat <<EOF
${BOLD_YELLOW}TERMUX_PKG_HOMEPAGE${RESET}=https://example.com
${BOLD_YELLOW}TERMUX_PKG_DESCRIPTION${RESET}="Short description of the tool"
${BOLD_YELLOW}TERMUX_PKG_LICENSE${RESET}="MIT"
${BOLD_YELLOW}TERMUX_PKG_MAINTAINER${RESET}="Your Name <email>"
${BOLD_YELLOW}TERMUX_PKG_VERSION${RESET}=1.0.0
${BOLD_YELLOW}TERMUX_PKG_SRCURL${RESET}="https://example.com/\${TERMUX_PKG_VERSION}.tar.gz"
${BOLD_YELLOW}TERMUX_PKG_SHA256${RESET}=PUT_REAL_SHA256_HERE
${BOLD_YELLOW}TERMUX_PKG_DEPENDS${RESET}="bash"

termux_step_make_install() {
  install -Dm755 yourtool \$TERMUX_PREFIX/bin/yourtool
}
EOF

echo
echo -e "${BOLD_GREEN}✔ Copy this template into packages/<name>/build.sh and edit accordingly.${RESET}"
