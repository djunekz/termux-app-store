TERMUX_PKG_HOMEPAGE=https://dalfox.hahwul.com
TERMUX_PKG_DESCRIPTION="🌙🦊 Dalfox is a powerful open-source XSS scanner and utility focused on automation."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=3.2.4
TERMUX_PKG_SRCURL=https://github.com/hahwul/dalfox/archive/refs/tags/v3.2.4.tar.gz
TERMUX_PKG_SHA256=d86cae222a4db6c8a335013c980d0c6d672b3abee8cfb44da6ce1b489e4d3a9b

TERMUX_PKG_DEPENDS="golang"

termux_step_make_install() {
    export GOPATH="$PWD/gopath"
    export GOPROXY="https://proxy.golang.org,direct"
    if [[ -f go.mod ]]; then
        go get ./... 2>/dev/null || true
        go build -v -o "$TERMUX_PREFIX/bin/dalfox" .
    else
        go mod init "dalfox" 2>/dev/null || true
        go get ./... 2>/dev/null || true
        go mod tidy 2>/dev/null || true
        go build -v -o "$TERMUX_PREFIX/bin/dalfox" . 2>/dev/null             || go build -v -o "$TERMUX_PREFIX/bin/dalfox" *.go
    fi
}
