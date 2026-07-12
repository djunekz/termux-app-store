TERMUX_PKG_HOMEPAGE=https://github.com/UltimateHackers/Hash-Buster
TERMUX_PKG_DESCRIPTION="hash-buster — auto-packaged by termux-build-init"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.0
TERMUX_PKG_SRCURL=https://github.com/UltimateHackers/Hash-Buster/archive/refs/tags/v3.0.tar.gz
TERMUX_PKG_SHA256=b6581a0ce55deab0f2fba7c670b00da1e3909bc24db51f0a85d6d47aa8a8cb2c


termux_step_make() {
    make -j"$(nproc)" PREFIX="$TERMUX_PREFIX"
}

termux_step_make_install() {
    make install PREFIX="$TERMUX_PREFIX"
}
