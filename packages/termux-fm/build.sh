TERMUX_PKG_HOMEPAGE=https://github.com/enrilinux/termux-fm
TERMUX_PKG_DESCRIPTION="TUI file manager root for Termux"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/enrilinux/termux-fm/archive/refs/tags/1.0.0.tar.gz
TERMUX_PKG_SHA256=bd273c29f85cf3361f64714afa370cc361041e16dd088187e0d7cbc67c04b92e
TERMUX_PKG_DEPENDS="ncurses, libandroid-selinux, clang, make"


termux_step_make() {
    if [[ ! -f Makefile && ! -f makefile ]]; then
        echo "[ WARN ] No Makefile found in $(pwd) — skipping make step"
        return 0
    fi

    local _mk_target=""
    local _mk_file="Makefile"
    [[ -f makefile ]] && _mk_file="makefile"

    if grep -qE "^termux-fm[[:space:]]*:" "$_mk_file" 2>/dev/null; then
        _mk_target="termux-fm"
    elif grep -qE "^(unix|linux|android)[[:space:]]*:" "$_mk_file" 2>/dev/null; then
        _mk_target=$(grep -E "^(unix|linux|android)[[:space:]]*:" "$_mk_file"             | head -n1 | sed 's/[[:space:]]*:.*//')
    fi

    if [[ -n "$_mk_target" ]]; then
        make -j"$(nproc)" PREFIX="$TERMUX_PREFIX" "$_mk_target" 2>/dev/null             || make PREFIX="$TERMUX_PREFIX" "$_mk_target"
    else
        make -j"$(nproc)" PREFIX="$TERMUX_PREFIX" 2>/dev/null             || make PREFIX="$TERMUX_PREFIX"
    fi
}

termux_step_make_install() {
    if [[ ! -f Makefile && ! -f makefile ]]; then
        echo "[ WARN ] No Makefile found — skipping install step"
        return 1
    fi

    local _mk_file="Makefile"
    [[ -f makefile ]] && _mk_file="makefile"

    local _install_ok=false
    if grep -qE "^install[[:space:]]*:" "$_mk_file" 2>/dev/null; then
        if grep -A5 "^install:" "$_mk_file" 2>/dev/null                 | grep -qE '$\(PREFIX\)|$\(DESTDIR\)|$\(prefix\)'; then
            make install PREFIX="$TERMUX_PREFIX" DESTDIR="" 2>/dev/null                 && _install_ok=true
        fi
    fi

    if [[ "$_install_ok" == true ]]; then
        return 0
    fi

    echo "[ INFO ] make install tidak support PREFIX — mencari binary hasil build..."
    local _bin=""

    local _mk_binary
    _mk_binary=$(grep -oE '\-o[[:space:]]+[a-zA-Z0-9_-]+' "$_mk_file" 2>/dev/null         | grep -viE '\-o[[:space:]]+(\.o|\.exe|.*\.o)'         | head -n1 | awk '{print $2}' || true)

    for _candidate in "$_mk_binary" "termux-fm" "termux-fm.out" "termux-fm-bin"; do
        [[ -z "$_candidate" ]] && continue
        if [[ -f "$_candidate" && -x "$_candidate" ]]; then
            _bin="$_candidate"; break
        fi
    done

    if [[ -z "$_bin" ]]; then
        _bin=$(find . -maxdepth 1 -type f -perm /111             ! -name "*.sh" ! -name "*.py" ! -name "*.pl"             ! -name "Makefile" ! -name "makefile" ! -name "configure"             ! -name "*.c" ! -name "*.h" ! -name "*.o"             2>/dev/null | head -n1 || true)
    fi

    if [[ -n "$_bin" ]]; then
        echo "[ INFO ] Binary ditemukan: $_bin"
        install -Dm755 "$_bin" "$TERMUX_PREFIX/bin/termux-fm"
        echo "[ OK ] Installed: $TERMUX_PREFIX/bin/termux-fm"
    else
        echo "[ WARN ] Binary tidak ditemukan — install manual diperlukan"
        echo "[ WARN ] Edit termux_step_make_install() di build.sh"
        return 1
    fi
}
