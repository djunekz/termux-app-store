TERMUX_PKG_HOMEPAGE=https://github.com/UndeadSec/GoblinWordGenerator
TERMUX_PKG_DESCRIPTION="Python wordlist generator "
TERMUX_PKG_LICENSE="BSD-3-Clause"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+6afad56
TERMUX_PKG_SRCURL=https://github.com/UndeadSec/GoblinWordGenerator/archive/6afad5658e7bda00441428efeb0ae35cc4397302.tar.gz
TERMUX_PKG_SHA256=f5a51887f2551e533bc3ab495bf95d9d4b1d16394cb8a5298e8389d7cd192e61

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/goblinwordgenerator"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/goblinwordgenerator" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/goblinwordgenerator" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/goblinwordgenerator/goblin.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/goblinwordgenerator"
    chmod 0755 "$TERMUX_PREFIX/bin/goblinwordgenerator"
}
