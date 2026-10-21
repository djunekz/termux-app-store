TERMUX_PKG_HOMEPAGE=https://github.com/bootandy/dust
TERMUX_PKG_DESCRIPTION="A more intuitive version of du in rust"
TERMUX_PKG_LICENSE="Apache-2.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.2.6
TERMUX_PKG_SRCURL=https://github.com/bootandy/dust/archive/refs/tags/v1.2.6.tar.gz
TERMUX_PKG_SHA256=9dd1ec7576d43574e6f48342cb96a5087338b4c308460a848f5895f72ddc3bc9
TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
