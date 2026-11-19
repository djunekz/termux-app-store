import importlib.util
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tester = _load("tas_build_tester_runtime", ROOT / "build-tester.py")
doctor = _load("tas_doctor_runtime", ROOT / "termux_app_store" / "doctor.py")


def _levels(issues):
    return [i.level for i in issues if i.category == "Runtime"]


def test_tester_flags_ignored_pip_failure():
    lines = ['pip install requests 2>/dev/null || echo "WARN: skipped"']
    assert tester.WARN in _levels(tester.test_runtime_deps(lines, {"TERMUX_PKG_DEPENDS": "python"}))


def test_tester_flags_hyphenated_module_name():
    lines = ['exec python3 -m my-tool "$@"']
    assert tester.FAIL in _levels(tester.test_runtime_deps(lines, {"TERMUX_PKG_DEPENDS": "python"}))


def test_tester_flags_missing_runtime_dependency():
    lines = ["termux_step_make_install() {", '  exec python3 "$f"', "}"]
    issues = tester.test_runtime_deps(lines, {"TERMUX_PKG_DEPENDS": "curl"})
    assert any("python is not in TERMUX_PKG_DEPENDS" in i.message for i in issues)


def test_tester_flags_node_copy_without_install():
    lines = ["termux_step_make_install() {", '  exec node "$f"', "}"]
    issues = tester.test_runtime_deps(lines, {"TERMUX_PKG_DEPENDS": "nodejs"})
    assert any("without installing its dependencies" in i.message for i in issues)


def test_tester_passes_clean_script():
    lines = ["termux_step_make_install() {", '  pip install . --prefix="$TERMUX_PREFIX"', "}"]
    issues = tester.test_runtime_deps(lines, {"TERMUX_PKG_DEPENDS": "python, python-pip"})
    assert _levels(issues) == [tester.PASS]


def test_tester_parses_declared_python_dependencies():
    assert tester._parse_python_deps("requirements.txt", "Requests>=2\n# c\n-r other.txt\nsix\n") == ["requests", "six"]
    setup_py = "setup(install_requires=['httpx>=0.2', \"rich\"])"
    assert tester._parse_python_deps("setup.py", setup_py) == ["httpx", "rich"]
    pyproject = '[project]\nname="x"\ndependencies=["colorama","tqdm>=4"]\n'
    assert tester._parse_python_deps("pyproject.toml", pyproject) == ["colorama", "tqdm"]


def test_doctor_required_imports_ignore_guarded_and_lazy(tmp_path):
    src = tmp_path / "m.py"
    src.write_text(
        "import os\nimport requests\ntry:\n    import fancy\nexcept ImportError:\n    fancy = None\n"
        "def f():\n    import lazy_only\n",
        encoding="utf-8",
    )
    names = {n.split(".")[0] for level, n, req in doctor.required_imports(src) if req}
    assert "requests" in names
    assert "fancy" not in names
    assert "lazy_only" not in names


def _make_python_package(prefix, body):
    (prefix / "bin").mkdir(parents=True)
    lib = prefix / "lib" / "demo"
    lib.mkdir(parents=True)
    (lib / "main.py").write_text(body, encoding="utf-8")
    (lib / "helper.py").write_text("import json\n", encoding="utf-8")
    launcher = prefix / "bin" / "demo"
    launcher.write_text(
        '#!/bin/bash\nexport PYTHONPATH="$PREFIX/lib/demo/.pydeps:$PREFIX/lib/demo"\nexec python3 "$PREFIX/lib/demo/main.py" "$@"\n',
        encoding="utf-8",
    )
    return launcher


def test_doctor_reports_missing_python_module(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "_PFX", str(tmp_path))
    launcher = _make_python_package(tmp_path, "import zz_missing_mod\nfrom helper import x\n")
    assert doctor.scan_python_launcher(str(launcher)) == {"zz_missing_mod": str(tmp_path / "lib/demo/main.py")}


def test_doctor_accepts_bundled_python_module(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "_PFX", str(tmp_path))
    launcher = _make_python_package(tmp_path, "import zz_bundled_mod\n")
    deps = tmp_path / "lib" / "demo" / ".pydeps"
    deps.mkdir()
    (deps / "zz_bundled_mod.py").write_text("", encoding="utf-8")
    assert doctor.scan_python_launcher(str(launcher)) == {}


def test_doctor_reports_missing_node_dependency(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "_PFX", str(tmp_path))
    (tmp_path / "bin").mkdir()
    pkg = tmp_path / "lib" / "node_modules" / "demo"
    (pkg / "bin").mkdir(parents=True)
    (pkg / "package.json").write_text('{"dependencies": {"present": "1", "absent": "1"}}', encoding="utf-8")
    (pkg / "bin" / "cli.js").write_text("#!/usr/bin/env node\n", encoding="utf-8")
    (pkg / "node_modules" / "present").mkdir(parents=True)
    link = tmp_path / "bin" / "demo"
    os.symlink("../lib/node_modules/demo/bin/cli.js", link)
    result = doctor.scan_node_launcher(str(link))
    assert result["missing"] == ["absent"]


def test_doctor_reports_dangling_node_link(tmp_path, monkeypatch):
    monkeypatch.setattr(doctor, "_PFX", str(tmp_path))
    (tmp_path / "bin").mkdir()
    link = tmp_path / "bin" / "demo"
    os.symlink("/nonexistent/build/cli.js", link)
    result = doctor.scan_node_launcher(str(link))
    assert result["problem"]


def test_doctor_fix_command_uses_termux_packages_and_pip():
    cmd = doctor._fix_cmd_for_modules(["numpy", "yaml", "rich"])
    assert "pkg install -y python-numpy" in cmd
    assert "pyyaml" in cmd and "rich" in cmd
    assert "--break-system-packages" in cmd


def test_doctor_has_modules_mode_in_help():
    text = (ROOT / "termux_app_store" / "doctor.py").read_text(encoding="utf-8")
    assert "--modules" in text
