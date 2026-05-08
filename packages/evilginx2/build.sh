TERMUX_PKG_HOMEPAGE=https://github.com/kgretzky/evilginx2
TERMUX_PKG_DESCRIPTION="Standalone man-in-the-middle attack framework used for phishing login credentials along with session cookies, allowing for the bypass of 2-factor authentication"
TERMUX_PKG_LICENSE="BSD-3-Clause"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.3.0
TERMUX_PKG_SRCURL=https://github.com/kgretzky/evilginx2/archive/refs/tags/v3.3.0.tar.gz
TERMUX_PKG_SHA256=6d33f0d0b4b569af5207102512945502ed37090879dcf6987322d670912a4133

TERMUX_PKG_DEPENDS="golang"

termux_step_make_install() {
    export GOPATH="$PWD/gopath"
    export GOPROXY="https://proxy.golang.org,direct"
    if [[ -f go.mod ]]; then
        go get ./... 2>/dev/null || true
        go build -v -o "$TERMUX_PREFIX/bin/evilginx2" .
    else
        go mod init "evilginx2" 2>/dev/null || true
        go get ./... 2>/dev/null || true
        go mod tidy 2>/dev/null || true
        go build -v -o "$TERMUX_PREFIX/bin/evilginx2" . 2>/dev/null             || go build -v -o "$TERMUX_PREFIX/bin/evilginx2" *.go
    fi
}
