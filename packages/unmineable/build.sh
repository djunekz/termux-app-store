TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/unmineable
TERMUX_PKG_DESCRIPTION="Mining multiple coins cryptocurrency with simple setup and pool unmineable"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.1.5
TERMUX_PKG_SRCURL=https://github.com/djunekz/unmineable/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=b82b0be329003a53667fde8c22e1385963caf97446a03e07c06089883d35cb36
TERMUX_PKG_DEPENDS="cmake, make, clang, libuv, openssl, build-essential"
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
