from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Markdown,
    Static,
)

from . import APP_NAME, APP_VERSION
from .ops import CommandError, build_install, open_url, uninstall
from .paths import find_root, packages_dir


def _import_package_manager(root: Path):
    if (root / "tools").is_dir() and str(root) not in sys.path:
        sys.path.insert(0, str(root))
    from tools.package_manager import PackageManager

    return PackageManager


def _normalize(pkg: Dict[str, Any]) -> Dict[str, Any]:
    pkg = dict(pkg)
    pkg.setdefault("name", pkg.get("package"))
    desc = pkg.get("desc") or pkg.get("description") or "-"
    pkg["desc"] = desc
    pkg.setdefault("description", desc)
    pkg.setdefault("homepage", "-")
    pkg.setdefault("license", "-")
    pkg.setdefault("maintainer", "-")
    pkg.setdefault("version", "?")
    deps = pkg.get("depends")
    if isinstance(deps, str):
        deps = [x.strip() for x in deps.split(",") if x.strip()]
    pkg["depends"] = deps or []
    return pkg


@dataclass
class Row:
    name: str
    version: str
    status: str
    desc: str


class StatusBar(Static):
    pass


class TermuxAppStore(App):
    CSS = """
    #topbar {height: 3;}
    #content {height: 1fr;}
    #table {width: 55%;}
    #details {width: 45%; padding: 1 1;}
    #actions {height: 3;}
    Button {margin-right: 1;}
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("i", "install", "Install/Upgrade"),
        ("u", "uninstall", "Uninstall"),
        ("o", "open_home", "Open homepage"),
        ("/", "focus_search", "Search"),
    ]

    query: str = reactive("")
    selected: Optional[str] = reactive(None)

    def __init__(self, root: Optional[Path] = None):
        super().__init__()
        self.root = root or find_root()
        PM = _import_package_manager(self.root)
        self.pm = PM(packages_dir(self.root))
        self._packages: List[Dict[str, Any]] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            with Horizontal(id="topbar"):
                yield Input(placeholder="Search packages…", id="search")
                yield StatusBar(f"{APP_NAME} v{APP_VERSION}")
            with Horizontal(id="content"):
                yield DataTable(id="table")
                yield Markdown("Select a package…", id="details")
            with Horizontal(id="actions"):
                yield Button("Install/Upgrade", id="btn_install", variant="primary")
                yield Button("Uninstall", id="btn_uninstall")
                yield Button("Open Homepage", id="btn_home")
                yield Button("Refresh", id="btn_refresh")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#table", DataTable)
        table.add_columns("Package", "Version", "Status", "Description")
        table.cursor_type = "row"
        self.refresh_packages()
        self.query_one("#search", Input).focus()

    def refresh_packages(self) -> None:
        self._packages = [_normalize(p) for p in self.pm.load_packages()]
        self._render_table()

    def _render_table(self) -> None:
        table = self.query_one("#table", DataTable)
        table.clear()
        q = self.query.strip().lower()
        rows: List[Row] = []

        for p in self._packages:
            name = p.get("package") or p.get("name")
            if not name:
                continue
            desc = p.get("desc") or "-"
            if q and q not in name.lower() and q not in desc.lower():
                continue
            status, _ = self.pm.get_status(name, p.get("version") or "?")
            rows.append(Row(name=name, version=p.get("version") or "?", status=status, desc=desc[:70]))

        for r in rows:
            table.add_row(r.name, r.version, r.status, r.desc, key=r.name)

        if rows:
            # Keep selection
            if self.selected and any(r.name == self.selected for r in rows):
                table.move_cursor(row=next(i for i, r in enumerate(rows) if r.name == self.selected), column=0)
            else:
                table.move_cursor(row=0, column=0)
                self.selected = rows[0].name
        else:
            self.selected = None
            self.query_one("#details", Markdown).update("No packages found.")

    def _selected_package(self) -> Optional[Dict[str, Any]]:
        if not self.selected:
            return None
        return self.pm.get_package(self.selected)

    def _render_details(self) -> None:
        md = self.query_one("#details", Markdown)
        pkg = self._selected_package()
        if not pkg:
            md.update("Select a package…")
            return
        pkg = _normalize(pkg)
        status, status_desc = self.pm.get_status(pkg["package"], pkg.get("version") or "?")
        deps = ", ".join(pkg.get("depends") or []) or "-"
        homepage = pkg.get("homepage") or "-"
        text = f"""# {pkg['package']}

**Version:** `{pkg.get('version') or '?'}`  
**Status:** `{status}` — {status_desc}  
**License:** `{pkg.get('license') or '-'}`  
**Maintainer:** `{pkg.get('maintainer') or '-'}`  
**Depends:** `{deps}`  
**Homepage:** {homepage}

---

{pkg.get('description') or pkg.get('desc') or '-'}
"""
        md.update(text)
        self.query_one(StatusBar).update(f"Selected: {pkg['package']}  •  {status}")

    @on(Input.Changed, "#search")
    def on_search(self, event: Input.Changed) -> None:
        self.query = event.value
        self._render_table()

    @on(DataTable.RowHighlighted, "#table")
    def on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        if event.row_key is None:
            return
        key = event.row_key
        # Textual versions differ: RowKey may expose `.value`.
        if hasattr(key, "value"):
            key = getattr(key, "value")
        self.selected = str(key)
        self._render_details()

    def action_focus_search(self) -> None:
        self.query_one("#search", Input).focus()

    def action_refresh(self) -> None:
        self.pm.clear_cache()
        self.refresh_packages()
        self.query_one(StatusBar).update("Refreshed")

    def action_install(self) -> None:
        if not self.selected:
            return
        try:
            code = build_install(self.root, self.selected)
            self.query_one(StatusBar).update(
                f"Install finished (exit {code}) — press r to refresh"
            )
        except CommandError as e:
            self.query_one(StatusBar).update(str(e))

    def action_uninstall(self) -> None:
        if not self.selected:
            return
        code, method = uninstall(self.selected)
        self.query_one(StatusBar).update(
            f"Uninstall via {method}: exit {code} — press r to refresh"
        )

    def action_open_home(self) -> None:
        pkg = self._selected_package()
        if not pkg:
            return
        url = (pkg.get("homepage") or "").strip()
        if not url or url == "-":
            self.query_one(StatusBar).update("No homepage URL")
            return
        code, method = open_url(url)
        if code == 0:
            self.query_one(StatusBar).update(f"Opened via {method}")
        else:
            self.query_one(StatusBar).update("No URL opener found")

    @on(Button.Pressed)
    def on_button(self, event: Button.Pressed) -> None:
        match event.button.id:
            case "btn_install":
                self.action_install()
            case "btn_uninstall":
                self.action_uninstall()
            case "btn_home":
                self.action_open_home()
            case "btn_refresh":
                self.action_refresh()


def main() -> None:
    TermuxAppStore().run()


if __name__ == "__main__":
    main()
