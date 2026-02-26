import re
import pytest


def _ver_tuple(v: str):
    v = v.strip()
    parts = v.split("-", 1)
    base = parts[0]
    rev_str = parts[1] if len(parts) > 1 else "0"

    base_parts = []
    for seg in re.split(r"[._]", base):
        try:
            base_parts.append(int(seg))
        except ValueError:
            base_parts.append(0)

    try:
        rev = int(rev_str)
    except ValueError:
        rev = 0

    return tuple(base_parts) + (rev,)


def is_installed_newer_or_equal(installed: str, store: str) -> bool:
    return _ver_tuple(installed) >= _ver_tuple(store)


class TestVerTuple:

    def test_simple_three_part(self):
        assert _ver_tuple("1.2.3") == (1, 2, 3, 0)

    def test_two_part(self):
        assert _ver_tuple("4.10") == (4, 10, 0)

    def test_one_part(self):
        assert _ver_tuple("1") == (1, 0)

    def test_four_part(self):
        assert _ver_tuple("1.2.3.4") == (1, 2, 3, 4, 0)

    def test_with_numeric_revision(self):
        assert _ver_tuple("4.10-1") == (4, 10, 1)

    def test_with_non_numeric_suffix(self):
        assert _ver_tuple("2.0-pre")  == (2, 0, 0)
        assert _ver_tuple("1.0-beta") == (1, 0, 0)
        assert _ver_tuple("1.0-rc1")  == (1, 0, 0)

    def test_with_leading_trailing_spaces(self):
        assert _ver_tuple("  1.2.3  ") == (1, 2, 3, 0)

    def test_non_numeric_segment(self):
        assert _ver_tuple("1.abc.3") == (1, 0, 3, 0)

    def test_zero_version(self):
        assert _ver_tuple("0.0.0") == (0, 0, 0, 0)

    def test_ordering_patch(self):
        assert _ver_tuple("1.2.3") < _ver_tuple("1.2.4")

    def test_ordering_minor(self):
        assert _ver_tuple("1.9.0") < _ver_tuple("1.10.0")

    def test_ordering_major(self):
        assert _ver_tuple("2.0.0") > _ver_tuple("1.9.9")

    def test_ordering_revision(self):
        assert _ver_tuple("4.10-1") < _ver_tuple("4.10-2")
        assert _ver_tuple("4.10-0") < _ver_tuple("4.10-1")

    def test_real_package_aircrack(self):
        assert _ver_tuple("1.7") == (1, 7, 0)

    def test_real_package_pnpm(self):
        assert _ver_tuple("10.30.1") == (10, 30, 1, 0)

    def test_real_package_tuifimanager(self):
        assert _ver_tuple("5.2.6") == (5, 2, 6, 0)

    def test_real_package_sigit_pre(self):
        assert _ver_tuple("2.0-pre") == (2, 0, 0)

    def test_equality(self):
        assert _ver_tuple("1.2.3") == _ver_tuple("1.2.3")



class TestIsInstalledNewerOrEqual:

    def test_same_version(self):
        assert is_installed_newer_or_equal("1.2.3", "1.2.3") is True

    def test_same_version_two_part(self):
        assert is_installed_newer_or_equal("4.10", "4.10") is True

    def test_newer_patch(self):
        assert is_installed_newer_or_equal("1.2.4", "1.2.3") is True

    def test_newer_minor(self):
        assert is_installed_newer_or_equal("1.10.0", "1.9.0") is True

    def test_newer_major(self):
        assert is_installed_newer_or_equal("2.0.0", "1.9.9") is True

    def test_newer_revision(self):
        assert is_installed_newer_or_equal("4.10-2", "4.10-1") is True

    def test_older_patch(self):
        assert is_installed_newer_or_equal("1.0.0", "1.0.1") is False

    def test_older_minor(self):
        assert is_installed_newer_or_equal("1.9.0", "1.10.0") is False

    def test_older_major(self):
        assert is_installed_newer_or_equal("1.9.9", "2.0.0") is False

    def test_older_revision(self):
        assert is_installed_newer_or_equal("4.10-1", "4.10-2") is False

    def test_bower_up_to_date(self):
        assert is_installed_newer_or_equal("1.8.12", "1.8.12") is True

    def test_bower_outdated(self):
        assert is_installed_newer_or_equal("1.8.11", "1.8.12") is False

    def test_pnpm_up_to_date(self):
        assert is_installed_newer_or_equal("10.30.1", "10.30.1") is True

    def test_pnpm_outdated(self):
        assert is_installed_newer_or_equal("10.29.0", "10.30.1") is False

    def test_ani_cli_up_to_date(self):
        assert is_installed_newer_or_equal("4.10", "4.10") is True

    def test_ani_cli_outdated(self):
        assert is_installed_newer_or_equal("4.9", "4.10") is False

    def test_non_numeric_suffix(self):
        assert is_installed_newer_or_equal("2.0-pre", "2.0") is True

    def test_uv_newer(self):
        assert is_installed_newer_or_equal("0.10.4", "0.10.3") is True

    def test_uv_outdated(self):
        assert is_installed_newer_or_equal("0.10.3", "0.10.4") is False
