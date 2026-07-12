TERMUX_PKG_HOMEPAGE=https://github.com/EgeBalci/The-Eye
TERMUX_PKG_DESCRIPTION="Simple security surveillance script for linux distributions."
TERMUX_PKG_LICENSE="GPL-3.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=0.0.0+51cfb45
TERMUX_PKG_SRCURL=https://github.com/EgeBalci/The-Eye/archive/51cfb45eaa031928c6815c4c8dd509ef5930abf8.tar.gz
TERMUX_PKG_SHA256=ce14826a7bc817d96fe0180bc9d952c91259bdfcd0681cd53af6ec03d6fd3b30

TERMUX_PKG_DEPENDS="golang"

termux_step_make_install() {
    export GOPATH="$PWD/gopath"
    export GOPROXY="https://proxy.golang.org,direct"
    if [[ -f go.mod ]]; then
        go get ./... 2>/dev/null || true
        go build -v -o "$TERMUX_PREFIX/bin/the-eye" .
    else
        # No go.mod — init module, fetch deps, then build
        go mod init "the-eye" 2>/dev/null || true
        go get ./... 2>/dev/null || true
        go mod tidy 2>/dev/null || true
        go build -v -o "$TERMUX_PREFIX/bin/the-eye" . 2>/dev/null             || go build -v -o "$TERMUX_PREFIX/bin/the-eye" *.go
    fi
}
