#!/usr/bin/env python3
# Termux App Store -- Smart Doctor
# github.com/djunekz/termux-app-store

import os, sys, json, shutil, platform, subprocess, textwrap, re, stat
import urllib.request, urllib.error
from pathlib import Path

R    = "\033[0m";  B    = "\033[1m";  DIM  = "\033[2m";  IT   = "\033[3m"
BRED = "\033[91m"; BGRN = "\033[92m"; BYLW = "\033[93m"
BCYN = "\033[96m"; BWHT = "\033[97m"
BG_BBLK = "\033[100m"; BG_BBLU = "\033[104m"

_PFX         = os.environ.get("PREFIX", "/data/data/com.termux/files/usr")
INSTALL_DIR  = os.path.join(_PFX, "lib/.tas")
SENTINEL     = os.path.join(INSTALL_DIR, ".installed")
BIN_TAS      = os.path.join(_PFX, "bin/termux-app-store")
BIN_TASCTL   = os.path.join(_PFX, "bin/tasctl")
SOURCES_DIR  = os.path.join(_PFX, "etc/apt/sources.list.d")
SOURCES_FILE = os.path.join(SOURCES_DIR, "tas.list")
MAIN_SOURCES = os.path.join(_PFX, "etc/apt/sources.list")
APT_LISTS    = os.path.join(_PFX, "var/lib/apt/lists")
REPO_URL     = "https://djunekz.github.io/termux-app-store"
ARCH_OK      = {"aarch64", "armv7l", "arm", "x86_64", "i686"}
MIN_PYTHON   = (3, 9)
MIN_TEXTUAL  = (8, 0, 0)
VERSION      = "2.0.0"

def TW(): return shutil.get_terminal_size((72, 24)).columns
def W():  return min(TW(), 76)

def _strip(s):
    out, i = "", 0
    while i < len(s):
        if s[i] == "\033":
            while i < len(s) and s[i] != "m": i += 1
        else:
            out += s[i]
        i += 1
    return out

