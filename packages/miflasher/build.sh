TERMUX_PKG_HOMEPAGE=https://github.com/djunekz/miflasher
TERMUX_PKG_DESCRIPTION="A lightweight CLI tool to flash and manage Xiaomi firmware packages (Fastboot/ROM) easily and safely"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=2.0.4
TERMUX_PKG_SRCURL=https://github.com/djunekz/miflasher/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz
TERMUX_PKG_SHA256=acd4d7af7b302fdec83a3d6e13f9f009c99b22be8b7872f7755dd39f400a84eb
TERMUX_PKG_DEPENDS="brotli, libc++, liblz4, termux-api, zlib, zstd, termux-adb"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    local libdir="$TERMUX_PREFIX/lib/miflasher"
    mkdir -p "$libdir"
    cp -r . "$libdir/"

    find "$libdir" -type d | while read -r _dir; do
        ls "$_dir"/*.py &>/dev/null 2>&1 && [ ! -f "$_dir/__init__.py" ] && \
            touch "$_dir/__init__.py"
    done

    cat > "$TERMUX_PREFIX/bin/miflasher" <<'WRAPPER'
#!/data/data/com.termux/files/usr/bin/bash
cd "/data/data/com.termux/files/usr/lib/miflasher" || exit 1
exec python3 "/data/data/com.termux/files/usr/lib/miflasher/miflasher" "$@"
WRAPPER
    chmod 0755 "$TERMUX_PREFIX/bin/miflasher"
}
