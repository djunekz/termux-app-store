TERMUX_PKG_HOMEPAGE=https://github.com/D4Vinci/Clickjacking-Tester
TERMUX_PKG_DESCRIPTION="A python script designed to check if the website if vulnerable of clickjacking and create a poc"
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+d75d5fc
TERMUX_PKG_SRCURL=https://github.com/D4Vinci/Clickjacking-Tester/archive/d75d5fcc62cef0031db9493b30911cd70c9bd606.tar.gz
TERMUX_PKG_SHA256=295aac00657fc24152d67a8c9c3766b24381de5f696f18631aa5b4ce6086336b

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true


    local libdir="$TERMUX_PREFIX/lib/clickjacking-tester"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done



    cat > "$TERMUX_PREFIX/bin/clickjacking-tester" <<'WRAPPER'
#!/usr/bin/env bash
cd "${TERMUX_PREFIX}/lib/clickjacking-tester" || exit 1
exec python3 "${TERMUX_PREFIX}/lib/clickjacking-tester/Clickjacking_Tester.py" "$@"
WRAPPER
    sed -i "s|\${TERMUX_PREFIX}|/data/data/com.termux/files/usr|g" "$TERMUX_PREFIX/bin/clickjacking-tester"
    chmod 0755 "$TERMUX_PREFIX/bin/clickjacking-tester"
}
