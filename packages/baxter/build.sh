TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/baxter
TERMUX_PKG_DESCRIPTION="Encrypt and decrypt files termux"
TERMUX_PKG_LICENSE="Apache-2.0"
TERMUX_PKG_MAINTAINER="@djunekz"
TERMUX_PKG_VERSION=1.4.0
TERMUX_PKG_SRCURL=https://github.com/djunekz/baxter/releases/download/v${TERMUX_PKG_VERSION}/baxter-v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=9afaf26be0c206b15c04225f128a85717c665b66305cef5a2b0dc765863b79f0
TERMUX_PKG_DEPENDS="nodejs"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local dest="$TERMUX_PREFIX/lib/node_modules/baxter"
    rm -rf "$dest"
    cp -r "$TERMUX_PKG_SRCDIR"/. "$dest/"

    mkdir -p "$TERMUX_PREFIX/bin"
    local entry="baxter"
    [ -f "$dest/baxter" ] && entry="baxter"
    [ -f "$dest/bin/baxter" ] && entry="bin/baxter"
    [ -f "$dest/src/baxter" ] && entry="src/baxter"

    cat > "$TERMUX_PREFIX/bin/baxter" << WRAPPER
#!/data/data/com.termux/files/usr/bin/bash
exec bash "/data/data/com.termux/files/usr/lib/node_modules/baxter/${entry}" "\$@"
WRAPPER
    chmod +x "$TERMUX_PREFIX/bin/baxter"
}
