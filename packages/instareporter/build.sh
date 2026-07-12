TERMUX_PKG_HOMEPAGE=https://github.com/muneebwanee/InstaReporter
TERMUX_PKG_DESCRIPTION="Instagram Mass Reporting Tool"
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+c8e1527
TERMUX_PKG_SRCURL=https://github.com/muneebwanee/InstaReporter/archive/c8e15277c0481f2cefa339b03818c412c0ab3186.tar.gz
TERMUX_PKG_SHA256=d0f3a77fd24ff76e72d3274104d4993f687fbc6f4117754e6ce1ff121372921f

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet asyncio colorama libs proxybroker requests --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/instareporter"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done

    cat > "$TERMUX_PREFIX/bin/instareporter" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/instareporter" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/instareporter/InstaReporter.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/instareporter"
    chmod 0755 "$TERMUX_PREFIX/bin/instareporter"
}
