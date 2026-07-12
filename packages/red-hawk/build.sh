TERMUX_PKG_HOMEPAGE=https://github.com/Tuhinshubhra/RED_HAWK
TERMUX_PKG_DESCRIPTION="All in one tool for Information Gathering, Vulnerability Scanning and Crawling. A must have tool for all penetration testers"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+fa54e23
TERMUX_PKG_SRCURL=https://github.com/Tuhinshubhra/RED_HAWK/archive/fa54e23a97bd025b735a53de3445a9c3dfd96d01.tar.gz
TERMUX_PKG_SHA256=ac7bb90ca2951db8bd3c082863bbf62bbccbc1fe91f02c723209d8812b0c074c

TERMUX_PKG_DEPENDS="php"

termux_step_make_install() {
    mkdir -p "$TERMUX_PREFIX/lib/red-hawk"
    cp -r . "$TERMUX_PREFIX/lib/red-hawk/"
    cat > "$TERMUX_PREFIX/bin/red-hawk" <<'WRAPPER'
#!/usr/bin/env bash
exec php "/data/data/com.termux/files/usr/lib/red-hawk/rhawk.php" "php red-hawk rhawk.php php   "
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/red-hawk"
}
