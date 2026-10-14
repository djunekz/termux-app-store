TERMUX_PKG_HOMEPAGE=https://github.com/pnpm/pnpm
TERMUX_PKG_DESCRIPTION="Fast, disk space efficient package manager"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=10.30.1
TERMUX_PKG_SRCURL=https://registry.npmjs.org/pnpm/-/pnpm-${TERMUX_PKG_VERSION}.tgz
TERMUX_PKG_SHA256=bc8bb877378eab6a8a83114eeb6a31ef88528db4ab5570299baba8fa54da2375
TERMUX_PKG_DEPENDS="nodejs"

termux_step_make_install() {
    local dest="$TERMUX_PREFIX/lib/node_modules/pnpm"
    rm -rf "$dest"
    cp -r "${TERMUX_PKG_SRCDIR:-$PWD}" "$dest"

    mkdir -p "$TERMUX_PREFIX/bin"
    cat > "$TERMUX_PREFIX/bin/pnpm" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/node
require('/data/data/com.termux/files/usr/lib/node_modules/pnpm/dist/pnpm.cjs');
WRAPPER
    chmod +x "$TERMUX_PREFIX/bin/pnpm"
}
