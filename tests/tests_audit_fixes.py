import importlib.util
import subprocess
from pathlib import Path

import pytest

from termux_app_store.core.binary_core import BinaryCache, _valid_target, _verify_sha256

ROOT = Path(__file__).resolve().parent.parent


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scaffold = _load("pkg_scaffold", "pkg-scaffold.py")


def _sample(**over):
    data = {
        "name": "demo-tool",
        "method": "shell",
        "entrypoint": "demo.sh",
        "homepage": "https://github.com/a/b",
        "description": "Plain description",
        "license": "MIT",
        "maintainer": "@demo",
        "version": "1.0.0",
        "srcurl": "https://github.com/a/b/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz",
        "sha256": "a" * 64,
        "depends": "curl",
    }
    data.update(over)
    return data


def _evaluate(content, tmp_path):
    header = content.split("termux_step_make_install")[0]
    script = tmp_path / "build.sh"
    script.write_text(
        header + '\nprintf "%s|%s|%s" "$TERMUX_PKG_DESCRIPTION" "$TERMUX_PKG_MAINTAINER" "$TERMUX_PKG_SRCURL"\n'
    )
    return subprocess.run(
        ["bash", "-c", f"TERMUX_PKG_VERSION=1.0.0; source {script}"], capture_output=True, text=True, cwd=tmp_path
    )


def test_scaffold_values_are_not_executed(tmp_path):
    marker = tmp_path / "pwned"
    description = f'x"; touch {marker}; echo "$(touch {marker}) `touch {marker}` \\'
    result = _evaluate(scaffold.build_sh_content(_sample(description=description)), tmp_path)
    assert result.returncode == 0
    assert not marker.exists()
    assert result.stdout.startswith(description)


def test_scaffold_keeps_version_placeholder_expandable(tmp_path):
    result = _evaluate(scaffold.build_sh_content(_sample()), tmp_path)
    assert result.stdout.endswith("v1.0.0.tar.gz")


def test_scaffold_plain_values_keep_original_format():
    content = scaffold.build_sh_content(_sample())
    assert 'TERMUX_PKG_DESCRIPTION="Plain description"' in content
    assert "TERMUX_PKG_SRCURL=https://github.com/a/b/archive/refs/tags/v${TERMUX_PKG_VERSION}.tar.gz" in content


@pytest.mark.parametrize("bad", ["$(id).py", "a b.sh", "../x.sh", "-rf", 'a".sh'])
def test_scaffold_rejects_unsafe_entrypoints(bad):
    assert scaffold.validate_entrypoint(bad)
    with pytest.raises(ValueError):
        scaffold.build_sh_content(_sample(entrypoint=bad))


@pytest.mark.parametrize("bad", ["https://x/a b", "https://x/$(id)", "https://x/`id`", "file:///etc/passwd"])
def test_scaffold_rejects_unsafe_urls(bad):
    assert scaffold.validate_url(bad)


def test_scaffold_refuses_non_http_download():
    assert scaffold.compute_sha256_from_url("file:///etc/hostname") is None


@pytest.mark.parametrize(
    "pkg,version,arch,ok",
    [
        ("tool", "1.0.0", "aarch64", True),
        ("../tool", "1.0.0", "aarch64", False),
        ("tool", "1/../0", "aarch64", False),
        ("tool", "1.0.0", "mips", False),
        ("", "1.0.0", "arm", False),
    ],
)
def test_binary_cache_identifier_validation(pkg, version, arch, ok):
    assert _valid_target(pkg, version, arch) is ok


def test_binary_cache_rejects_unsafe_input(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    cache = BinaryCache()
    assert cache.download_from_mirror("../evil", "1.0", "arm", "https://example.invalid", "a" * 64) is None
    assert cache.download_from_mirror("tool", "1.0", "arm", "file:///tmp", "a" * 64) is None
    assert cache.get_best_binary("../evil", "1.0", "arm", "a" * 64) is None


def test_sha256_comparison_ignores_case(tmp_path):
    f = tmp_path / "x.deb"
    f.write_bytes(b"data")
    import hashlib

    digest = hashlib.sha256(b"data").hexdigest()
    assert _verify_sha256(f, digest.upper())
    assert _verify_sha256(f, digest)
    assert not _verify_sha256(f, "0" * 64)
