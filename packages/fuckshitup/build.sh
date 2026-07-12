TERMUX_PKG_HOMEPAGE=https://github.com/Smaash/fuckshitup
TERMUX_PKG_DESCRIPTION="php-cli vulnerability scanner"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+91e555c
TERMUX_PKG_SRCURL=https://github.com/Smaash/fuckshitup/archive/91e555c704fe48f26b71392c77a658f463014150.tar.gz
TERMUX_PKG_SHA256=5b0931fd97faf4005cb305c05443a01faebe8e601a5b5105a18b23a334c600db

TERMUX_PKG_DEPENDS="php"

termux_step_make_install() {
    mkdir -p "$TERMUX_PREFIX/lib/fuckshitup"
    cp -r . "$TERMUX_PREFIX/lib/fuckshitup/"
    cat > "$TERMUX_PREFIX/bin/fuckshitup" <<'WRAPPER'
#!/usr/bin/env bash
exec php "/data/data/com.termux/files/usr/lib/fuckshitup/fsu.php" "php fuckshitup fsu.php php    3"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/fuckshitup"
}
