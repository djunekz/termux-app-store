TERMUX_PKG_HOMEPAGE=https://github.com/ruped24/killchain
TERMUX_PKG_DESCRIPTION="killchain — auto-packaged by termux-build-init"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+fef616f
TERMUX_PKG_SRCURL=https://github.com/ruped24/killchain/archive/fef616f66ae18b9855cdd7f58a586551fcd3cdcb.tar.gz
TERMUX_PKG_SHA256=c6b0bd9887ca2bb9ded7084ec7a3e907d5625c272de1df6db92789461323c609

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/killchain"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/killchain" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/killchain" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/killchain/killchain.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/killchain"
    chmod 0755 "$TERMUX_PREFIX/bin/killchain"
}
