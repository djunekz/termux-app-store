TERMUX_PKG_HOMEPAGE=https://github.com/ReFirmLabs/binwalk
TERMUX_PKG_DESCRIPTION="Firmware Analysis Tool"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.1.0
TERMUX_PKG_SRCURL=https://github.com/ReFirmLabs/binwalk/archive/refs/tags/v3.1.0.tar.gz
TERMUX_PKG_SHA256=06f595719417b70a592580258ed980237892eadc198e02363201abe6ca59e49a

TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
