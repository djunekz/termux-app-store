TERMUX_PKG_HOMEPAGE=https://leaf.rivolink.mg
TERMUX_PKG_DESCRIPTION="Terminal Markdown previewer — GUI-like experience."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.29.3
TERMUX_PKG_SRCURL=https://github.com/RivoLink/leaf/archive/refs/tags/${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=6d7343042c072f0065d4357666aa3530a3fce03d79cea7378fe20e816e2b5240
TERMUX_PKG_DEPENDS="rust, bash"

termux_step_make_install() {
    cargo install --locked --path . --root "$TERMUX_PREFIX"
}
