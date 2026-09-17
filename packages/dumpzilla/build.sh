TERMUX_PKG_HOMEPAGE=https://gitlab.com/groups/kalilinux/packages
TERMUX_PKG_DESCRIPTION="dumpzilla packaging for Kali Linux"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://gitlab.com/kalilinux/packages/dumpzilla/-/archive/kali/master/dumpzilla-kali/master.tar.gz
TERMUX_PKG_SHA256=ba9d8d93a49603eccbcc6b85dda7a2f38e0f4e47d59bdede0760f2f6177b4d3d

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/dumpzilla"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/dumpzilla" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/dumpzilla" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/dumpzilla/dumpzilla.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/dumpzilla"
    chmod 0755 "$TERMUX_PREFIX/bin/dumpzilla"
}
