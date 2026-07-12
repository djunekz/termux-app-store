TERMUX_PKG_HOMEPAGE=https://kasroudra.github.io/IP-Tracker
TERMUX_PKG_DESCRIPTION="Track anyone's IP just opening a link!"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+728535e
TERMUX_PKG_SRCURL=https://github.com/KasRoudra/IP-Tracker/archive/728535ebc14e650d5309f72ee5d78b2d194e7649.tar.gz
TERMUX_PKG_SHA256=28ca93cebf7cd59e76c9eb798f119bb594f633130d9f1d2c5c9d953a5e2a4a09

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    install -Dm755 "ip.sh" "$TERMUX_PREFIX/bin/ip-tracker"
}
