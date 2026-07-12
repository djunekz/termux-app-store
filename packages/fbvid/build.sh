TERMUX_PKG_HOMEPAGE=https://github.com/Tuhinshubhra/fbvid
TERMUX_PKG_DESCRIPTION="Facebook Video Downloader (CLI) For Linux Systems Coded in PHP"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+3786551
TERMUX_PKG_SRCURL=https://github.com/Tuhinshubhra/fbvid/archive/37865517a3f13a53acaf0fbc5dbf02f68bab7a01.tar.gz
TERMUX_PKG_SHA256=de8c174dc5bce8ec4c0af8f9939f6b00635b341fe1e5b78303cad73e3e5c03a7

TERMUX_PKG_DEPENDS="php"

termux_step_make_install() {
    mkdir -p "$TERMUX_PREFIX/lib/fbvid"
    cp -r . "$TERMUX_PREFIX/lib/fbvid/"
    cat > "$TERMUX_PREFIX/bin/fbvid" <<'WRAPPER'
#!/usr/bin/env bash
exec php "/data/data/com.termux/files/usr/lib/fbvid/fb.php" "php fbvid fb.php php    3"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/fbvid"
}
