import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import patch


class BuildShParser:

    def __init__(self, build_sh_path: str):
        self.path = build_sh_path
        self.content = self._read_file()

    def _read_file(self) -> str:
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"[ERROR] Gagal membaca {self.path}: {e}")
            return ""

    def _extract_var(self, var_name: str) -> Optional[str]:
        patterns = [
            rf'{var_name}="([^"]*)"',
            rf"{var_name}='([^']*)'",
            rf'{var_name}=([^\s\n]+)'
        ]
        for pattern in patterns:
            match = re.search(pattern, self.content)
            if match:
                return match.group(1).strip()
        return None

    def parse(self) -> Dict:
        data = {
            'homepage':             self._extract_var('TERMUX_PKG_HOMEPAGE') or '',
            'description':          self._extract_var('TERMUX_PKG_DESCRIPTION') or '',
            'license':              self._extract_var('TERMUX_PKG_LICENSE') or '',
            'maintainer':           self._extract_var('TERMUX_PKG_MAINTAINER') or '',
            'version':              self._extract_var('TERMUX_PKG_VERSION') or '',
            'srcurl':               self._extract_var('TERMUX_PKG_SRCURL') or '',
            'sha256':               self._extract_var('TERMUX_PKG_SHA256') or '',
            'depends':              self._parse_depends(),
            'platform_independent': self._extract_var('TERMUX_PKG_PLATFORM_INDEPENDENT') == 'true',
        }
        return data

    def _parse_depends(self) -> List[str]:
        depends_str = self._extract_var('TERMUX_PKG_DEPENDS')
        if not depends_str:
            return []
        deps = [dep.strip() for dep in depends_str.split(',')]
        return [dep for dep in deps if dep]


class PackageIndexGenerator:

    def __init__(self, packages_dir: str = "packages", output_file: str = "tools/index.json"):
        self.packages_dir = Path(packages_dir)
        self.output_file = Path(output_file)
        self.repo_source = "https://github.com/djunekz/termux-app-store"

    def _get_package_dirs(self) -> List[Path]:
        if not self.packages_dir.exists():
            print(f"[ERROR] Directory {self.packages_dir} tidak ditemukan!")
            return []
        package_dirs = []
        for item in self.packages_dir.iterdir():
            if item.is_dir() and (item / "build.sh").exists():
                package_dirs.append(item)
        return sorted(package_dirs)

    def _estimate_download_size(self, srcurl: str) -> str:
        return "Unknown"

    def _estimate_installed_size(self, package_name: str) -> str:
        return "Unknown"

    def _create_package_entry(self, package_dir: Path) -> Dict:
        package_name = package_dir.name
        build_sh_path = package_dir / "build.sh"
        parser = BuildShParser(str(build_sh_path))
        metadata = parser.parse()
        entry = {
            "package":            package_name,
            "version":            metadata['version'],
            "maintainer":         metadata['maintainer'],
            "description":        metadata['description'],
            "homepage":           metadata['homepage'],
            "license":            metadata['license'],
            "download_size":      self._estimate_download_size(metadata['srcurl']),
            "installed_size":     self._estimate_installed_size(package_name),
            "source":             self.repo_source,
            "srcurl":             metadata['srcurl'],
            "sha256":             metadata['sha256'],
            "platform_independent": metadata['platform_independent'],
        }
        if metadata['depends']:
            entry['depends'] = metadata['depends']
        return entry

    def generate(self) -> Dict:
        package_dirs = self._get_package_dirs()
        if not package_dirs:
            return {"packages": [], "total": 0}
        packages = []
        for pkg_dir in package_dirs:
            try:
                entry = self._create_package_entry(pkg_dir)
                packages.append(entry)
            except Exception as e:
                print(f"[ERROR] Failed to process {pkg_dir.name}: {e}")
                continue
        packages.sort(key=lambda x: x['package'])
        from datetime import datetime, timezone
        index_data = {
            "version":      "1.0",
            "repository":   self.repo_source,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total":        len(packages),
            "packages":     packages,
        }
        return index_data

    def save(self, data: Dict):
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def run(self):
        data = self.generate()
        self.save(data)


def make_build_sh(pkg_dir: Path, fields: dict) -> Path:
    pkg_dir.mkdir(parents=True, exist_ok=True)
    lines = [f'{k}="{v}"' for k, v in fields.items()]
    (pkg_dir / "build.sh").write_text("\n".join(lines) + "\n")
    return pkg_dir


