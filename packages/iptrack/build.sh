TERMUX_PKG_HOMEPAGE=https://github.com/droidv1/termool
TERMUX_PKG_DESCRIPTION="Track IP Location With Live Address And Accuracy"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/droidv1/termool/releases/download/v${TERMUX_PKG_VERSION}/iptrack.tar.gz
TERMUX_PKG_SHA256=43c5fe4734ef358fe17659a08b5846682d43f046e880233503f7412ebbdf1238
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
  install -Dm755 iptrack.py $TERMUX_PREFIX/bin/iptrack
}
