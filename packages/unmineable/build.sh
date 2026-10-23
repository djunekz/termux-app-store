TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/unmineable
TERMUX_PKG_DESCRIPTION="Mining multiple coins cryptocurrency with simple setup and pool unmineable"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.1.0
TERMUX_PKG_SRCURL=https://github.com/djunekz/unmineable/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=cdc2b594fb341b34ffe1ea9557de140366ddc3a66f394ddfa4c62c5ca3f149a7
TERMUX_PKG_DEPENDS="python, cmake, make, clang, libuv, openssl, build-essential"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/unmineable"
    mkdir -p "$libdir"
    cp -r . "$libdir/"
    chmod 0755 "$libdir/unmineable.sh"

    cat > "$TERMUX_PREFIX/bin/unmineable" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
exec bash "/data/data/com.termux/files/usr/lib/unmineable/unmineable.sh" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/unmineable"
}
