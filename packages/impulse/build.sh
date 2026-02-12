TERMUX_PKG_HOMEPAGE=https://github.com/username/Impulse
TERMUX_PKG_DESCRIPTION="Denial-of-Service ToolKit with multiple attack methods"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/droidv1/termool/releases/download/v${TERMUX_PKG_VERSION}/impulse.tar.gz
TERMUX_PKG_SHA256=d2f1c7310b1b0503d1e88aabb29eec686acc6db52eb6585102f4b129a919ee2f
TERMUX_PKG_DEPENDS="python"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    mkdir -p $TERMUX_PREFIX/bin

    install -m 0755 impulse.py $TERMUX_PREFIX/bin/impulse

    cp -r tools $TERMUX_PREFIX/share/impulse

    cp requirements.txt $TERMUX_PREFIX/share/impulse/
}
