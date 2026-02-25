from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import APP_NAME, APP_VERSION
from .paths import find_root, packages_dir
from .ops import CommandError, build_install, environment_summary, open_url, uninstall


def _import_package_manager(root: Path):
    """Import tools.package_manager from either repo root or installed root."""
    tools_path = root / "tools"
    if tools_path.is_dir() and str(root) not in sys.path:
        sys.path.insert(0, str(root))
    try:
        from tools.package_manager import AppUpdateChecker, PackageManager

        return PackageManager, AppUpdateChecker
    except Exception as e:  # pragma: no cover
        raise RuntimeError(
            "Cannot import tools/package_manager.py. "
            "If you installed from source, make sure tools/ was copied."
        ) from e


def _normalize(pkg: Dict[str, Any]) -> Dict[str, Any]:
    # Keep compatibility across local/remote formats
    pkg = dict(pkg)
    pkg.setdefault("name", pkg.get("package"))
    desc = pkg.get("desc") or pkg.get("description") or pkg.get("summary") or "-"
    pkg["desc"] = desc
    pkg.setdefault("description", desc)
    pkg.setdefault("homepage", "-")
    pkg.setdefault("license", "-")
    pkg.setdefault("maintainer", "-")
    pkg.setdefault("version", "?")
    pkg.setdefault("depends", pkg.get("depends") or pkg.get("depends") or [])
    if isinstance(pkg.get("depends"), str):
        pkg["depends"] = [x.strip() for x in pkg["depends"].split(",") if x.strip()]
    return pkg


def _print_table(rows: List[List[str]], headers: List[str]) -> None:
    widths = [len(h) for h in headers]
    for r in rows:
        for i, c in enumerate(r):
            widths[i] = max(widths[i], len(c))

    def fmt(r):
        return "  ".join(c.ljust(widths[i]) for i, c in enumerate(r))

    print(fmt(headers))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print(fmt(r))


def cmd_list(pm, args) -> int:
    packages = [_normalize(p) for p in pm.load_packages()]
    if args.query:
        q = args.query.lower()
        packages = [
            p
            for p in packages
            if q in (p.get("package") or "").lower() or q in (p.get("desc") or "").lower()
        ]

    if args.json:
        print(json.dumps(packages, indent=2, ensure_ascii=False))
        return 0

    rows = []
    for p in packages:
        status, status_desc = pm.get_status(p["package"], p.get("version") or "?")
        if args.installed and status == "NOT_INSTALLED":
            continue
        if args.updates and status != "UPDATE":
            continue
        rows.append([
            p["package"],
            p.get("version") or "?",
            status,
            (p.get("desc") or "-")[:60],
        ])

    _print_table(rows, ["PACKAGE", "VERSION", "STATUS", "DESCRIPTION"])
    return 0


def cmd_show(pm, args) -> int:
    pkg = pm.get_package(args.package)
    if not pkg:
        print(f"[!] Package not found: {args.package}")
        return 1
    pkg = _normalize(pkg)
    status, status_desc = pm.get_status(pkg["package"], pkg.get("version") or "?")
    print(f"{pkg['package']}  (v{pkg.get('version') or '?'})")
    print(f"Status     : {status} — {status_desc}")
    print(f"Maintainer : {pkg.get('maintainer','-')}")
    print(f"License    : {pkg.get('license','-')}")
    print(f"Homepage   : {pkg.get('homepage','-')}")
    if pkg.get("depends"):
        print(f"Depends    : {', '.join(pkg['depends'])}")
    print("")
    print(pkg.get("description") or pkg.get("desc") or "-")
    return 0


def cmd_install(root: Path, pm, args) -> int:
    pkg = pm.get_package(args.package)
    if not pkg:
        print(f"[!] Package not found: {args.package}")
        return 1
    try:
        return build_install(root, args.package)
    except CommandError as e:
        print(f"[✗] {e}")
        return 1


def cmd_uninstall(pm, args) -> int:
    code, method = uninstall(args.package)
    if code == 0:
        print(f"[✓] Uninstalled via {method}: {args.package}")
    else:
        print(f"[✗] Uninstall failed ({method}).")
    return code


def cmd_update(pm, args) -> int:
    pm.clear_cache()
    pkgs = pm.load_packages()
    print(f"[✓] Index refreshed. Packages: {len(pkgs)}")
    return 0


