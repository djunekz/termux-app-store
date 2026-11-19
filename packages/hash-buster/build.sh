TERMUX_PKG_HOMEPAGE=https://github.com/UltimateHackers/Hash-Buster
TERMUX_PKG_DESCRIPTION="Crack hashes in seconds."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.0
TERMUX_PKG_SRCURL=https://github.com/UltimateHackers/Hash-Buster/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=b6581a0ce55deab0f2fba7c670b00da1e3909bc24db51f0a85d6d47aa8a8cb2c
TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet requests --break-system-packages 2>/dev/null || true
    install -Dm755 hash.py "$TERMUX_PREFIX/bin/buster"
}
