TERMUX_PKG_HOMEPAGE=https://github.com/Souhardya/Zerodoor
TERMUX_PKG_DESCRIPTION="A script written lazily for generating cross-platform  backdoors on the go :) "
TERMUX_PKG_LICENSE="NOASSERTION"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+e287b64
TERMUX_PKG_SRCURL=https://github.com/Souhardya/Zerodoor/archive/e287b6474ca497e18a12991851bfc911a6cf28a7.tar.gz
TERMUX_PKG_SHA256=95f3fa20943d79c60fdd9974e604848822e04d0c8f4ab6658fc68d07d54ff755

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/zerodoor"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/zerodoor" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/zerodoor" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/zerodoor/zerodoor.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/zerodoor"
    chmod 0755 "$TERMUX_PREFIX/bin/zerodoor"
}
