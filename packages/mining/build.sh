TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/mining
TERMUX_PKG_DESCRIPTION="Termux mining coin, simple tools and userfriendly"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.4
TERMUX_PKG_SRCURL=https://github.com/djunekz/mining/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=8f2d3c07fa0c1cc550fe2d5510e8a6392ecdaa1d70115c1d127f6cc8dba99555
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/mining"
    mkdir -p "$libdir"
    cp -r . "$libdir/"
    chmod 0755 "$libdir/mining.sh"

    cat > "$TERMUX_PREFIX/bin/mining" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
exec bash "/data/data/com.termux/files/usr/lib/mining/mining.sh" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/mining"
}
