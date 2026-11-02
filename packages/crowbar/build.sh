TERMUX_PKG_HOMEPAGE=https://github.com/galkan/crowbar
TERMUX_PKG_DESCRIPTION="Crowbar is brute forcing tool that can be used during penetration tests. It is developed to support protocols that are not currently supported by thc-hydra and other popular brute forcing tools. "
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=4.2
TERMUX_PKG_SRCURL=https://github.com/galkan/crowbar/archive/refs/tags/v4.2.tar.gz
TERMUX_PKG_SHA256=b65cd4c39e50a4311d075f9c219b2ebb7ba06a48f8e4e5cb0082d48412bcb23d

TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --prefix="$TERMUX_PREFIX" --break-system-packages 2>/dev/null || true
    pip install --quiet paramiko setuptools --prefix="$TERMUX_PREFIX" --break-system-packages 2>/dev/null || true
    local libdir="$TERMUX_PREFIX/lib/crowbar"
    export PYTHONPATH="$TERMUX_PREFIX/lib/python$(python3 -c 'import sys; print("%d.%d" % sys.version_info[:2])')/site-packages:${PYTHONPATH:-}"
    pip install . --prefix="$TERMUX_PREFIX" --no-deps --break-system-packages 2>/dev/null \
        || pip install . --prefix="$TERMUX_PREFIX" --no-deps --no-build-isolation --break-system-packages || {
            echo "pip failed — falling back to manual install"
            mkdir -p "$libdir"
            cp -r . "$libdir/"
        }

    find "$libdir" -type d 2>/dev/null | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done

    cat > "$TERMUX_PREFIX/bin/crowbar" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/crowbar" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/crowbar/crowbar.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/crowbar"
    chmod 0755 "$TERMUX_PREFIX/bin/crowbar"
}
