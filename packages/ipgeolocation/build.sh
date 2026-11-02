TERMUX_PKG_HOMEPAGE=https://github.com/maldevel/IPGeoLocation
TERMUX_PKG_DESCRIPTION="Retrieve IP Geolocation information"
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=2.0.4
TERMUX_PKG_SRCURL=https://github.com/maldevel/IPGeoLocation/archive/refs/tags/2.0.4.tar.gz
TERMUX_PKG_SHA256=fabc086113f89f9e8fe1ed7fbfec776780d43df63c67401c48b8f36948fa9ecb

TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet colorama core termcolor --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/ipgeolocation"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/ipgeolocation" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/ipgeolocation" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/ipgeolocation/ipgeolocation.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/ipgeolocation"
    chmod 0755 "$TERMUX_PREFIX/bin/ipgeolocation"
}
