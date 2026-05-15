#!/usr/bin/env python3
# Termux App Store -- Interactive Bilingual Guidebook
# github.com/djunekz/termux-app-store
# Redesigned with a refined, high-contrast terminal aesthetic

import os
import sys
import shutil
import textwrap

R    = "\033[0m"
B    = "\033[1m"
DIM  = "\033[2m"
IT   = "\033[3m"
UL   = "\033[4m"

BLK  = "\033[30m"
RED  = "\033[31m"
GRN  = "\033[32m"
YLW  = "\033[33m"
BLU  = "\033[34m"
MAG  = "\033[35m"
CYN  = "\033[36m"
WHT  = "\033[37m"

BRED = "\033[91m"
BGRN = "\033[92m"
BYLW = "\033[93m"
BBLU = "\033[94m"
BMAG = "\033[95m"
BCYN = "\033[96m"
BWHT = "\033[97m"

BG_BLK  = "\033[40m"
BG_RED  = "\033[41m"
BG_GRN  = "\033[42m"
BG_YLW  = "\033[43m"
BG_BLU  = "\033[44m"
BG_MAG  = "\033[45m"
BG_CYN  = "\033[46m"
BG_WHT  = "\033[47m"

BG_BBLK = "\033[100m"
BG_BRED = "\033[101m"
BG_BGRN = "\033[102m"
BG_BYLW = "\033[103m"
BG_BBLU = "\033[104m"
BG_BMAG = "\033[105m"
BG_BCYN = "\033[106m"
BG_BWHT = "\033[107m"

def TW(): return shutil.get_terminal_size((80, 24)).columns
def TH(): return shutil.get_terminal_size((80, 24)).lines
def W():  return min(TW(), 78)

def cls():
# FIX: 使用subprocess替代os.system
# os.system("clear" if os.name != "nt" else "cls")

def strip_ansi(text):
    clean, i = "", 0
    while i < len(text):
        if text[i] == "\033":
            while i < len(text) and text[i] != "m":
                i += 1
        else:
            clean += text[i]
        i += 1
    return clean

def vlen(text):
    return len(strip_ansi(text))

