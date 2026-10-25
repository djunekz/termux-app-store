import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("update_citation_under_test", ROOT / "ci" / "update_citation.py")
uc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(uc)

CFF = """cff-version: 1.2.0
message: "Please cite."
title: "Termux App Store"
version: "0.9.1"
date-released: "2026-10-21"
license: MIT
authors:
  - alias: "djunekz"
"""

CHANGELOG = """# Changelog

## [Unreleased]

## [v0.9.2] - 2026-11-03

### Fixed
- something

## [v0.9.1] - 2026-10-21
"""


@pytest.fixture
def files(tmp_path):
    cff = tmp_path / "CITATION.cff"
    log = tmp_path / "CHANGELOG.md"
    cff.write_text(CFF, encoding="utf-8")
    log.write_text(CHANGELOG, encoding="utf-8")
    return cff, log


def run(files, *extra):
    cff, log = files
    return uc.main(["--file", str(cff), "--changelog", str(log), *extra])


class TestNormalizeVersion:
    def test_strips_leading_v(self):
        assert uc.normalize_version("v1.2.3") == "1.2.3"

    def test_accepts_prerelease(self):
        assert uc.normalize_version("v1.0.0-rc1") == "1.0.0-rc1"

    @pytest.mark.parametrize("bad", ["latest", "v1.2", "1.2.3; rm -rf /", "", "v1.2.3 "])
    def test_rejects_invalid(self, bad):
        if bad == "v1.2.3 ":
            assert uc.normalize_version(bad) == "1.2.3"
        else:
            with pytest.raises(ValueError):
                uc.normalize_version(bad)


class TestChangelogDate:
    def test_finds_date(self):
        assert uc.changelog_date(CHANGELOG, "0.9.2") == "2026-11-03"

    def test_missing_entry(self):
        assert uc.changelog_date(CHANGELOG, "9.9.9") is None


class TestWrite:
    def test_updates_version_and_date_from_changelog(self, files):
        assert run(files, "--version", "v0.9.2") == 0
        text = files[0].read_text(encoding="utf-8")
        assert 'version: "0.9.2"' in text
        assert 'date-released: "2026-11-03"' in text

    def test_other_lines_unchanged(self, files):
        run(files, "--version", "v0.9.2")
        new = files[0].read_text(encoding="utf-8").splitlines()
        old = CFF.splitlines()
        assert len(new) == len(old)
        changed = [i for i, (a, b) in enumerate(zip(old, new)) if a != b]
        assert len(changed) == 2

    def test_cff_version_line_is_not_touched(self, files):
        run(files, "--version", "v0.9.2")
        assert "cff-version: 1.2.0" in files[0].read_text(encoding="utf-8")

    def test_explicit_date_wins(self, files):
        run(files, "--version", "v0.9.2", "--date", "2027-01-02")
        assert 'date-released: "2027-01-02"' in files[0].read_text(encoding="utf-8")

    def test_idempotent(self, files):
        run(files, "--version", "v0.9.2")
        first = files[0].read_text(encoding="utf-8")
        run(files, "--version", "v0.9.2")
        assert files[0].read_text(encoding="utf-8") == first

    def test_falls_back_to_today_without_changelog_entry(self, files, monkeypatch):
        monkeypatch.setattr(uc, "today_utc", lambda: "2030-05-06")
        run(files, "--version", "v9.9.9")
        assert 'date-released: "2030-05-06"' in files[0].read_text(encoding="utf-8")

    def test_invalid_version_is_an_error(self, files):
        assert run(files, "--version", "nonsense") == 2

    def test_invalid_date_is_an_error(self, files):
        assert run(files, "--version", "v0.9.2", "--date", "03-11-2026") == 2

    def test_missing_file_is_an_error(self, tmp_path):
        assert uc.main(["--file", str(tmp_path / "none.cff"), "--version", "v1.0.0"]) == 2

    def test_missing_fields_are_an_error(self, files):
        files[0].write_text('title: "x"\n', encoding="utf-8")
        assert run(files, "--version", "v0.9.2") == 2


class TestCheck:
    def test_stale_file_fails(self, files):
        assert run(files, "--version", "v0.9.2", "--check") == 1
        assert files[0].read_text(encoding="utf-8") == CFF

    def test_matching_file_passes(self, files):
        assert run(files, "--version", "v0.9.1", "--check") == 0


class TestOnlyIfNewer:
    def test_does_not_downgrade(self, files):
        run(files, "--version", "v0.9.2")
        assert run(files, "--version", "v0.9.1", "--only-if-newer") == 0
        assert 'version: "0.9.2"' in files[0].read_text(encoding="utf-8")

    def test_upgrades(self, files):
        assert run(files, "--version", "v0.9.2", "--only-if-newer") == 0
        assert 'version: "0.9.2"' in files[0].read_text(encoding="utf-8")

    def test_prerelease_sorts_before_release(self):
        assert uc.version_key("1.0.0-rc1") < uc.version_key("1.0.0")
        assert uc.version_key("0.9.10") > uc.version_key("0.9.2")


class TestGithubOutput:
    def test_writes_changed_flag(self, files, tmp_path, monkeypatch):
        out = tmp_path / "out.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(out))
        run(files, "--version", "v0.9.2")
        assert "changed=true" in out.read_text(encoding="utf-8")
        run(files, "--version", "v0.9.2")
        assert out.read_text(encoding="utf-8").strip().splitlines()[-2] == "changed=false"
