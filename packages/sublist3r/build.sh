TERMUX_PKG_HOMEPAGE=https://github.com/aboul3la/Sublist3r
TERMUX_PKG_DESCRIPTION="Fast subdomains enumeration tool for penetration testers"
TERMUX_PKG_LICENSE="GPL-2.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.1
TERMUX_PKG_SRCURL=https://github.com/aboul3la/Sublist3r/archive/refs/tags/1.1.tar.gz
TERMUX_PKG_SHA256=7bb915954bb0db9a8f0a3be2a38bc77e932174be5e8d02c7d5dd4bc56ec30195

TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet argparse dnspython requests --break-system-packages 2>/dev/null || true
    local libdir="$TERMUX_PREFIX/lib/sublist3r"
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

    if grep -rlE         'print [^(]|^\s*print$|except \w+,\s*\w+:|^from __future__ import|basestring|xrange|raw_input'         "$libdir" --include="*.py" 2>/dev/null | grep -q .; then
        echo "  [2to3] Python 2 syntax detected — running 2to3 auto-conversion..."
        if command -v 2to3 >/dev/null 2>&1; then
            2to3 --write --nobackups -n "$libdir" 2>/dev/null || true
            echo "  [2to3] Conversion complete"
        fi
    fi


}
