TERMUX_PKG_HOMEPAGE=https://github.com/Anon4You/Termux-Ai
TERMUX_PKG_DESCRIPTION="Interactive AI tool for Termux with 10+ providers and 50+ image models ✨"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+7e1b8ff
TERMUX_PKG_SRCURL=https://github.com/Anon4You/Termux-Ai/archive/7e1b8ff3c0da05bc805d68a634bc2bc8aabcd62e.tar.gz
TERMUX_PKG_SHA256=e65144e01ef0619b064809798c6cf5c19f0ee811ec8045b05caed26f68910217

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    install -Dm755 "termux-ai.sh" "$TERMUX_PREFIX/bin/termux-ai"
}
