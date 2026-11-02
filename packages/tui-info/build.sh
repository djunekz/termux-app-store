TERMUX_PKG_HOMEPAGE=https://github.com/enrilinux/tui-info
TERMUX_PKG_DESCRIPTION="A TUI system information tool for Android/Termux"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@enrilinux"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/enrilinux/tui-info/archive/refs/tags/1.0.0.tar.gz
TERMUX_PKG_SHA256=093866eb613a800427995ba02cb8637a9df3f2a5aff256236f38a8664e0c2a1d
TERMUX_PKG_DEPENDS="ncurses, clang, make"







termux_step_make() {
    if [[ ! -f Makefile && ! -f makefile ]]; then
        echo "[ WARN ] No Makefile found in $(pwd) — skipping make step"
        return 0
    fi

    local _mk_target=""
    local _mk_file="Makefile"
    [[ -f makefile ]] && _mk_file="makefile"

    if grep -qE "^tui-info[[:space:]]*:" "$_mk_file" 2>/dev/null; then
        _mk_target="tui-info"
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

    for _candidate in "$_mk_binary" "tui-info" "tui-info.out" "tui-info-bin"; do
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
        install -Dm755 "$_bin" "$TERMUX_PREFIX/bin/tui-info"
        echo "[ OK ] Installed: $TERMUX_PREFIX/bin/tui-info"
    else
        echo "[ WARN ] Binary tidak ditemukan — install manual diperlukan"
        echo "[ WARN ] Edit termux_step_make_install() di build.sh"
        return 1
    fi
}