def cmd_upgrade(root: Path, pm, args) -> int:
    packages = [_normalize(p) for p in pm.load_packages()]
    targets: List[str]
    if args.package:
        targets = [args.package]
    else:
        targets = []
        for p in packages:
            status, _ = pm.get_status(p["package"], p.get("version") or "?")
            if status in ("NOT_INSTALLED", "UPDATE"):
                targets.append(p["package"])

    if not targets:
        print("[i] Nothing to upgrade.")
        return 0

    failures = 0
    for t in targets:
        print(f"\n==> {t}")
        code = cmd_install(root, pm, argparse.Namespace(package=t))
        if code != 0:
            failures += 1

    return 1 if failures else 0


def cmd_doctor(root: Path) -> int:
    info = environment_summary()
    info["root"] = str(root)
    info["packages_dir"] = str(packages_dir(root) or "-")
    print(json.dumps(info, indent=2, ensure_ascii=False))
    return 0


def cmd_open(pm, args) -> int:
    pkg = pm.get_package(args.package)
    if not pkg:
        print(f"[!] Package not found: {args.package}")
        return 1
    url = (pkg.get("homepage") or "").strip()
    if not url or url == "-":
        print("[!] Package has no homepage")
        return 1
    code, method = open_url(url)
    if code == 0:
        print(f"[✓] Opened via {method}")
    else:
        print(f"[!] Could not open URL (no opener found). URL: {url}")
    return code


def cmd_version(root: Path, UpdateChecker) -> int:
    print(f"{APP_NAME} v{APP_VERSION}")
    try:
        has_update, latest = UpdateChecker.check_update()
        if has_update and latest:
            print(f"Update available: v{latest}")
        else:
            print("Up to date")
    except Exception:
        print("(update check unavailable)")
    print(f"Root: {root}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog=APP_NAME)
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("list", help="List packages")
    sp.add_argument("query", nargs="?", help="Optional search query")
    sp.add_argument("--installed", action="store_true", help="Show only installed")
    sp.add_argument("--updates", action="store_true", help="Show only packages with updates")
    sp.add_argument("--json", action="store_true", help="Output JSON")

    sp = sub.add_parser("show", help="Show package details")
    sp.add_argument("package")

    sp = sub.add_parser("search", help="Search packages")
    sp.add_argument("query")
    sp.add_argument("--json", action="store_true")

    sp = sub.add_parser("install", help="Build & install a package")
    sp.add_argument("package")

    sp = sub.add_parser("uninstall", help="Uninstall a package")
    sp.add_argument("package")

    sp = sub.add_parser("update", help="Refresh remote index cache")

    sp = sub.add_parser("upgrade", help="Install/upgrade packages")
    sp.add_argument("package", nargs="?")

    sp = sub.add_parser("open", help="Open package homepage")
    sp.add_argument("package")

    sub.add_parser("doctor", help="Print environment diagnostics (JSON)")
    sub.add_parser("version", help="Show app version and update status")

    return p


def main(argv: Optional[List[str]] = None) -> int:
    root = find_root()
    PackageManager, UpdateChecker = _import_package_manager(root)
    pm = PackageManager(packages_dir(root))

    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.cmd:
        # Default: open the TUI
        try:
            from .tui import TermuxAppStore

            TermuxAppStore(root=root).run()
            return 0
        except Exception as e:
            print(f"[!] Failed to start TUI: {e}")
            print(f"Use `{APP_NAME} -h` for CLI help.")
            return 1

    if args.cmd == "list":
        return cmd_list(pm, args)
    if args.cmd == "search":
        return cmd_list(pm, argparse.Namespace(
            query=args.query,
            installed=False,
            updates=False,
            json=args.json,
        ))
    if args.cmd == "show":
        return cmd_show(pm, args)
    if args.cmd == "install":
        return cmd_install(root, pm, args)
    if args.cmd == "uninstall":
        return cmd_uninstall(pm, args)
    if args.cmd == "update":
        return cmd_update(pm, args)
    if args.cmd == "upgrade":
        return cmd_upgrade(root, pm, args)
    if args.cmd == "open":
        return cmd_open(pm, args)
    if args.cmd == "doctor":
        return cmd_doctor(root)
    if args.cmd == "version":
        return cmd_version(root, UpdateChecker)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
