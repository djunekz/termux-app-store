TERMUX_PKG_HOMEPAGE=https://github.com/mishakorzik/UserFinder
TERMUX_PKG_DESCRIPTION="userfinder — auto-packaged by termux-build-init"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+a08a9a6
TERMUX_PKG_SRCURL=https://github.com/mishakorzik/UserFinder/archive/a08a9a682b743fae9c84c9794d88b5b0e98946a7.tar.gz
TERMUX_PKG_SHA256=da66d1d975f7325a4ef96ba8fb0641d788d8434e4e0de748423e769dd6bdb1a6

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    install -Dm755 "UserFinder.sh" "$TERMUX_PREFIX/bin/userfinder"
}
