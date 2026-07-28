TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/termux-sync
TERMUX_PKG_DESCRIPTION="OpenSource Backup and restore your entire Termux environment across devices."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.2.4
TERMUX_PKG_SRCURL=https://github.com/djunekz/termux-sync/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=59a061d919e3abb83b07c9169fd417bd4a86ac1244194de8d3caf584e28071a9

TERMUX_PKG_DEPENDS="git, python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/termux-sync"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done


    if [[ -f "$libdir/install.sh" ]]; then
        echo "[ INFO ] Running install.sh..."
        (cd "$libdir" && bash install.sh 2>/dev/null || true)
        echo "[ INFO ] Installer selesai"
    fi

    cat > "$TERMUX_PREFIX/bin/termux-sync" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/termux-sync" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/termux-sync/termux-sync.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/termux-sync"
    chmod 0755 "$TERMUX_PREFIX/bin/termux-sync"
}
