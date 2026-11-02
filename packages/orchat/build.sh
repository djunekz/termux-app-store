TERMUX_PKG_HOMEPAGE=https://github.com/oop7/OrChat
TERMUX_PKG_DESCRIPTION="A powerful, feature-rich command-line interface for interacting with AI models through OpenRouter."
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_MAINTAINER="@termux-app-store"
TERMUX_PKG_VERSION=1.4.6
TERMUX_PKG_SRCURL=https://github.com/oop7/OrChat/archive/refs/tags/v1.4.6.tar.gz
TERMUX_PKG_SHA256=fbe070754e2d66c3f724e496241975f0cd4e209c7c590cca395c38cabd3b65ae

TERMUX_PKG_DEPENDS="python, python-pip"
TERMUX_PKG_BUILD_IN_SRC=true

termux_step_make_install() {
    pip install --quiet setuptools wheel --break-system-packages 2>/dev/null || true
    pip install --quiet beautifulsoup4 --break-system-packages 2>/dev/null || echo "[ WARN ] pip install beautifulsoup4 failed — may be missing at runtime"
    pip install --quiet black --break-system-packages 2>/dev/null || echo "[ WARN ] pip install black failed — may be missing at runtime"
    pip install --quiet build --break-system-packages 2>/dev/null || echo "[ WARN ] pip install build failed — may be missing at runtime"
    pip install --quiet colorama --break-system-packages 2>/dev/null || echo "[ WARN ] pip install colorama failed — may be missing at runtime"
    pip install --quiet cryptography --break-system-packages 2>/dev/null || echo "[ WARN ] pip install cryptography failed — may be missing at runtime"
    pip install --quiet flake8 --break-system-packages 2>/dev/null || echo "[ WARN ] pip install flake8 failed — may be missing at runtime"
    pip install --quiet html2text --break-system-packages 2>/dev/null || echo "[ WARN ] pip install html2text failed — may be missing at runtime"
    pip install --quiet isort --break-system-packages 2>/dev/null || echo "[ WARN ] pip install isort failed — may be missing at runtime"
    pip install --quiet packaging --break-system-packages 2>/dev/null || echo "[ WARN ] pip install packaging failed — may be missing at runtime"
    pip install --quiet pre-commit --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pre-commit failed — may be missing at runtime"
    pip install --quiet prompt_toolkit --break-system-packages 2>/dev/null || echo "[ WARN ] pip install prompt_toolkit failed — may be missing at runtime"
    pip install --quiet pyfzf --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pyfzf failed — may be missing at runtime"
    pip install --quiet pytest --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pytest failed — may be missing at runtime"
    pip install --quiet pytest-cov --break-system-packages 2>/dev/null || echo "[ WARN ] pip install pytest-cov failed — may be missing at runtime"
    pip install --quiet python-dotenv --break-system-packages 2>/dev/null || echo "[ WARN ] pip install python-dotenv failed — may be missing at runtime"
    pip install --quiet requests --break-system-packages 2>/dev/null || echo "[ WARN ] pip install requests failed — may be missing at runtime"
    pip install --quiet rich --break-system-packages 2>/dev/null || echo "[ WARN ] pip install rich failed — may be missing at runtime"
    pip install --quiet tiktoken --break-system-packages 2>/dev/null || echo "[ WARN ] pip install tiktoken failed — may be missing at runtime"
    pip install --quiet twine --break-system-packages 2>/dev/null || echo "[ WARN ] pip install twine failed — may be missing at runtime"
    local libdir="$TERMUX_PREFIX/lib/orchat"
    # Install with deps first (reads pyproject.toml/setup.py dependencies automatically)
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
