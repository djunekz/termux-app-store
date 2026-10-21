TERMUX_PKG_HOMEPAGE=https://github.com/Anon4You/Termux-Ai
TERMUX_PKG_DESCRIPTION="Interactive AI tool for Termux with 10+ providers and 50+ image models ✨"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+0dea995
TERMUX_PKG_SRCURL=https://github.com/Anon4You/Termux-Ai/archive/0dea9953a863fb0df884a4fefa01b82ae01924a2.tar.gz
TERMUX_PKG_SHA256=f5a4c4f7c6f77377dfd80fd86070070452d6277de1522ec044f8254907c8e64d

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    install -Dm755 "termux-ai.sh" "$TERMUX_PREFIX/bin/termux-ai"
}
