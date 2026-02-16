#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COLORS_FILE="$ROOT/tools/colors.sh"

if [[ -f "$COLORS_FILE" ]]; then
  source "$COLORS_FILE"
else
  BOLD_CYAN="\033[1;36m"
  BOLD_YELLOW="\033[1;33m"
  BOLD_GREEN="\033[1;32m"
  RESET="\033[0m"
fi

echo -e "${BOLD_GREEN}This is ${BOLD_YELLOW}build.sh ${BOLD_GREEN}template (Termux package)${BOLD_YELLOW}"
echo
cat <<EOF
TERMUX_PKG_HOMEPAGE=
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER=""
TERMUX_PKG_VERSION=
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=
TERMUX_PKG_DEPENDS="" (Optional)
EOF
echo
echo -e "${BOLD_GREEN}===== [ ${BOLD_YELLOW}EXAMPLE ${BOLD_GREEN}] =====${RESET}"
echo
echo -e "${BOLD_YELLOW}TERMUX_PKG_HOMEPAGE${RESET}=https://example.com"
echo -e "${BOLD_YELLOW}TERMUX_PKG_DESCRIPTION${RESET}=\"Short description of the tool\""
echo -e "${BOLD_YELLOW}TERMUX_PKG_LICENSE${RESET}=\"MIT\""
echo -e "${BOLD_YELLOW}TERMUX_PKG_MAINTAINER${RESET}=\"Your Name <email>\""
echo -e "${BOLD_YELLOW}TERMUX_PKG_VERSION${RESET}=1.0.0"
echo -e "${BOLD_YELLOW}TERMUX_PKG_SRCURL${RESET}=\"https://example.com/\${TERMUX_PKG_VERSION}.tar.gz\""
echo -e "${BOLD_YELLOW}TERMUX_PKG_SHA256${RESET}=<PUT_REAL_SHA256_HERE>"
echo -e "${BOLD_YELLOW}TERMUX_PKG_DEPENDS${RESET}=\"bash\""

echo
echo "termux_step_make_install() {"
echo "  install -Dm755 yourtool \$TERMUX_PREFIX/bin/yourtool"
echo "}"

echo
echo -e "${BOLD_GREEN}✔ Copy this template into ${BOLD_YELLOW}packages/<name>/build.sh ${BOLD_GREEN}and edit accordingly.${RESET}"
