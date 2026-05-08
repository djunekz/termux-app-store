TERMUX_PKG_HOMEPAGE=https://github.com/peterpt/eternal_scanner
TERMUX_PKG_DESCRIPTION="An internet scanner for exploit CVE-2017-0144 (Eternal Blue) & CVE-2017-0145 (Eternal Romance)"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=2.2
TERMUX_PKG_SRCURL=https://github.com/peterpt/eternal_scanner/archive/refs/tags/2.2.tar.gz
TERMUX_PKG_SHA256=104bf52263192824556afbe5aa061b888310dd8de2afc0ee520d456595db884b

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet impacket --break-system-packages 2>/dev/null || echo "[ WARN ] pip install impacket failed — may be missing at runtime"

    local libdir="$TERMUX_PREFIX/lib/eternal-scanner"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/eternal-scanner" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/eternal-scanner" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/eternal-scanner/mysmb.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/eternal-scanner"
    chmod 0755 "$TERMUX_PREFIX/bin/eternal-scanner"
}
