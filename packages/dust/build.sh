TERMUX_PKG_HOMEPAGE=https://github.com/bootandy/dust
TERMUX_PKG_DESCRIPTION="A more intuitive version of du in rust"
TERMUX_PKG_LICENSE="Apache-2.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.2.7
TERMUX_PKG_SRCURL=https://github.com/bootandy/dust/archive/refs/tags/v1.2.7.tar.gz
TERMUX_PKG_SHA256=923a2eed637d2ea5f4ad5f820b6f87cc6e0081cfa4bc5ed1fe09278dd74db963
TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
