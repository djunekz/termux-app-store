TERMUX_PKG_HOMEPAGE=http://www.behindthefirewalls.com/
TERMUX_PKG_DESCRIPTION="Parsero | Robots.txt audit tool"
TERMUX_PKG_LICENSE="GPL-2.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+e5b585a
TERMUX_PKG_SRCURL=https://github.com/behindthefirewalls/Parsero/archive/e5b585a19b79426975a825cafa4cc8a353cd267e.tar.gz
TERMUX_PKG_SHA256=1780ddf21a5e51ef192529e108be10d516df7ad3a6822676b49abe36415259ef

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet beautifulsoup4 pip setuptools urllib3 --break-system-packages 2>/dev/null || true
    local libdir="$TERMUX_PREFIX/lib/parsero"
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
