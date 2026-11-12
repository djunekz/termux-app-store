TERMUX_PKG_HOMEPAGE=https://pkg.go.dev/github.com/x90skysn3k/brutespray/v2
TERMUX_PKG_DESCRIPTION="Fast, multi-protocol credential brute-forcer. Parses Nmap, Nessus, and Nexpose output to automatically test default and custom credentials across 30+ protocols."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=2.7.3
TERMUX_PKG_SRCURL=https://github.com/x90skysn3k/brutespray/archive/refs/tags/v2.7.3.tar.gz
TERMUX_PKG_SHA256=2efb6faa7b580cf0d2fce3a5519759529254717bc9014ffc13d251e3ef839167

TERMUX_PKG_DEPENDS="golang"

termux_step_make_install() {
	export GOPATH="$PWD/gopath"
	export GOPROXY="https://proxy.golang.org,direct"
	export GOTOOLCHAIN=local
	export GOFLAGS="-mod=mod"

	if [[ -f go.mod ]]; then
		sed -i -E 's/^go [0-9]+\.[0-9]+(\.[0-9]+)?/go 1.21/' go.mod
		go get ./... 2>/dev/null || true
		go build -v -o "$TERMUX_PREFIX/bin/brutespray" .
	else
		go mod init "brutespray" 2>/dev/null || true
		go get ./... 2>/dev/null || true
		go mod tidy 2>/dev/null || true
		go build -v -o "$TERMUX_PREFIX/bin/brutespray" . 2>/dev/null \
			|| go build -v -o "$TERMUX_PREFIX/bin/brutespray" *.go
	fi
}
