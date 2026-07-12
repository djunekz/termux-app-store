TERMUX_PKG_HOMEPAGE=https://github.com/Gameye98/Lazymux
TERMUX_PKG_DESCRIPTION="termux tool installer"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+3b4e747
TERMUX_PKG_SRCURL=https://github.com/Gameye98/Lazymux/archive/3b4e747e1bdd10f1240f78018ac8ee6fff6d0379.tar.gz
TERMUX_PKG_SHA256=d30e4ee4e6490b2e6fa288a03f3120426d6bdea53c0f7a04f7d7ec7815e8a5e0

TERMUX_PKG_DEPENDS="python, python-core, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/lazymux"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    cat > "$TERMUX_PREFIX/bin/lazymux" <<'WRAPPER'

cd "${TERMUX_PREFIX}/lib/lazymux" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/lazymux/lazymux.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/lazymux"
    chmod 0755 "$TERMUX_PREFIX/bin/lazymux"
}
