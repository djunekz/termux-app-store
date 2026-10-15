TERMUX_PKG_HOMEPAGE=https://github.com/enrilinux/termux-fm
TERMUX_PKG_DESCRIPTION="TUI file manager root for Termux"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/enrilinux/termux-fm/archive/refs/tags/1.0.0.tar.gz
TERMUX_PKG_SHA256=bd273c29f85cf3361f64714afa370cc361041e16dd088187e0d7cbc67c04b92e
TERMUX_PKG_DEPENDS="ncurses, libandroid-selinux, clang, make"

termux_step_make() {
    make LDFLAGS="-landroid-selinux -lncurses"
}

termux_step_make_install() {
    install -Dm755 termux-fm "$TERMUX_PREFIX/bin/termux-fm"
}
