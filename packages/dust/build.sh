TERMUX_PKG_HOMEPAGE=https://github.com/bootandy/dust
TERMUX_PKG_DESCRIPTION="A more intuitive version of du in rust"
TERMUX_PKG_LICENSE="Apache-2.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.2.8
TERMUX_PKG_SRCURL=https://github.com/bootandy/dust/archive/refs/tags/v1.2.8.tar.gz
TERMUX_PKG_SHA256=2df7ea0258025b2061e1a1819ee7fc48b69fbf8c084c5f0e51a457f37695453e
TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
