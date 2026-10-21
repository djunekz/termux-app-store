TERMUX_PKG_HOMEPAGE=https://github.com/Mebus/cupp
TERMUX_PKG_DESCRIPTION="cupp — auto-packaged by termux-build-init"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+b77f1ae
TERMUX_PKG_SRCURL=https://github.com/Mebus/cupp/archive/b77f1ae66c10ab2d0fa09c67017949fb5ba187aa.tar.gz
TERMUX_PKG_SHA256=2b88e3df1af6df952dfe6b08d151fe017f527388e35dd44940b4e6bcfc16d918

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/cupp"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/cupp" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/cupp" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/cupp/cupp.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/cupp"
    chmod 0755 "$TERMUX_PREFIX/bin/cupp"
}
