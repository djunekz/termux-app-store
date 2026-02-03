#!/usr/bin/env bash

cat <<'EOF'
# build.sh template (Termux package)

TERMUX_PKG_HOMEPAGE=https://example.com
TERMUX_PKG_DESCRIPTION="Short description"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="Your Name <email>"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL="https://example.com/source.tar.gz"
TERMUX_PKG_SHA256=<INPUT_SHA256_HERE>
TERMUX_PKG_DEPENDS="python, bash, and etc"

termux_step_make_install() {
  install -Dm755 yourtool $TERMUX_PREFIX/bin/yourtool
}
EOF
