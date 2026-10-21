TERMUX_PKG_HOMEPAGE=https://github.com/Canop/broot
TERMUX_PKG_DESCRIPTION="A new way to see and navigate directory trees : https://dystroy.org/broot"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.61.0
TERMUX_PKG_SRCURL=https://github.com/Canop/broot/archive/refs/tags/v1.61.0.tar.gz
TERMUX_PKG_SHA256=458f1be5d78fe3b062618e9b1dbc32cf53171b0ca0769b3f32dfae65e753c264
TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
