TERMUX_PKG_HOMEPAGE=https://github.com/pnpm/pnpm
TERMUX_PKG_DESCRIPTION="Fast, disk space efficient package manager"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=12.16.1
TERMUX_PKG_SRCURL=https://registry.npmjs.org/pnpm/-/pnpm-${TERMUX_PKG_VERSION}.tgz
TERMUX_PKG_SHA256=ca362a16f2e1c3cfa81d406f3242446179a0e4aea457ba3e9e6c39e6476aba65
TERMUX_PKG_DEPENDS="nodejs"

termux_step_make_install() {
    local dest="$TERMUX_PREFIX/lib/node_modules/pnpm"
    rm -rf "$dest"
    mkdir -p "$(dirname "$dest")"
    cp -r "${TERMUX_PKG_SRCDIR:-$PWD}" "$dest"

    mkdir -p "$TERMUX_PREFIX/bin"
    cat > "$TERMUX_PREFIX/bin/pnpm" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/node
require('/data/data/com.termux/files/usr/lib/node_modules/pnpm/dist/pnpm.cjs');
WRAPPER
    chmod +x "$TERMUX_PREFIX/bin/pnpm"
}
