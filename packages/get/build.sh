TERMUX_PKG_HOMEPAGE=https://github.com/peterpt/get
TERMUX_PKG_DESCRIPTION="Get is a simple script to retrieve an ip from hostname or vice-versa ."
TERMUX_PKG_LICENSE="UNKNOWN"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+14b0bc3
TERMUX_PKG_SRCURL=https://github.com/peterpt/get/archive/14b0bc3f922abbe3d11087051b9b9c06f37284f4.tar.gz
TERMUX_PKG_SHA256=4d28e816c7ecbdf3d2a812e3dbd6c7639c7a03eca35e0c01700d0ac46419efe7

TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/get"

    local _has_support=false
    for _dir in core lib modules plugins data assets resources config; do
        [[ -d "$_dir" ]] && _has_support=true && break
    done

    if [[ "$_has_support" == true ]]; then
        mkdir -p "$libdir"
        cp -r . "$libdir/"
        chmod 0755 "$libdir/get"

        mkdir -p "$TERMUX_PREFIX/bin"
        printf '#!/data/data/com.termux/files/usr/bin/bash\nexec bash "%s" "$@"\n'             "$libdir/get" > "$TERMUX_PREFIX/bin/get"
        chmod 0755 "$TERMUX_PREFIX/bin/get"
    else
        install -Dm755 "get" "$TERMUX_PREFIX/bin/get"
    fi
}
