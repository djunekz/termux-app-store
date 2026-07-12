TERMUX_PKG_HOMEPAGE=https://github.com/TermuxHackz/Hammer
TERMUX_PKG_DESCRIPTION="Ddos attack tool for termux"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+e63fbd7
TERMUX_PKG_SRCURL=https://github.com/TermuxHackz/Hammer/archive/e63fbd772394f14ee48342518845c479878fb16a.tar.gz
TERMUX_PKG_SHA256=68485d03070aef653cf875afe57608777ccde31c1eabde71a2628a967dc0a3f6

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/hammer"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    cat > "$TERMUX_PREFIX/bin/hammer" <<'WRAPPER'
#!/usr/bin/env bash
# cd ke libdir dulu agar relative path (./config.json, dll) bisa ditemukan
cd "${TERMUX_PREFIX}/lib/hammer" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/hammer/hammer.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/hammer"
    chmod 0755 "$TERMUX_PREFIX/bin/hammer"
}
