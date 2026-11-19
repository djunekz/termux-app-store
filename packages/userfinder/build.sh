TERMUX_PKG_HOMEPAGE=https://github.com/mishakorzik/UserFinder
TERMUX_PKG_DESCRIPTION="OSINT tool for finding profiles by username"
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0
TERMUX_PKG_SRCURL=https://github.com/mishakorzik/UserFinder/archive/a08a9a682b743fae9c84c9794d88b5b0e98946a7.tar.gz
TERMUX_PKG_SHA256=da66d1d975f7325a4ef96ba8fb0641d788d8434e4e0de748423e769dd6bdb1a6
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/userfinder"
    mkdir -p "$libdir"
    cp -r . "$libdir/"
    chmod 0755 "$libdir/UserFinder.sh"

    cat > "$TERMUX_PREFIX/bin/userfinder" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
exec bash "/data/data/com.termux/files/usr/lib/userfinder/UserFinder.sh" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/userfinder"
}

