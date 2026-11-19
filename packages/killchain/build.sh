TERMUX_PKG_HOMEPAGE=https://github.com/ruped24/killchain
TERMUX_PKG_DESCRIPTION='A unified console to perform the "kill chain" stages of attacks.'
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+fef616f
TERMUX_PKG_SRCURL=https://github.com/ruped24/killchain/archive/fef616f66ae18b9855cdd7f58a586551fcd3cdcb.tar.gz
TERMUX_PKG_SHA256=c6b0bd9887ca2bb9ded7084ec7a3e907d5625c272de1df6db92789461323c609
TERMUX_PKG_DEPENDS="python"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/killchain"
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

    cat > "$TERMUX_PREFIX/bin/killchain" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
export PYTHONPATH="/data/data/com.termux/files/usr/lib/killchain/.pydeps:/data/data/com.termux/files/usr/lib/killchain${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "/data/data/com.termux/files/usr/lib/killchain/killchain.py" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/killchain"
}
