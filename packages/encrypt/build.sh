TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/encrypt
TERMUX_PKG_DESCRIPTION="ELF binary for file python/python3 with build deb package"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@djunekz"
TERMUX_PKG_VERSION=1.1
TERMUX_PKG_SRCURL=https://github.com/djunekz/encrypt/archive/refs/tags/${TERMUX_PKG_VERSION}.zip
TERMUX_PKG_SHA256=07d954452ed93a1aec029e727da275004bdb67940743a41b357f333b7cc36d5a

termux_step_make() {
	make
}

termux_step_make_install() {
    install -Dm755 "$TERMUX_PKG_SRCDIR/encrypt" \
        "$TERMUX_PREFIX/bin/encrypt"
}
