TERMUX_PKG_HOMEPAGE=https://github.com/Gameye98/Auxscan
TERMUX_PKG_DESCRIPTION="Vulnerability Scanner to automate certain tasks"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+4551c2f
TERMUX_PKG_SRCURL=https://github.com/Gameye98/Auxscan/archive/4551c2f418070217a33297bdd981d6fddf1a6492.tar.gz
TERMUX_PKG_SHA256=44c08fa9d4e2d1b2d8bb5bac1118f5915ff801b58d93716214172d859144e11f

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet requests --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/auxscan"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done

    cat > "$TERMUX_PREFIX/bin/auxscan" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/auxscan" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/auxscan/auxscan.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/auxscan"
    chmod 0755 "$TERMUX_PREFIX/bin/auxscan"
}
