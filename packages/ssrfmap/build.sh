TERMUX_PKG_HOMEPAGE=https://github.com/swisskyrepo/SSRFmap
TERMUX_PKG_DESCRIPTION="Automatic SSRF fuzzer and exploitation tool"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+69103b2
TERMUX_PKG_SRCURL=https://github.com/swisskyrepo/SSRFmap/archive/69103b27f5898d9707630dc572798df63727b90f.tar.gz
TERMUX_PKG_SHA256=c1ef86b06978c036c1312f99719e246b479b520fd9fdae87c9ad2a9aa900efe2

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet Flask --break-system-packages 2>/dev/null || echo "[ WARN ] pip install Flask failed — may be missing at runtime"
    pip install --quiet _thread --break-system-packages 2>/dev/null || echo "[ WARN ] pip install _thread failed — may be missing at runtime"
    pip install --quiet dns --break-system-packages 2>/dev/null || echo "[ WARN ] pip install dns failed — may be missing at runtime"
    pip install --quiet dnslib --break-system-packages 2>/dev/null || echo "[ WARN ] pip install dnslib failed — may be missing at runtime"
    pip install --quiet dnspython --break-system-packages 2>/dev/null || echo "[ WARN ] pip install dnspython failed — may be missing at runtime"
    pip install --quiet flask --break-system-packages 2>/dev/null || echo "[ WARN ] pip install flask failed — may be missing at runtime"
    pip install --quiet requests --break-system-packages 2>/dev/null || echo "[ WARN ] pip install requests failed — may be missing at runtime"
    pip install --quiet urllib3 --break-system-packages 2>/dev/null || echo "[ WARN ] pip install urllib3 failed — may be missing at runtime"

    local libdir="$TERMUX_PREFIX/lib/ssrfmap"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/ssrfmap" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/ssrfmap" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/ssrfmap/ssrfmap.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/ssrfmap"
    chmod 0755 "$TERMUX_PREFIX/bin/ssrfmap"
}
