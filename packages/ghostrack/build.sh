TERMUX_PKG_HOMEPAGE=https://github.com/HunxByts/GhostTrack
TERMUX_PKG_DESCRIPTION="Useful tool to track location or mobile number"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/djunekz/archive/releases/download/v${TERMUX_PKG_VERSION}/ghostrack.tar.gz
TERMUX_PKG_SHA256=43c5fe4734ef358fe17659a08b5846682d43f046e880233503f7412ebbdf1238
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
  install -Dm755 ghostrack.py $TERMUX_PREFIX/bin/ghostrack
}

