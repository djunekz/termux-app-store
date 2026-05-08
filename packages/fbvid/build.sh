TERMUX_PKG_HOMEPAGE=https://github.com/Tuhinshubhra/fbvid
TERMUX_PKG_DESCRIPTION="Facebook Video Downloader (CLI) For Linux Systems Coded in PHP"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/Tuhinshubhra/fbvid/archive/refs/heads/master.tar.gz
TERMUX_PKG_SHA256=43ca23d947d52f32b330161c7700d5f5ce52c16018ec98e2aac37b0f2ded6edb

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
