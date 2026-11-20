import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "build-package.sh"


def test_build_package_has_valid_syntax():
    result = subprocess.run(["bash", "-n", str(SCRIPT)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_generated_python_launchers_silence_syntax_warnings():
    text = SCRIPT.read_text(encoding="utf-8")
    assert text.count('export PYTHONWARNINGS="ignore::SyntaxWarning') >= 3
    assert "_silence_python_syntax_warnings" in text


def test_existing_python_wrapper_gets_patched(tmp_path):
    wrapper = tmp_path / "pkg" / "prefix" / "bin" / "tool"
    wrapper.parent.mkdir(parents=True)
    wrapper.write_text(
        '#!/data/data/com.termux/files/usr/bin/bash\nexec python3 "/x/hash.py" "$@"\n',
        encoding="utf-8",
    )
    text = SCRIPT.read_text(encoding="utf-8")
    start = text.index("_silence_python_syntax_warnings() {")
    end = text.index("_check_staged_links() {")
    func = text[start:end]
    harness = f'WORK_DIR="{tmp_path}"; PREFIX="/prefix"\n{func}\n_silence_python_syntax_warnings\n'
    harness = harness.replace('"$WORK_DIR/pkg$PREFIX/bin/"', f'"{tmp_path}/pkg/prefix/bin/"')
    result = subprocess.run(["bash", "-c", harness], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    lines = wrapper.read_text(encoding="utf-8").splitlines()
    assert lines[1].startswith('export PYTHONWARNINGS="ignore::SyntaxWarning')
    assert lines[2].startswith("exec python3")


def test_patch_is_not_applied_twice(tmp_path):
    wrapper = tmp_path / "pkg" / "prefix" / "bin" / "tool"
    wrapper.parent.mkdir(parents=True)
    wrapper.write_text(
        '#!/data/data/com.termux/files/usr/bin/bash\nexport PYTHONWARNINGS="ignore::SyntaxWarning"\nexec python3 "/x/a.py"\n',
        encoding="utf-8",
    )
    text = SCRIPT.read_text(encoding="utf-8")
    func = text[text.index("_silence_python_syntax_warnings() {") : text.index("_check_staged_links() {")]
    func = func.replace('"$WORK_DIR/pkg$PREFIX/bin/"', f'"{tmp_path}/pkg/prefix/bin/"')
    subprocess.run(["bash", "-c", f"{func}\n_silence_python_syntax_warnings\n"], check=True)
    assert wrapper.read_text(encoding="utf-8").count("PYTHONWARNINGS") == 1
