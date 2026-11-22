TERMUX_PKG_HOMEPAGE=https://djunekz.github.io
TERMUX_PKG_DESCRIPTION="Bundle a Python script and its dependencies into a single ELF binary for Termux/Android. Embedded loader, zlib-compressed payload, optional UPX and isolated mode."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=2.1.0
TERMUX_PKG_SRCURL=https://github.com/djunekz/zorabuilder/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=f689991dca3660ffb83ed2eb41658d469ea1eecca8c6d3b5ad6164b50d2d6abf
TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/zorabuilder"
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

    cat > "$TERMUX_PREFIX/bin/zorabuilder" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
export PYTHONPATH="/data/data/com.termux/files/usr/lib/zorabuilder/.pydeps:/data/data/com.termux/files/usr/lib/zorabuilder${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "/data/data/com.termux/files/usr/lib/zorabuilder/zorabuilder.py" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/zorabuilder"
}
