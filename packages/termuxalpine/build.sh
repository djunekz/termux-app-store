TERMUX_PKG_HOMEPAGE=https://github.com/Hax4us/TermuxAlpine
TERMUX_PKG_DESCRIPTION="Use TermuxAlpine.sh calling to install Alpine Linux in Termux on Android. This setup script will attempt to set Alpine Linux up in your Termux environment."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+6c5d10c
TERMUX_PKG_SRCURL=https://github.com/Hax4us/TermuxAlpine/archive/6c5d10ca41273fccc2370cb969b94211018ba3e3.tar.gz
TERMUX_PKG_SHA256=6f2473ea2a292f3b85ceeb778f259289bcaa5e1e7dd7947b1b58ccc63310a6e1

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    install -Dm755 "TermuxAlpine.sh" "$TERMUX_PREFIX/bin/termuxalpine"
}
