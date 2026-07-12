TERMUX_PKG_HOMEPAGE=https://github.com/HunxByts/GhostTrack
TERMUX_PKG_DESCRIPTION="Useful tool to track location or mobile number"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+a5cb8ad
TERMUX_PKG_SRCURL=https://github.com/HunxByts/GhostTrack/archive/a5cb8ad4c08acd803f166fb067b7dac724d6cb3d.tar.gz
TERMUX_PKG_SHA256=19c209bca69ecac3a775b8961170a74f0afde555357be6894148c9a366515db6

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet phonenumbers requests --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/ghosttrack"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/ghosttrack" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/ghosttrack" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/ghosttrack/GhostTR.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/ghosttrack"
    chmod 0755 "$TERMUX_PREFIX/bin/ghosttrack"
}
