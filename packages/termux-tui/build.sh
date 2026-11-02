TERMUX_PKG_HOMEPAGE=https://github.com/opsonusdh/Termux-TUI
TERMUX_PKG_DESCRIPTION="A futuristic Jarvis-style terminal dashboard for Termux"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@opsonusdh"
TERMUX_PKG_VERSION=2.9.5
TERMUX_PKG_SRCURL=https://github.com/opsonusdh/Termux-TUI/archive/refs/tags/v${TERMUX_PKG_VERSION}.zip
TERMUX_PKG_SHA256=ae189b47863f724ccddf8ea77de7707a1840a94d613658d5c90b988c13b4adba

TERMUX_PKG_DEPENDS="python, python-pip, python-yt-dlp"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet rich speedtest-cli textual --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/termux-tui"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done

    cat > "$TERMUX_PREFIX/bin/termux-tui" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/termux-tui" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/termux-tui/main.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/termux-tui"
    chmod 0755 "$TERMUX_PREFIX/bin/termux-tui"
}
