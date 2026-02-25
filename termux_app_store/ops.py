from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterable, Optional, Tuple


class CommandError(RuntimeError):
    pass


def run(
    cmd: Iterable[str],
    *,
    cwd: Optional[Path] = None,
    env: Optional[dict] = None,
) -> int:
    """Run a command and stream output."""
    try:
        return subprocess.call(list(cmd), cwd=str(cwd) if cwd else None, env=env)
    except FileNotFoundError as e:
        raise CommandError(str(e)) from e


def ensure_executable(path: Path) -> None:
    try:
        mode = path.stat().st_mode
        path.chmod(mode | 0o111)
    except Exception:
        # Best effort
        pass


def build_install(root: Path, package: str) -> int:
    script = root / "build-package.sh"
    if not script.exists():
        raise CommandError("build-package.sh not found. Install the source edition or clone the repo.")
    ensure_executable(script)
    return run(["bash", str(script), package], cwd=root)


def uninstall(package: str) -> Tuple[int, str]:
    """Uninstall using Termux's pkg wrapper when available."""
    # Prefer pkg (Termux), fallback to dpkg
    if shutil_which("pkg"):
        code = run(["pkg", "uninstall", "-y", package])
        return code, "pkg"
    if shutil_which("dpkg"):
        code = run(["dpkg", "-r", package])
        return code, "dpkg"
    return 1, "none"


def shutil_which(cmd: str) -> Optional[str]:
    from shutil import which

    return which(cmd)


def open_url(url: str) -> Tuple[int, str]:
    """Open URL on Android if possible."""
    if shutil_which("termux-open-url"):
        return run(["termux-open-url", url]), "termux-open-url"
    if shutil_which("xdg-open"):
        return run(["xdg-open", url]), "xdg-open"
    return 1, "none"


def environment_summary() -> dict:
    import platform
    from shutil import which

    info = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "termux": bool(os.environ.get("PREFIX", "").startswith("/data/data/com.termux")),
        "bin": {
            "pkg": bool(which("pkg")),
            "dpkg": bool(which("dpkg")),
            "curl": bool(which("curl")),
            "termux-open-url": bool(which("termux-open-url")),
        },
    }
    try:
        import textual

        info["textual"] = getattr(textual, "__version__", "unknown")
    except Exception:
        info["textual"] = None
    return info
