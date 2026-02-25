from __future__ import annotations

import os
from pathlib import Path
from typing import Optional


def _is_project_root(p: Path) -> bool:
    return (p / "packages").is_dir() and (
        (p / "build-package.sh").is_file() or (p / "tools").is_dir()
    )


def find_root(start: Optional[Path] = None) -> Path:
    """Best-effort project root discovery.

    Priority:
      1) TERMUX_APP_STORE_HOME (set by the wrapper installed by install.sh)
      2) explicit start
      3) walk up from current file / cwd
    """

    env = os.environ.get("TERMUX_APP_STORE_HOME")
    if env:
        p = Path(env).expanduser().resolve()
        if p.exists():
            return p

    candidates = []
    if start:
        candidates.append(start)
    candidates.append(Path.cwd())

    for base in candidates:
        base = base.resolve()
        p = base
        for _ in range(10):
            if _is_project_root(p):
                return p
            if p.parent == p:
                break
            p = p.parent

    # Fallback to cwd
    return Path.cwd().resolve()


def packages_dir(root: Path) -> Optional[Path]:
    p = root / "packages"
    return p if p.is_dir() else None


def tools_dir(root: Path) -> Optional[Path]:
    p = root / "tools"
    return p if p.is_dir() else None
