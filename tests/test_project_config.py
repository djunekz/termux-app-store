import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(name: str) -> str:
    return (ROOT / name).read_text(encoding="utf-8")


class TestTestCommandWiring:
    def test_pyproject_declares_pytest_dependency(self):
        assert "pytest>=" in read("pyproject.toml")

    def test_makefile_test_target_runs_pytest(self):
        match = re.search(r"^test:\n((?:\t.*\n)+)", read("Makefile"), re.MULTILINE)
        assert match is not None
        assert "pytest" in match.group(1)

    def test_makefile_coverage_target_uses_pytest_cov(self):
        match = re.search(r"^coverage:\n((?:\t.*\n)+)", read("Makefile"), re.MULTILINE)
        assert match is not None
        assert "--cov" in match.group(1)

    def test_pytest_config_points_at_existing_directory(self):
        match = re.search(r'^testpaths\s*=\s*\["([^"]+)"\]', read("pyproject.toml"), re.MULTILINE)
        assert match is not None
        assert (ROOT / match.group(1)).is_dir()

    def test_pytest_config_lives_only_in_pyproject(self):
        assert "[tool.pytest.ini_options]" in read("pyproject.toml")
        assert not (ROOT / "pytest.ini").exists()

    def test_tox_runs_pytest(self):
        assert re.search(r"^commands\s*=\s*(python -m )?pytest\b", read("tox.ini"), re.MULTILINE)

    def test_ci_workflow_runs_pytest(self):
        assert "python -m pytest" in read(".github/workflows/ci.yml")

    def test_readme_documents_test_command(self):
        assert "make test" in read("README.md")

    def test_contributing_documents_test_command(self):
        assert "make test" in read("CONTRIBUTING.md")
