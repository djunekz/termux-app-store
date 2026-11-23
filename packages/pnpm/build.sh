TERMUX_PKG_HOMEPAGE=https://github.com/pnpm/pnpm
TERMUX_PKG_DESCRIPTION="Fast, disk space efficient package manager"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=12.23.0
TERMUX_PKG_SRCURL=https://registry.npmjs.org/pnpm/-/pnpm-${TERMUX_PKG_VERSION}.tgz
TERMUX_PKG_SHA256=6501a897dcfe072e8df2957c94c46f27f71901b28f2e02a167f91e0ac7905859
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
