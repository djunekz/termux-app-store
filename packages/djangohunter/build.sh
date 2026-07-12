TERMUX_PKG_HOMEPAGE=https://github.com/6IX7ine/djangohunter
TERMUX_PKG_DESCRIPTION="djangohunter — auto-packaged by termux-build-init"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+a5a715e
TERMUX_PKG_SRCURL=https://github.com/6IX7ine/djangohunter/archive/a5a715ee393f463dddf48d1b893eaaede241c58a.tar.gz
TERMUX_PKG_SHA256=1d753e468b7acb3c856079a0316c6c001cf23e36d57134caadb33dbf81ee7ada

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet beautifulsoup4 pyfiglet requests shodan --break-system-packages 2>/dev/null || true
    local libdir="$TERMUX_PREFIX/lib/djangohunter"
    pip install . --prefix="$TERMUX_PREFIX" --no-deps --break-system-packages 2>/dev/null \
        || pip install . --prefix="$TERMUX_PREFIX" --no-deps --no-build-isolation --break-system-packages || {
            echo "pip failed — falling back to manual install"
            mkdir -p "$libdir"
            cp -r . "$libdir/"
        }

    find "$libdir" -type d 2>/dev/null | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done


}