class TestMakeBuildSh:

    def test_creates_dir_and_file(self, tmp_path):
        pkg_dir = tmp_path / "bower"
        result = make_build_sh(pkg_dir, {"TERMUX_PKG_VERSION": "1.8.12"})
        assert result == pkg_dir
        assert (pkg_dir / "build.sh").exists()

    def test_file_content_correct(self, tmp_path):
        pkg_dir = tmp_path / "mytool"
        make_build_sh(pkg_dir, {
            "TERMUX_PKG_VERSION": "1.0",
            "TERMUX_PKG_LICENSE": "MIT",
        })
        content = (pkg_dir / "build.sh").read_text()
        assert 'TERMUX_PKG_VERSION="1.0"' in content
        assert 'TERMUX_PKG_LICENSE="MIT"' in content

    def test_creates_nested_dirs(self, tmp_path):
        pkg_dir = tmp_path / "deep" / "nested" / "pkg"
        make_build_sh(pkg_dir, {"TERMUX_PKG_VERSION": "2.0"})
        assert pkg_dir.exists()
        assert (pkg_dir / "build.sh").exists()


class TestBuildShParserReadFile:

    def test_reads_valid_file(self, tmp_path):
        f = tmp_path / "build.sh"
        f.write_text('TERMUX_PKG_VERSION="1.0"\n')
        parser = BuildShParser(str(f))
        assert 'TERMUX_PKG_VERSION' in parser.content

    def test_returns_empty_on_missing_file(self, tmp_path):
        parser = BuildShParser(str(tmp_path / "nonexistent.sh"))
        assert parser.content == ""

    def test_returns_empty_on_permission_error(self, tmp_path):
        f = tmp_path / "build.sh"
        f.write_text("content")
        with patch("builtins.open", side_effect=PermissionError("denied")):
            parser = BuildShParser(str(f))
            assert parser.content == ""


class TestBuildShParserExtractVar:

    def _parser(self, content: str) -> BuildShParser:
        p = BuildShParser.__new__(BuildShParser)
        p.path = "mock"
        p.content = content
        return p

    def test_double_quotes(self):
        p = self._parser('TERMUX_PKG_VERSION="1.2.3"\n')
        assert p._extract_var("TERMUX_PKG_VERSION") == "1.2.3"

    def test_single_quotes(self):
        p = self._parser("TERMUX_PKG_VERSION='1.2.3'\n")
        assert p._extract_var("TERMUX_PKG_VERSION") == "1.2.3"

    def test_no_quotes(self):
        p = self._parser("TERMUX_PKG_VERSION=1.2.3\n")
        assert p._extract_var("TERMUX_PKG_VERSION") == "1.2.3"

    def test_returns_none_when_missing(self):
        p = self._parser("TERMUX_PKG_LICENSE=MIT\n")
        assert p._extract_var("TERMUX_PKG_VERSION") is None

    def test_empty_content(self):
        p = self._parser("")
        assert p._extract_var("TERMUX_PKG_VERSION") is None

    def test_platform_independent_true(self):
        p = self._parser('TERMUX_PKG_PLATFORM_INDEPENDENT="true"\n')
        assert p._extract_var("TERMUX_PKG_PLATFORM_INDEPENDENT") == "true"

    def test_platform_independent_false(self):
        p = self._parser('TERMUX_PKG_PLATFORM_INDEPENDENT="false"\n')
        assert p._extract_var("TERMUX_PKG_PLATFORM_INDEPENDENT") == "false"


class TestBuildShParserParse:

    def test_full_parse(self, tmp_path):
        f = tmp_path / "build.sh"
        f.write_text(
            'TERMUX_PKG_HOMEPAGE="https://example.com"\n'
            'TERMUX_PKG_DESCRIPTION="A cool tool"\n'
            'TERMUX_PKG_LICENSE="MIT"\n'
            'TERMUX_PKG_MAINTAINER="@djunekz"\n'
            'TERMUX_PKG_VERSION="1.2.3"\n'
            'TERMUX_PKG_SRCURL="https://example.com/src.tar.gz"\n'
            'TERMUX_PKG_SHA256="abc123"\n'
            'TERMUX_PKG_DEPENDS="nodejs, python"\n'
            'TERMUX_PKG_PLATFORM_INDEPENDENT="true"\n'
        )
        parser = BuildShParser(str(f))
        data = parser.parse()
        assert data['homepage']             == "https://example.com"
        assert data['description']          == "A cool tool"
        assert data['license']              == "MIT"
        assert data['maintainer']           == "@djunekz"
        assert data['version']              == "1.2.3"
        assert data['srcurl']               == "https://example.com/src.tar.gz"
        assert data['sha256']               == "abc123"
        assert data['depends']              == ["nodejs", "python"]
        assert data['platform_independent'] is True

    def test_empty_file_defaults(self, tmp_path):
        f = tmp_path / "build.sh"
        f.write_text("")
        data = BuildShParser(str(f)).parse()
        assert data['version']              == ""
        assert data['description']          == ""
        assert data['depends']              == []
        assert data['platform_independent'] is False

    def test_missing_file_defaults(self, tmp_path):
        data = BuildShParser(str(tmp_path / "missing.sh")).parse()
        assert data['version'] == ""
        assert data['depends'] == []


