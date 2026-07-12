TERMUX_PKG_HOMEPAGE=https://github.com/makefu/dnsmap
TERMUX_PKG_DESCRIPTION="fork of http://code.google.com/p/dnsmap/source/checkout"
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+d2f89e0
TERMUX_PKG_SRCURL=https://github.com/makefu/dnsmap/archive/d2f89e0e97969961d53e2222839cdd079d7b4ed2.tar.gz
TERMUX_PKG_SHA256=65bdf7f1f95df1ba1bb28d0b0be52c40b329df4107d8a3d29895824e511eabe3


termux_step_make() {
    if [[ ! -f Makefile && ! -f makefile ]]; then
        echo "[ WARN ] No Makefile found in $(pwd) — skipping make step"
        return 0
    fi

    # Deteksi target build yang tepat dari Makefile:
    # Beberapa project (seperti dbd) pakai target 'unix'/'linux' bukan 'all'
    local _mk_target=""
    local _mk_file="Makefile"
    [[ -f makefile ]] && _mk_file="makefile"

    # Cek apakah ada target yang namanya = pkg
    if grep -qE "^dnsmap[[:space:]]*:" "$_mk_file" 2>/dev/null; then
        _mk_target="dnsmap"
    # Cek target platform: unix/linux/android (umum di C security tools)
    elif grep -qE "^(unix|linux|android)[[:space:]]*:" "$_mk_file" 2>/dev/null; then
        _mk_target=$(grep -E "^(unix|linux|android)[[:space:]]*:" "$_mk_file"             | head -n1 | sed 's/[[:space:]]*:.*//')
    fi

    # Build dengan target yang ditemukan, atau default
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

    # Cek apakah make install pakai PREFIX (bukan hardcoded path)
    local _install_ok=false
    if grep -qE "^install[[:space:]]*:" "$_mk_file" 2>/dev/null; then
        if grep -A5 "^install:" "$_mk_file" 2>/dev/null                 | grep -qE '$\(PREFIX\)|$\(DESTDIR\)|$\(prefix\)'; then
            make install PREFIX="$TERMUX_PREFIX" DESTDIR="" 2>/dev/null                 && _install_ok=true
        fi
    fi

    if [[ "$_install_ok" == true ]]; then
        return 0
    fi

    # Fallback: cari binary hasil build dari flag -o di Makefile
    echo "[ INFO ] make install tidak support PREFIX — mencari binary hasil build..."
    local _bin=""

    # Ambil nama binary dari flag -o di Makefile
    local _mk_binary
    _mk_binary=$(grep -oE '\-o[[:space:]]+[a-zA-Z0-9_-]+' "$_mk_file" 2>/dev/null         | grep -viE '\-o[[:space:]]+(\.o|\.exe|.*\.o)'         | head -n1 | awk '{print $2}' || true)

    # Cek kandidat binary: dari Makefile -o, lalu nama pkg, lalu semua executable
    for _candidate in "$_mk_binary" "dnsmap" "dnsmap.out" "dnsmap-bin"; do
        [[ -z "$_candidate" ]] && continue
        if [[ -f "$_candidate" && -x "$_candidate" ]]; then
            _bin="$_candidate"; break
        fi
    done

    # Jika masih tidak ketemu, scan semua executable di direktori
    if [[ -z "$_bin" ]]; then
        _bin=$(find . -maxdepth 1 -type f -perm /111             ! -name "*.sh" ! -name "*.py" ! -name "*.pl"             ! -name "Makefile" ! -name "makefile" ! -name "configure"             ! -name "*.c" ! -name "*.h" ! -name "*.o"             2>/dev/null | head -n1 || true)
    fi

    if [[ -n "$_bin" ]]; then
        echo "[ INFO ] Binary ditemukan: $_bin"
        install -Dm755 "$_bin" "$TERMUX_PREFIX/bin/dnsmap"
        echo "[ OK ] Installed: $TERMUX_PREFIX/bin/dnsmap"
    else
        echo "[ WARN ] Binary tidak ditemukan — install manual diperlukan"
        echo "[ WARN ] Edit termux_step_make_install() di build.sh"
        return 1
    fi
}
