TERMUX_PKG_HOMEPAGE=https://github.com/LimerBoy/Impulse
TERMUX_PKG_DESCRIPTION="Denial-of-Service ToolKit with multiple attack methods"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.0.0
TERMUX_PKG_SRCURL=https://github.com/droidv1/termool/releases/download/v${TERMUX_PKG_VERSION}/impulse.tar.gz
TERMUX_PKG_SHA256=cb78b4bfe4f4bb29aaa773f0b0939de4ea3c84796d5a6c169a728f0a4266d710
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    mkdir -p $TERMUX_PREFIX/lib/impulse
    mkdir -p $TERMUX_PREFIX/bin

    cp -r * $TERMUX_PREFIX/lib/impulse/

    cat > $TERMUX_PREFIX/bin/impulse <<EOF
#!/data/data/com.termux/files/usr/bin/bash
cd $TERMUX_PREFIX/lib/impulse
exec python3 impulse.py "\$@"
EOF

    chmod +x $TERMUX_PREFIX/bin/impulse
}
