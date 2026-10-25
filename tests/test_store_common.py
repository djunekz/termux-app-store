import ast
import hashlib
import json
import re
from pathlib import Path

import pytest
from _loader import PACKAGE_DIR, load_cli, load_store_common

sc = load_store_common()


class TestVerTuple:
    @pytest.mark.parametrize(
        "version,expected",
        [
            ("1.2.3", (1, 2, 3, 0)),
            ("1.2.3-4", (1, 2, 3, 4)),
            ("0.0.0+4551c2f", (0, 0, 0, 0)),
            ("1.alpha.3", (1, 0, 3, 0)),
            ("1.2.3-beta", (1, 2, 3, 0)),
            ("  2.0  ", (2, 0, 0)),
        ],
    )
    def test_values(self, version, expected):
        assert sc.ver_tuple(version) == expected

    def test_ordering(self):
        assert sc.ver_tuple("1.10.0") > sc.ver_tuple("1.9.0")
        assert sc.ver_tuple("1.0.0-2") > sc.ver_tuple("1.0.0-1")


class TestPackageNames:
    @pytest.mark.parametrize("name", ["aichat", "ani-cli", "python3.12", "g++", "a_b".replace("_", "-")])
    def test_safe(self, name):
        assert sc.is_safe_pkg_name(name)

    @pytest.mark.parametrize("name", ["", "../etc", "a/b", "a b", "-lead", "x;rm", "a..b", ".hidden"])
    def test_unsafe(self, name):
        assert not sc.is_safe_pkg_name(name)

    def test_normalize_sha256(self):
        good = "a" * 64
        assert sc.normalize_sha256(good.upper()) == good
        assert sc.normalize_sha256(" " + good + "\n") == good
        assert sc.normalize_sha256("a" * 16) == ""
        assert sc.normalize_sha256(None) == ""
        assert sc.normalize_sha256("g" * 64) == ""


def make_root(root: Path, fingerprint: bool = True) -> Path:
    (root / "packages").mkdir(parents=True, exist_ok=True)
    head = f"#!/bin/bash\n# {sc.FINGERPRINT_STRING}\n" if fingerprint else "#!/bin/bash\n"
    (root / "build-package.sh").write_text(head + "set -e\n")
    return root


