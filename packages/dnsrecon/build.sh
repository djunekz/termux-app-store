TERMUX_PKG_HOMEPAGE=https://github.com/darkoperator/dnsrecon
TERMUX_PKG_DESCRIPTION="DNS Enumeration Script"
TERMUX_PKG_LICENSE="GPL-2.0"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.6.0
TERMUX_PKG_SRCURL=https://github.com/darkoperator/dnsrecon/archive/refs/tags/1.6.0.tar.gz
TERMUX_PKG_SHA256=21b83c22e4dcf684b623c824a678c371d803952d99d4758c9b1c45bce409eb3d

TERMUX_PKG_DEPENDS="python, python-pip, python-setuptools"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet dns --break-system-packages 2>/dev/null || echo "[ WARN ] pip install dns failed — may be missing at runtime"
    pip install --quiet dnspython --break-system-packages 2>/dev/null || echo "[ WARN ] pip install dnspython failed — may be missing at runtime"
    pip install --quiet fastapi --break-system-packages 2>/dev/null || echo "[ WARN ] pip install fastapi failed — may be missing at runtime"
    pip install --quiet httpx --break-system-packages 2>/dev/null || echo "[ WARN ] pip install httpx failed — may be missing at runtime"
    pip install --quiet loguru --break-system-packages 2>/dev/null || echo "[ WARN ] pip install loguru failed — may be missing at runtime"
    pip install --quiet netaddr --break-system-packages 2>/dev/null || echo "[ WARN ] pip install netaddr failed — may be missing at runtime"
    pip install --quiet pydantic --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pydantic failed — may be missing at runtime"
    pip install --quiet pytest --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pytest failed — may be missing at runtime"
    pip install --quiet pytest-asyncio --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pytest-asyncio failed — may be missing at runtime"
    pip install --quiet pyupgrade --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pyupgrade failed — may be missing at runtime"
    pip install --quiet ruff --break-system-packages 2>/dev/null || echo "[ WARN ] pip install ruff failed — may be missing at runtime"
    pip install --quiet slowapi --break-system-packages 2>/dev/null || echo "[ WARN ] pip install slowapi failed — may be missing at runtime"
    pip install --quiet stamina --break-system-packages 2>/dev/null || echo "[ WARN ] pip install stamina failed — may be missing at runtime"
    pip install --quiet types-ujson --break-system-packages 2>/dev/null || echo "[ WARN ] pip install types-ujson failed — may be missing at runtime"
    pip install --quiet uvicorn --break-system-packages 2>/dev/null || echo "[ WARN ] pip install uvicorn failed — may be missing at runtime"
    local libdir="$TERMUX_PREFIX/lib/dnsrecon"
    pip install . --prefix="$TERMUX_PREFIX" --break-system-packages 2>/dev/null \
        || pip install . --prefix="$TERMUX_PREFIX" --no-build-isolation --break-system-packages 2>/dev/null \
        || pip install . --prefix="$TERMUX_PREFIX" --no-deps --no-build-isolation --break-system-packages || {
            echo "pip failed — falling back to manual install"
            mkdir -p "$libdir"
            cp -r . "$libdir/"
        }

    find "$libdir" -type d 2>/dev/null | while read -r _dir; do
        if ls "$_dir"/*.py &>/dev/null 2>&1 && [[ ! -f "$_dir/__init__.py" ]]; then
            touch "$_dir/__init__.py"
        fi
    done


}
