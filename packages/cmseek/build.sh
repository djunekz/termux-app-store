TERMUX_PKG_HOMEPAGE=https://github.com/Tuhinshubhra/CMSeeK
TERMUX_PKG_DESCRIPTION="CMS Detection and Exploitation suite - Scan WordPress, Joomla, Drupal and over 180 other CMSs"
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.1.3
TERMUX_PKG_SRCURL=https://github.com/Tuhinshubhra/CMSeeK/archive/refs/tags/v.1.1.3.tar.gz
TERMUX_PKG_SHA256=2e7562c7d9e131cc0a3623922df92fbfd98dd8e8e6b0321002c4fd5e06531249

TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet VersionDetect cmseekdb deepscans errno requests --break-system-packages 2>/dev/null || true

    local libdir="$TERMUX_PREFIX/lib/cmseek"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    cat > "$TERMUX_PREFIX/bin/cmseek" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/cmseek" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/cmseek/cmseek.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/cmseek"
    chmod 0755 "$TERMUX_PREFIX/bin/cmseek"
}
