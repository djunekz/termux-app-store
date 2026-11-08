TERMUX_PKG_HOMEPAGE=https://dalfox.hahwul.com
TERMUX_PKG_DESCRIPTION="🌙🦊 Dalfox is a powerful open-source XSS scanner and utility focused on automation."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.3.0
TERMUX_PKG_SRCURL=https://github.com/hahwul/dalfox/archive/refs/tags/v3.3.0.tar.gz
TERMUX_PKG_SHA256=9613d8266b7fa7348829590caed0af567ba7cd0137075add913d8037066dd9dd

TERMUX_PKG_DEPENDS="rust"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
