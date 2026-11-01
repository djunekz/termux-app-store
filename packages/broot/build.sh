TERMUX_PKG_HOMEPAGE=https://github.com/Canop/broot
TERMUX_PKG_DESCRIPTION="A new way to see and navigate directory trees : https://dystroy.org/broot"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.62.0
TERMUX_PKG_SRCURL=https://github.com/Canop/broot/archive/refs/tags/v1.62.0.tar.gz
TERMUX_PKG_SHA256=7c3445a6eef45fe67fe2e1f4e0e1f9dca796237d6303615e31b07798cc1716ba
TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