def vcenter(text, width=None):
    if width is None: width = W()
    pad = max(0, (width - vlen(text)) // 2)
    return " " * pad + text

def vright(text, width=None):
    if width is None: width = W()
    pad = max(0, width - vlen(text))
    return " " * pad + text

def wrap_plain(text, indent=2, width=None):
    if width is None: width = W() - indent - 2
    lines = []
    for para in text.split("\n"):
        if not para.strip():
            lines.append("")
            continue
        for ln in textwrap.wrap(para, width):
            lines.append(" " * indent + ln)
    return lines

def pause(lang="id"):
    msg = "Press Enter to continue..." if lang == "en" else "Tekan Enter untuk lanjut..."
    print(f"\n  {DIM}{BG_BBLK}  {msg}  {R}", end="")
    try:    input()
    except (EOFError, KeyboardInterrupt): pass

def pager(lines, lang="id"):
    back = "back" if lang == "en" else "kembali"
    cont = "next" if lang == "en" else "lanjut"
    msg  = f"Enter = {cont}   q = {back}"
    chunk = max(TH() - 5, 8)
    i = 0
    while i < len(lines):
        cls()
        for ln in lines[i : i + chunk]:
            print(ln)
        i += chunk
        if i < len(lines):
            print(f"\n  {DIM}{msg}{R}", end="", flush=True)
            try:    ch = input()
            except (EOFError, KeyboardInterrupt): break
            if ch.strip().lower() == "q": break
        else:
            pause(lang)


def hline(char="─", color=DIM, width=None):
    if width is None: width = W()
    return f"{color}{char * width}{R}"

def thick_rule(color=BCYN, width=None):
    if width is None: width = W()
    return f"{color}{'━' * width}{R}"

def double_rule(color=DIM, width=None):
    if width is None: width = W()
    return f"{color}{'═' * width}{R}"

def section_header(title, tag_str="", color=BCYN, width=None):
    if width is None: width = W()
    if tag_str:
        plain_tag   = strip_ansi(tag_str)
        plain_inner = f"  {plain_tag}  {title}  "
        inner       = f"  {tag_str}  {title}  "
    else:
        plain_inner = f"  {title}  "
        inner       = f"  {B}{title}{R}  "
    pad        = max(0, width - len(plain_inner))
    bar_top    = f"{color}{'▄' * width}{R}"
    bar_label  = f"{BG_BBLU}{BWHT}{B}{inner}{R}{BG_BBLU}{' ' * pad}{R}"
    bar_bottom = f"{color}{'▀' * width}{R}"
    return ["", bar_top, bar_label, bar_bottom, ""]

def subsection(title, color=BCYN):
    marker = f"{color}▌{R}"
    return ["", f"{marker} {B}{BWHT}{title}{R}", f"  {DIM}{'─' * (W() - 2)}{R}", ""]

def code_block(*cmds, title=""):
    w = W() - 6

    prefix_l = f"  {DIM}│{R} "
    prefix_r = f" {DIM}│{R}"
    dash_w   = w + 2

    lines = []

    if title:
        title_str  = f" {title} "
        fill_count = max(0, dash_w - len(title_str))
        top = f"  {DIM}┌{title_str}{'─' * fill_count}┐{R}"
    else:
        top = f"  {DIM}┌{'─' * dash_w}┐{R}"

    lines.append(top)

    for cmd in cmds:
        if cmd == "":
            lines.append(f"{prefix_l}{' ' * w}{prefix_r}")
        elif cmd.startswith("#"):
            pad     = max(0, w - len(cmd))
            content = f"{DIM}{IT}{cmd}{R}{' ' * pad}"
            lines.append(f"{prefix_l}{content}{prefix_r}")
        else:
            pad     = max(0, w - 2 - len(cmd))
            content = f"{BYLW}$ {R}{BCYN}{cmd}{R}{' ' * pad}"
            lines.append(f"{prefix_l}{content}{prefix_r}")

    lines.append(f"  {DIM}└{'─' * dash_w}┘{R}")
    return lines

def bullet(items, color=BCYN, indent=2):
    out = []
    for item in items:
        leader = f"{' ' * indent}{color}◆{R} "
        first = True
        for part in item.split("\n"):
            if first:
                out.append(f"{leader}{part}")
                first = False
            else:
                out.append(f"{' ' * (indent + 2)}{part}")
    return out

def numbered(items, color=BCYN, indent=2):
    out = []
    for i, item in enumerate(items, 1):
        num_str = f"{color}{B}{i:>2}.{R}"
        out.append(f"{' ' * indent}{num_str} {item}")
    return out

def callout(label, text, style="info"):
    styles = {
        "info":    (BCYN,  "INFO",    "╭", "│", "╰", "╮", "╯"),
        "note":    (BYLW,  "CATATAN", "╭", "│", "╰", "╮", "╯"),
        "warning": (BRED,  "WARNING", "╭", "│", "╰", "╮", "╯"),
        "tip":     (BGRN,  "TIP",     "╭", "│", "╰", "╮", "╯"),
        "success": (BGRN,  "OK",      "╭", "│", "╰", "╮", "╯"),
    }
    col, default_label, tl, ml, bl, tr, br = styles.get(style, styles["info"])
    lbl = label or default_label

    w = W() - 4

    dash_right = max(0, w - len(lbl) - 5)
    top = f"  {col}{tl}─[ {R}{col}{B}{lbl}{R}{col} ]{'─' * dash_right}{tr}{R}"

    body_w = w - 4
    body_lines = textwrap.wrap(text, max(10, body_w)) if text else [""]
    body = []
    for ln in body_lines:
        pad = max(0, body_w - len(ln))
        body.append(f"  {col}{ml}{R}  {IT}{ln}{R}{' ' * pad}  {col}{ml}{R}")

    bot = f"  {col}{bl}{'─' * w}{br}{R}"

    return [top] + body + [bot]

def badge(text, color=BG_BBLK, fg=BWHT):
    return f"{color}{fg} {text} {R}"

def kv_row(key, value, key_color=DIM, val_color=BCYN, indent=2):
    return f"{' ' * indent}{key_color}{key}{R}  {val_color}{value}{R}"

def tag(text, color=BG_BBLU, fg=BWHT):
    return f"{color}{fg}[{text}]{R}"


def content_about(L):
    en = L == "en"
    if en:
        lines  = section_header("ABOUT  TERMUX APP STORE", tag("TAS")
)
        lines += subsection("What is Termux App Store?")
        lines += [
            f"  Termux App Store is the first {BCYN}{B}TUI (Terminal User Interface){R}",
            f"  package manager built natively for Termux.",
            f"  Written in Python ({BCYN}Textual{R}) + CLI -- browse, build, and manage",
            f"  tools directly on Android. No account. No telemetry. No cloud.", "",
        ]
        lines += subsection("Philosophy")
        lines += [
            f"  {IT}{DIM}\"Local first. Control over convenience. Transparency over magic.\"{R}", "",
        ]
        lines += bullet([
            f"{B}Offline-first{R}   -- no server or cloud required",
            f"{B}Source-based{R}    -- all builds transparent, full user control",
            f"{B}Binary-safe{R}     -- binary distribution only for the store itself",
            f"{B}Termux-native{R}   -- built for the Termux / Android ecosystem",
        ])
        lines += subsection("Who built it?")
        lines += [
            f"  Created by {BGRN}{B}Djunekz{R} -- Independent Developer.",
            f"  This is a community project, not an official Termux product.", "",
            kv_row("GitHub   :", "https://github.com/djunekz"),
            kv_row("Repo     :", "https://github.com/djunekz/termux-app-store"),
            kv_row("Issues   :", "https://github.com/djunekz/termux-app-store/issues"),
            kv_row("Email    :", "gab288.gab288@passinbox.com"),
            kv_row("License  :", f"{BGRN}MIT License{R}"),
            "",
        ]
        lines += subsection("History & Timeline")
        timeline = [
            ("v0.0.1", "Jan 2026", "Internal prototype, local-only"),
            ("v0.1.0", "Feb 2026", "First TUI with Textual, package browser"),
            ("v0.1.2", "Feb 2026", "tasctl, lint/check-pr, status badges"),
            ("v0.1.4", "Feb 2026", "termux-build create, CLI upgrade, new UI"),
            ("v0.1.6", "Feb 2026", "index.json, update/upgrade, CI workflows"),
            ("v0.1.7", "Mar 2026", "15+ new packages, uninstall button in TUI"),
            ("v0.2.3", "Apr 2026", "pip install support, source mode resolver"),
            ("v0.2.4", "Apr 2026", "termux-build init (auto create & build)"),
            ("v0.2.6", "Apr 2026", "Update termux-app-store TUI to new version Textual"),
        ]
        for ver, date, desc in timeline:
            lines.append(f"  {BCYN}{B}{ver:<8}{R}  {DIM}{date}{R}  {desc}")
        lines += [""]
        lines += subsection("Architecture Overview")
        arch = [
            ("User Interface", "Textual TUI"),
            ("Application Core", "State, Events, Logic"),
            ("Package Resolver", "build.sh inspection"),
            ("Build Executor", "build-package.sh"),
            ("Termux Environment", "pkg / apt / shell"),
        ]
        for i, (layer, detail) in enumerate(arch):
            connector = f"  {DIM}│{R}" if i < len(arch) - 1 else ""
            lines.append(f"  {BCYN}▣{R}  {B}{layer:<20}{R}  {DIM}{detail}{R}")
            if connector: lines.append(connector)
        lines += [""]
        lines += callout("", "Termux App Store is NOT a replacement for pkg/apt.", "note")
    else:
        lines  = section_header("TENTANG  TERMUX APP STORE", tag("TAS"))
        lines += subsection("Apa itu Termux App Store?")
        lines += [
            f"  Termux App Store adalah {BCYN}{B}TUI (Terminal User Interface){R} package",
            f"  manager pertama yang dibangun khusus untuk Termux secara native.",
            f"  Dibuat dengan Python ({BCYN}Textual{R}) dan CLI -- browse, build, dan",
            f"  manage tools langsung di Android. Tanpa akun. Tanpa telemetri. Tanpa cloud.", "",
        ]
        lines += subsection("Filosofi")
        lines += [
            f"  {IT}{DIM}\"Local first. Control over convenience. Transparency over magic.\"{R}", "",
        ]
        lines += bullet([
            f"{B}Offline-first{R}   -- tidak butuh server atau cloud",
            f"{B}Source-based{R}    -- semua build transparan, user punya kontrol penuh",
            f"{B}Binary-safe{R}     -- binary distribution hanya untuk app-store-nya sendiri",
            f"{B}Termux-native{R}   -- dibangun khusus untuk ekosistem Termux / Android",
        ])
        lines += subsection("Siapa yang membuatnya?")
        lines += [
            f"  Dibuat oleh {BGRN}{B}Djunekz{R} -- Independent Developer.",
            f"  Ini adalah proyek komunitas, bukan proyek resmi Termux.", "",
            kv_row("GitHub   :", "https://github.com/djunekz"),
            kv_row("Repo     :", "https://github.com/djunekz/termux-app-store"),
            kv_row("Issues   :", "https://github.com/djunekz/termux-app-store/issues"),
            kv_row("Email    :", "gab288.gab288@passinbox.com"),
            kv_row("Lisensi  :", f"{BGRN}MIT License{R}"),
            "",
        ]
        lines += subsection("Sejarah & Timeline")
        timeline = [
            ("v0.0.1", "Jan 2026", "Prototype internal, local-only"),
            ("v0.1.0", "Feb 2026", "TUI pertama dengan Textual, package browser"),
            ("v0.1.2", "Feb 2026", "tasctl, lint/check-pr, badge status"),
            ("v0.1.4", "Feb 2026", "termux-build create, CLI upgrade, UI baru"),
            ("v0.1.6", "Feb 2026", "index.json, update/upgrade, CI workflows"),
            ("v0.1.7", "Mar 2026", "15+ package baru, uninstall button di TUI"),
            ("v0.2.3", "Apr 2026", "pip install support, source mode resolver"),
            ("v0.2.4", "Apr 2026", "termux-build init (auto create & build)"),
        ]
        for ver, date, desc in timeline:
            lines.append(f"  {BCYN}{B}{ver:<8}{R}  {DIM}{date}{R}  {desc}")
        lines += [""]
        lines += subsection("Arsitektur Singkat")
        arch = [
            ("User Interface",   "Textual TUI"),
            ("Application Core", "State, Events, Logic"),
            ("Package Resolver", "build.sh inspection"),
            ("Build Executor",   "build-package.sh"),
            ("Termux Env",       "pkg / apt / shell"),
        ]
        for i, (layer, detail) in enumerate(arch):
            connector = f"  {DIM}│{R}" if i < len(arch) - 1 else ""
            lines.append(f"  {BCYN}▣{R}  {B}{layer:<20}{R}  {DIM}{detail}{R}")
            if connector: lines.append(connector)
        lines += [""]
        lines += callout("", "Termux App Store BUKAN pengganti pkg/apt.", "note")
    lines.append("")
    return lines


def content_install(L):
    en = L == "en"
    if en:
        lines  = section_header("HOW TO INSTALL", tag("#"))
        lines += subsection("Requirements")
        lines += bullet([
            "Termux (latest version recommended)",
            "Internet connection",
            f"Architecture: {BCYN}aarch64{R} (recommended)  /  {BCYN}armv7l{R}  /  {BCYN}x86_64{R}",
        ])
        lines += subsection(f"{BGRN}Option 1 -- Recommended (pip){R}")
        lines += code_block("pkg install python", "pip install termux-app-store", title="terminal")
        lines += [""] + subsection("Option 2 -- Manual (git clone)")
        lines += code_block(
            "git clone https://github.com/djunekz/termux-app-store",
            "cd termux-app-store",
            "bash install.sh",
            title="terminal",
        )
        lines += ["", f"  {DIM}or with tasctl:{R}", ""]
        lines += code_block(
            "git clone https://github.com/djunekz/termux-app-store",
            "cd termux-app-store",
            "./tasctl install",
            title="terminal",
        )
        lines += [""] + subsection("After Install")
        lines += code_block(
            "termux-app-store        # Open interactive TUI",
            "termux-app-store -h     # Show CLI help",
            title="terminal",
        )
        lines += subsection("File Locations After Install")
        lines += [
            kv_row("Binary/source :", f"{BCYN}$PREFIX/lib/.tas/{R}"),
            kv_row("Symlink       :", f"{BCYN}$PREFIX/bin/termux-app-store{R}"),
            kv_row("packages/     :", f"{BCYN}$PREFIX/lib/.tas/packages/{R}"),
            "",
        ]
        lines += subsection("Install Troubleshooting")
        troubles = [
            ("command not found",    f"Restart Termux, or run: {BCYN}hash -r{R}"),
            ("Permission denied",    f"{BCYN}chmod +x $PREFIX/bin/termux-app-store{R}"),
            ("Arch unsupported",     f"Check: {BCYN}uname -m{R}"),
            ("ModuleNotFoundError",  f"{BCYN}pip install textual{R}"),
        ]
        for err, fix in troubles:
            lines.append(f"  {BYLW}[!]{R} {B}{err:<22}{R}  {fix}")
        lines += [""]
    else:
        lines  = section_header("CARA INSTALL TERMUX APP STORE", tag("#"))
        lines += subsection("Requirements")
        lines += bullet([
            "Termux (versi terbaru direkomendasikan)",
            "Koneksi internet",
            f"Arsitektur: {BCYN}aarch64{R} (direkomendasikan)  /  {BCYN}armv7l{R}  /  {BCYN}x86_64{R}",
        ])
        lines += subsection(f"{BGRN}Opsi 1 -- Recommended (pip){R}")
        lines += code_block("pkg install python", "pip install termux-app-store", title="terminal")
        lines += [""] + subsection("Opsi 2 -- Manual (git clone)")
        lines += code_block(
            "git clone https://github.com/djunekz/termux-app-store",
            "cd termux-app-store",
            "bash install.sh",
            title="terminal",
        )
        lines += ["", f"  {DIM}atau dengan tasctl:{R}", ""]
        lines += code_block(
            "git clone https://github.com/djunekz/termux-app-store",
            "cd termux-app-store",
            "./tasctl install",
            title="terminal",
        )
        lines += [""] + subsection("Setelah Install")
        lines += code_block(
            "termux-app-store        # Buka TUI interaktif",
            "termux-app-store -h     # Tampilkan CLI help",
            title="terminal",
        )
        lines += subsection("Lokasi File Setelah Install")
        lines += [
            kv_row("Binary/source :", f"{BCYN}$PREFIX/lib/.tas/{R}"),
            kv_row("Symlink       :", f"{BCYN}$PREFIX/bin/termux-app-store{R}"),
            kv_row("packages/     :", f"{BCYN}$PREFIX/lib/.tas/packages/{R}"),
            "",
        ]
        lines += subsection("Troubleshooting Install")
        troubles = [
            ("command not found",    f"Restart Termux atau: {BCYN}hash -r{R}"),
            ("Permission denied",    f"{BCYN}chmod +x $PREFIX/bin/termux-app-store{R}"),
            ("Arch unsupported",     f"Cek: {BCYN}uname -m{R}"),
            ("ModuleNotFoundError",  f"{BCYN}pip install textual{R}"),
        ]
        for err, fix in troubles:
            lines.append(f"  {BYLW}[!]{R} {B}{err:<22}{R}  {fix}")
        lines += [""]
    return lines


def content_uninstall(L):
    en = L == "en"
    if en:
        lines  = section_header("HOW TO UNINSTALL", tag("X"))
        lines += subsection("Option 1 -- pip (if installed via pip)")
        lines += code_block("pip uninstall termux-app-store", title="terminal")
        lines += [""] + subsection("Option 2 -- tasctl")
        lines += code_block("./tasctl uninstall", title="terminal")
        lines += [""] + subsection("Option 3 -- Manual")
        lines += code_block(
            "rm -f $PREFIX/bin/termux-app-store",
            "rm -rf $PREFIX/lib/.tas",
            title="terminal",
        )
        lines += [""]
        lines += callout("", "Uninstall does not remove packages/ you created manually.", "note")
    else:
        lines  = section_header("CARA UNINSTALL", tag("X"))
        lines += subsection("Opsi 1 -- pip (jika install via pip)")
        lines += code_block("pip uninstall termux-app-store", title="terminal")
        lines += [""] + subsection("Opsi 2 -- tasctl")
        lines += code_block("./tasctl uninstall", title="terminal")
        lines += [""] + subsection("Opsi 3 -- Manual")
        lines += code_block(
            "rm -f $PREFIX/bin/termux-app-store",
            "rm -rf $PREFIX/lib/.tas",
            title="terminal",
        )
        lines += [""]
        lines += callout("", "Uninstall tidak menghapus packages/ yang sudah kamu buat sendiri.", "note")
    lines.append("")
    return lines


def content_usage(L):
    en = L == "en"
    if en:
        lines  = section_header("USING termux-app-store", tag(">"))
        lines += subsection("TUI -- Interactive Interface")
        lines += code_block("termux-app-store", title="terminal")
        lines += ["", f"  {DIM}TUI Navigation:{R}", ""]
        lines += bullet([
            f"{BCYN}Up / Down{R}   -- navigate package list",
            f"{BCYN}Enter{R}       -- view detail / install",
            f"{BCYN}Ctrl+Q{R}      -- quit",
            "Touchscreen fully supported",
        ])
        lines += subsection("CLI -- Command Line")
        lines += code_block(
            "termux-app-store list",
            "termux-app-store show <package>",
            "termux-app-store install <package>",
            "termux-app-store update",
            "termux-app-store upgrade",
            "termux-app-store upgrade <package>",
            "termux-app-store version",
            "termux-app-store help",
            title="terminal",
        )
        lines += subsection("CLI Shortcuts")
        shortcuts = [
            ("-h",           "help"),
            ("-v",           "version"),
            ("-i <package>", "install package"),
            ("-l / -L",      "list packages"),
        ]
        for flag, desc in shortcuts:
            lines.append(f"  {BCYN}{B}{flag:<18}{R}  {desc}")
        lines += subsection("Package Status Badges")
        lines += [
            f"  {BG_BGRN}{BLK} INSTALLED {R}   installed version is up-to-date",
            f"  {BG_BCYN}{BLK}  UPDATE   {R}   a newer version is available",
            f"  {BG_BYLW}{BLK}   NEW     {R}   newly added (< 7 days)",
            f"  {BG_BRED}{BWHT} UNSUPPORTED {R}   dependency not available in Termux",
            "",
        ]
    else:
        lines  = section_header("PENGGUNAAN termux-app-store", tag(">"))
        lines += subsection("TUI -- Interface Interaktif")
        lines += code_block("termux-app-store", title="terminal")
        lines += ["", f"  {DIM}Navigasi TUI:{R}", ""]
        lines += bullet([
            f"{BCYN}Atas / Bawah{R}   -- pindah package",
            f"{BCYN}Enter{R}          -- lihat detail / install",
            f"{BCYN}Ctrl+Q{R}         -- keluar",
            "Touchscreen didukung penuh",
        ])
        lines += subsection("CLI -- Command Line")
        lines += code_block(
            "termux-app-store list",
            "termux-app-store show <package>",
            "termux-app-store install <package>",
            "termux-app-store update",
            "termux-app-store upgrade",
            "termux-app-store upgrade <package>",
            "termux-app-store version",
            "termux-app-store help",
            title="terminal",
        )
        lines += subsection("Shortcut CLI")
        shortcuts = [
            ("-h",           "help"),
            ("-v",           "version"),
            ("-i <package>", "install package"),
            ("-l / -L",      "list package"),
        ]
        for flag, desc in shortcuts:
            lines.append(f"  {BCYN}{B}{flag:<18}{R}  {desc}")
        lines += subsection("Status Badge Package")
        lines += [
            f"  {BG_BGRN}{BLK} INSTALLED {R}   versi terinstal sudah up-to-date",
            f"  {BG_BCYN}{BLK}  UPDATE   {R}   ada versi baru tersedia",
            f"  {BG_BYLW}{BLK}   NEW     {R}   package baru (< 7 hari)",
            f"  {BG_BRED}{BWHT} UNSUPPORTED {R}   dependency tidak tersedia di Termux",
            "",
        ]
    return lines


def content_tasctl(L):
    en = L == "en"
    if en:
        lines  = section_header("USING tasctl", tag("!"))
        lines += [
            f"  {DIM}tasctl = Termux App Store Controller{R}",
            f"  Tool to install, update, and uninstall Termux App Store itself.", "",
        ]
        lines += subsection("Commands")
        lines += code_block(
            "tasctl install      # Install latest TAS",
            "tasctl update       # Update to latest version",
            "tasctl uninstall    # Remove TAS",
            "tasctl doctor       # Diagnose environment",
            "tasctl self-update  # Update tasctl itself",
            "tasctl help         # Show help",
            title="terminal",
        )
        lines += subsection("tasctl doctor -- Checks")
        lines += bullet([
            "CPU architecture (aarch64 / armv7l / x86_64)",
            "Python & pip installed",
            "Textual (TUI framework) installed",
            "curl available",
            "TAS install status (binary / source / unknown)",
            "TERMUX_APP_STORE_HOME in wrapper",
        ])
        lines += [""]
        lines += callout("TIP", "If something feels broken, run 'tasctl doctor' before reporting a bug.", "tip")
    else:
        lines  = section_header("PENGGUNAAN tasctl", tag("!"))
        lines += [
            f"  {DIM}tasctl = Termux App Store Controller{R}",
            f"  Tool untuk install, update, dan uninstall Termux App Store itu sendiri.", "",
        ]
        lines += subsection("Perintah")
        lines += code_block(
            "tasctl install      # Install TAS versi terbaru",
            "tasctl update       # Update ke versi terbaru",
            "tasctl uninstall    # Hapus TAS",
            "tasctl doctor       # Diagnosa environment",
            "tasctl self-update  # Update tasctl itu sendiri",
            "tasctl help         # Tampilkan bantuan",
            title="terminal",
        )
        lines += subsection("tasctl doctor -- Cek Apa Saja?")
        lines += bullet([
            "Arsitektur CPU (aarch64 / armv7l / x86_64)",
            "Python & pip terinstall",
            "Textual (TUI framework) terinstall",
            "curl tersedia",
            "Status instalasi TAS (binary / source / unknown)",
            "TERMUX_APP_STORE_HOME di wrapper",
        ])
        lines += [""]
        lines += callout("TIP", "Jika ada masalah aneh, coba 'tasctl doctor' dulu sebelum report bug.", "tip")
    lines.append("")
    return lines


def content_termux_build(L):
    en = L == "en"
    if en:
        lines  = section_header("USING termux-build", tag("@"))
        lines += [
            f"  {DIM}termux-build = validation & review tool{R}",
            f"  NOT auto-upload or auto-publish. Only reads and validates.", "",
        ]
        lines += subsection("All Sub-commands")
        lines += code_block(
            "./termux-build create <package>",
            "./termux-build init <repo-url>",
            "./termux-build lint <package>",
            "./termux-build check-pr <package>",
            "./termux-build doctor",
            "./termux-build suggest <package>",
            "./termux-build explain <package>",
            "./termux-build template",
            "./termux-build guide",
            title="terminal",
        )
        lines += subsection("Command Descriptions")
        cmds = [
            ("create",   "Create new package folder with empty build.sh"),
            ("init",     f"{BGRN}Auto-detect{R} GitHub repo, generate build.sh"),
            ("lint",     "Validate build.sh (fields, format, version)"),
            ("check-pr", "Check Pull Request readiness"),
            ("doctor",   "Diagnose build environment"),
            ("suggest",  "Get improvement suggestions for a package"),
            ("explain",  "Detailed package explanation"),
            ("template", "Generate a new build.sh template"),
            ("guide",    "Show contribution guide"),
        ]
        for cmd, desc in cmds:
            lines.append(f"  {BCYN}{B}{cmd:<12}{R}  {desc}")
        lines += subsection("termux-build init -- Most Powerful Feature")
        lines += [
            f"  Auto-detect a GitHub repo, generate a complete build.sh,",
            f"  and optionally build a .deb package.", "",
        ]
        lines += code_block("./termux-build init https://github.com/user/repo", title="terminal")
        lines += ["", f"  {DIM}What it does automatically:{R}", ""]
        lines += bullet([
            "Fetch GitHub metadata (name, description, license, language)",
            "Download source code",
            "Detect build method (python-script / pip / shell / cargo / etc)",
            "Detect main entrypoint file",
            "Detect installer scripts (install_Termux.sh, install.sh, etc)",
            "Scan dependencies (imports, requirements.txt, shell deps)",
            "Compute SHA256 checksum automatically",
            "Generate complete build.sh",
            "Optional: test build & install as .deb",
        ])
        lines += [""]
        lines += callout("", "termux-build does NOT modify files, auto-build, or upload to GitHub.", "note")
    else:
        lines  = section_header("PENGGUNAAN termux-build", tag("@"))
        lines += [
            f"  {DIM}termux-build = validation & review tool{R}",
            f"  Bukan auto-upload atau auto-publish. Hanya membaca & memvalidasi.", "",
        ]
        lines += subsection("Semua Sub-command")
        lines += code_block(
            "./termux-build create <package>",
            "./termux-build init <repo-url>",
            "./termux-build lint <package>",
            "./termux-build check-pr <package>",
            "./termux-build doctor",
            "./termux-build suggest <package>",
            "./termux-build explain <package>",
            "./termux-build template",
            "./termux-build guide",
            title="terminal",
        )
        lines += subsection("Penjelasan Tiap Command")
        cmds = [
            ("create",   "Buat folder package baru dengan build.sh kosong"),
            ("init",     f"{BGRN}Auto-detect{R} repo GitHub, generate build.sh otomatis"),
            ("lint",     "Cek validasi build.sh (field, format, versi)"),
            ("check-pr", "Cek kesiapan Pull Request"),
            ("doctor",   "Diagnosa environment build"),
            ("suggest",  "Saran perbaikan untuk package"),
            ("explain",  "Penjelasan detail package"),
            ("template", "Generate template build.sh baru"),
            ("guide",    "Tampilkan contribution guide"),
        ]
        for cmd, desc in cmds:
            lines.append(f"  {BCYN}{B}{cmd:<12}{R}  {desc}")
        lines += subsection("termux-build init -- Fitur Paling Powerful")
        lines += [
            f"  Auto-detect repo GitHub, generate build.sh lengkap,",
            f"  lalu opsional build jadi .deb.", "",
        ]
        lines += code_block("./termux-build init https://github.com/user/repo", title="terminal")
        lines += ["", f"  {DIM}Yang dilakukan otomatis:{R}", ""]
        lines += bullet([
            "Fetch metadata GitHub (nama, deskripsi, lisensi, bahasa)",
            "Download source code",
            "Deteksi build method (python-script / pip / shell / cargo / dll)",
            "Deteksi entrypoint utama",
            "Deteksi installer script (install_Termux.sh, install.sh, dll)",
            "Scan dependency (imports, requirements.txt, shell deps)",
            "Hitung SHA256 checksum otomatis",
            "Generate build.sh lengkap",
            "Opsional: langsung test build & install jadi .deb",
        ])
        lines += [""]
        lines += callout("", "termux-build TIDAK memodifikasi file, tidak auto-build, tidak upload ke GitHub.", "note")
    lines.append("")
    return lines


def content_build_package(L):
    en = L == "en"
    if en:
        lines  = section_header("USING build-package.sh", tag("$"))
        lines += [
            f"  {DIM}build-package.sh = core build engine{R}",
            f"  Used by TUI and CLI to build & install packages as .deb files.", "",
        ]
        lines += subsection("Manual Usage")
        lines += code_block(
            "./build-package.sh <package-name>",
            "",
            "# Example:",
            "./build-package.sh mr-holmes",
            title="terminal",
        )
        lines += subsection("What build-package.sh Does")
        lines += numbered([
            "Validate build.sh (syntax + required fields)",
            "Detect CPU architecture",
            "Install dependencies via pkg",
            f"Download source from {BCYN}TERMUX_PKG_SRCURL{R}",
            "Verify SHA256 checksum",
            "Extract source archive",
            f"Run {BCYN}termux_step_make_install(){R}",
            "Generate .deb metadata",
            "Build .deb with dpkg-deb",
            "Install package with dpkg -i",
            "Hold package from pkg upgrade overwrite",
        ])
        lines += subsection("Output Structure")
        lines += [
            kv_row("build/<package>/", "build working directory"),
            kv_row("output/<pkg>.deb", "generated .deb package file"),
            "",
        ]
    else:
        lines  = section_header("PENGGUNAAN build-package.sh", tag("$"))
        lines += [
            f"  {DIM}build-package.sh = core build engine{R}",
            f"  Dipakai oleh TUI dan CLI untuk build & install package jadi .deb.", "",
        ]
        lines += subsection("Cara Pakai Manual")
        lines += code_block(
            "./build-package.sh <package-name>",
            "",
            "# Contoh:",
            "./build-package.sh mr-holmes",
            title="terminal",
        )
        lines += subsection("Yang Dilakukan build-package.sh")
        lines += numbered([
            "Validasi build.sh (syntax + required fields)",
            "Deteksi arsitektur CPU",
            "Install dependencies via pkg",
            f"Download source dari {BCYN}TERMUX_PKG_SRCURL{R}",
            "Verifikasi SHA256 checksum",
            "Extract source archive",
            f"Jalankan {BCYN}termux_step_make_install(){R}",
            "Generate metadata .deb",
            "Build file .deb dengan dpkg-deb",
            "Install package dengan dpkg -i",
            "Hold package dari pkg upgrade",
        ])
        lines += subsection("Struktur Output")
        lines += [
            kv_row("build/<package>/", "working directory build"),
            kv_row("output/<pkg>.deb", "file .deb hasil build"),
            "",
        ]
    return lines


def content_upload(L):
    en = L == "en"
    if en:
        lines  = section_header("HOW TO UPLOAD A TOOL TO TAS", tag("^"))
        steps_en = [
            ("Fork the repository",
             [f"Open: {BCYN}https://github.com/djunekz/termux-app-store{R}",
              "Click Fork -> Create fork",
              "Keep the repo name: termux-app-store"],
             []),
            ("Clone your fork", [],
             ["git clone https://github.com/USERNAME/termux-app-store",
              "cd termux-app-store"]),
            ("Create a new branch", [],
             ["git checkout -b your-tool-name"]),
            ("Create package folder", [],
             ["mkdir -p packages/your-tool-name",
              "nano packages/your-tool-name/build.sh"]),
            ("Fill in build.sh", [],
             ['TERMUX_PKG_HOMEPAGE=https://github.com/user/tool',
              'TERMUX_PKG_DESCRIPTION="Short tool description"',
              'TERMUX_PKG_LICENSE="MIT"',
              'TERMUX_PKG_MAINTAINER="@your-github-username"',
              "TERMUX_PKG_VERSION=1.0.0",
              "TERMUX_PKG_SRCURL=https://...",
              "TERMUX_PKG_SHA256=abc123..."]),
            ("Validate before committing", [],
             ["./termux-build lint packages/your-tool-name",
              "./termux-build check-pr your-tool-name",
              "./termux-build doctor"]),
            ("Commit and push", [],
             ["git add packages/your-tool-name",
              'git commit -m "pkg: add your-tool-name"',
              "git push origin your-tool-name"]),
            ("Create a Pull Request",
             [f"Open your fork on GitHub",
              "Click Compare & Pull Request",
              "Describe: what the tool does, upstream source, how to test",
              "Submit PR -- CI will validate automatically"],
             []),
        ]
        for i, (title, buls, cmds) in enumerate(steps_en, 1):
            lines.append(f"  {BCYN}{BG_BBLK} Step {i} {R} {B}{title}{R}")
            lines.append("")
            if buls:
                lines += bullet(buls)
                lines.append("")
            if cmds:
                lines += code_block(*cmds, title="terminal")
                lines.append("")
            lines.append(f"  {DIM}{'─' * (W() - 4)}{R}")
            lines.append("")
        lines += subsection("Important Rules")
        lines += bullet([
            f"{BRED}DO NOT{R} upload locally compiled binaries",
            f"{BRED}DO NOT{R} hardcode paths outside $PREFIX",
            "Source MUST come from official upstream",
            "CI (GitHub Actions) will reject PRs that fail lint",
            f"Commit message: {BCYN}pkg: add <name>{R}  or  {BCYN}fix: ...{R}",
        ])
        lines += [""]
        lines += callout("TIP", "Auto-generate build.sh with: ./termux-build init <repo-url>", "tip")
    else:
        lines  = section_header("CARA UPLOAD TOOL KE TERMUX APP STORE", tag("^"))
        steps_id = [
            ("Fork repository",
             [f"Buka: {BCYN}https://github.com/djunekz/termux-app-store{R}",
              "Klik tombol Fork -> Create fork",
              "Pastikan nama repo tetap: termux-app-store"],
             []),
            ("Clone fork kamu", [],
             ["git clone https://github.com/USERNAME/termux-app-store",
              "cd termux-app-store"]),
            ("Buat branch baru", [],
             ["git checkout -b nama-tool-kamu"]),
            ("Buat folder package", [],
             ["mkdir -p packages/nama-tool-kamu",
              "nano packages/nama-tool-kamu/build.sh"]),
            ("Isi build.sh", [],
             ["TERMUX_PKG_HOMEPAGE=https://github.com/user/tool",
              'TERMUX_PKG_DESCRIPTION="Deskripsi singkat tool"',
              'TERMUX_PKG_LICENSE="MIT"',
              'TERMUX_PKG_MAINTAINER="@github-username-kamu"',
              "TERMUX_PKG_VERSION=1.0.0",
              "TERMUX_PKG_SRCURL=https://...",
              "TERMUX_PKG_SHA256=abc123..."]),
            ("Validasi sebelum commit", [],
             ["./termux-build lint packages/nama-tool-kamu",
              "./termux-build check-pr nama-tool-kamu",
              "./termux-build doctor"]),
            ("Commit dan push", [],
             ["git add packages/nama-tool-kamu",
              'git commit -m "pkg: add nama-tool-kamu"',
              "git push origin nama-tool-kamu"]),
            ("Buat Pull Request",
             ["Buka fork kamu di GitHub",
              "Klik Compare & Pull Request",
              "Isi deskripsi: apa tool-nya, sumber upstream, cara test",
              "Submit PR -- CI akan otomatis validasi"],
             []),
        ]
        for i, (title, buls, cmds) in enumerate(steps_id, 1):
            lines.append(f"  {BCYN}{BG_BBLK} Langkah {i} {R} {B}{title}{R}")
            lines.append("")
            if buls:
                lines += bullet(buls)
                lines.append("")
            if cmds:
                lines += code_block(*cmds, title="terminal")
                lines.append("")
            lines.append(f"  {DIM}{'─' * (W() - 4)}{R}")
            lines.append("")
        lines += subsection("Aturan Penting")
        lines += bullet([
            f"{BRED}JANGAN{R} upload binary compiled dari local",
            f"{BRED}JANGAN{R} hardcode path di luar $PREFIX",
            "Source HARUS dari upstream resmi",
            "CI (GitHub Actions) akan reject PR yang gagal lint",
            f"Commit message: {BCYN}pkg: add <nama>{R}  atau  {BCYN}fix: ...{R}",
        ])
        lines += [""]
        lines += callout("TIP", "Bisa generate otomatis dengan: ./termux-build init <url-repo>", "tip")
    lines.append("")
    return lines


def content_buildsh(L):
    en = L == "en"
    if en:
        lines  = section_header("GUIDE TO WRITING build.sh", tag("%"))
        lines += subsection("Required Fields")
        fields_req = [
            ("TERMUX_PKG_HOMEPAGE",    "Homepage URL / repo of the tool"),
            ("TERMUX_PKG_DESCRIPTION", "Short description (cannot be empty)"),
            ("TERMUX_PKG_LICENSE",     "License (MIT, GPL-3.0, Apache-2.0, etc)"),
            ("TERMUX_PKG_MAINTAINER",  "@your-github-username"),
            ("TERMUX_PKG_VERSION",     "Version, must start with a digit"),
            ("TERMUX_PKG_SRCURL",      "Download URL for source .tar.gz"),
            ("TERMUX_PKG_SHA256",      "SHA256 checksum of the source file"),
        ]
        for key, desc in fields_req:
            lines.append(f"  {BCYN}{B}{key:<30}{R}  {desc}")
        lines += subsection("Optional Fields")
        fields_opt = [
            ("TERMUX_PKG_DEPENDS",        "pkg dependencies (python, curl, etc)"),
            ("TERMUX_PKG_BUILD_IN_SRC",   "true = build inside src directory"),
            ("termux_step_make_install()", "Custom install function"),
        ]
        for key, desc in fields_opt:
            lines.append(f"  {DIM}{key:<30}{R}  {desc}")
        lines += subsection("Valid Version Formats")
        lines += [
            f"  {BGRN}OK{R}  1.0.0     {BGRN}OK{R}  2.3.4     {BGRN}OK{R}  0.1-alpha     {BGRN}OK{R}  3.1.4-rc2",
            f"  {BRED}NO{R}  v1.2.3    {DIM}(no 'v' prefix){R}     {BRED}NO{R}  latest     {BRED}NO{R}  T.G.D-1.0",
            "",
        ]
        lines += subsection("Example build.sh for a Python Script")
    else:
        lines  = section_header("PANDUAN MENULIS build.sh", tag("%"))
        lines += subsection("Field Wajib")
        fields_req = [
            ("TERMUX_PKG_HOMEPAGE",    "URL homepage / repo tool"),
            ("TERMUX_PKG_DESCRIPTION", "Deskripsi singkat (tidak boleh kosong)"),
            ("TERMUX_PKG_LICENSE",     "Lisensi (MIT, GPL-3.0, Apache-2.0, dll)"),
            ("TERMUX_PKG_MAINTAINER",  "@github-username kamu"),
            ("TERMUX_PKG_VERSION",     "Versi, harus mulai dengan angka"),
            ("TERMUX_PKG_SRCURL",      "URL download source .tar.gz"),
            ("TERMUX_PKG_SHA256",      "SHA256 checksum file source"),
        ]
        for key, desc in fields_req:
            lines.append(f"  {BCYN}{B}{key:<30}{R}  {desc}")
        lines += subsection("Field Opsional")
        fields_opt = [
            ("TERMUX_PKG_DEPENDS",        "Dependency pkg (python, curl, dll)"),
            ("TERMUX_PKG_BUILD_IN_SRC",   "true = build langsung di src dir"),
            ("termux_step_make_install()", "Custom install function"),
        ]
        for key, desc in fields_opt:
            lines.append(f"  {DIM}{key:<30}{R}  {desc}")
        lines += subsection("Format Versi yang Valid")
        lines += [
            f"  {BGRN}OK{R}  1.0.0     {BGRN}OK{R}  2.3.4     {BGRN}OK{R}  0.1-alpha     {BGRN}OK{R}  3.1.4-rc2",
            f"  {BRED}NO{R}  v1.2.3    {DIM}(tanpa 'v'){R}     {BRED}NO{R}  latest     {BRED}NO{R}  T.G.D-1.0",
            "",
        ]
        lines += subsection("Contoh build.sh untuk Python Script")

    lines += code_block(
        "TERMUX_PKG_HOMEPAGE=https://github.com/user/tool",
        'TERMUX_PKG_DESCRIPTION="Tool description"',
        'TERMUX_PKG_LICENSE="MIT"',
        'TERMUX_PKG_MAINTAINER="@username"',
        "TERMUX_PKG_VERSION=1.0.0",
        "TERMUX_PKG_SRCURL=https://github.com/user/tool/archive/v1.0.0.tar.gz",
        "TERMUX_PKG_SHA256=abc123...",
        'TERMUX_PKG_DEPENDS="python, python-pip"',
        "TERMUX_PKG_BUILD_IN_SRC=true",
        "",
        "termux_step_make_install() {",
        "    pip install -r requirements.txt \\",
        "        --break-system-packages || true",
        '    mkdir -p "$TERMUX_PREFIX/lib/tool"',
        '    cp -r . "$TERMUX_PREFIX/lib/tool/"',
        "    cat > \"$TERMUX_PREFIX/bin/tool\" <<'EOF'",
        "#!/usr/bin/env bash",
        'exec python3 "$TERMUX_PREFIX/lib/tool/main.py" "$@"',
        "EOF",
        '    chmod 0755 "$TERMUX_PREFIX/bin/tool"',
        "}",
        title="build.sh",
    )
    lines.append("")
    return lines


def content_faq(L):
    en = L == "en"
    if en:
        lines = section_header("FAQ -- FREQUENTLY ASKED QUESTIONS", tag("?"))
        qa = [
            ("Is TAS a replacement for pkg/apt?",
             "No. TAS is a source-based app store, not a replacement for pkg. "
             "pkg is still used to install dependencies."),
            ("Is this an official Termux project?",
             "No. TAS is an independent project, not affiliated with official Termux maintainers."),
            ("Why are some packages marked UNSUPPORTED?",
             "Because the package depends on libraries not available in Termux "
             "(e.g. gtk, zenity/X11, systemd)."),
            ("Does it work offline?",
             "The TUI works offline. Installing packages requires internet to download source code."),
            ("Where are packages stored?",
             "$PREFIX/lib/.tas/packages/ (after install via tasctl) "
             "or termux-app-store/packages/ if running manually."),
            ("Is root required?",
             "No. TAS runs entirely in Termux user space."),
            ("Why is installation slow?",
             "Possible reasons: slow network, large source, or a compilation step. "
             "Check the log panel for progress."),
            ("Why is Python source hidden in binary releases?",
             "Binary releases speed up startup and prevent accidental edits. "
             "The project remains open-source on GitHub."),
            ("Can I move the termux-app-store folder?",
             "Yes. TAS has a self-healing path resolver -- auto-detects its location "
             "even after a move or rename."),
            ("Where do I report bugs?",
             f"GitHub Issues: {BCYN}github.com/djunekz/termux-app-store/issues{R}"),
        ]
    else:
        lines = section_header("FAQ -- PERTANYAAN UMUM", tag("?"))
        qa = [
            ("Apakah TAS pengganti pkg/apt?",
             "Tidak. TAS adalah source-based app store, bukan pengganti pkg. "
             "pkg tetap dipakai untuk install dependencies."),
            ("Apakah ini proyek resmi Termux?",
             "Tidak. TAS adalah proyek independen, tidak berafiliasi dengan maintainer Termux resmi."),
            ("Kenapa beberapa package ditandai UNSUPPORTED?",
             "Karena package tersebut bergantung pada library yang tidak ada di Termux "
             "(misal: gtk, zenity/X11, systemd)."),
            ("Apakah bisa jalan offline?",
             "TUI bisa offline. Install package butuh internet untuk download source code."),
            ("Di mana package disimpan?",
             "$PREFIX/lib/.tas/packages/ (setelah install via tasctl) "
             "atau termux-app-store/packages/ jika manual."),
            ("Apakah butuh root?",
             "Tidak. TAS berjalan sepenuhnya di user space Termux."),
            ("Kok install lambat?",
             "Kemungkinan: jaringan lambat, source besar, atau ada tahap kompilasi. "
             "Cek log panel untuk progress."),
            ("Kenapa Python source disembunyikan di binary?",
             "Binary release dibuat agar lebih cepat startup, mencegah modifikasi tidak sengaja. "
             "Proyek tetap open-source di GitHub."),
            ("Bisa pindah folder termux-app-store?",
             "Bisa. TAS punya self-healing path resolver -- otomatis detect lokasinya "
             "walau folder dipindah atau rename."),
            ("Dimana laporkan bug?",
             f"GitHub Issues: {BCYN}github.com/djunekz/termux-app-store/issues{R}"),
        ]
    for i, (q, a) in enumerate(qa, 1):
        lines.append(f"  {BCYN}{B}Q{i}.{R}  {B}{q}{R}")
        lines += wrap_plain(a, indent=6)
        lines.append("")
    return lines


def content_troubleshoot(L):
    en = L == "en"
    if en:
        lines  = section_header("TROUBLESHOOTING", tag("!"))
        issues = [
            ("command not found: termux-app-store",
             "Restart Termux or run hash -r",
             ["hash -r", "termux-app-store"]),
            ("packages/ not found",
             "Ensure folder structure: termux-app-store/packages/<name>/build.sh",
             []),
            ("ModuleNotFoundError: textual",
             "Install textual manually",
             ["pkg install python -y", "pip install textual"]),
            ("Permission denied",
             "Make the binary executable",
             ["chmod +x $PREFIX/bin/termux-app-store"]),
            ("Unsupported architecture",
             "Supported: aarch64, armv7l, x86_64 -- check with uname -m",
             ["uname -m"]),
            ("Build failed",
             "Scroll the log panel to find the cause",
             ["./termux-build doctor", "./termux-build lint <pkg>"]),
            ("Complete failure -- clean reinstall",
             "Clean reinstall from scratch",
             ["rm -f $PREFIX/bin/termux-app-store",
              "rm -rf $PREFIX/lib/.tas",
              "pip install termux-app-store"]),
        ]
    else:
        lines  = section_header("TROUBLESHOOTING", tag("!"))
        issues = [
            ("command not found: termux-app-store",
             "Restart Termux atau jalankan hash -r",
             ["hash -r", "termux-app-store"]),
            ("packages/ not found",
             "Pastikan struktur folder ada: termux-app-store/packages/<nama>/build.sh",
             []),
            ("ModuleNotFoundError: textual",
             "Install textual secara manual",
             ["pkg install python -y", "pip install textual"]),
            ("Permission denied",
             "Pastikan binary executable",
             ["chmod +x $PREFIX/bin/termux-app-store"]),
            ("Unsupported architecture",
             "Support: aarch64, armv7l, x86_64 -- cek dengan uname -m",
             ["uname -m"]),
            ("Build failed",
             "Scroll log panel, cari penyebabnya",
             ["./termux-build doctor", "./termux-build lint <pkg>"]),
            ("Gagal total -- clean install",
             "Clean reinstall dari awal",
             ["rm -f $PREFIX/bin/termux-app-store",
              "rm -rf $PREFIX/lib/.tas",
              "pip install termux-app-store"]),
        ]
    for err_title, desc, cmds in issues:
        lines.append(f"  {BG_BRED}{BWHT} {err_title} {R}")
        lines += wrap_plain(desc, indent=4)
        lines.append("")
        if cmds:
            lines += code_block(*cmds, title="terminal")
            lines.append("")
        lines.append(f"  {DIM}{'─' * (W() - 4)}{R}")
        lines.append("")
    return lines


def content_contributing(L):
    en = L == "en"
    if en:
        lines  = section_header("CONTRIBUTING", tag("<3"))
        lines += subsection("Accepted Contributions")
        lines += bullet([
            "Add new packages (packages/<name>/build.sh)",
            "Fix existing build.sh files",
            "Fix CI / validation logic",
            "Improve CLI tools (termux-build, tasctl)",
            "Documentation & guides",
            "Bug reports & fixes",
            "Feature proposals",
        ])
        lines += subsection("Contribution Principles")
        lines += bullet([
            f"{BCYN}Automation-first{R}  -- if it can be validated, it must be",
            f"{BCYN}Reproducibility{R}   -- builds must be deterministic",
            f"{BCYN}Transparency{R}      -- no hidden logic",
            f"{BCYN}Community-first{R}   -- breaking changes require discussion",
        ])
        lines += subsection("Commit Message Convention")
        conventions = [
            ("pkg:",      "new or updated package"),
            ("fix:",      "bug fix"),
            ("ci:",       "CI / workflow changes"),
            ("docs:",     "documentation"),
            ("refactor:", "internal changes"),
            ("chore:",    "maintenance"),
        ]
        for prefix, desc in conventions:
            lines.append(f"  {BCYN}{B}{prefix:<12}{R}  {desc}")
        lines += [""]
        lines += code_block(
            'git commit -m "pkg: add ripgrep"',
            'git commit -m "fix: validate TERMUX_PKG_VERSION"',
            title="terminal",
        )
        lines += subsection("What is NOT Allowed")
        lines += bullet([
            f"{BRED}Do not{R} submit malicious code / malware",
            f"{BRED}Do not{R} submit binaries from local builds",
            f"{BRED}Do not{R} hardcode paths outside $PREFIX",
            f"{BRED}Do not{R} make breaking changes without discussion",
        ])
        lines += ["",
                  f"  {DIM}All PRs are automatically checked via GitHub Actions CI.{R}",
                  f"  {DIM}PRs cannot be merged if CI fails.{R}", ""]
    else:
        lines  = section_header("CARA KONTRIBUSI", tag("<3"))
        lines += subsection("Kontribusi yang Diterima")
        lines += bullet([
            "Tambah package baru (packages/<nama>/build.sh)",
            "Perbaiki build.sh yang ada",
            "Perbaiki CI / validation logic",
            "Improvement CLI (termux-build, tasctl)",
            "Dokumentasi & panduan",
            "Bug report & fixes",
            "Feature proposal",
        ])
        lines += subsection("Prinsip Kontribusi")
        lines += bullet([
            f"{BCYN}Automation-first{R}  -- kalau bisa divalidasi, harus divalidasi",
            f"{BCYN}Reproducibility{R}   -- build harus deterministic",
            f"{BCYN}Transparency{R}      -- tidak ada hidden logic",
            f"{BCYN}Community-first{R}   -- breaking change harus diskusi dulu",
        ])
        lines += subsection("Commit Message Convention")
        conventions = [
            ("pkg:",      "package baru atau update"),
            ("fix:",      "bug fix"),
            ("ci:",       "CI / workflow changes"),
            ("docs:",     "dokumentasi"),
            ("refactor:", "internal changes"),
            ("chore:",    "maintenance"),
        ]
        for prefix, desc in conventions:
            lines.append(f"  {BCYN}{B}{prefix:<12}{R}  {desc}")
        lines += [""]
        lines += code_block(
            'git commit -m "pkg: add ripgrep"',
            'git commit -m "fix: validate TERMUX_PKG_VERSION"',
            title="terminal",
        )
        lines += subsection("Yang TIDAK Boleh")
        lines += bullet([
            f"{BRED}Jangan{R} submit kode berbahaya / malware",
            f"{BRED}Jangan{R} submit binary dari local build",
            f"{BRED}Jangan{R} hardcode path di luar $PREFIX",
            f"{BRED}Jangan{R} breaking change tanpa diskusi",
        ])
        lines += ["",
                  f"  {DIM}Semua PR dicek otomatis via GitHub Actions CI.{R}",
                  f"  {DIM}PR tidak bisa merge kalau CI gagal.{R}", ""]
    return lines



def get_menu(L):
    en = L == "en"
    return [
        ("1", "About Termux App Store"           if en else "Tentang Termux App Store",    content_about),
        ("2", "How to Install"                   if en else "Cara Install",                 content_install),
        ("3", "How to Uninstall"                 if en else "Cara Uninstall",               content_uninstall),
        ("4", "Using termux-app-store"           if en else "Penggunaan termux-app-store",  content_usage),
        ("5", "Using tasctl"                     if en else "Penggunaan tasctl",            content_tasctl),
        ("6", "Using termux-build"               if en else "Penggunaan termux-build",      content_termux_build),
        ("7", "Using build-package.sh"           if en else "Penggunaan build-package.sh",  content_build_package),
        ("8", "How to Upload a Tool"             if en else "Cara Upload Tool ke TAS",      content_upload),
        ("9", "Guide to Writing build.sh"        if en else "Panduan Menulis build.sh",     content_buildsh),
        ("f", "FAQ"                              if en else "FAQ",                          content_faq),
        ("t", "Troubleshooting"                  if en else "Troubleshooting",              content_troubleshoot),
        ("c", "Contributing"                     if en else "Cara Kontribusi",              content_contributing),
        ("l", f"{DIM}Switch language / Ganti bahasa{R}",                                    None),
        ("q", "Exit"                             if en else "Keluar",                       "quit"),
    ]



def banner(lang_label=""):
    cls()
    w = W()
    print(thick_rule(BCYN, w))
    title_text = f"{B}{BWHT}TERMUX APP STORE{R}  {DIM}-- Guidebook{R}"
    print(vcenter(title_text, w))
    sub_text   = f"{DIM}github.com/djunekz/termux-app-store{R}"
    print(vcenter(sub_text, w))
    if lang_label:
        lang_text = f"{BG_BBLK}{DIM}  {lang_label}  {R}"
        print(vcenter(lang_text, w))
    print(thick_rule(BCYN, w))
    print()


def select_language():
    while True:
        banner()
        w = W()
        print(vcenter(f"{B}Select language / Pilih bahasa{R}", w))
        print()
        print(vcenter(f"  {DIM}[{R}{BCYN}{B}1{R}{DIM}]{R}  {B}English{R}          {DIM}[{R}{BCYN}{B}2{R}{DIM}]{R}  {B}Indonesia{R}  ", w))
        print()
        print(vcenter(f"{DIM}[{R}{BRED}{B}q{R}{DIM}]{R}  Exit / Keluar", w))
        print()
        print(thick_rule(DIM, w))
        print(f"  {DIM}Choice:{R} ", end="", flush=True)
        try:
            ch = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            ch = "q"
        if ch == "1": return "en"
        if ch == "2": return "id"
        if ch == "q":
            cls()
            print(f"\n  {BGRN}Goodbye / Sampai jumpa!{R}\n")
            sys.exit(0)


def main_menu(lang):
    while True:
        lang_label = "English" if lang == "en" else "Indonesia"
        menu = get_menu(lang)
        topic  = "Choose a topic:"      if lang == "en" else "Pilih topik:"
        prompt = "Type key then Enter"  if lang == "en" else "Ketik tombol lalu Enter"
        bye    = (f"\n  {BGRN}{B}Thanks for using Termux App Store!{R}\n"
                  if lang == "en" else
                  f"\n  {BGRN}{B}Terima kasih telah menggunakan Termux App Store!{R}\n")
        unknown = "Unknown choice" if lang == "en" else "Pilihan tidak dikenali"

        banner(lang_label)
        print(f"  {B}{topic}{R}")
        print()

        w = W()
        main_items = [m for m in menu if m[0] not in ("l", "q")]
        special    = [m for m in menu if m[0] in ("l", "q")]

        col_w = (w - 4) // 2
        mid   = (len(main_items) + 1) // 2
        left  = main_items[:mid]
        right = main_items[mid:]

        for i in range(max(len(left), len(right))):
            left_str  = ""
            right_str = ""
            if i < len(left):
                k, lbl, _ = left[i]
                left_str = f"  {DIM}[{R}{BCYN}{B}{k}{R}{DIM}]{R}  {lbl}"
            if i < len(right):
                k, lbl, _ = right[i]
                right_str = f"  {DIM}[{R}{BCYN}{B}{k}{R}{DIM}]{R}  {lbl}"
            lv  = vlen(left_str)
            pad = max(0, col_w - lv)
            print(f"{left_str}{' ' * pad}{right_str}")

        print()
        for k, lbl, fn in special:
            if k == "q":
                print(f"  {DIM}[{R}{BRED}{B}{k}{R}{DIM}]{R}  {lbl}")
            else:
                print(f"  {DIM}[{R}{BYLW}{B}{k}{R}{DIM}]{R}  {lbl}")

        print()
        print(thick_rule(DIM, w))
        print(f"  {DIM}{prompt}:{R} ", end="", flush=True)
        try:
            choice = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            choice = "q"

        matched = False
        for key, _, fn in menu:
            if choice == key:
                matched = True
                if fn == "quit":
                    cls()
                    print(bye)
                    print(f"  {DIM}github.com/djunekz/termux-app-store{R}\n")
                    sys.exit(0)
                elif fn is None:
                    lang = "id" if lang == "en" else "en"
                else:
                    pager(fn(lang), lang)
                break

        if not matched:
            banner(lang_label)
            print(f"\n  {BYLW}[?]{R} {unknown}: {B}'{choice}'{R}\n")
            pause(lang)


if __name__ == "__main__":
    try:
        lang = select_language()
        main_menu(lang)
    except KeyboardInterrupt:
        cls()
        print(f"\n  {DIM}Bye.{R}\n")
        sys.exit(0)
