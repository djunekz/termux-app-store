TERMUX_PKG_HOMEPAGE=https://github.com/s0md3v/Photon
TERMUX_PKG_DESCRIPTION="Incredibly fast crawler designed for OSINT."
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.3.0
TERMUX_PKG_SRCURL=https://github.com/s0md3v/Photon/archive/refs/tags/v1.3.0.tar.gz
TERMUX_PKG_SHA256=99a8bc0f52b46a37acd8e0877ea4231ea7b3d9f8b603c90c6641837117d7666f

TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet requests --break-system-packages 2>/dev/null || echo "[ WARN ] pip install requests failed — may be missing at runtime"
    pip install --quiet tld --break-system-packages 2>/dev/null || echo "[ WARN ] pip install tld failed — may be missing at runtime"
    pip install --quiet urllib3 --break-system-packages 2>/dev/null || echo "[ WARN ] pip install urllib3 failed — may be missing at runtime"

    local libdir="$TERMUX_PREFIX/lib/photon"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/photon" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/photon" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/photon/photon.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/photon"
    chmod 0755 "$TERMUX_PREFIX/bin/photon"
}
