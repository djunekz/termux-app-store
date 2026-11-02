TERMUX_PKG_HOMEPAGE=https://github.com/s0md3v/XSStrike
TERMUX_PKG_DESCRIPTION="Most advanced XSS scanner."
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.1.6
TERMUX_PKG_SRCURL=https://github.com/s0md3v/XSStrike/archive/refs/tags/3.1.6.tar.gz
TERMUX_PKG_SHA256=d8c6c2f4dbcee5836d552cc193cad4b6dfa6c9a9471680d5d2f2b3d278b021f2

TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet fuzzywuzzy requests tld urllib3 --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/xsstrike"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/xsstrike" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/xsstrike" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/xsstrike/xsstrike.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/xsstrike"
    chmod 0755 "$TERMUX_PREFIX/bin/xsstrike"
}