def vlen(s): return len(_strip(s))
def vcenter(t, w=None):
    w = w or W()
    return " " * max(0, (w - vlen(t)) // 2) + t

def blank():  print()
def rule(c="─", col=DIM, w=None): print(f"{col}{c*(w or W())}{R}")
def thick_rule(col=BCYN, w=None): print(f"{col}{'━'*(w or W())}{R}")

def header_bar(title, w=None):
    w = w or W()
    pad = max(0, w - len(f"  {title}  "))
    print(f"{BCYN}{'▄'*w}{R}")
    print(f"{BG_BBLU}{BWHT}{B}  {title}  {R}{BG_BBLU}{' '*pad}{R}")
    print(f"{BCYN}{'▀'*w}{R}")

def section(title):
    blank()
    print(f"  {BCYN}{B}>{R} {B}{BWHT}{title}{R}")
    print(f"  {DIM}{'─'*(W()-2)}{R}")

def code(cmd, indent=4): print(f"{' '*indent}{BYLW}${R} {BCYN}{cmd}{R}")

def callout(label, text, style="note"):
    S = {"note":(BYLW,"CATATAN"), "tip":(BGRN,"TIP"),
         "warning":(BRED,"WARNING"), "pass":(BGRN,"PASS"), "fail":(BRED,"FAIL")}
    col, lbl0 = S.get(style, S["note"])
    lbl = label or lbl0
    w   = W() - 4
    print(f"  {col}╭─[ {B}{lbl}{R}{col} ]{'─'*max(0,w-len(lbl)-5)}╮{R}")
    for ln in textwrap.wrap(text, w-4) or [""]:
        print(f"  {col}│{R}  {ln}{' '*max(0,w-4-len(ln))}  {col}│{R}")
    print(f"  {col}╰{'─'*w}╯{R}")

_LOGO = """\
 ████████╗ █████╗ ███████╗
    ██╔══╝██╔══██╗██╔════╝
    ██║   ███████║███████╗
    ██║   ██╔══██║╚════██║
    ██║   ██║  ██║███████║
    ╚═╝   ╚═╝  ╚═╝╚══════╝"""

def banner():
    w = W()
    thick_rule(BCYN, w)
    blank()
    for ln in _LOGO.splitlines():
        print(vcenter(f"{BCYN}{B}{ln}{R}", w))
    blank()
    print(vcenter(f"{BWHT}{B}Termux App Store{R}  {DIM}--  Smart Doctor{R}", w))
    print(vcenter(f"{DIM}Diagnoses & fixes environment, build.sh, and tool issues{R}", w))
    blank()
    thick_rule(BCYN, w)
    blank()

PASS, WARN, FAIL, INFO, SKIP = "PASS","WARN","FAIL","INFO","SKIP"

class Check:
    def __init__(self, name, status, detail="",
                 fix_cmd=None, fix_hint=None, fix_fn=None, category=""):
        self.name     = name
        self.status   = status
        self.detail   = detail
        self.fix_cmd  = fix_cmd
        self.fix_hint = fix_hint
        self.fix_fn   = fix_fn
        self.category = category

    def print_line(self):
        badge = {PASS: f"{BGRN}{B}  OK  {R}", WARN: f"{BYLW}{B}  !!  {R}",
                 FAIL: f"{BRED}{B}  XX  {R}", INFO: f"{BCYN}{B}  --  {R}",
                 SKIP: f"{DIM}  --  {R}"}.get(self.status, f"{DIM}  ??  {R}")
        nw = 32
        print(f"  {badge}  {B}{self.name:<{nw}}{R}  {DIM}{self.detail}{R}")
        if self.fix_hint and self.status in (FAIL, WARN):
            for ln in textwrap.wrap(self.fix_hint, W()-14) or []:
                print(f"              {DIM}{IT}{ln}{R}")

    def to_dict(self):
        return {"name":self.name, "status":self.status, "detail":self.detail,
                "fix_cmd":self.fix_cmd, "fix_hint":self.fix_hint,
                "category":self.category}

def _sh(cmd, timeout=6):
    try:
r = subprocess.run(cmd, shell=False, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.returncode
    except Exception:
        return "", 1

def _which(p): return shutil.which(p) is not None

def chk_termux():
    inside = "com.termux" in _PFX or Path("/data/data/com.termux").exists()
    if inside:
        return Check("Termux environment", PASS, f"PREFIX={_PFX}", category="System")
    return Check("Termux environment", WARN,
                 f"non-Termux (PREFIX={_PFX})",
                 fix_hint="Run inside Termux on Android for full functionality.",
                 category="System")

def chk_arch():
    arch = platform.machine()
    if arch in ARCH_OK:
        return Check("CPU architecture", PASS, arch, category="System")
    return Check("CPU architecture", WARN,
                 f"{arch} — untested (supported: {', '.join(sorted(ARCH_OK))})",
                 category="System")

def chk_storage():
    try:
        st   = os.statvfs(_PFX)
        free = st.f_bavail * st.f_frsize // (1024*1024)
        tot  = st.f_blocks * st.f_frsize // (1024*1024)
        det  = f"{free} MB free / {tot} MB total"
        if free < 100:
            return Check("Storage space", WARN, det,
                         fix_hint="Low storage — builds may fail.", category="System")
        return Check("Storage space", PASS, det, category="System")
    except Exception:
        return Check("Storage space", INFO, "could not check", category="System")

def chk_python():
    v  = sys.version_info
    vs = f"{v.major}.{v.minor}.{v.micro}"
    if (v.major, v.minor) >= MIN_PYTHON:
        return Check("Python version", PASS, f"Python {vs}", category="Python")
    return Check("Python version", FAIL,
                 f"Python {vs} (need >= {MIN_PYTHON[0]}.{MIN_PYTHON[1]})",
                 fix_cmd="pkg install python",
                 fix_hint="pkg install python",
                 category="Python")

def chk_pip():
    for cmd in ["pip --version 2>/dev/null",
                "python3 -m pip --version 2>/dev/null"]:
        out, rc = _sh(cmd)
        if rc == 0 and out:
            ver = out.split()[1] if len(out.split()) > 1 else "?"
            return Check("pip", PASS, f"pip {ver}", category="Python")
    return Check("pip", FAIL, "not found",
                 fix_cmd="pkg install python",
                 fix_hint="pkg install python  (pip is included)",
                 category="Python")

def chk_textual():
    try:
        import importlib.metadata
        ver_str = importlib.metadata.version("textual")
        parts   = [int(x) for x in re.findall(r"\d+", ver_str)[:3]]
        while len(parts) < 3: parts.append(0)
        if tuple(parts) >= MIN_TEXTUAL:
            return Check("textual", PASS,
                         f"textual {ver_str}", category="Python")
        return Check("textual", WARN,
                     f"textual {ver_str} (need >= {'.'.join(map(str,MIN_TEXTUAL))})",
                     fix_cmd="pip install --upgrade textual --break-system-packages",
                     fix_hint="pip install --upgrade textual --break-system-packages",
                     category="Python")
    except Exception:
        pass
    out, rc = _sh("python3 -c 'import textual; print(textual.__version__)' 2>/dev/null")
    if rc == 0 and out:
        return Check("textual", PASS, f"textual {out}", category="Python")
    return Check("textual", FAIL, "not installed",
                 fix_cmd="pip install textual --break-system-packages",
                 fix_hint="pip install textual --break-system-packages",
                 category="Python")

def chk_python_importpath():
    out, rc = _sh(
        "python3 -c 'import sys; sp=[p for p in sys.path if \"site-packages\" in p];"
        " print(sp[0] if sp else \"\")' 2>/dev/null"
    )
    if rc != 0 or not out:
        return Check("Python site-packages", WARN,
                     "site-packages not in sys.path",
                     fix_hint="pkg reinstall python",
                     category="Python")
    sp = Path(out)
    if not sp.exists():
        return Check("Python site-packages", WARN,
                     f"path does not exist: {out}",
                     fix_hint="pkg reinstall python",
                     category="Python")
    return Check("Python site-packages", PASS, out, category="Python")

def chk_curl():
    if not _which("curl"):
        return Check("curl", FAIL, "not found",
                     fix_cmd="pkg install curl", fix_hint="pkg install curl",
                     category="Tools")
    out, _ = _sh("curl --version 2>/dev/null | head -1")
    return Check("curl", PASS, " ".join(out.split()[:2]) if out else "available",
                 category="Tools")

def chk_git():
    if not _which("git"):
        return Check("git", WARN, "not found (needed for contributing)",
                     fix_cmd="pkg install git", fix_hint="pkg install git",
                     category="Tools")
    out, _ = _sh("git --version 2>/dev/null")
    return Check("git", PASS, out or "available", category="Tools")

def chk_dpkg():
    has_d  = _which("dpkg")
    has_dd = _which("dpkg-deb")
    if has_d and has_dd:
        out, _ = _sh("dpkg --version 2>/dev/null | head -1")
        return Check("dpkg / dpkg-deb", PASS, out or "available", category="Tools")
    missing = [x for x, ok in [("dpkg",has_d),("dpkg-deb",has_dd)] if not ok]
    return Check("dpkg / dpkg-deb", WARN,
                 f"missing: {', '.join(missing)} (needed for .deb builds)",
                 fix_cmd="pkg install dpkg", fix_hint="pkg install dpkg",
                 category="Tools")

def chk_pkg():
    if _which("pkg"):
        return Check("pkg (Termux)", PASS, "available", category="Tools")
    return Check("pkg (Termux)", FAIL,
                 "not found — must run inside Termux", category="Tools")

def chk_sha256sum():
    if _which("sha256sum"):
        return Check("sha256sum", PASS, "available", category="Tools")
    if _which("shasum"):
        return Check("sha256sum", WARN,
                     "not found but shasum available — build scripts may break",
                     fix_hint="pkg install coreutils", category="Tools")
    return Check("sha256sum", WARN, "not found",
                 fix_cmd="pkg install coreutils",
                 fix_hint="pkg install coreutils", category="Tools")

def chk_tas_binary():
    p = Path(BIN_TAS)
    if not p.exists():
        return Check("termux-app-store binary", FAIL, "not installed",
                     fix_cmd="pip install termux-app-store --break-system-packages",
                     fix_hint="pip install termux-app-store  OR  bash install.sh",
                     category="TAS")
    if not (p.stat().st_mode & 0o111):
        return Check("termux-app-store binary", WARN,
                     f"{p} is not executable",
                     fix_cmd=f"chmod +x {BIN_TAS}",
                     fix_hint=f"chmod +x {BIN_TAS}", category="TAS")
    return Check("termux-app-store binary", PASS, str(p), category="TAS")

def chk_tas_wrapper():
    p = Path(BIN_TAS)
    if not p.exists():
        return Check("TAS wrapper integrity", SKIP, "binary not present", category="TAS")
    try:
        content = p.read_text(errors="replace")
    except Exception as e:
        return Check("TAS wrapper integrity", WARN, f"cannot read: {e}", category="TAS")

    issues = []
    if "TERMUX_APP_STORE_HOME" not in content:
        issues.append("TERMUX_APP_STORE_HOME missing")

    m = re.search(r'TERMUX_APP_STORE_HOME="?([^"\n]+)"?', content)
    if m:
        home = Path(m.group(1).strip())
        if not home.exists():
            issues.append(f"TERMUX_APP_STORE_HOME={home} does not exist")
        elif not (home / "termux_app_store" / "main.py").exists():
            issues.append(f"main.py not found in {home}")

    if issues:
        return Check("TAS wrapper integrity", WARN,
                     "; ".join(issues),
                     fix_cmd="bash install.sh 2>/dev/null || true",
                     fix_hint="bash install.sh  to regenerate wrapper",
                     category="TAS")
    return Check("TAS wrapper integrity", PASS,
                 "TERMUX_APP_STORE_HOME set and valid", category="TAS")

def chk_tas_version():
    s = Path(SENTINEL)
    if s.exists():
        try:
            for ln in s.read_text().splitlines():
                if ln.startswith("version="):
                    return Check("TAS version", PASS,
                                 f"v{ln.split('=',1)[1]}", category="TAS")
        except Exception:
            pass
    try:
        import importlib.metadata
        ver = importlib.metadata.version("termux-app-store")
        return Check("TAS version", PASS, f"v{ver}", category="TAS")
    except Exception:
        pass
    out, rc = _sh(f"{BIN_TAS} --version 2>/dev/null || {BIN_TAS} version 2>/dev/null")
    if rc == 0 and out:
        return Check("TAS version", PASS, out.strip(), category="TAS")
    return Check("TAS version", INFO, "could not determine", category="TAS")

def chk_tas_can_run():
    install_dir = Path(INSTALL_DIR)
    main_py     = install_dir / "termux_app_store" / "main.py"

    if not main_py.exists():
        out, rc = _sh("python3 -c 'import termux_app_store; print(\"ok\")' 2>/dev/null")
        if rc == 0 and "ok" in out:
            return Check("TAS importable", PASS, "pip-installed OK", category="TAS")
        return Check("TAS importable", FAIL,
                     "termux_app_store module not found",
                     fix_cmd="pip install termux-app-store --break-system-packages",
                     fix_hint="pip install termux-app-store --break-system-packages",
                     category="TAS")

    out, rc = _sh(
        f"python3 -c 'import sys; sys.path.insert(0,\"{install_dir}\"); "
        f"from termux_app_store import termux_app_store; print(\"ok\")' 2>/dev/null"
    )
    if rc == 0 and "ok" in out:
        return Check("TAS importable", PASS, "source module OK", category="TAS")

    out2, _ = _sh(
        f"python3 -c 'import sys; sys.path.insert(0,\"{install_dir}\"); "
        f"from termux_app_store import termux_app_store' 2>&1"
    )
    detail = (out2.strip().split("\n")[-1])[:60] if out2 else "import failed"
    fix    = None
    if "textual" in out2.lower():
        fix = "pip install textual --break-system-packages"
    elif "No module named" in out2:
        fix = "pip install termux-app-store --break-system-packages"

    return Check("TAS importable", FAIL, detail,
                 fix_cmd=fix,
                 fix_hint=fix or "Check Python path and re-run install.sh",
                 category="TAS")

def chk_tasctl():
    for candidate in [BIN_TASCTL,
                      str(Path(INSTALL_DIR) / "tasctl"),
                      "./tasctl"]:
        if Path(candidate).exists():
            return Check("tasctl", PASS, str(Path(candidate).resolve()), category="TAS")
    out, rc = _sh("which tasctl 2>/dev/null")
    if rc == 0 and out:
        return Check("tasctl", PASS, out, category="TAS")
    return Check("tasctl", WARN, "not found",
                 fix_cmd="bash install.sh 2>/dev/null || true",
                 fix_hint="bash install.sh  (from inside the repo directory)",
                 category="TAS")

def _fix_repo_file():
    entry = f"deb [trusted=yes] {REPO_URL} termux main\n"
    Path(SOURCES_DIR).mkdir(parents=True, exist_ok=True)
    Path(SOURCES_FILE).write_text(
        "# Termux App Store\n"
        "# https://github.com/djunekz/termux-app-store\n"
        + entry
    )
    print(f"  {BGRN}OK{R}  Written: {SOURCES_FILE}")
    return True

def chk_repo_file():
    p = Path(SOURCES_FILE)
    if p.exists():
        try:
            txt = p.read_text()
        except Exception as e:
            return Check("apt repo (tas.list)", WARN, f"read error: {e}",
                         category="Repo")
        if REPO_URL in txt:
            active = [ln for ln in txt.splitlines()
                      if ln.strip() and not ln.strip().startswith("#")]
            if len(active) > 1:
                return Check("apt repo (tas.list)", WARN,
                             f"{len(active)} entries (duplicate risk)",
                             fix_fn=_fix_repo_file,
                             fix_hint="python3 install-repo.py  to clean up",
                             category="Repo")
            return Check("apt repo (tas.list)", PASS, str(p), category="Repo")
        return Check("apt repo (tas.list)", WARN,
                     f"{p} exists but TAS URL not found",
                     fix_fn=_fix_repo_file,
                     fix_hint="python3 install-repo.py",
                     category="Repo")
    if Path(MAIN_SOURCES).exists():
        try:
            if REPO_URL in Path(MAIN_SOURCES).read_text():
                return Check("apt repo (tas.list)", WARN,
                             "URL found in main sources.list (wrong location)",
                             fix_fn=_fix_repo_file,
                             fix_hint="python3 install-repo.py",
                             category="Repo")
        except Exception:
            pass
    return Check("apt repo (tas.list)", FAIL, "not configured",
                 fix_fn=_fix_repo_file,
                 fix_hint="python3 install-repo.py",
                 category="Repo")

def chk_apt_lists():
    if not Path(SOURCES_FILE).exists():
        return Check("apt lists (freshness)", SKIP,
                     "repo not configured yet", category="Repo")
    lists_dir = Path(APT_LISTS)
    if not lists_dir.exists():
        return Check("apt lists (freshness)", WARN,
                     "apt lists directory missing",
                     fix_cmd="pkg update",
                     fix_hint="pkg update", category="Repo")
    tas_lists = (list(lists_dir.glob("*djunekz*")) +
                 list(lists_dir.glob("*termux-app-store*")))
    if not tas_lists:
        return Check("apt lists (freshness)", WARN,
                     "apt lists not updated since repo install",
                     fix_cmd="pkg update",
                     fix_hint="pkg update  (fetch package list from TAS repo)",
                     category="Repo")
    try:
        import time
        mtime    = max(f.stat().st_mtime for f in tas_lists)
        age_days = (time.time() - mtime) / 86400
        if age_days > 7:
            return Check("apt lists (freshness)", WARN,
                         f"lists are {age_days:.0f} days old (> 7)",
                         fix_cmd="pkg update",
                         fix_hint="pkg update  (refresh TAS package list)",
                         category="Repo")
        return Check("apt lists (freshness)", PASS,
                     f"up to date ({age_days:.0f} days old)", category="Repo")
    except Exception:
        return Check("apt lists (freshness)", PASS, "lists exist", category="Repo")

def _find_root():
    for p in [Path("."), Path(__file__).parent, Path(INSTALL_DIR)]:
        if (p / "packages").is_dir() and (p / "build-package.sh").exists():
            return p
    return None

def chk_packages_dir():
    root = _find_root()
    for base in ([root / "packages"] if root else []) + \
                [Path("packages"), Path(INSTALL_DIR) / "packages"]:
        if base and base.is_dir():
            count = sum(1 for x in base.iterdir()
                        if x.is_dir() and (x / "build.sh").exists())
            return Check("packages/ directory", PASS,
                         f"{base}  ({count} packages)", category="Project")
    return Check("packages/ directory", WARN,
                 "not found — run from inside the repo",
                 fix_hint="cd ~/termux-app-store  then re-run doctor",
                 category="Project")

def chk_build_package_sh():
    root = _find_root()
    candidates = ([root / "build-package.sh"] if root else []) + \
                 [Path("build-package.sh"),
                  Path(INSTALL_DIR) / "build-package.sh"]
    for p in candidates:
        if p and p.exists():
            if p.stat().st_mode & 0o111:
                return Check("build-package.sh", PASS, str(p), category="Project")
            return Check("build-package.sh", WARN,
                         f"{p} not executable",
                         fix_cmd=f"chmod +x {p}",
                         fix_hint=f"chmod +x {p}", category="Project")
    return Check("build-package.sh", WARN,
                 "not found — run from inside the repo",
                 fix_hint="cd ~/termux-app-store", category="Project")

def chk_termux_build():
    root = _find_root()
    candidates = ([root / "termux-build"] if root else []) + \
                 [Path("termux-build"), Path(INSTALL_DIR) / "termux-build"]
    for p in candidates:
        if p and p.exists():
            return Check("termux-build tool", PASS, str(p), category="Project")
    return Check("termux-build tool", WARN,
                 "not found — run from inside the repo",
                 fix_hint="cd ~/termux-app-store", category="Project")

def chk_build_sh_scan():
    root = _find_root()
    pkgs_dir = None
    for base in ([root / "packages"] if root else []) + \
                [Path("packages"), Path(INSTALL_DIR) / "packages"]:
        if base and base.is_dir():
            pkgs_dir = base
            break
    if not pkgs_dir:
        return Check("build.sh scan", SKIP,
                     "packages/ not found", category="Project")

    broken, total = [], 0
    for pkg_dir in sorted(pkgs_dir.iterdir()):
        if not pkg_dir.is_dir(): continue
        bsh = pkg_dir / "build.sh"
        total += 1
        if not bsh.exists():
            broken.append(f"{pkg_dir.name}:missing")
            continue
        if not bsh.read_text(errors="replace").strip():
            broken.append(f"{pkg_dir.name}:empty")
            continue
        _, rc = _sh(f"bash -n {bsh} 2>/dev/null")
        if rc != 0:
            broken.append(f"{pkg_dir.name}:syntax")

    if broken:
        return Check("build.sh scan", WARN,
                     f"{len(broken)}/{total} broken: "
                     + ", ".join(broken[:4]) + ("..." if len(broken) > 4 else ""),
                     fix_hint="python3 build-tester.py --all  for full details",
                     category="Project")
    return Check("build.sh scan", PASS,
                 f"all {total} packages OK", category="Project")

def chk_last_build():
    root = _find_root()
    if not root:
        return Check("recent build status", SKIP,
                     "project root not found", category="Build")
    build_dir = root / "build"
    if not build_dir.exists():
        return Check("recent build status", INFO,
                     "no builds yet", category="Build")

    incomplete = []
    output_dir = root / "output"
    for pkg_dir in build_dir.iterdir():
        if not pkg_dir.is_dir(): continue
        debs = list(output_dir.glob(f"{pkg_dir.name}_*.deb")) \
               if output_dir.exists() else []
        if not debs:
            incomplete.append(pkg_dir.name)

    if incomplete:
        def _clean():
            for pkg in incomplete:
                d = root / "build" / pkg
                if d.exists():
                    shutil.rmtree(d)
                    print(f"  {BGRN}OK{R}  Removed {d}")
            return True
        return Check("recent build status", WARN,
                     f"incomplete build dirs: {', '.join(incomplete[:3])}",
                     fix_fn=_clean,
                     fix_hint=f"rm -rf {root}/build/  to clean up",
                     category="Build")
    return Check("recent build status", PASS,
                 "no incomplete builds", category="Build")

def chk_output_dir():
    root = _find_root()
    if not root:
        return Check("output/ (.deb files)", SKIP,
                     "project root not found", category="Build")
    output = root / "output"
    if not output.exists():
        return Check("output/ (.deb files)", INFO, "no builds yet", category="Build")
    debs    = list(output.glob("*.deb"))
    if not debs:
        return Check("output/ (.deb files)", INFO, "no .deb files", category="Build")
    corrupt = [d for d in debs if d.stat().st_size == 0]
    if corrupt:
        names = ", ".join(d.name for d in corrupt[:3])
        return Check("output/ (.deb files)", WARN,
                     f"corrupt (0-byte): {names}",
                     fix_cmd=f"rm -f {output}/*.deb",
                     fix_hint=f"rm {output}/*.deb  then rebuild",
                     category="Build")
    return Check("output/ (.deb files)", PASS,
                 f"{len(debs)} .deb file(s)", category="Build")

def chk_installed_tas_pkgs():
    if not _which("dpkg"):
        return Check("TAS packages (installed)", SKIP,
                     "dpkg not available", category="Build")
    out, rc = _sh("dpkg --get-selections 2>/dev/null | grep -i 'install$'")
    if rc != 0:
        return Check("TAS packages (installed)", INFO,
                     "could not query dpkg", category="Build")
    root  = _find_root()
    known = set()
    if root and (root / "packages").is_dir():
        known = {d.name for d in (root/"packages").iterdir()
                 if d.is_dir() and (d/"build.sh").exists()}
    installed = [ln.split()[0] for ln in out.splitlines()
                 if ln.split() and ln.split()[0] in known]
    if installed:
        return Check("TAS packages (installed)", PASS,
                     f"{len(installed)}: {', '.join(installed[:5])}",
                     category="Build")
    return Check("TAS packages (installed)", INFO,
                 "none installed yet", category="Build")

def chk_network():
    try:
        req = urllib.request.Request(
            REPO_URL,
            headers={"User-Agent": f"tas-doctor/{VERSION}"},
            method="HEAD"
        )
        with urllib.request.urlopen(req, timeout=7) as r:
            code = r.getcode()
        if code == 200:
            return Check("Repo reachable", PASS, REPO_URL, category="Network")
        return Check("Repo reachable", WARN, f"HTTP {code}", category="Network")
    except urllib.error.URLError as e:
        return Check("Repo reachable", WARN,
                     f"unreachable: {e.reason}",
                     fix_hint="Check internet connection", category="Network")
    except Exception as e:
        return Check("Repo reachable", WARN, str(e)[:50], category="Network")

def chk_github():
    try:
        req = urllib.request.Request(
            "https://api.github.com/repos/djunekz/termux-app-store",
            headers={"User-Agent": f"tas-doctor/{VERSION}",
                     "Accept": "application/vnd.github+json"}
        )
        with urllib.request.urlopen(req, timeout=7) as r:
            data = json.loads(r.read().decode())
        stars = data.get("stargazers_count", "?")
        return Check("GitHub API", PASS,
                     f"reachable (stars: {stars})", category="Network")
    except Exception as e:
        return Check("GitHub API", WARN,
                     str(e)[:50],
                     fix_hint="Check internet connection", category="Network")


REQUIRED_FIELDS = [
    "TERMUX_PKG_HOMEPAGE", "TERMUX_PKG_DESCRIPTION", "TERMUX_PKG_LICENSE",
    "TERMUX_PKG_MAINTAINER", "TERMUX_PKG_VERSION",
    "TERMUX_PKG_SRCURL", "TERMUX_PKG_SHA256",
]

def _parse_build_sh(path: Path) -> dict:
    vals = {}
    for raw in path.read_text(errors="replace").splitlines():
        ln = raw.strip()
        if not ln or ln.startswith("#"): continue
        m = re.match(r'^(TERMUX_PKG_\w+)=(.*)$', ln)
        if not m: continue
        k, v = m.group(1), m.group(2).strip()
        if (v.startswith('"') and v.endswith('"')) or \
           (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        vals[k] = v
    ver = vals.get("TERMUX_PKG_VERSION","")
    if ver:
        for k in vals:
            vals[k] = vals[k].replace("${TERMUX_PKG_VERSION}", ver)
    return vals

def _find_build_sh(pkg_name: str):
    root = _find_root()
    for base in ([root / "packages"] if root else []) + \
                [Path("packages"), Path(INSTALL_DIR) / "packages"]:
        if base and (base / pkg_name / "build.sh").exists():
            return base / pkg_name / "build.sh"
    return None

def diagnose_build_sh(pkg_name: str) -> list:
    results = []

    build_sh = _find_build_sh(pkg_name)
    if not build_sh:
        results.append(Check(
            "packages/"+pkg_name+"/build.sh", FAIL,
            "file not found",
            fix_hint=f"python3 pkg-scaffold.py {pkg_name}  to create it",
            category="build.sh"
        ))
        return results
    results.append(Check("build.sh found", PASS, str(build_sh), category="build.sh"))

    content = build_sh.read_text(errors="replace")
    if not content.strip():
        results.append(Check("build.sh not empty", FAIL,
                             "file is empty",
                             fix_hint=f"python3 pkg-scaffold.py {pkg_name}",
                             category="build.sh"))
        return results
    lines = content.splitlines()
    results.append(Check("build.sh not empty", PASS,
                         f"{len(lines)} lines", category="build.sh"))

    out, rc = _sh(f"bash -n '{build_sh}' 2>&1")
    if rc != 0:
        m       = re.search(r'line (\d+)', out)
        lineno  = f" (line {m.group(1)})" if m else ""
        snippet = (out.strip().split("\n")[-1])[:55] if out else "syntax error"
        results.append(Check("bash syntax", FAIL,
                             f"error{lineno}: {snippet}",
                             fix_hint=f"nano {build_sh}  — look for unmatched quotes/braces/EOF",
                             category="build.sh"))
        return results
    results.append(Check("bash syntax", PASS, "OK", category="build.sh"))

    try:
        vals = _parse_build_sh(build_sh)
    except Exception as e:
        results.append(Check("build.sh parse", FAIL, str(e), category="build.sh"))
        return results

    for field in REQUIRED_FIELDS:
        val = vals.get(field, "")
        if not val:
            hint = f"Add  {field}=...  to build.sh"
            if field == "TERMUX_PKG_SHA256":
                hint = ("python3 build-tester.py " + pkg_name +
                        " --deep  to compute SHA256 automatically")
            elif field == "TERMUX_PKG_SRCURL":
                hint = "URL to .tar.gz or .zip of the upstream source"
            results.append(Check(field, FAIL, "missing or empty",
                                 fix_hint=hint, category="build.sh"))
        else:
            results.append(Check(field, PASS, val[:52], category="build.sh"))

    ver = vals.get("TERMUX_PKG_VERSION","")
    if ver and not re.match(r"^\d", ver):
        results.append(Check("VERSION format", FAIL,
                             f"'{ver}' does not start with digit",
                             fix_hint=f"Change to: TERMUX_PKG_VERSION={ver.lstrip('v')}",
                             category="build.sh"))
    elif ver:
        results.append(Check("VERSION format", PASS, ver, category="build.sh"))

    sha = vals.get("TERMUX_PKG_SHA256","")
    if sha and sha.upper() != "SKIP" and not re.match(r"^[0-9a-fA-F]{64}$", sha):
        results.append(Check("SHA256 format", FAIL,
                             f"invalid ({len(sha)} chars, need 64 hex)",
                             fix_hint=("python3 build-tester.py " + pkg_name +
                                       " --deep  to compute the correct hash"),
                             category="build.sh"))
    elif sha and sha.upper() == "SKIP":
        results.append(Check("SHA256 format", WARN,
                             "SHA256=SKIP — verification disabled",
                             fix_hint=("python3 build-tester.py " + pkg_name +
                                       " --deep  to generate real hash"),
                             category="build.sh"))

    forbidden = [
        (r"\bsudo\b",             "sudo not allowed in Termux"),
        (r"\bapt-get\b",          "use pkg instead of apt-get"),
        (r"\bapt install\b",      "use pkg install instead of apt install"),
        (r"TERMUX_PKG_VERSION=v\d","VERSION starts with 'v' (remove the v)"),
        (r"\bchown\b",            "chown not available in Termux userspace"),
        (r"rm -rf /[^/\n]",       "dangerous rm -rf detected"),
    ]
    in_heredoc, end_token = False, ""
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if not in_heredoc:
            m = re.search(r"<<\s*['\"]?(\w+)['\"]?", ln)
            if m:
                in_heredoc = True
                end_token  = m.group(1)
                continue
        else:
            if stripped == end_token:
                in_heredoc, end_token = False, ""
            continue
        if stripped.startswith("#"): continue
        for pattern, msg in forbidden:
            if re.search(pattern, ln):
                results.append(Check(f"Lint: {msg[:32]}", FAIL,
                                     f"line {i}: {ln.strip()[:42]}",
                                     fix_hint=f"Edit line {i} of {build_sh.name}",
                                     category="build.sh"))
                break

    hc_re = re.compile(r'/data/data/com\.termux/files/usr(?!/bin/env)')
    in_heredoc, end_token = False, ""
    for i, ln in enumerate(lines, 1):
        stripped = ln.strip()
        if not in_heredoc:
            m = re.search(r"<<\s*['\"]?(\w+)['\"]?", ln)
            if m:
                in_heredoc = True
                end_token  = m.group(1)
                continue
        else:
            if stripped == end_token:
                in_heredoc, end_token = False, ""
            continue
        if stripped.startswith("#"): continue
        if hc_re.search(ln):
            results.append(Check("Lint: hardcoded prefix", WARN,
                                 f"line {i}: use $TERMUX_PREFIX instead",
                                 fix_hint=f"Replace hardcoded path with $TERMUX_PREFIX (line {i})",
                                 category="build.sh"))
            break

    has_fn  = "termux_step_make_install()" in content
    deps    = vals.get("TERMUX_PKG_DEPENDS","").lower()
    scripted = any(k in deps for k in ["python","nodejs","ruby","perl","php","lua"])
    if not has_fn and scripted:
        results.append(Check("termux_step_make_install()", WARN,
                             "missing — needed for script-based packages",
                             fix_hint="Add termux_step_make_install() { ... } to build.sh",
                             category="build.sh"))
    elif has_fn:
        results.append(Check("termux_step_make_install()", PASS,
                             "found", category="build.sh"))
    else:
        results.append(Check("termux_step_make_install()", INFO,
                             "not present (using default build flow)",
                             category="build.sh"))

    if has_fn and "TERMUX_PKG_BUILD_IN_SRC" not in content:
        results.append(Check("TERMUX_PKG_BUILD_IN_SRC", WARN,
                             "not set — needed for most script packages",
                             fix_hint="Add: TERMUX_PKG_BUILD_IN_SRC=true",
                             category="build.sh"))
    elif "TERMUX_PKG_BUILD_IN_SRC=true" in content:
        results.append(Check("TERMUX_PKG_BUILD_IN_SRC", PASS,
                             "true", category="build.sh"))

    if _which("pkg"):
        dep_str = vals.get("TERMUX_PKG_DEPENDS","")
        if dep_str:
            for dep in [d.strip().split()[0] for d in dep_str.split(",") if d.strip()]:
                out, rc = _sh(f"pkg info {dep} 2>/dev/null | head -1")
                if rc == 0 and out:
                    results.append(Check(f"dep: {dep}", PASS,
                                         out[:40], category="build.sh"))
                else:
                    results.append(Check(f"dep: {dep}", WARN,
                                         "not found via pkg",
                                         fix_hint=f"Verify: pkg info {dep}",
                                         category="build.sh"))

    src = vals.get("TERMUX_PKG_SRCURL","")
    if src and src.startswith("http") and "${" not in src:
        try:
            req = urllib.request.Request(
                src, headers={"User-Agent": "tas-doctor/2.0"}, method="HEAD"
            )
            with urllib.request.urlopen(req, timeout=8) as r:
                code = r.getcode()
            if code == 200:
                size = r.headers.get("Content-Length","?")
                sz   = f"{int(size)//1024} KB" if str(size).isdigit() else "?"
                results.append(Check("SRCURL reachable", PASS,
                                     f"HTTP 200 ({sz})", category="build.sh"))
            else:
                results.append(Check("SRCURL reachable", WARN,
                                     f"HTTP {code}", category="build.sh"))
        except urllib.error.HTTPError as e:
            lvl = WARN if e.code in (403,405) else FAIL
            results.append(Check("SRCURL reachable", lvl,
                                 f"HTTP {e.code} (may still be valid)",
                                 category="build.sh"))
        except Exception as e:
            results.append(Check("SRCURL reachable", WARN,
                                 str(e)[:50], category="build.sh"))

    return results


def run_fix(check: Check, mode_fix: bool):
    if not mode_fix or check.status not in (FAIL, WARN):
        return
    if not (check.fix_cmd or check.fix_fn or check.fix_hint):
        return

    blank()
    print(f"  {BCYN}{B}FIX{R}  {B}{check.name}{R}")
    rule("─", DIM)

    if check.fix_fn:
        try:
            ok = check.fix_fn()
            print(f"  {BGRN if ok else BYLW}{B}{'OK  Fix applied' if ok else '!!  Fix ran — review result'}{R}")
        except Exception as e:
            print(f"  {BRED}{B}XX{R}  Fix function failed: {e}")
        return

    if check.fix_cmd:
        print(f"  {DIM}Running:{R}  {BCYN}{check.fix_cmd}{R}")
        blank()
# FIX: 使用subprocess替代os.system
rc = # os.system(check.fix_cmd)
        blank()
        rule("─", DIM)
        if rc == 0:
            print(f"  {BGRN}{B}OK{R}  Fix applied")
        else:
            print(f"  {BRED}{B}XX{R}  Fix failed (exit {rc})")
            if check.fix_hint:
                print(f"  {DIM}Try manually:{R}  {BCYN}{check.fix_hint}{R}")
        return

    print(f"  {BYLW}{B}!!{R}  No automatic fix — manual steps:")
    blank()
    for ln in textwrap.wrap(check.fix_hint, W()-8):
        code(ln)
    rule("─", DIM)


SECTIONS = [
    ("System",           [chk_termux, chk_arch, chk_storage]),
    ("Python",           [chk_python, chk_pip, chk_textual, chk_python_importpath]),
    ("Tools",            [chk_curl, chk_git, chk_dpkg, chk_pkg, chk_sha256sum]),
    ("TAS Installation", [chk_tas_binary, chk_tas_wrapper, chk_tas_version,
                          chk_tas_can_run, chk_tasctl]),
    ("Repository",       [chk_repo_file, chk_apt_lists]),
    ("Project",          [chk_packages_dir, chk_build_package_sh,
                          chk_termux_build, chk_build_sh_scan]),
    ("Build",            [chk_last_build, chk_output_dir, chk_installed_tas_pkgs]),
    ("Network",          [chk_network, chk_github]),
]
ALL_FNS = [fn for _, fns in SECTIONS for fn in fns]


def print_summary(checks, mode_fix=False):
    blank()
    header_bar("DIAGNOSIS SUMMARY")
    blank()

    n_pass = sum(1 for c in checks if c.status == PASS)
    n_warn = sum(1 for c in checks if c.status == WARN)
    n_fail = sum(1 for c in checks if c.status == FAIL)
    n_info = sum(1 for c in checks if c.status in (INFO, SKIP))

    w  = W() - 6
    rows = [
        ("Checks passed", str(n_pass), n_fail == 0 and n_warn == 0),
        ("Warnings",      str(n_warn), n_warn == 0),
        ("Failures",      str(n_fail), n_fail == 0),
        ("Info / Skip",   str(n_info), True),
    ]
    lw = max(len(r[0]) for r in rows) + 2
    print(f" {DIM}┌{'─'*(w+2)}┐{R}")
    for label, val, good in rows:
        col = BGRN if good else (BYLW if "Warn" in label else BRED)
        pad = max(0, w - 2 - lw - len(val))
        print(f" {DIM}│{R} {DIM}{label:<{lw}}{R} {col}{B}{val}{R}{' '*pad}  {DIM}│{R}")
    print(f" {DIM}└{'─'*(w+2)}┘{R}")
    blank()

    if n_fail:
        thick_rule(BRED)
        print(vcenter(f"{BRED}{B}FAIL  --  {n_fail} error(s) must be fixed{R}", W()))
        thick_rule(BRED)
    elif n_warn:
        thick_rule(BYLW)
        print(vcenter(f"{BYLW}{B}WARN  --  {n_warn} item(s) to review{R}", W()))
        thick_rule(BYLW)
    else:
        thick_rule(BGRN)
        print(vcenter(f"{BGRN}{B}ALL PASS  --  environment is healthy{R}", W()))
        thick_rule(BGRN)
    blank()

    actions = [c for c in checks if c.status in (FAIL, WARN)
               and (c.fix_cmd or c.fix_hint or c.fix_fn)]
    if actions and not mode_fix:
        section("Action items")
        for c in actions:
            col = BRED if c.status == FAIL else BYLW
            fix = c.fix_cmd or c.fix_hint or ""
            print(f"\n  {col}{B}{c.status}{R}  {B}{c.name}{R}")
            if c.category: print(f"  {DIM}category: {c.category}{R}")
            if fix: code(fix.split("\n")[0])
        blank()
        callout("TIP",
                "Run with --fix to automatically apply fixes where possible.",
                "tip")
        blank()


def print_help():
    blank()
    header_bar("SMART DOCTOR -- HELP")
    blank()
    rows = [
        ("(no args)",       "Full environment diagnosis"),
        ("--fix",           "Diagnose + auto-fix all fixable issues"),
        ("--pkg <name>",    "Deep diagnosis of one package's build.sh"),
        ("--brief",         "One-line-per-check output"),
        ("--json",          "JSON output for CI / scripting"),
        ("--help",          "Show this help"),
    ]
    w  = W() - 6
    lw = max(len(r[0]) for r in rows) + 2
    print(f" {DIM}┌{'─'*(w+2)}┐{R}")
    for cmd, desc in rows:
        pad = max(0, w - 2 - lw - 2 - len(desc))
        print(f" {DIM}│{R} {BCYN}{cmd:<{lw}}{R}  {desc}{' '*pad}   {DIM}│{R}")
    print(f" {DIM}└{'─'*(w+2)}┘{R}")
    blank()
    section("Sections in full diagnosis")
    blank()
    cats = [
        ("System",           "Termux env, CPU arch, free storage"),
        ("Python",           "Python version, pip, textual, site-packages"),
        ("Tools",            "curl, git, dpkg, pkg, sha256sum"),
        ("TAS Installation", "binary, wrapper, version, importable, tasctl"),
        ("Repository",       "apt sources.list.d/tas.list, list freshness"),
        ("Project",          "packages/, build-package.sh, termux-build, build.sh scan"),
        ("Build",            "incomplete builds, output .deb, installed packages"),
        ("Network",          "repo URL, GitHub API"),
    ]
    lw2 = max(len(c[0]) for c in cats) + 2
    for cat, desc in cats:
        print(f"  {BCYN}{cat:<{lw2}}{R}  {DIM}{desc}{R}")
    blank()
    section("--pkg: what it checks")
    blank()
    items = [
        "File exists and is not empty",
        "Bash syntax (bash -n)",
        "All 7 required TERMUX_PKG_* fields",
        "VERSION format (must start with digit)",
        "SHA256 format (64 hex chars or SKIP)",
        "Forbidden patterns (sudo, apt-get, hardcoded paths, etc.)",
        "termux_step_make_install() presence",
        "TERMUX_PKG_BUILD_IN_SRC consistency",
        "Dependency availability via pkg info",
        "SRCURL HTTP reachability",
    ]
    for item in items:
        print(f"  {BCYN}+{R}  {item}")
    blank()
    section("Examples")
    blank()
    code("python3 doctor.py")
    code("python3 doctor.py --fix")
    code("python3 doctor.py --pkg baxter")
    code("python3 doctor.py --pkg mypackage --fix")
    code("python3 doctor.py --brief")
    code("python3 doctor.py --json | python3 -m json.tool")
    blank()


def main():
    args       = sys.argv[1:]
    mode_fix   = "--fix"   in args
    mode_brief = "--brief" in args
    mode_json  = "--json"  in args
    mode_help  = "--help"  in args or "-h" in args
    mode_pkg   = None
    if "--pkg" in args:
        i = args.index("--pkg")
        if i + 1 < len(args):
            mode_pkg = args[i + 1]

    if not mode_json:
        banner()

    if mode_help:
        print_help()
        sys.exit(0)

    if mode_pkg:
        section(f"build.sh diagnosis: {mode_pkg}")
        blank()
        checks = diagnose_build_sh(mode_pkg)
        for c in checks:
            c.print_line()
            run_fix(c, mode_fix)
        blank()
        n_fail = sum(1 for c in checks if c.status == FAIL)
        n_warn = sum(1 for c in checks if c.status == WARN)
        if n_fail:
            callout("FAIL",
                    f"Package '{mode_pkg}' has {n_fail} error(s) that must be fixed "
                    f"before building or submitting a PR.", "fail")
        elif n_warn:
            callout("WARN",
                    f"Package '{mode_pkg}' has {n_warn} warning(s). "
                    f"Review before submitting PR.", "note")
        else:
            callout("PASS",
                    f"build.sh for '{mode_pkg}' looks good.", "pass")
        blank()
        sys.exit(1 if n_fail else 0)

    if mode_brief:
        all_checks = [fn() for fn in ALL_FNS]
        for c in all_checks:
            sym = {PASS:"+", WARN:"!", FAIL:"X", INFO:"-", SKIP:"-"}.get(c.status,"?")
            col = {PASS:BGRN, WARN:BYLW, FAIL:BRED}.get(c.status, DIM)
            print(f"  {col}[{sym}]{R} {c.name}: {DIM}{c.detail}{R}")
        blank()
        sys.exit(1 if any(c.status == FAIL for c in all_checks) else 0)

    if mode_json:
        all_checks = [fn() for fn in ALL_FNS]
        data = {
            "version": VERSION,
            "total":   len(all_checks),
            "passed":  sum(1 for c in all_checks if c.status == PASS),
            "warned":  sum(1 for c in all_checks if c.status == WARN),
            "failed":  sum(1 for c in all_checks if c.status == FAIL),
            "checks":  [c.to_dict() for c in all_checks],
        }
        print(json.dumps(data, indent=2))
        sys.exit(0)

    if mode_fix:
        callout("FIX MODE",
                "Doctor will attempt to auto-fix issues as it finds them. "
                "Items with no automatic fix will show manual instructions.",
                "tip")
        blank()

    all_checks = []
    for sec_name, fns in SECTIONS:
        section(sec_name)
        blank()
        for fn in fns:
            c = fn()
            all_checks.append(c)
            c.print_line()
            run_fix(c, mode_fix)
        blank()

    print_summary(all_checks, mode_fix=mode_fix)
    sys.exit(1 if any(c.status == FAIL for c in all_checks) else 0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        blank()
        rule("─", DIM)
        print(f"  {BYLW}Cancelled.{R}")
        rule("─", DIM)
        blank()
        sys.exit(130)
