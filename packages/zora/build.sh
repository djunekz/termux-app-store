TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/zora
TERMUX_PKG_DESCRIPTION="A modular OSINT and network-reconnaissance toolkit"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=2.2.0
TERMUX_PKG_SRCURL=https://github.com/djunekz/zora/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=ed8a2589051cd38e14f54108bd268770a5e69d25e26a09efc916d2d36eaa571c
TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/zora"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    if [ -f requirements.txt ]; then
        pip install --no-cache-dir --disable-pip-version-check --target "$libdir/.pydeps" -r requirements.txt \
            || sed 's/[[:space:]]*#.*//' requirements.txt | grep -vE '^[[:space:]]*(-|$)' | while read -r _req; do
                pip install --no-cache-dir --disable-pip-version-check --target "$libdir/.pydeps" "$_req" \
                    || pip show "${_req%%[<>=!~;[ ]*}" > /dev/null 2>&1 \
                    || { echo "Missing Python dependency: $_req" >&2; exit 1; }
            done
    fi

    cat > "$TERMUX_PREFIX/bin/zora" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
export PYTHONPATH="/data/data/com.termux/files/usr/lib/zora/.pydeps:/data/data/com.termux/files/usr/lib/zora${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "/data/data/com.termux/files/usr/lib/zora/zora/main.py" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/zora"
}