class TestParseDependsMethod:

    def _parser(self, content: str) -> BuildShParser:
        p = BuildShParser.__new__(BuildShParser)
        p.path = "mock"
        p.content = content
        return p

    def test_single_dep(self):
        p = self._parser('TERMUX_PKG_DEPENDS="nodejs"\n')
        assert p._parse_depends() == ["nodejs"]

    def test_multiple_deps(self):
        p = self._parser('TERMUX_PKG_DEPENDS="nodejs, python, git"\n')
        assert p._parse_depends() == ["nodejs", "python", "git"]

    def test_no_depends(self):
        p = self._parser('TERMUX_PKG_VERSION="1.0"\n')
        assert p._parse_depends() == []

    def test_empty_depends(self):
        p = self._parser('TERMUX_PKG_DEPENDS=""\n')
        assert p._parse_depends() == []

    def test_strips_whitespace(self):
        p = self._parser('TERMUX_PKG_DEPENDS="  nodejs ,  python  "\n')
        assert "nodejs" in p._parse_depends()
        assert "python" in p._parse_depends()


class TestGetPackageDirs:

    def test_returns_sorted_dirs(self, tmp_path):
        for name in ["zx", "aircrack", "bower"]:
            d = tmp_path / name
            d.mkdir()
            (d / "build.sh").write_text("")
        gen = PackageIndexGenerator(str(tmp_path))
        dirs = gen._get_package_dirs()
        names = [d.name for d in dirs]
        assert names == sorted(names)

    def test_skips_dirs_without_build_sh(self, tmp_path):
        valid = tmp_path / "valid"
        valid.mkdir()
        (valid / "build.sh").write_text("")
        (tmp_path / "nodotbuildsh").mkdir()
        gen = PackageIndexGenerator(str(tmp_path))
        names = [d.name for d in gen._get_package_dirs()]
        assert "valid" in names
        assert "nodotbuildsh" not in names

    def test_missing_packages_dir_returns_empty(self, tmp_path):
        gen = PackageIndexGenerator(str(tmp_path / "nonexistent"))
        assert gen._get_package_dirs() == []

    def test_empty_dir_returns_empty(self, tmp_path):
        gen = PackageIndexGenerator(str(tmp_path))
        assert gen._get_package_dirs() == []


class TestGenerate:

    def test_empty_packages(self, tmp_path):
        gen = PackageIndexGenerator(str(tmp_path))
        result = gen.generate()
        assert result == {"packages": [], "total": 0}

    def test_missing_dir_returns_empty(self, tmp_path):
        gen = PackageIndexGenerator(str(tmp_path / "missing"))
        result = gen.generate()
        assert result["total"] == 0
        assert result["packages"] == []

    def test_generates_with_packages(self, tmp_path):
        for name, ver in [("bower", "1.8.12"), ("zx", "8.0.0")]:
            d = tmp_path / name
            d.mkdir()
            (d / "build.sh").write_text(f'TERMUX_PKG_VERSION="{ver}"\n')
        gen = PackageIndexGenerator(str(tmp_path))
        result = gen.generate()
        assert result["total"] == 2

    def test_packages_sorted_alphabetically(self, tmp_path):
        for name in ["zx", "aircrack", "bower"]:
            d = tmp_path / name
            d.mkdir()
            (d / "build.sh").write_text(f'TERMUX_PKG_VERSION="1.0"\n')
        gen = PackageIndexGenerator(str(tmp_path))
        result = gen.generate()
        names = [p["package"] for p in result["packages"]]
        assert names == sorted(names)

    def test_error_in_one_package_continues(self, tmp_path):
        good = tmp_path / "good"
        good.mkdir()
        (good / "build.sh").write_text('TERMUX_PKG_VERSION="1.0"\n')

        bad = tmp_path / "bad"
        bad.mkdir()
        (bad / "build.sh").write_text('TERMUX_PKG_VERSION="1.0"\n')

        gen = PackageIndexGenerator(str(tmp_path))
        original = gen._create_package_entry

        def mock_entry(pkg_dir):
            if pkg_dir.name == "good":
                return original(pkg_dir)
            raise RuntimeError("simulated error")

        gen._create_package_entry = mock_entry
        result = gen.generate()
        assert result["total"] == 1
        assert result["packages"][0]["package"] == "good"

    def test_result_has_required_keys(self, tmp_path):
        d = tmp_path / "mytool"
        d.mkdir()
        (d / "build.sh").write_text('TERMUX_PKG_VERSION="1.0"\n')
        gen = PackageIndexGenerator(str(tmp_path))
        result = gen.generate()
        for key in ["version", "repository", "generated_at", "total", "packages"]:
            assert key in result

    def test_platform_independent_field(self, tmp_path):
        d = tmp_path / "mytool"
        d.mkdir()
        (d / "build.sh").write_text(
            'TERMUX_PKG_VERSION="1.0"\n'
            'TERMUX_PKG_PLATFORM_INDEPENDENT="true"\n'
        )
        gen = PackageIndexGenerator(str(tmp_path))
        result = gen.generate()
        assert result["packages"][0]["platform_independent"] is True

    def test_depends_included_when_present(self, tmp_path):
        d = tmp_path / "mytool"
        d.mkdir()
        (d / "build.sh").write_text(
            'TERMUX_PKG_VERSION="1.0"\n'
            'TERMUX_PKG_DEPENDS="nodejs"\n'
        )
        gen = PackageIndexGenerator(str(tmp_path))
        result = gen.generate()
        assert "depends" in result["packages"][0]
        assert result["packages"][0]["depends"] == ["nodejs"]

    def test_depends_omitted_when_absent(self, tmp_path):
        d = tmp_path / "mytool"
        d.mkdir()
        (d / "build.sh").write_text('TERMUX_PKG_VERSION="1.0"\n')
        gen = PackageIndexGenerator(str(tmp_path))
        result = gen.generate()
        assert "depends" not in result["packages"][0]


