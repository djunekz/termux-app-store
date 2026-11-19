TERMUX_PKG_HOMEPAGE=https://github.com/UltimateHackers/Hash-Buster
TERMUX_PKG_DESCRIPTION="Crack hashes in seconds."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.0
TERMUX_PKG_SRCURL=https://github.com/UltimateHackers/Hash-Buster/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=b6581a0ce55deab0f2fba7c670b00da1e3909bc24db51f0a85d6d47aa8a8cb2c
TERMUX_PKG_DEPENDS="python"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/hash-buster"
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

    cat > "$TERMUX_PREFIX/bin/hash-buster" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
export PYTHONPATH="/data/data/com.termux/files/usr/lib/hash-buster/.pydeps:/data/data/com.termux/files/usr/lib/hash-buster${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "/data/data/com.termux/files/usr/lib/hash-buster/hash.py" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/hash-buster"
}
