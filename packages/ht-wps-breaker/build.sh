TERMUX_PKG_HOMEPAGE=https://github.com/SilentGhostX/HT-WPS-Breaker
TERMUX_PKG_DESCRIPTION="HT-WPS Breaker (High Touch WPS Breaker)"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+e218bdf
TERMUX_PKG_SRCURL=https://github.com/SilentGhostX/HT-WPS-Breaker/archive/e218bdfa34364eabe6de2e982264451d2c597ff5.tar.gz
TERMUX_PKG_SHA256=867c609f5abbe16e64721d559e6615411dd09c45abc834e4c98dd9755093048d

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    install -Dm755 "HT-WB.sh" "$TERMUX_PREFIX/bin/ht-wps-breaker"
}
