TERMUX_PKG_HOMEPAGE=https://github.com/b3-v3r/Hunner
TERMUX_PKG_DESCRIPTION="Hacking framework"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+5e46a45
TERMUX_PKG_SRCURL=https://github.com/b3-v3r/Hunner/archive/5e46a4532469df816e0a4329671cb76fb1300d74.tar.gz
TERMUX_PKG_SHA256=e6f6ebfae6e0c442fb4d6c489c72b9d446fc2e87d08e9acc5a6a3b5d5151c278

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet pexpect --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/hunner"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/hunner" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/hunner" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/hunner/hunner.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/hunner"
    chmod 0755 "$TERMUX_PREFIX/bin/hunner"
}
