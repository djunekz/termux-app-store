TERMUX_PKG_HOMEPAGE=https://github.com/Dionach/CMSmap
TERMUX_PKG_DESCRIPTION="CMSmap is a python open source CMS scanner that automates the process of detecting security flaws of the most popular CMSs. "
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+59dd0e2
TERMUX_PKG_SRCURL=https://github.com/Dionach/CMSmap/archive/59dd0e2b3b0c751c6da2b0565374ab83c736b0e6.tar.gz
TERMUX_PKG_SHA256=37644d93c791528c83f069a8c9fee78ebba0527ef1cf35b5752aa5037561fbc2

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet cmsmap package setuptools --break-system-packages 2>/dev/null || true
    pip install . --prefix="$TERMUX_PREFIX" --no-deps --break-system-packages 2>/dev/null \
        || pip install . --prefix="$TERMUX_PREFIX" --no-deps --no-build-isolation --break-system-packages || {
            echo "pip failed — falling back to manual install"
            mkdir -p "$TERMUX_PREFIX/lib/cmsmap"
            cp -r . "$TERMUX_PREFIX/lib/cmsmap/"
        }
}