class TestRoots:
    def test_fingerprint(self, tmp_path):
        assert sc.has_store_fingerprint(make_root(tmp_path / "a"))
        assert not sc.has_store_fingerprint(make_root(tmp_path / "b", fingerprint=False))
        assert not sc.has_store_fingerprint(tmp_path / "missing")

    def test_valid_root(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        assert sc.is_valid_root(make_root(tmp_path / "ok"))
        assert not sc.is_valid_root(make_root(tmp_path / "nofp", fingerprint=False))
        assert not sc.is_valid_root(tmp_path / "nothing")
        (tmp_path / "nopkgs").mkdir()
        assert not sc.is_valid_root(tmp_path / "nopkgs")

    def test_cache_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        root = make_root(tmp_path / "root")
        cache = tmp_path / "deep" / "path.json"
        sc.save_cached_root(root, cache)
        assert json.loads(cache.read_text()) == {"app_root": str(root)}
        assert sc.load_cached_root(cache) == root.resolve()

    def test_cache_rejects_garbage_and_stale_entries(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        cache = tmp_path / "path.json"
        assert sc.load_cached_root(cache) is None
        cache.write_text("{ not json")
        assert sc.load_cached_root(cache) is None
        cache.write_text(json.dumps({"other": 1}))
        assert sc.load_cached_root(cache) is None
        cache.write_text(json.dumps({"app_root": str(tmp_path / "gone")}))
        assert sc.load_cached_root(cache) is None
        cache.write_text(json.dumps(["not", "a", "dict"]))
        assert sc.load_cached_root(cache) is None

    def test_resolve_prefers_environment(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        root = make_root(tmp_path / "envroot")
        monkeypatch.setenv("TERMUX_APP_STORE_HOME", str(root))
        cache = tmp_path / "path.json"
        assert sc.resolve_app_root(str(tmp_path / "x" / "y" / "mod.py"), cache) == root.resolve()
        assert sc.load_cached_root(cache) == root.resolve()

    def test_resolve_ignores_invalid_environment(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        monkeypatch.setenv("TERMUX_APP_STORE_HOME", str(tmp_path / "bogus"))
        source = make_root(tmp_path / "src")
        module_file = source / "termux_app_store" / "mod.py"
        module_file.parent.mkdir()
        module_file.write_text("")
        assert sc.resolve_app_root(str(module_file), tmp_path / "path.json") == source.resolve()

    def test_resolve_falls_back_to_pip_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path / "home"))
        monkeypatch.delenv("TERMUX_APP_STORE_HOME", raising=False)
        module_file = tmp_path / "site" / "termux_app_store" / "mod.py"
        module_file.parent.mkdir(parents=True)
        module_file.write_text("")
        result = sc.resolve_app_root(str(module_file), tmp_path / "path.json")
        assert result == tmp_path / "home" / ".termux-app-store"
        assert (result / "packages").is_dir()


class TestIndexCache:
    def test_load(self, tmp_path):
        cache = tmp_path / "index.json"
        assert sc.load_index_cache(cache) == []
        cache.write_text(json.dumps({"packages": [{"package": "a"}]}))
        assert sc.load_index_cache(cache) == [{"package": "a"}]
        cache.write_text("{ broken")
        assert sc.load_index_cache(cache) == []

    def test_recipe_checksum_lookup(self, tmp_path):
        cache = tmp_path / "index.json"
        digest = "b" * 64
        cache.write_text(
            json.dumps(
                {
                    "packages": [
                        {"package": "a", "recipe_sha256": digest.upper()},
                        {"package": "b"},
                        {"package": "c", "recipe_sha256": "short"},
                    ]
                }
            )
        )
        assert sc.lookup_recipe_sha256("a", cache) == digest
        assert sc.lookup_recipe_sha256("b", cache) == ""
        assert sc.lookup_recipe_sha256("c", cache) == ""
        assert sc.lookup_recipe_sha256("missing", cache) == ""


class FakeResponse:
    def __init__(self, body: bytes):
        self.body = body

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.body


def serve(monkeypatch, body: bytes, seen=None):
    def fake_urlopen(req, timeout=0):
        if seen is not None:
            seen.append(req.full_url)
        return FakeResponse(body)

    monkeypatch.setattr(sc.urllib.request, "urlopen", fake_urlopen)


def collect():
    messages = []
    return messages, lambda kind, text: messages.append((kind, text))


class TestVerifyDownloadedScript:
    SCRIPT = b"#!/bin/bash\necho hi\n"

    def test_requires_pin_by_default(self, monkeypatch):
        monkeypatch.delenv("PIN_VAR", raising=False)
        monkeypatch.delenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH", raising=False)
        messages, log = collect()
        assert sc.verify_downloaded_script(self.SCRIPT, "PIN_VAR", log) is False
        assert any(kind == "error" and "pinned checksum" in text for kind, text in messages)
        assert any(hashlib.sha256(self.SCRIPT).hexdigest() in text for _, text in messages)

    def test_matching_pin_passes(self, monkeypatch):
        monkeypatch.setenv("PIN_VAR", hashlib.sha256(self.SCRIPT).hexdigest().upper())
        assert sc.verify_downloaded_script(self.SCRIPT, "PIN_VAR") is True

    def test_wrong_pin_fails(self, monkeypatch):
        monkeypatch.setenv("PIN_VAR", "0" * 64)
        assert sc.verify_downloaded_script(self.SCRIPT, "PIN_VAR") is False

    def test_explicit_opt_out(self, monkeypatch):
        monkeypatch.delenv("PIN_VAR", raising=False)
        monkeypatch.setenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH", "1")
        assert sc.verify_downloaded_script(self.SCRIPT, "PIN_VAR") is True

    def test_syntax_error_fails_even_with_valid_pin(self, monkeypatch):
        broken = b"if then\n"
        monkeypatch.setenv("PIN_VAR", hashlib.sha256(broken).hexdigest())
        assert sc.verify_downloaded_script(broken, "PIN_VAR") is False

    def test_empty_payload(self):
        assert sc.verify_downloaded_script(b"", "PIN_VAR") is False


class TestEnsureBuildPackageSh:
    def test_existing_file_is_kept(self, tmp_path, monkeypatch):
        (tmp_path / "build-package.sh").write_text("mine")
        monkeypatch.setattr(sc, "packaged_build_script", lambda: None)
        serve(monkeypatch, b"never")
        assert sc.ensure_build_package_sh(tmp_path) is True
        assert (tmp_path / "build-package.sh").read_text() == "mine"

    def test_packaged_copy_needs_no_network(self, tmp_path, monkeypatch):
        packaged = tmp_path / "packaged.sh"
        packaged.write_text("#!/bin/bash\necho packaged\n")
        monkeypatch.setattr(sc, "packaged_build_script", lambda: packaged)

        def no_network(*args, **kwargs):
            raise AssertionError("network must not be used")

        monkeypatch.setattr(sc.urllib.request, "urlopen", no_network)
        root = tmp_path / "root"
        root.mkdir()
        assert sc.ensure_build_package_sh(root) is True
        assert (root / "build-package.sh").read_text() == packaged.read_text()
        assert (root / "build-package.sh").stat().st_mode & 0o111

    def test_download_refused_without_pin(self, tmp_path, monkeypatch):
        monkeypatch.setattr(sc, "packaged_build_script", lambda: None)
        monkeypatch.delenv("TERMUX_APP_STORE_BUILD_SH_SHA256", raising=False)
        monkeypatch.delenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH", raising=False)
        serve(monkeypatch, b"#!/bin/bash\necho x\n")
        messages, log = collect()
        assert sc.ensure_build_package_sh(tmp_path, log) is False
        assert not (tmp_path / "build-package.sh").exists()
        assert any("refusing" in text for _, text in messages)

    def test_download_accepted_with_matching_pin(self, tmp_path, monkeypatch):
        body = b"#!/bin/bash\necho ok\n"
        monkeypatch.setattr(sc, "packaged_build_script", lambda: None)
        monkeypatch.setenv("TERMUX_APP_STORE_BUILD_SH_SHA256", hashlib.sha256(body).hexdigest())
        serve(monkeypatch, body)
        messages, log = collect()
        assert sc.ensure_build_package_sh(tmp_path, log) is True
        assert (tmp_path / "build-package.sh").read_bytes() == body
        assert ("ok", "build-package.sh ready.") in messages

    def test_network_error_is_reported(self, tmp_path, monkeypatch):
        monkeypatch.setattr(sc, "packaged_build_script", lambda: None)

        def boom(*args, **kwargs):
            raise OSError("offline")

        monkeypatch.setattr(sc.urllib.request, "urlopen", boom)
        messages, log = collect()
        assert sc.ensure_build_package_sh(tmp_path, log) is False
        assert any(kind == "error" and "offline" in text for kind, text in messages)


class TestDownloadRecipe:
    BODY = b"TERMUX_PKG_VERSION=1\n"

    def digest(self, body=None):
        return hashlib.sha256(body or self.BODY).hexdigest()

    def test_verified_recipe_is_written(self, tmp_path, monkeypatch):
        seen = []
        serve(monkeypatch, self.BODY, seen)
        assert sc.download_recipe(tmp_path, "demo", self.digest()) is True
        assert (tmp_path / "demo" / "build.sh").read_bytes() == self.BODY
        assert seen == [f"{sc.RAW_BASE}/packages/demo/build.sh"]
        assert not list((tmp_path / "demo").glob("*.part"))

    def test_existing_recipe_is_kept_without_network(self, tmp_path, monkeypatch):
        (tmp_path / "demo").mkdir()
        (tmp_path / "demo" / "build.sh").write_text("local")
        serve(monkeypatch, b"never")
        assert sc.download_recipe(tmp_path, "demo", self.digest()) is True
        assert (tmp_path / "demo" / "build.sh").read_text() == "local"

    def test_force_update_replaces_existing(self, tmp_path, monkeypatch):
        (tmp_path / "demo").mkdir()
        (tmp_path / "demo" / "build.sh").write_text("old")
        serve(monkeypatch, self.BODY)
        assert sc.download_recipe(tmp_path, "demo", self.digest(), force_update=True) is True
        assert (tmp_path / "demo" / "build.sh").read_bytes() == self.BODY

    def test_checksum_mismatch_is_refused(self, tmp_path, monkeypatch):
        serve(monkeypatch, b"evil\n")
        messages, log = collect()
        assert sc.download_recipe(tmp_path, "demo", self.digest(), log=log) is False
        assert not (tmp_path / "demo" / "build.sh").exists()
        assert any("does not match" in text for _, text in messages)

    def test_missing_checksum_is_refused(self, tmp_path, monkeypatch):
        monkeypatch.delenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_RECIPE", raising=False)
        serve(monkeypatch, self.BODY)
        messages, log = collect()
        assert sc.download_recipe(tmp_path, "demo", "", log=log) is False
        assert not (tmp_path / "demo" / "build.sh").exists()
        assert any("No recipe checksum" in text for _, text in messages)

    def test_explicit_opt_out_accepts_unpinned(self, tmp_path, monkeypatch):
        monkeypatch.setenv("TERMUX_APP_STORE_ALLOW_UNVERIFIED_RECIPE", "1")
        serve(monkeypatch, self.BODY)
        assert sc.download_recipe(tmp_path, "demo", "") is True

    def test_syntax_error_is_refused_even_with_valid_checksum(self, tmp_path, monkeypatch):
        broken = b"if then\n"
        serve(monkeypatch, broken)
        assert sc.download_recipe(tmp_path, "demo", self.digest(broken)) is False
        assert not (tmp_path / "demo" / "build.sh").exists()

    @pytest.mark.parametrize("name", ["../evil", "a/b", "", "x;y"])
    def test_unsafe_names_never_touch_the_network(self, tmp_path, monkeypatch, name):
        def no_network(*args, **kwargs):
            raise AssertionError("network must not be used")

        monkeypatch.setattr(sc.urllib.request, "urlopen", no_network)
        assert sc.download_recipe(tmp_path, name, self.digest()) is False

    def test_network_error_is_reported(self, tmp_path, monkeypatch):
        def boom(*args, **kwargs):
            raise OSError("offline")

        monkeypatch.setattr(sc.urllib.request, "urlopen", boom)
        messages, log = collect()
        assert sc.download_recipe(tmp_path, "demo", self.digest(), log=log) is False
        assert any(kind == "error" for kind, _ in messages)


class TestMirrors:
    def test_index_urls_keep_their_order_and_skip_jsdelivr(self):
        assert sc.index_urls() == [
            "https://raw.githubusercontent.com/djunekz/termux-app-store/master/tools/index.json",
            "https://termux-app-store.pages.dev/tools/index.json",
            "https://djunekz.github.io/termux-app-store/tools/index.json",
        ]

    def test_single_mirror_list_with_unique_priorities(self):
        priorities = [m["priority"] for m in sc.MIRRORS]
        assert priorities == sorted(priorities) and len(set(priorities)) == len(priorities)
        assert [m["id"] for m in sc.MIRRORS] == ["cloudflare", "github-pages", "jsdelivr"]
        assert all(m["base_url"].startswith("https://") for m in sc.MIRRORS)


FRONTENDS = ["termux_app_store_cli.py", "termux_app_store.py", "fast_install.py"]
MOVED = {
    "_ver_tuple",
    "ver_tuple",
    "is_safe_pkg_name",
    "has_store_fingerprint",
    "is_valid_root",
    "_verify_downloaded_script",
    "verify_downloaded_script",
}


class TestNoDuplicatedLogic:
    @pytest.mark.parametrize("filename", FRONTENDS)
    def test_moved_functions_are_not_redefined(self, filename):
        tree = ast.parse((PACKAGE_DIR / filename).read_text(encoding="utf-8"))
        defined = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
        assert not (defined & MOVED), f"{filename} redefines shared logic: {defined & MOVED}"

    @pytest.mark.parametrize("filename", FRONTENDS)
    def test_frontends_use_the_shared_module(self, filename):
        text = (PACKAGE_DIR / filename).read_text(encoding="utf-8")
        assert "store_common" in text

    def test_mirror_urls_live_in_one_place(self):
        offenders = [
            p.name
            for p in PACKAGE_DIR.glob("*.py")
            if p.name != "store_common.py" and "termux-app-store.pages.dev" in p.read_text(encoding="utf-8")
        ]
        assert offenders == []

    def test_recipe_download_is_defined_once(self):
        offenders = [
            p.name
            for p in PACKAGE_DIR.glob("*.py")
            if p.name != "store_common.py"
            and re.search(r"/packages/\{[a-z_]+\}/build\.sh", p.read_text(encoding="utf-8"))
        ]
        assert offenders == []

    def test_frontends_share_the_same_objects(self):
        cli = load_cli()
        assert cli.MIRRORS == sc.MIRRORS
        assert cli._ver_tuple("1.2.3-4") == sc.ver_tuple("1.2.3-4")
        assert cli.GITHUB_REPO == sc.GITHUB_REPO
        assert cli.FINGERPRINT_STRING == sc.FINGERPRINT_STRING
