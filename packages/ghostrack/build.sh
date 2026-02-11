TERMUX_PKG_HOMEPAGE=https://github.com/HunxByts/GhostTrack
TERMUX_PKG_DESCRIPTION="Useful tool to track location or mobile number"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/droidv1/termool/releases/download/v${TERMUX_PKG_VERSION}/ghostrack.tar.gz
TERMUX_PKG_SHA256=93f935f38efffc574c44f2c73e2ef90064747efed92c0765b0fd7f1bc07ea662
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
  install -Dm755 ghostrack.py $TERMUX_PREFIX/bin/ghostrack
}

