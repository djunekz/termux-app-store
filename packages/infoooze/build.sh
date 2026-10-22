TERMUX_PKG_HOMEPAGE=https://github.com/devxprite/infoooze
TERMUX_PKG_DESCRIPTION="A OSINT tool which helps you to quickly find information effectively."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.2.2
TERMUX_PKG_SRCURL=https://api.github.com/repos/devxprite/infoooze/tarball/v1.2.2
TERMUX_PKG_SHA256=4a02d4b6e878f9abb76d340574199bf4b6bf4eb0edb252e7eb6967903e121d62
TERMUX_PKG_DEPENDS="nodejs"

termux_step_make_install() {
    local dest="$TERMUX_PREFIX/lib/node_modules/infoooze"
    rm -rf "$dest"
    cp -r "${TERMUX_PKG_SRCDIR:-$PWD}" "$dest"
    cd "$dest"
    npm install --production

    mkdir -p "$TERMUX_PREFIX/bin"
    cat > "$TERMUX_PREFIX/bin/infoooze" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
exec node /data/data/com.termux/files/usr/lib/node_modules/infoooze/index.js "$@"
WRAPPER
    chmod +x "$TERMUX_PREFIX/bin/infoooze"
}
