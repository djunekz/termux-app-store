TERMUX_PKG_HOMEPAGE=https://github.com/D4Vinci/elpscrk
TERMUX_PKG_DESCRIPTION="An Intelligent wordlist generator based on user profiling, permutations, and statistics. (Named after the same tool in Mr.Robot series S01E01)"
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/D4Vinci/elpscrk/archive/refs/heads/master.tar.gz
TERMUX_PKG_SHA256=14077506c401e1c899103273c1691e743cb9d15731949841c977b6c1ac2003ac

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools, python-psutil"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet click --break-system-packages 2>/dev/null || echo "[ WARN ] pip install click failed — may be missing at runtime"
    pip install --quiet colorama --break-system-packages 2>/dev/null || echo "[ WARN ] pip install colorama failed — may be missing at runtime"
    pip install --quiet phonenumbers --break-system-packages 2>/dev/null || echo "[ WARN ] pip install phonenumbers failed — may be missing at runtime"
    pip install --quiet psutil --break-system-packages 2>/dev/null || echo "[ WARN ] pip install psutil failed — may be missing at runtime"

    local libdir="$TERMUX_PREFIX/lib/elpscrk"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/elpscrk" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/elpscrk" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/elpscrk/elpscrk.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/elpscrk"
    chmod 0755 "$TERMUX_PREFIX/bin/elpscrk"
}
