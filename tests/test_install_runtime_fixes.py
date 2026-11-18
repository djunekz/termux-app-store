import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scaffold = _load("pkg_scaffold_runtime", "pkg-scaffold.py")


def _sample(method, **extra):
    data = {
        "name": "my-tool",
        "description": "d",
        "homepage": "https://example.com",
        "license": "MIT",
        "maintainer": "@a",
        "version": "1.0",
        "srcurl": "https://example.com/a.tar.gz",
        "sha256": "a" * 64,
        "method": method,
        "entrypoint": "main.py",
        "depends": "",
    }
    data.update(extra)
    return data


def test_every_scaffold_template_is_valid_bash(tmp_path):
    for method, _ in scaffold.BUILD_METHODS:
        target = tmp_path / f"{method}.sh"
        target.write_text(scaffold.build_sh_content(_sample(method)), encoding="utf-8")
        result = subprocess.run(["bash", "-n", str(target)], capture_output=True, text=True)
        assert result.returncode == 0, (method, result.stderr)


def test_pip_template_installs_dependencies():
    content = scaffold.build_sh_content(_sample("pip"))
    assert "--no-deps" not in content


def test_python_script_template_bundles_requirements_and_uses_pythonpath():
    content = scaffold.build_sh_content(_sample("python-script"))
    assert "requirements.txt" in content
    assert ".pydeps" in content
    assert "PYTHONPATH" in content
    assert 'cd "/data/data' not in content
    assert "__init__.py" not in content


def test_npm_template_copies_instead_of_linking():
    assert "--install-links" in scaffold.build_sh_content(_sample("npm"))


def test_php_wrapper_does_not_use_usr_bin_env():
    assert "/usr/bin/env" not in scaffold.build_sh_content(_sample("php"))


def test_scaffold_dependencies_are_deduplicated():
    content = scaffold.build_sh_content(_sample("python-script", depends="python, curl, curl"))
    line = next(x for x in content.splitlines() if x.startswith("TERMUX_PKG_DEPENDS="))
    assert line == 'TERMUX_PKG_DEPENDS="python, curl"'


def test_version_is_extracted_from_odd_tags():
    assert scaffold._version_from_tag("v1.2.3") == "1.2.3"
    assert scaffold._version_from_tag("release-2.0") == "2.0"


def test_build_package_declares_runtime_dependencies_in_control():
    script = (ROOT / "build-package.sh").read_text(encoding="utf-8")
    assert 'echo "Depends: $_DEPENDS_LINE"' in script
    assert "_infer_runtime_deps" in script


def test_build_package_keeps_symlinks_and_node_dependencies():
    script = (ROOT / "build-package.sh").read_text(encoding="utf-8")
    assert "_stage_tree" in script
    assert "_ensure_node_deps" in script
    assert "--install-links" in script


def test_build_package_restarts_with_original_arguments():
    script = (ROOT / "build-package.sh").read_text(encoding="utf-8")
    assert 'exec "$0" "${_ORIG_ARGS[@]}"' in script
    assert 'exec "$0" "$@"' not in script


def test_build_package_has_valid_syntax():
    result = subprocess.run(["bash", "-n", str(ROOT / "build-package.sh")], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