class TestRun:

    def test_run_creates_output_file(self, tmp_path):
        d = tmp_path / "bower"
        d.mkdir()
        (d / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        output = tmp_path / "out" / "index.json"
        gen = PackageIndexGenerator(str(tmp_path), str(output))
        gen.run()
        assert output.exists()
        data = json.loads(output.read_text())
        assert data["total"] == 1

    def test_run_empty_packages(self, tmp_path):
        output = tmp_path / "index.json"
        gen = PackageIndexGenerator(str(tmp_path), str(output))
        gen.run()
        assert output.exists()
        data = json.loads(output.read_text())
        assert data == {"packages": [], "total": 0}


class TestSave:

    def test_saves_valid_json(self, tmp_path):
        output = tmp_path / "out" / "index.json"
        gen = PackageIndexGenerator(output_file=str(output))
        data = {"packages": [], "total": 0, "version": "1.0"}
        gen.save(data)
        assert output.exists()
        loaded = json.loads(output.read_text())
        assert loaded["total"] == 0

    def test_creates_parent_dirs(self, tmp_path):
        output = tmp_path / "deep" / "nested" / "index.json"
        gen = PackageIndexGenerator(output_file=str(output))
        gen.save({"packages": []})
        assert output.exists()

    def test_unicode_preserved(self, tmp_path):
        output = tmp_path / "index.json"
        gen = PackageIndexGenerator(output_file=str(output))
        gen.save({"desc": "Tes bahasa Indonesia: €, ñ, 中文"})
        content = output.read_text(encoding="utf-8")
        assert "Indonesia" in content


import importlib.util as _ilu

def _import_build():
    build_path = Path(__file__).parent.parent / "tools" / "build.py"
    spec = _ilu.spec_from_file_location("build_module", str(build_path))
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestMainFunction:

    def test_main_from_root_with_packages(self, tmp_path, monkeypatch):
        (tmp_path / "packages").mkdir()
        bower = tmp_path / "packages" / "bower"
        bower.mkdir()
        (bower / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        (tmp_path / "tools").mkdir()
        monkeypatch.chdir(tmp_path)

        build = _import_build()
        result = build.main()
        assert result == 0
        assert (tmp_path / "tools" / "index.json").exists()

    def test_main_from_tools_subdir(self, tmp_path, monkeypatch):
        (tmp_path / "packages").mkdir()
        bower = tmp_path / "packages" / "bower"
        bower.mkdir()
        (bower / "build.sh").write_text('TERMUX_PKG_VERSION="1.8.12"\n')
        tools_dir = tmp_path / "tools"
        tools_dir.mkdir()
        monkeypatch.chdir(tools_dir)

        build = _import_build()
        result = build.main()
        assert result == 0

    def test_main_no_packages_dir_returns_1(self, tmp_path, monkeypatch):
        isolated = tmp_path / "a" / "b" / "c"
        isolated.mkdir(parents=True)
        monkeypatch.chdir(isolated)

        build = _import_build()
        result = build.main()
        assert result == 1
