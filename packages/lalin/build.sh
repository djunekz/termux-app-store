TERMUX_PKG_HOMEPAGE=https://github.com/Screetsec/LALIN
TERMUX_PKG_DESCRIPTION="this script automatically install any package for pentest with uptodate tools , and lazy command for run the tools like lazynmap , install another and update to new #actually for lazy people hahaha #and Lalin is remake the lazykali with fixed bugs , added new features and uptodate tools . It's compatible with the latest release of Kali (Rolling)"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+ab55979
TERMUX_PKG_SRCURL=https://github.com/Screetsec/LALIN/archive/ab559794057a31ba9e38a4200073e5ca2d1f429a.tar.gz
TERMUX_PKG_SHA256=482d6f88dbf07f82693372ddcea0444779b67f525d65fc50cb45be0c4aa1128a

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    install -Dm755 "Lalin.sh" "$TERMUX_PREFIX/bin/lalin"
}
