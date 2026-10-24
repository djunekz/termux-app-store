#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import textwrap

R = "\033[0m"
B = "\033[1m"
DIM = "\033[2m"
IT = "\033[3m"
UL = "\033[4m"

BLK = "\033[30m"
RED = "\033[31m"
GRN = "\033[32m"
YLW = "\033[33m"
BLU = "\033[34m"
MAG = "\033[35m"
CYN = "\033[36m"
WHT = "\033[37m"

BRED = "\033[91m"
BGRN = "\033[92m"
BYLW = "\033[93m"
BBLU = "\033[94m"
BMAG = "\033[95m"
BCYN = "\033[96m"
BWHT = "\033[97m"

BG_BLK = "\033[40m"
BG_RED = "\033[41m"
BG_GRN = "\033[42m"
BG_YLW = "\033[43m"
BG_BLU = "\033[44m"
BG_MAG = "\033[45m"
BG_CYN = "\033[46m"
BG_WHT = "\033[47m"

BG_BBLK = "\033[100m"
BG_BRED = "\033[101m"
BG_BGRN = "\033[102m"
BG_BYLW = "\033[103m"
BG_BBLU = "\033[104m"
BG_BMAG = "\033[105m"
BG_BCYN = "\033[106m"
BG_BWHT = "\033[107m"

REPO_URL = "https://github.com/djunekz/termux-app-store"
KEY_FPR = "D39134A177717A5BEBEEAE7105D70CDBB6D80295"
TASCTL_URL = "https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl"
REPO_INSTALL = "https://djunekz.github.io/termux-app-store/install-repo.py"


def TW():
    return shutil.get_terminal_size((80, 24)).columns


def TH():
    return shutil.get_terminal_size((80, 24)).lines


def W():
    return min(TW(), 78)


def cls():
    if os.name == "nt":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run(["clear"])


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
    if width is None:
        width = W()
    pad = max(0, (width - vlen(text)) // 2)
    return " " * pad + text


def vright(text, width=None):
    if width is None:
        width = W()
    pad = max(0, width - vlen(text))
    return " " * pad + text


def wrap_plain(text, indent=2, width=None):
    if width is None:
        width = W() - indent - 2
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
    try:
        input()
    except (EOFError, KeyboardInterrupt):
        pass


def pager(lines, lang="id"):
    back = "back" if lang == "en" else "kembali"
    cont = "next" if lang == "en" else "lanjut"
    msg = f"Enter = {cont}   q = {back}"
    chunk = max(TH() - 5, 8)
    i = 0
    while i < len(lines):
        cls()
        for ln in lines[i : i + chunk]:
            print(ln)
        i += chunk
        if i < len(lines):
            print(f"\n  {DIM}{msg}{R}", end="", flush=True)
            try:
                ch = input()
            except (EOFError, KeyboardInterrupt):
                break
            if ch.strip().lower() == "q":
                break
        else:
            pause(lang)


def hline(char="─", color=DIM, width=None):
    if width is None:
        width = W()
    return f"{color}{char * width}{R}"


def thick_rule(color=BCYN, width=None):
    if width is None:
        width = W()
    return f"{color}{'━' * width}{R}"


def double_rule(color=DIM, width=None):
    if width is None:
        width = W()
    return f"{color}{'═' * width}{R}"


def section_header(title, tag_str="", color=BCYN, width=None):
    if width is None:
        width = W()
    if tag_str:
        plain_tag = strip_ansi(tag_str)
        plain_inner = f"  {plain_tag}  {title}  "
        inner = f"  {tag_str}  {title}  "
    else:
        plain_inner = f"  {title}  "
        inner = f"  {B}{title}{R}  "
    pad = max(0, width - len(plain_inner))
    bar_top = f"{color}{'▄' * width}{R}"
    bar_label = f"{BG_BBLU}{BWHT}{B}{inner}{R}{BG_BBLU}{' ' * pad}{R}"
    bar_bottom = f"{color}{'▀' * width}{R}"
    return ["", bar_top, bar_label, bar_bottom, ""]


def subsection(title, color=BCYN):
    marker = f"{color}▌{R}"
    return ["", f"{marker} {B}{BWHT}{title}{R}", f"  {DIM}{'─' * (W() - 2)}{R}", ""]


def code_block(*cmds, title=""):
    w = W() - 6

    prefix_l = f"  {DIM}│{R} "
    prefix_r = f" {DIM}│{R}"
    dash_w = w + 2

    lines = []

    if title:
        title_str = f" {title} "
        fill_count = max(0, dash_w - len(title_str))
        top = f"  {DIM}┌{title_str}{'─' * fill_count}┐{R}"
    else:
        top = f"  {DIM}┌{'─' * dash_w}┐{R}"

    lines.append(top)

    for cmd in cmds:
        if cmd == "":
            lines.append(f"{prefix_l}{' ' * w}{prefix_r}")
        elif cmd.startswith("#"):
            pad = max(0, w - len(cmd))
            content = f"{DIM}{IT}{cmd}{R}{' ' * pad}"
            if len(cmd) > w:
                lines.append(f"{prefix_l}{content}")
            else:
                lines.append(f"{prefix_l}{content}{prefix_r}")
        else:
            pad = w - 2 - len(cmd)
            content = f"{BYLW}$ {R}{BCYN}{cmd}{R}{' ' * max(0, pad)}"
            if pad < 0:
                # long command: keep it on one line so it can be copied intact
                lines.append(f"{prefix_l}{content}")
            else:
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
        "info": (BCYN, "INFO", "╭", "│", "╰", "╮", "╯"),
        "note": (BYLW, "NOTE", "╭", "│", "╰", "╮", "╯"),
        "warning": (BRED, "WARNING", "╭", "│", "╰", "╮", "╯"),
        "tip": (BGRN, "TIP", "╭", "│", "╰", "╮", "╯"),
        "success": (BGRN, "OK", "╭", "│", "╰", "╮", "╯"),
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
        lines = section_header("ABOUT  TERMUX APP STORE", tag("TAS"))
        lines += subsection("What is Termux App Store?")
        lines += [
            f"  Termux App Store is a {BCYN}{B}TUI (Terminal User Interface){R} and CLI",
            "  package manager built natively for Termux.",
            f"  Written in Python ({BCYN}Textual{R}) -- browse, install, and manage",
            "  tools directly on Android. No account. No telemetry. No root.",
            "",
            f"  {DIM}Fetching the package index and downloading packages needs{R}",
            f"  {DIM}an internet connection.{R}",
            "",
        ]
        lines += subsection("Philosophy")
        lines += [
            f'  {IT}{DIM}"Local first. Control over convenience. Transparency over magic."{R}',
            "",
        ]
        lines += bullet(
            [
                f"{B}Local-first{R}        -- runs on your device, no account needed",
                f"{B}Checksum-verified{R}  -- every .deb must match a SHA256 or it is refused",
                f"{B}Source fallback{R}    -- builds from build.sh when no verified binary exists",
                f"{B}Termux-native{R}      -- built for the Termux / Android ecosystem",
            ]
        )
        lines += subsection("Who built it?")
        lines += [
            f"  Created and maintained by {BGRN}{B}Djunekz{R} -- Independent Developer.",
            "  This is a community project, not an official Termux product.",
            "",
            kv_row("GitHub   :", "https://github.com/djunekz"),
            kv_row("Repo     :", REPO_URL),
            kv_row("Issues   :", REPO_URL + "/issues"),
            kv_row("Q&A      :", REPO_URL + "/discussions"),
            kv_row("Email    :", "gab288.gab288@passinbox.com"),
            kv_row("License  :", f"{BGRN}MIT License{R}"),
            "",
        ]
        lines += subsection("History & Timeline")
        timeline = [
            ("v0.0.1", "Jan 2026", "Internal prototype, local-only"),
            ("v0.1.0", "Feb 2026", "First TUI with Textual, package browser"),
            ("v0.1.2", "Feb 2026", "tasctl, lint and check-pr"),
            ("v0.1.4", "Feb 2026", "termux-build create, CLI upgrade, new UI"),
            ("v0.1.6", "Feb 2026", "index.json, update/upgrade, CI workflows"),
            ("v0.1.7", "Mar 2026", "15+ new packages, uninstall button in TUI"),
            ("v0.2.3", "Apr 2026", "pip install support, source mode resolver"),
            ("v0.2.4", "Apr 2026", "termux-build init (auto create & build)"),
            ("v0.2.6", "Apr 2026", "Update termux-app-store TUI to new version Textual"),
            ("v0.3.0", "May 2026", "Dozens of new packages added to the store"),
            ("v0.4.0", "May 2026", "Fast install (.deb from mirrors), search, multi-install"),
            ("v0.4.5", "Jul 2026", "Security hardening: SHA256 checks, name validation"),
            ("v0.8.5", "Oct 2026", "Shared store_common module, checksum-gated cache"),
            ("v0.9.1", "Oct 2026", "Signed apt repository (signed-by), key pinning"),
        ]
        for ver, date, desc in timeline:
            lines.append(f"  {BCYN}{B}{ver:<8}{R}  {DIM}{date}{R}  {desc}")
        lines += [""]
        lines += subsection("Architecture Overview")
        arch = [
            ("User Interface", "Textual TUI + CLI"),
            ("Application Core", "store_common: index, mirrors, checks"),
            ("Fast Install", "mirror pool, SHA256, .deb cache"),
            ("Source Fallback", "build-package.sh + build.sh"),
            ("Termux Env", "dpkg / pkg / apt / shell"),
        ]
        for i, (layer, detail) in enumerate(arch):
            connector = f"  {DIM}│{R}" if i < len(arch) - 1 else ""
            lines.append(f"  {BCYN}▣{R}  {B}{layer:<18}{R}  {DIM}{detail}{R}")
            if connector:
                lines.append(connector)
        lines += [""]
        lines += callout("NOTE", "Termux App Store works alongside pkg/apt, it does not replace them.", "note")
    else:
        lines = section_header("TENTANG  TERMUX APP STORE", tag("TAS"))
        lines += subsection("Apa itu Termux App Store?")
        lines += [
            f"  Termux App Store adalah package manager {BCYN}{B}TUI (Terminal User Interface){R}",
            "  dan CLI yang dibangun khusus untuk Termux secara native.",
            f"  Dibuat dengan Python ({BCYN}Textual{R}) -- browse, install, dan",
            "  kelola tools langsung di Android. Tanpa akun. Tanpa telemetri. Tanpa root.",
            "",
            f"  {DIM}Mengambil index package dan mengunduh package membutuhkan{R}",
            f"  {DIM}koneksi internet.{R}",
            "",
        ]
        lines += subsection("Filosofi")
        lines += [
            f'  {IT}{DIM}"Local first. Control over convenience. Transparency over magic."{R}',
            "",
        ]
        lines += bullet(
            [
                f"{B}Local-first{R}        -- jalan di perangkatmu, tanpa akun",
                f"{B}Checksum-verified{R}  -- setiap .deb harus cocok SHA256 atau ditolak",
                f"{B}Source fallback{R}    -- build dari build.sh jika tidak ada binary terverifikasi",
                f"{B}Termux-native{R}      -- dibangun khusus untuk ekosistem Termux / Android",
            ]
        )
        lines += subsection("Siapa yang membuatnya?")
        lines += [
            f"  Dibuat dan dikelola oleh {BGRN}{B}Djunekz{R} -- Independent Developer.",
            "  Ini adalah proyek komunitas, bukan proyek resmi Termux.",
            "",
            kv_row("GitHub   :", "https://github.com/djunekz"),
            kv_row("Repo     :", REPO_URL),
            kv_row("Issues   :", REPO_URL + "/issues"),
            kv_row("Tanya    :", REPO_URL + "/discussions"),
            kv_row("Email    :", "gab288.gab288@passinbox.com"),
            kv_row("Lisensi  :", f"{BGRN}MIT License{R}"),
            "",
        ]
        lines += subsection("Sejarah & Timeline")
        timeline = [
            ("v0.0.1", "Jan 2026", "Prototype internal, local-only"),
            ("v0.1.0", "Feb 2026", "TUI pertama dengan Textual, package browser"),
            ("v0.1.2", "Feb 2026", "tasctl, lint dan check-pr"),
            ("v0.1.4", "Feb 2026", "termux-build create, CLI upgrade, UI baru"),
            ("v0.1.6", "Feb 2026", "index.json, update/upgrade, CI workflows"),
            ("v0.1.7", "Mar 2026", "15+ package baru, uninstall button di TUI"),
            ("v0.2.3", "Apr 2026", "pip install support, source mode resolver"),
            ("v0.2.4", "Apr 2026", "termux-build init (auto create & build)"),
            ("v0.2.6", "Apr 2026", "Update TUI termux-app-store ke Textual versi baru"),
            ("v0.3.0", "Mei 2026", "Puluhan package baru ditambahkan ke store"),
            ("v0.4.0", "Mei 2026", "Fast install (.deb dari mirror), search, multi-install"),
            ("v0.4.5", "Jul 2026", "Penguatan keamanan: cek SHA256, validasi nama"),
            ("v0.8.5", "Okt 2026", "Modul store_common bersama, cache wajib checksum"),
            ("v0.9.1", "Okt 2026", "Repository apt bertanda tangan (signed-by), key pinning"),
        ]
        for ver, date, desc in timeline:
            lines.append(f"  {BCYN}{B}{ver:<8}{R}  {DIM}{date}{R}  {desc}")
        lines += [""]
        lines += subsection("Arsitektur Singkat")
        arch = [
            ("User Interface", "Textual TUI + CLI"),
            ("Application Core", "store_common: index, mirror, pengecekan"),
            ("Fast Install", "pool mirror, SHA256, cache .deb"),
            ("Source Fallback", "build-package.sh + build.sh"),
            ("Termux Env", "dpkg / pkg / apt / shell"),
        ]
        for i, (layer, detail) in enumerate(arch):
            connector = f"  {DIM}│{R}" if i < len(arch) - 1 else ""
            lines.append(f"  {BCYN}▣{R}  {B}{layer:<18}{R}  {DIM}{detail}{R}")
            if connector:
                lines.append(connector)
        lines += [""]
        lines += callout(
            "CATATAN", "Termux App Store berjalan berdampingan dengan pkg/apt, bukan menggantikannya.", "note"
        )
    lines.append("")
    return lines


def content_install(L):
    en = L == "en"
    if en:
        lines = section_header("HOW TO INSTALL", tag("#"))
        lines += subsection("Requirements")
        lines += bullet(
            [
                "Termux (latest version recommended)",
                "Internet connection",
                f"Python 3.9 or newer {DIM}(pkg install python){R}",
                f"Architecture: {BCYN}aarch64{R} (recommended)  /  {BCYN}armv7l{R}  /  {BCYN}x86_64{R}",
            ]
        )
        lines += ["", f"  {DIM}Check your architecture with: uname -m{R}", ""]
        lines += subsection("Choose ONE method")
        lines += [
            f"  {DIM}Use only one method. Mixing them can leave two copies of the{R}",
            f"  {DIM}termux-app-store command on your system.{R}",
            "",
        ]
        lines += subsection(f"{BGRN}Option 1 -- Recommended (pip){R}")
        lines += code_block("pkg install python", "pip install termux-app-store", title="terminal")
        lines += [
            "",
            f'  {DIM}If pip says "externally-managed-environment", add:{R}',
            f"  {DIM}--break-system-packages{R}",
            "",
        ]
        lines += subsection("Option 2 -- tasctl (light download)")
        lines += [
            f"  {DIM}Good for low-memory devices. Also adds the signed apt repository.{R}",
            "",
        ]
        lines += code_block(f"curl -fsSL {TASCTL_URL} | bash -s install", title="terminal")
        lines += [""] + subsection("Option 3 -- install.sh (official release archive)")
        lines += [
            f"  {DIM}Downloads the latest release, verifies its SHA256 and installs it.{R}",
            "",
        ]
        lines += code_block(
            f"git clone --depth 1 --single-branch --branch master {REPO_URL}",
            "cd termux-app-store",
            "bash install.sh",
            title="terminal",
        )
        lines += [""] + subsection("Optional -- Signed apt repository")
        lines += [
            f"  {DIM}Lets you use plain 'pkg install'. Added with a pinned signing key{R}",
            f"  {DIM}(signed-by), never with trusted=yes. tasctl install does this for you.{R}",
            "",
        ]
        lines += code_block(f"curl -fsSL {REPO_INSTALL} | python", title="terminal")
        lines += [""] + subsection("Quick Start")
        lines += code_block(
            "termux-app-store version          # check it works",
            "termux-app-store update           # refresh the package index",
            "termux-app-store search <word>    # find a package",
            "termux-app-store install <name>   # install it",
            "termux-app-store                  # open the interactive TUI",
            title="terminal",
        )
        lines += subsection("File Locations After Install")
        lines += [
            kv_row("Command       :", f"{BCYN}$PREFIX/bin/termux-app-store{R}  {DIM}(also: tas){R}"),
            kv_row("Install folder:", f"{BCYN}$PREFIX/lib/.tas/{R}  {DIM}(tasctl, install.sh){R}"),
            kv_row("Cache         :", f"{BCYN}~/.cache/termux-app-store/{R}"),
            "",
        ]
        lines += subsection("Install Troubleshooting")
        troubles = [
            ("command not found", f"Restart Termux, or run: {BCYN}hash -r{R}"),
            ("Permission denied", f"{BCYN}chmod +x $PREFIX/bin/termux-app-store{R}"),
            ("Arch unsupported", f"Check: {BCYN}uname -m{R}"),
            ("No module textual", f"{BCYN}pip install --upgrade textual{R}"),
        ]
        for err, fix in troubles:
            lines.append(f"  {BYLW}[!]{R} {B}{err:<20}{R}  {fix}")
        lines += ["", f"  {DIM}More fixes: open Troubleshooting from the main menu.{R}", ""]
    else:
        lines = section_header("CARA INSTALL TERMUX APP STORE", tag("#"))
        lines += subsection("Persyaratan")
        lines += bullet(
            [
                "Termux (versi terbaru direkomendasikan)",
                "Koneksi internet",
                f"Python 3.9 atau lebih baru {DIM}(pkg install python){R}",
                f"Arsitektur: {BCYN}aarch64{R} (direkomendasikan)  /  {BCYN}armv7l{R}  /  {BCYN}x86_64{R}",
            ]
        )
        lines += ["", f"  {DIM}Cek arsitektur kamu dengan: uname -m{R}", ""]
        lines += subsection("Pilih SATU metode")
        lines += [
            f"  {DIM}Pakai satu metode saja. Mencampurnya bisa membuat dua salinan{R}",
            f"  {DIM}perintah termux-app-store di perangkatmu.{R}",
            "",
        ]
        lines += subsection(f"{BGRN}Opsi 1 -- Direkomendasikan (pip){R}")
        lines += code_block("pkg install python", "pip install termux-app-store", title="terminal")
        lines += [
            "",
            f'  {DIM}Jika pip menampilkan "externally-managed-environment", tambahkan:{R}',
            f"  {DIM}--break-system-packages{R}",
            "",
        ]
        lines += subsection("Opsi 2 -- tasctl (unduhan ringan)")
        lines += [
            f"  {DIM}Cocok untuk perangkat dengan memori kecil. Sekaligus menambah repository apt.{R}",
            "",
        ]
        lines += code_block(f"curl -fsSL {TASCTL_URL} | bash -s install", title="terminal")
        lines += [""] + subsection("Opsi 3 -- install.sh (arsip rilis resmi)")
        lines += [
            f"  {DIM}Mengunduh rilis terbaru, memverifikasi SHA256, lalu memasangnya.{R}",
            "",
        ]
        lines += code_block(
            f"git clone --depth 1 --single-branch --branch master {REPO_URL}",
            "cd termux-app-store",
            "bash install.sh",
            title="terminal",
        )
        lines += [""] + subsection("Opsional -- Repository apt bertanda tangan")
        lines += [
            f"  {DIM}Memungkinkan 'pkg install' biasa. Ditambahkan dengan signing key yang{R}",
            f"  {DIM}dipin (signed-by), tidak pernah trusted=yes. tasctl install sudah melakukannya.{R}",
            "",
        ]
        lines += code_block(f"curl -fsSL {REPO_INSTALL} | python", title="terminal")
        lines += [""] + subsection("Mulai Cepat")
        lines += code_block(
            "termux-app-store version          # cek apakah berjalan",
            "termux-app-store update           # perbarui index package",
            "termux-app-store search <kata>    # cari package",
            "termux-app-store install <nama>   # install package",
            "termux-app-store                  # buka TUI interaktif",
            title="terminal",
        )
        lines += subsection("Lokasi File Setelah Install")
        lines += [
            kv_row("Perintah      :", f"{BCYN}$PREFIX/bin/termux-app-store{R}  {DIM}(juga: tas){R}"),
            kv_row("Folder install:", f"{BCYN}$PREFIX/lib/.tas/{R}  {DIM}(tasctl, install.sh){R}"),
            kv_row("Cache         :", f"{BCYN}~/.cache/termux-app-store/{R}"),
            "",
        ]
        lines += subsection("Troubleshooting Install")
        troubles = [
            ("command not found", f"Restart Termux atau: {BCYN}hash -r{R}"),
            ("Permission denied", f"{BCYN}chmod +x $PREFIX/bin/termux-app-store{R}"),
            ("Arch unsupported", f"Cek: {BCYN}uname -m{R}"),
            ("No module textual", f"{BCYN}pip install --upgrade textual{R}"),
        ]
        for err, fix in troubles:
            lines.append(f"  {BYLW}[!]{R} {B}{err:<20}{R}  {fix}")
        lines += ["", f"  {DIM}Solusi lain: buka Troubleshooting dari menu utama.{R}", ""]
    return lines


def content_uninstall(L):
    en = L == "en"
    if en:
        lines = section_header("HOW TO UNINSTALL", tag("X"))
        lines += subsection("Step 1 -- Remove packages you installed (optional)")
        lines += code_block(
            "termux-app-store uninstall <package>",
            "termux-app-store uninstall pkg1 pkg2",
            title="terminal",
        )
        lines += [""] + subsection("Step 2 -- Remove the app")
        lines += [f"  {BCYN}Installed with pip:{R}", ""]
        lines += code_block("pip uninstall termux-app-store", title="terminal")
        lines += ["", f"  {BCYN}Installed with tasctl or install.sh:{R}", ""]
        lines += code_block("tasctl uninstall", title="terminal")
        lines += [
            "",
            f"  {DIM}This removes the command, the install folder and the apt repository entry.{R}",
            "",
            f"  {BCYN}Manual removal:{R}",
            "",
        ]
        lines += code_block(
            "rm -f $PREFIX/bin/termux-app-store",
            "rm -f $PREFIX/bin/tasctl",
            "rm -rf $PREFIX/lib/.tas",
            title="terminal",
        )
        lines += [""] + subsection("Step 3 -- Clean up leftovers (optional)")
        lines += code_block(
            "tasctl uninstall-repo           # remove the apt repository and key",
            "rm -rf ~/.cache/termux-app-store   # remove the cache",
            title="terminal",
        )
        lines += [""]
        lines += callout(
            "NOTE",
            "Packages you installed through the store stay installed until you remove them with 'termux-app-store uninstall'. A pip uninstall also leaves the cache and any apt repository entry in place.",
            "note",
        )
    else:
        lines = section_header("CARA UNINSTALL", tag("X"))
        lines += subsection("Langkah 1 -- Hapus package yang kamu install (opsional)")
        lines += code_block(
            "termux-app-store uninstall <package>",
            "termux-app-store uninstall pkg1 pkg2",
            title="terminal",
        )
        lines += [""] + subsection("Langkah 2 -- Hapus aplikasinya")
        lines += [f"  {BCYN}Diinstall dengan pip:{R}", ""]
        lines += code_block("pip uninstall termux-app-store", title="terminal")
        lines += ["", f"  {BCYN}Diinstall dengan tasctl atau install.sh:{R}", ""]
        lines += code_block("tasctl uninstall", title="terminal")
        lines += [
            "",
            f"  {DIM}Ini menghapus perintah, folder instalasi, dan entri repository apt.{R}",
            "",
            f"  {BCYN}Hapus manual:{R}",
            "",
        ]
        lines += code_block(
            "rm -f $PREFIX/bin/termux-app-store",
            "rm -f $PREFIX/bin/tasctl",
            "rm -rf $PREFIX/lib/.tas",
            title="terminal",
        )
        lines += [""] + subsection("Langkah 3 -- Bersihkan sisa (opsional)")
        lines += code_block(
            "tasctl uninstall-repo           # hapus repository apt dan key",
            "rm -rf ~/.cache/termux-app-store   # hapus cache",
            title="terminal",
        )
        lines += [""]
        lines += callout(
            "CATATAN",
            "Package yang kamu install lewat store tetap terpasang sampai kamu menghapusnya dengan 'termux-app-store uninstall'. Uninstall lewat pip juga tidak menghapus cache dan entri repository apt.",
            "note",
        )
    lines.append("")
    return lines


def content_usage(L):
    en = L == "en"
    if en:
        lines = section_header("USING termux-app-store", tag(">"))
        lines += subsection("TUI -- Interactive Interface")
        lines += code_block("termux-app-store", title="terminal")
        lines += ["", f"  {DIM}TUI keys:{R}", ""]
        lines += bullet(
            [
                f"{BCYN}Up / Down{R}   -- navigate package list",
                f"{BCYN}Enter{R}       -- view detail / install",
                f"{BCYN}Ctrl+R{R}      -- refresh packages",
                f"{BCYN}Ctrl+I{R}      -- install selected package",
                f"{BCYN}Ctrl+Q{R}      -- quit",
                "Touchscreen fully supported",
            ]
        )
        lines += [
            "",
            f"  {DIM}In many terminals Ctrl+I is the same key as Tab. If it does not{R}",
            f"  {DIM}install, use Enter or the CLI command instead.{R}",
            "",
        ]
        lines += subsection("CLI -- Command Line")
        lines += code_block(
            "termux-app-store list                  # all packages",
            "termux-app-store search <query>        # search name / description",
            "termux-app-store show <package>        # package details",
            "termux-app-store install <package>     # fast install (.deb)",
            "termux-app-store install pkg1 pkg2     # several at once",
            "termux-app-store fix-install <package> # force source build",
            "termux-app-store uninstall <package>   # remove a package",
            "termux-app-store update                # core + index",
            "termux-app-store upgrade               # upgrade all outdated",
            "termux-app-store upgrade <package>     # upgrade one package",
            "termux-app-store mirrors               # test download mirrors",
            "termux-app-store cache info            # show .deb cache",
            "termux-app-store cache clear           # clear .deb cache",
            "termux-app-store version               # app version",
            "termux-app-store help                  # full help",
            title="terminal",
        )
        lines += subsection("CLI Shortcuts")
        shortcuts = [
            ("-h", "help"),
            ("-v", "version"),
            ("-l / -L", "list packages"),
            ("-s / -f / find", "search packages"),
            ("-i / i <package>", "install package"),
            ("-fi <package>", "fix-install (source build)"),
            ("un / remove", "uninstall"),
            ("-m", "mirrors"),
            ("-c", "cache"),
        ]
        for flag, desc in shortcuts:
            lines.append(f"  {BCYN}{B}{flag:<18}{R}  {desc}")
        lines += subsection("What Happens When You Install")
        lines += numbered(
            [
                "Look for a cached .deb (kept for 7 days)",
                "If none, pick the fastest reachable mirror",
                "Download the .deb for your CPU architecture",
                "Verify its SHA256 -- a mismatch is refused",
                "Install it with dpkg",
                "No verified binary? Fall back to a source build",
            ]
        )
        lines += [""]
        lines += callout(
            "TIP",
            "Update vs upgrade: 'update' refreshes the index, 'upgrade' installs newer versions of packages you already have.",
            "tip",
        )
    else:
        lines = section_header("PENGGUNAAN termux-app-store", tag(">"))
        lines += subsection("TUI -- Interface Interaktif")
        lines += code_block("termux-app-store", title="terminal")
        lines += ["", f"  {DIM}Tombol TUI:{R}", ""]
        lines += bullet(
            [
                f"{BCYN}Atas / Bawah{R}   -- pindah package",
                f"{BCYN}Enter{R}          -- lihat detail / install",
                f"{BCYN}Ctrl+R{R}         -- refresh package",
                f"{BCYN}Ctrl+I{R}         -- install package terpilih",
                f"{BCYN}Ctrl+Q{R}         -- keluar",
                "Touchscreen didukung penuh",
            ]
        )
        lines += [
            "",
            f"  {DIM}Di banyak terminal Ctrl+I sama dengan tombol Tab. Jika tidak{R}",
            f"  {DIM}menginstall, pakai Enter atau perintah CLI.{R}",
            "",
        ]
        lines += subsection("CLI -- Command Line")
        lines += code_block(
            "termux-app-store list                  # semua package",
            "termux-app-store search <kata>         # cari nama / deskripsi",
            "termux-app-store show <package>        # detail package",
            "termux-app-store install <package>     # fast install (.deb)",
            "termux-app-store install pkg1 pkg2     # beberapa sekaligus",
            "termux-app-store fix-install <package> # paksa build source",
            "termux-app-store uninstall <package>   # hapus package",
            "termux-app-store update                # core + index",
            "termux-app-store upgrade               # upgrade semua yang usang",
            "termux-app-store upgrade <package>     # upgrade satu package",
            "termux-app-store mirrors               # tes mirror download",
            "termux-app-store cache info            # info cache .deb",
            "termux-app-store cache clear           # hapus cache .deb",
            "termux-app-store version               # versi aplikasi",
            "termux-app-store help                  # bantuan lengkap",
            title="terminal",
        )
        lines += subsection("Shortcut CLI")
        shortcuts = [
            ("-h", "help"),
            ("-v", "version"),
            ("-l / -L", "list package"),
            ("-s / -f / find", "cari package"),
            ("-i / i <package>", "install package"),
            ("-fi <package>", "fix-install (build source)"),
            ("un / remove", "uninstall"),
            ("-m", "mirrors"),
            ("-c", "cache"),
        ]
        for flag, desc in shortcuts:
            lines.append(f"  {BCYN}{B}{flag:<18}{R}  {desc}")
        lines += subsection("Yang Terjadi Saat Install")
        lines += numbered(
            [
                "Cari .deb di cache (disimpan 7 hari)",
                "Jika tidak ada, pilih mirror tercepat yang bisa dijangkau",
                "Unduh .deb sesuai arsitektur CPU kamu",
                "Verifikasi SHA256 -- jika tidak cocok, ditolak",
                "Install dengan dpkg",
                "Tidak ada binary terverifikasi? Beralih ke build dari source",
            ]
        )
        lines += [""]
        lines += callout(
            "TIP",
            "Update vs upgrade: 'update' memperbarui index, 'upgrade' memasang versi baru dari package yang sudah kamu install.",
            "tip",
        )
    lines.append("")
    return lines


def content_tasctl(L):
    en = L == "en"
    if en:
        lines = section_header("USING tasctl", tag("!"))
        lines += [
            f"  {DIM}tasctl = Termux App Store Controller{R}",
            "  Tool to install, update, and uninstall Termux App Store itself.",
            "  It is not used to install packages.",
            "",
        ]
        lines += subsection("Commands")
        lines += code_block(
            "tasctl install         # Install Termux App Store",
            "tasctl update          # Update to the latest version",
            "tasctl uninstall       # Remove Termux App Store",
            "tasctl install-repo    # Add the signed apt repository only",
            "tasctl uninstall-repo  # Remove the apt repository and key",
            "tasctl doctor          # Diagnose the environment",
            "tasctl self-update     # Update tasctl itself",
            "tasctl help            # Show help",
            title="terminal",
        )
        lines += subsection("tasctl doctor -- Checks")
        lines += bullet(
            [
                "CPU architecture (aarch64 / armv7l / x86_64)",
                "Python & pip installed",
                "Textual (TUI framework) installed",
                "curl available",
                "Install status (pip / source / release)",
                "TERMUX_APP_STORE_HOME in the launcher",
            ]
        )
        lines += subsection("doctor.py -- Deeper Diagnosis")
        lines += [
            f"  {DIM}Run from the project folder for a full report and automatic fixes:{R}",
            "",
        ]
        lines += code_block(
            "python doctor.py             # full diagnosis",
            "python doctor.py --brief     # one line per check",
            "python doctor.py --fix       # also apply automatic fixes",
            "python doctor.py --json      # machine-readable output",
            "python doctor.py --pkg <n>   # check one package's build.sh",
            title="terminal",
        )
        lines += [""]
        lines += callout(
            "TIP",
            "If something feels broken, run 'tasctl doctor' before reporting a bug and include the result in your report.",
            "tip",
        )
    else:
        lines = section_header("PENGGUNAAN tasctl", tag("!"))
        lines += [
            f"  {DIM}tasctl = Termux App Store Controller{R}",
            "  Tool untuk install, update, dan uninstall Termux App Store itu sendiri.",
            "  Bukan untuk meng-install package.",
            "",
        ]
        lines += subsection("Perintah")
        lines += code_block(
            "tasctl install         # Install Termux App Store",
            "tasctl update          # Update ke versi terbaru",
            "tasctl uninstall       # Hapus Termux App Store",
            "tasctl install-repo    # Tambah repository apt bertanda tangan saja",
            "tasctl uninstall-repo  # Hapus repository apt beserta key-nya",
            "tasctl doctor          # Diagnosa environment",
            "tasctl self-update     # Update tasctl itu sendiri",
            "tasctl help            # Tampilkan bantuan",
            title="terminal",
        )
        lines += subsection("tasctl doctor -- Cek Apa Saja?")
        lines += bullet(
            [
                "Arsitektur CPU (aarch64 / armv7l / x86_64)",
                "Python & pip terinstall",
                "Textual (TUI framework) terinstall",
                "curl tersedia",
                "Status instalasi (pip / source / release)",
                "TERMUX_APP_STORE_HOME di launcher",
            ]
        )
        lines += subsection("doctor.py -- Diagnosa Lebih Dalam")
        lines += [
            f"  {DIM}Jalankan dari folder proyek untuk laporan lengkap dan perbaikan otomatis:{R}",
            "",
        ]
        lines += code_block(
            "python doctor.py             # diagnosa lengkap",
            "python doctor.py --brief     # satu baris per pengecekan",
            "python doctor.py --fix       # sekaligus terapkan perbaikan otomatis",
            "python doctor.py --json      # keluaran untuk mesin",
            "python doctor.py --pkg <n>   # cek build.sh satu package",
            title="terminal",
        )
        lines += [""]
        lines += callout(
            "TIP",
            "Jika ada masalah aneh, jalankan 'tasctl doctor' dulu sebelum report bug dan sertakan hasilnya di laporanmu.",
            "tip",
        )
    lines.append("")
    return lines


def content_termux_build(L):
    en = L == "en"
    if en:
        lines = section_header("USING termux-build", tag("@"))
        lines += [
            f"  {DIM}termux-build = validation & review tool for contributors{R}",
            "  NOT auto-upload or auto-publish. Only reads and validates.",
            "  Run it from the project folder (a git clone of the repository).",
            "",
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
            ("create", "Create new package folder with empty build.sh"),
            ("init", f"{BGRN}Auto-detect{R} GitHub repo, generate build.sh"),
            ("lint", "Validate build.sh (fields, format, version)"),
            ("check-pr", "Check Pull Request readiness"),
            ("doctor", "Diagnose build environment"),
            ("suggest", "Get improvement suggestions for a package"),
            ("explain", "Detailed package explanation"),
            ("template", "Generate a new build.sh template"),
            ("guide", "Show contribution guide"),
        ]
        for cmd, desc in cmds:
            lines.append(f"  {BCYN}{B}{cmd:<12}{R}  {desc}")
        lines += subsection("termux-build init -- Most Powerful Feature")
        lines += [
            "  Auto-detect a GitHub repo, generate a complete build.sh,",
            "  and optionally build a .deb package.",
            "",
        ]
        lines += code_block("./termux-build init https://github.com/user/repo", title="terminal")
        lines += ["", f"  {DIM}What it does automatically:{R}", ""]
        lines += bullet(
            [
                "Fetch GitHub metadata (name, description, license, language)",
                "Download source code",
                "Detect build method (python-script / pip / shell / cargo / etc)",
                "Detect main entrypoint file",
                "Detect installer scripts (install_Termux.sh, install.sh, etc)",
                "Scan dependencies (imports, requirements.txt, shell deps)",
                "Compute SHA256 checksum automatically",
                "Generate complete build.sh",
                "Optional: test build & install as .deb",
            ]
        )
        lines += [""]
        lines += callout("NOTE", "termux-build does NOT modify files, auto-build, or upload to GitHub.", "note")
    else:
        lines = section_header("PENGGUNAAN termux-build", tag("@"))
        lines += [
            f"  {DIM}termux-build = tool validasi & review untuk kontributor{R}",
            "  Bukan auto-upload atau auto-publish. Hanya membaca & memvalidasi.",
            "  Jalankan dari folder proyek (hasil git clone repository).",
            "",
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
            ("create", "Buat folder package baru dengan build.sh kosong"),
            ("init", f"{BGRN}Auto-detect{R} repo GitHub, generate build.sh otomatis"),
            ("lint", "Cek validasi build.sh (field, format, versi)"),
            ("check-pr", "Cek kesiapan Pull Request"),
            ("doctor", "Diagnosa environment build"),
            ("suggest", "Saran perbaikan untuk package"),
            ("explain", "Penjelasan detail package"),
            ("template", "Generate template build.sh baru"),
            ("guide", "Tampilkan contribution guide"),
        ]
        for cmd, desc in cmds:
            lines.append(f"  {BCYN}{B}{cmd:<12}{R}  {desc}")
        lines += subsection("termux-build init -- Fitur Paling Powerful")
        lines += [
            "  Auto-detect repo GitHub, generate build.sh lengkap,",
            "  lalu opsional build jadi .deb.",
            "",
        ]
        lines += code_block("./termux-build init https://github.com/user/repo", title="terminal")
        lines += ["", f"  {DIM}Yang dilakukan otomatis:{R}", ""]
        lines += bullet(
            [
                "Fetch metadata GitHub (nama, deskripsi, lisensi, bahasa)",
                "Download source code",
                "Deteksi build method (python-script / pip / shell / cargo / dll)",
                "Deteksi entrypoint utama",
                "Deteksi installer script (install_Termux.sh, install.sh, dll)",
                "Scan dependency (imports, requirements.txt, shell deps)",
                "Hitung SHA256 checksum otomatis",
                "Generate build.sh lengkap",
                "Opsional: langsung test build & install jadi .deb",
            ]
        )
        lines += [""]
        lines += callout(
            "CATATAN", "termux-build TIDAK memodifikasi file, tidak auto-build, tidak upload ke GitHub.", "note"
        )
    lines.append("")
    return lines


def content_build_package(L):
    en = L == "en"
    if en:
        lines = section_header("USING build-package.sh", tag("$"))
        lines += [
            f"  {DIM}build-package.sh = source build engine (the fallback path){R}",
            "  Builds a package from its build.sh into a .deb and installs it.",
            "",
            "  You normally do not run it by hand:",
            f"  {BCYN}termux-app-store fix-install <package>{R} calls it for you.",
            "",
        ]
        lines += subsection("Manual Usage (from a project checkout)")
        lines += code_block(
            "./build-package.sh <package-name>",
            "",
            "# Example:",
            "./build-package.sh tdoc",
            title="terminal",
        )
        lines += subsection("What build-package.sh Does")
        lines += numbered(
            [
                "Validate build.sh (syntax + required fields)",
                "Detect CPU architecture",
                f"Install dependencies via pkg {DIM}(retries up to 5 times){R}",
                f"Download source from {BCYN}TERMUX_PKG_SRCURL{R}",
                "Verify SHA256 checksum",
                "Extract source archive",
                f"Run {BCYN}termux_step_make_install(){R}",
                "Generate .deb metadata",
                "Build the .deb file",
                "Install package with dpkg",
                "Hold the package (apt-mark) so pkg upgrade does not overwrite it",
            ]
        )
        lines += [""]
        lines += callout(
            "NOTE",
            "If a dependency still cannot be installed after the retries, the build stops with a FATAL message instead of failing later with 'command not found'.",
            "note",
        )
        lines += subsection("Output Structure")
        lines += [
            kv_row("build/<package>/", "build working directory"),
            kv_row("output/<pkg>.deb", "generated .deb package file"),
            "",
        ]
    else:
        lines = section_header("PENGGUNAAN build-package.sh", tag("$"))
        lines += [
            f"  {DIM}build-package.sh = engine build dari source (jalur cadangan){R}",
            "  Membangun package dari build.sh menjadi .deb lalu menginstallnya.",
            "",
            "  Biasanya tidak dijalankan manual:",
            f"  {BCYN}termux-app-store fix-install <package>{R} yang memanggilnya.",
            "",
        ]
        lines += subsection("Cara Pakai Manual (dari checkout proyek)")
        lines += code_block(
            "./build-package.sh <package-name>",
            "",
            "# Contoh:",
            "./build-package.sh tdoc",
            title="terminal",
        )
        lines += subsection("Yang Dilakukan build-package.sh")
        lines += numbered(
            [
                "Validasi build.sh (syntax + required fields)",
                "Deteksi arsitektur CPU",
                f"Install dependencies via pkg {DIM}(coba ulang sampai 5 kali){R}",
                f"Download source dari {BCYN}TERMUX_PKG_SRCURL{R}",
                "Verifikasi SHA256 checksum",
                "Extract source archive",
                f"Jalankan {BCYN}termux_step_make_install(){R}",
                "Generate metadata .deb",
                "Build file .deb",
                "Install package dengan dpkg",
                "Hold package (apt-mark) agar tidak ditimpa pkg upgrade",
            ]
        )
        lines += [""]
        lines += callout(
            "CATATAN",
            "Jika dependency tetap gagal di-install setelah dicoba ulang, build berhenti dengan pesan FATAL, bukan gagal belakangan dengan 'command not found'.",
            "note",
        )
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
        lines = section_header("HOW TO UPLOAD A TOOL TO TAS", tag("^"))
        lines += [
            f"  {DIM}Just want a tool added, without writing the recipe yourself?{R}",
            f"  {DIM}Open a 'Package Request' issue on GitHub instead.{R}",
            "",
        ]
        steps_en = [
            (
                "Fork the repository",
                [f"Open: {BCYN}{REPO_URL}{R}", "Click Fork -> Create fork", "Keep the repo name: termux-app-store"],
                [],
            ),
            ("Clone your fork", [], ["git clone --depth 1 --single-branch --branch master https://github.com/USERNAME/termux-app-store", "cd termux-app-store"]),
            ("Create a new branch", [], ["git checkout -b your-tool-name"]),
            (
                "Create package folder",
                [],
                ["mkdir -p packages/your-tool-name", "nano packages/your-tool-name/build.sh"],
            ),
            (
                "Fill in build.sh",
                [],
                [
                    "TERMUX_PKG_HOMEPAGE=https://github.com/user/tool",
                    'TERMUX_PKG_DESCRIPTION="Short tool description"',
                    'TERMUX_PKG_LICENSE="MIT"',
                    'TERMUX_PKG_MAINTAINER="@your-github-username"',
                    "TERMUX_PKG_VERSION=1.0.0",
                    "TERMUX_PKG_SRCURL=https://...",
                    "TERMUX_PKG_SHA256=abc123...",
                ],
            ),
            (
                "Validate before committing",
                [],
                [
                    "./termux-build lint packages/your-tool-name",
                    "./termux-build check-pr your-tool-name",
                    "./termux-build doctor",
                ],
            ),
            (
                "Commit and push",
                [],
                [
                    "git add packages/your-tool-name",
                    'git commit -m "pkg: add your-tool-name"',
                    "git push origin your-tool-name",
                ],
            ),
            (
                "Create a Pull Request",
                [
                    "Open your fork on GitHub",
                    "Click Compare & Pull Request",
                    "Describe: what the tool does, upstream source, how to test",
                    "Submit PR -- CI will validate automatically",
                ],
                [],
            ),
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
        lines += bullet(
            [
                f"{BRED}DO NOT{R} upload locally compiled binaries",
                f"{BRED}DO NOT{R} hardcode paths outside $PREFIX",
                "Source MUST come from official upstream",
                "Package names use '-' and no spaces: my-tool-name",
                "Tools for credential brute-forcing, DDoS, backdoors or tracking\npeople without a stated defensive use are not accepted",
                "CI (GitHub Actions) will reject PRs that fail lint",
                f"Commit message: {BCYN}pkg: add <name>{R}  or  {BCYN}fix: ...{R}",
            ]
        )
        lines += [""]
        lines += callout(
            "TIP",
            "Auto-generate build.sh with: ./termux-build init <repo-url>. Full guide: HOW_TO_UPLOAD.md in the repository.",
            "tip",
        )
    else:
        lines = section_header("CARA UPLOAD TOOL KE TERMUX APP STORE", tag("^"))
        lines += [
            f"  {DIM}Hanya ingin tool ditambahkan, tanpa menulis recipe sendiri?{R}",
            f"  {DIM}Buka issue 'Package Request' di GitHub.{R}",
            "",
        ]
        steps_id = [
            (
                "Fork repository",
                [
                    f"Buka: {BCYN}{REPO_URL}{R}",
                    "Klik tombol Fork -> Create fork",
                    "Pastikan nama repo tetap: termux-app-store",
                ],
                [],
            ),
            ("Clone fork kamu", [], ["git clone --depth 1 --single-branch --branch master https://github.com/USERNAME/termux-app-store", "cd termux-app-store"]),
            ("Buat branch baru", [], ["git checkout -b nama-tool-kamu"]),
            ("Buat folder package", [], ["mkdir -p packages/nama-tool-kamu", "nano packages/nama-tool-kamu/build.sh"]),
            (
                "Isi build.sh",
                [],
                [
                    "TERMUX_PKG_HOMEPAGE=https://github.com/user/tool",
                    'TERMUX_PKG_DESCRIPTION="Deskripsi singkat tool"',
                    'TERMUX_PKG_LICENSE="MIT"',
                    'TERMUX_PKG_MAINTAINER="@github-username-kamu"',
                    "TERMUX_PKG_VERSION=1.0.0",
                    "TERMUX_PKG_SRCURL=https://...",
                    "TERMUX_PKG_SHA256=abc123...",
                ],
            ),
            (
                "Validasi sebelum commit",
                [],
                [
                    "./termux-build lint packages/nama-tool-kamu",
                    "./termux-build check-pr nama-tool-kamu",
                    "./termux-build doctor",
                ],
            ),
            (
                "Commit dan push",
                [],
                [
                    "git add packages/nama-tool-kamu",
                    'git commit -m "pkg: add nama-tool-kamu"',
                    "git push origin nama-tool-kamu",
                ],
            ),
            (
                "Buat Pull Request",
                [
                    "Buka fork kamu di GitHub",
                    "Klik Compare & Pull Request",
                    "Isi deskripsi: apa tool-nya, sumber upstream, cara test",
                    "Submit PR -- CI akan otomatis validasi",
                ],
                [],
            ),
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
        lines += bullet(
            [
                f"{BRED}JANGAN{R} upload binary compiled dari local",
                f"{BRED}JANGAN{R} hardcode path di luar $PREFIX",
                "Source HARUS dari upstream resmi",
                "Nama package pakai '-' tanpa spasi: nama-tool-kamu",
                "Tool untuk brute-force kredensial, DDoS, backdoor, atau melacak\norang tanpa tujuan defensif yang jelas tidak diterima",
                "CI (GitHub Actions) akan reject PR yang gagal lint",
                f"Commit message: {BCYN}pkg: add <nama>{R}  atau  {BCYN}fix: ...{R}",
            ]
        )
        lines += [""]
        lines += callout(
            "TIP",
            "Bisa generate otomatis dengan: ./termux-build init <url-repo>. Panduan lengkap: HOW_TO_UPLOAD.md di repository.",
            "tip",
        )
    lines.append("")
    return lines


def content_buildsh(L):
    en = L == "en"
    if en:
        lines = section_header("GUIDE TO WRITING build.sh", tag("%"))
        lines += subsection("Required Fields")
        fields_req = [
            ("TERMUX_PKG_HOMEPAGE", "Homepage URL / repo of the tool"),
            ("TERMUX_PKG_DESCRIPTION", "Short description (cannot be empty)"),
            ("TERMUX_PKG_LICENSE", "License (MIT, GPL-3.0, Apache-2.0, etc)"),
            ("TERMUX_PKG_MAINTAINER", "@your-github-username"),
            ("TERMUX_PKG_VERSION", "Version, must start with a digit"),
            ("TERMUX_PKG_SRCURL", "Download URL for source .tar.gz"),
            ("TERMUX_PKG_SHA256", "SHA256 checksum of the source file"),
        ]
        for key, desc in fields_req:
            lines.append(f"  {BCYN}{B}{key:<30}{R}  {desc}")
        lines += subsection("Optional Fields")
        fields_opt = [
            ("TERMUX_PKG_DEPENDS", "pkg dependencies (python, curl, etc)"),
            ("TERMUX_PKG_BUILD_IN_SRC", "true = build inside src directory"),
            ("TERMUX_PKG_AUTO_UPDATE", "false = opt out of the automatic version updater"),
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
        lines += callout(
            "NOTE",
            "Packages are checked against their upstream about twice a day, and the version, URL and SHA256 are updated automatically. Keep TERMUX_PKG_VERSION, SRCURL and SHA256 consistent with each other.",
            "note",
        )
        lines += subsection("Example build.sh for a Python Script")
    else:
        lines = section_header("PANDUAN MENULIS build.sh", tag("%"))
        lines += subsection("Field Wajib")
        fields_req = [
            ("TERMUX_PKG_HOMEPAGE", "URL homepage / repo tool"),
            ("TERMUX_PKG_DESCRIPTION", "Deskripsi singkat (tidak boleh kosong)"),
            ("TERMUX_PKG_LICENSE", "Lisensi (MIT, GPL-3.0, Apache-2.0, dll)"),
            ("TERMUX_PKG_MAINTAINER", "@github-username kamu"),
            ("TERMUX_PKG_VERSION", "Versi, harus mulai dengan angka"),
            ("TERMUX_PKG_SRCURL", "URL download source .tar.gz"),
            ("TERMUX_PKG_SHA256", "SHA256 checksum file source"),
        ]
        for key, desc in fields_req:
            lines.append(f"  {BCYN}{B}{key:<30}{R}  {desc}")
        lines += subsection("Field Opsional")
        fields_opt = [
            ("TERMUX_PKG_DEPENDS", "Dependency pkg (python, curl, dll)"),
            ("TERMUX_PKG_BUILD_IN_SRC", "true = build langsung di src dir"),
            ("TERMUX_PKG_AUTO_UPDATE", "false = keluar dari updater versi otomatis"),
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
        lines += callout(
            "CATATAN",
            "Package dicek terhadap upstream-nya sekitar dua kali sehari, lalu versi, URL, dan SHA256 diperbarui otomatis. Jaga agar TERMUX_PKG_VERSION, SRCURL, dan SHA256 selalu konsisten.",
            "note",
        )
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


def content_security(L):
    en = L == "en"
    if en:
        lines = section_header("SECURITY & TRUST", tag("S"))
        lines += subsection("What protects you")
        lines += bullet(
            [
                f"{B}SHA256 on every .deb{R}  -- a mismatch is refused, including cached files",
                f"{B}Recipe checks{R}         -- build.sh is matched against the published index",
                f"{B}Signed apt repository{R} -- verified with signed-by, never trusted=yes",
                f"{B}Official source only{R}  -- the installers refuse unofficial copies",
                f"{B}Review and CI{R}         -- packages are validated before they are published",
            ]
        )
        lines += subsection("What SHA256 does NOT prove")
        lines += wrap_plain(
            "SHA256 detects corrupted or mismatched files. It is an integrity check, "
            "not a publisher signature, and it cannot tell you whether the software "
            "itself is safe. Packages are third-party software, so read a package's "
            "build.sh before building it from source.",
            indent=2,
        )
        lines += [""]
        lines += subsection("APT signing key fingerprint")
        lines += [
            f"  {DIM}The installers accept only a key with exactly this fingerprint:{R}",
            "",
            f"  {BGRN}{B}{KEY_FPR}{R}",
            "",
            f"  {DIM}Compare it with SECURITY.md in the repository. If a key is rejected,{R}",
            f"  {DIM}do not work around it. Report it privately.{R}",
            "",
        ]
        lines += subsection("Good habits")
        lines += bullet(
            [
                "Install only from the official repository or PyPI",
                "Never add the apt repository with [trusted=yes]",
                "Do not bypass checks with the TERMUX_APP_STORE_ALLOW_UNVERIFIED_* variables",
                "Keep the app updated: termux-app-store update",
            ]
        )
        lines += subsection("Privacy")
        lines += wrap_plain(
            "No account, no analytics, no telemetry. The network is used only to fetch "
            "the index, mirrors, checksums, .deb files and package sources, when you "
            "run a command that needs it.",
            indent=2,
        )
        lines += [""]
        lines += callout(
            "WARNING",
            "Report security problems privately, never in a public issue: GitHub Security Advisories or gab288.gab288@passinbox.com.",
            "warning",
        )
    else:
        lines = section_header("KEAMANAN & KEPERCAYAAN", tag("S"))
        lines += subsection("Yang melindungimu")
        lines += bullet(
            [
                f"{B}SHA256 di setiap .deb{R}   -- jika tidak cocok ditolak, termasuk file cache",
                f"{B}Cek recipe{R}             -- build.sh dicocokkan dengan index yang dipublikasikan",
                f"{B}Repository apt bertanda tangan{R} -- diverifikasi dengan signed-by, bukan trusted=yes",
                f"{B}Hanya sumber resmi{R}      -- installer menolak salinan tidak resmi",
                f"{B}Review dan CI{R}           -- package divalidasi sebelum dipublikasikan",
            ]
        )
        lines += subsection("Yang TIDAK dibuktikan oleh SHA256")
        lines += wrap_plain(
            "SHA256 mendeteksi file rusak atau tidak cocok. Ini pengecekan integritas, "
            "bukan tanda tangan penerbit, dan tidak bisa memastikan software-nya aman. "
            "Package adalah software pihak ketiga, jadi baca build.sh sebelum "
            "membangunnya dari source.",
            indent=2,
        )
        lines += [""]
        lines += subsection("Fingerprint signing key APT")
        lines += [
            f"  {DIM}Installer hanya menerima key dengan fingerprint persis ini:{R}",
            "",
            f"  {BGRN}{B}{KEY_FPR}{R}",
            "",
            f"  {DIM}Bandingkan dengan SECURITY.md di repository. Jika key ditolak,{R}",
            f"  {DIM}jangan dilewati. Laporkan secara privat.{R}",
            "",
        ]
        lines += subsection("Kebiasaan baik")
        lines += bullet(
            [
                "Install hanya dari repository resmi atau PyPI",
                "Jangan tambah repository apt dengan [trusted=yes]",
                "Jangan lewati pengecekan dengan variabel TERMUX_APP_STORE_ALLOW_UNVERIFIED_*",
                "Selalu perbarui aplikasi: termux-app-store update",
            ]
        )
        lines += subsection("Privasi")
        lines += wrap_plain(
            "Tanpa akun, tanpa analitik, tanpa telemetri. Jaringan hanya dipakai untuk "
            "mengambil index, mirror, checksum, file .deb dan source package, saat kamu "
            "menjalankan perintah yang membutuhkannya.",
            indent=2,
        )
        lines += [""]
        lines += callout(
            "PERINGATAN",
            "Laporkan masalah keamanan secara privat, jangan lewat issue publik: GitHub Security Advisories atau gab288.gab288@passinbox.com.",
            "warning",
        )
    lines.append("")
    return lines


def content_faq(L):
    en = L == "en"
    if en:
        lines = section_header("FAQ -- FREQUENTLY ASKED QUESTIONS", tag("?"))
        qa = [
            (
                "Is TAS a replacement for pkg/apt?",
                "No. It works alongside pkg. Packages installed through TAS are normal "
                ".deb packages managed by dpkg, and pkg is still used for dependencies.",
            ),
            (
                "Is this an official Termux project?",
                "No. TAS is an independent project, not affiliated with the official Termux maintainers.",
            ),
            (
                "How does installing a package work?",
                "TAS downloads a pre-built .deb from the fastest mirror, verifies its "
                "SHA256 for your architecture, caches it and installs it with dpkg. If "
                "no verified binary exists it builds from source instead.",
            ),
            ("What if a fast install fails?", "Use: termux-app-store fix-install <package> to force a source build."),
            (
                "Does it work offline?",
                "Partly. The interface works with data already on your device, but "
                "fetching the index, downloading packages and building from source need "
                "the internet. A cached .deb may be reused if its checksum can be verified.",
            ),
            (
                "Where are things stored?",
                "Downloaded .deb files and the index are in ~/.cache/termux-app-store/. "
                "The app itself is in $PREFIX/lib/.tas/ (tasctl and install.sh installs).",
            ),
            ("Is root required?", "No. TAS runs entirely in Termux user space."),
            (
                "Which install method should I use?",
                "pip install termux-app-store is the simplest. tasctl suits low-memory "
                "devices or if you also want the apt repository. Use only one method.",
            ),
            (
                "Does SHA256 prove a package is safe?",
                "No. It detects corrupted or mismatched files. It is not a publisher "
                "signature, so read build.sh before building from source.",
            ),
            (
                "Why is installation slow?",
                "Possible reasons: slow network, a large download, or a compilation "
                "step. Check the log panel for progress.",
            ),
            (
                "Is the source code available?",
                "Yes. TAS is open source (MIT) on GitHub. Pre-built .deb files are a "
                "distribution format for packages, not closed-source software.",
            ),
            (
                "Can I move the termux-app-store folder?",
                "Yes. TAS detects its own location and repairs cached paths after a "
                "move or rename. If needed, set TERMUX_APP_STORE_HOME.",
            ),
            (
                "Where do I report bugs or ask for help?",
                f"GitHub Issues: {BCYN}github.com/djunekz/termux-app-store/issues{R}\n"
                f"Questions: open the Q&A category in GitHub Discussions.",
            ),
        ]
    else:
        lines = section_header("FAQ -- PERTANYAAN UMUM", tag("?"))
        qa = [
            (
                "Apakah TAS pengganti pkg/apt?",
                "Tidak. TAS berjalan berdampingan dengan pkg. Package yang diinstall "
                "lewat TAS adalah paket .deb biasa yang dikelola dpkg, dan pkg tetap "
                "dipakai untuk dependency.",
            ),
            (
                "Apakah ini proyek resmi Termux?",
                "Tidak. TAS adalah proyek independen, tidak berafiliasi dengan maintainer Termux resmi.",
            ),
            (
                "Bagaimana cara install package bekerja?",
                "TAS mengunduh .deb siap pakai dari mirror tercepat, memverifikasi "
                "SHA256 untuk arsitekturmu, menyimpannya di cache lalu menginstall "
                "dengan dpkg. Jika tidak ada binary terverifikasi, TAS build dari source.",
            ),
            (
                "Bagaimana jika fast install gagal?",
                "Pakai: termux-app-store fix-install <package> untuk memaksa build source.",
            ),
            (
                "Apakah bisa jalan offline?",
                "Sebagian. Tampilan bisa memakai data yang sudah ada di perangkat, tetapi "
                "mengambil index, mengunduh package, dan build dari source butuh internet. "
                "File .deb di cache bisa dipakai ulang jika checksum-nya bisa diverifikasi.",
            ),
            (
                "Di mana semuanya disimpan?",
                "File .deb dan index ada di ~/.cache/termux-app-store/. Aplikasinya "
                "ada di $PREFIX/lib/.tas/ (instalasi tasctl dan install.sh).",
            ),
            ("Apakah butuh root?", "Tidak. TAS berjalan sepenuhnya di user space Termux."),
            (
                "Metode install mana yang sebaiknya dipakai?",
                "pip install termux-app-store paling sederhana. tasctl cocok untuk "
                "perangkat dengan memori kecil atau jika ingin repository apt juga. "
                "Pakai satu metode saja.",
            ),
            (
                "Apakah SHA256 membuktikan package aman?",
                "Tidak. SHA256 mendeteksi file rusak atau tidak cocok. Ini bukan tanda "
                "tangan penerbit, jadi baca build.sh sebelum build dari source.",
            ),
            (
                "Kok install lambat?",
                "Kemungkinan: jaringan lambat, unduhan besar, atau ada tahap kompilasi. Cek log panel untuk progress.",
            ),
            (
                "Apakah source code tersedia?",
                "Ya. TAS open source (MIT) di GitHub. File .deb siap pakai adalah format "
                "distribusi package, bukan software closed-source.",
            ),
            (
                "Bisa pindah folder termux-app-store?",
                "Bisa. TAS mendeteksi lokasinya sendiri dan memperbaiki path cache setelah "
                "dipindah atau di-rename. Jika perlu, atur TERMUX_APP_STORE_HOME.",
            ),
            (
                "Di mana melapor bug atau minta bantuan?",
                f"GitHub Issues: {BCYN}github.com/djunekz/termux-app-store/issues{R}\n"
                f"Pertanyaan: buka kategori Q&A di GitHub Discussions.",
            ),
        ]
    for i, (q, a) in enumerate(qa, 1):
        lines.append(f"  {BCYN}{B}Q{i}.{R}  {B}{q}{R}")
        lines += wrap_plain(a, indent=6)
        lines.append("")
    return lines


def content_troubleshoot(L):
    en = L == "en"
    if en:
        lines = section_header("TROUBLESHOOTING", tag("!"))
        lines += [
            f"  {DIM}Start with these two commands. They explain most problems:{R}",
            "",
        ]
        lines += code_block("tasctl doctor", "termux-app-store mirrors", title="terminal")
        lines += [""]
        issues = [
            (
                "command not found: termux-app-store",
                "Clear the shell cache. If it still fails, reinstall.",
                ["hash -r", "termux-app-store version"],
            ),
            (
                "Package '<name>' not found",
                "Check the spelling and refresh the index.",
                ["termux-app-store search <name>", "termux-app-store update"],
            ),
            (
                "ModuleNotFoundError: textual",
                "Install or upgrade Textual (8.0.0 or newer, Python 3.9+).",
                ["pkg install python -y", "pip install --upgrade textual"],
            ),
            ("Permission denied", "Make the command executable.", ["chmod +x $PREFIX/bin/termux-app-store"]),
            (
                "Unsupported architecture",
                "Supported: aarch64, armv7l, x86_64. Check yours, and use a source build if no binary exists.",
                ["uname -m", "termux-app-store fix-install <pkg>"],
            ),
            (
                "Fast install failed",
                "Test the mirrors, clear the cache, then retry. Last resort: build from source.",
                ["termux-app-store mirrors", "termux-app-store cache clear", "termux-app-store fix-install <pkg>"],
            ),
            (
                "SHA256 mismatch",
                "Usually a corrupted or stale download. Clear the cache and retry. If it repeats, report it (privately if you suspect tampering).",
                ["termux-app-store cache clear", "termux-app-store update"],
            ),
            (
                "apt: NO_PUBKEY / repository is not signed",
                "Re-add the repository so the signing key is downloaded and checked again.",
                ["tasctl install-repo", "pkg update"],
            ),
            (
                "Could not resolve host / timeouts",
                "Check your connection and try another Termux mirror.",
                ["termux-app-store mirrors", "termux-change-repo"],
            ),
            (
                "Build failed",
                "Scroll the log and read the FIRST error. Then check the recipe.",
                ["python doctor.py --pkg <pkg>", "./termux-build lint <pkg>"],
            ),
            (
                "Complete failure -- clean reinstall",
                "Remove everything and install again.",
                [
                    "pip uninstall termux-app-store",
                    "rm -rf $PREFIX/lib/.tas ~/.cache/termux-app-store",
                    "pip install termux-app-store",
                ],
            ),
        ]
    else:
        lines = section_header("TROUBLESHOOTING", tag("!"))
        lines += [
            f"  {DIM}Mulai dengan dua perintah ini. Keduanya menjelaskan sebagian besar masalah:{R}",
            "",
        ]
        lines += code_block("tasctl doctor", "termux-app-store mirrors", title="terminal")
        lines += [""]
        issues = [
            (
                "command not found: termux-app-store",
                "Bersihkan cache shell. Jika masih gagal, install ulang.",
                ["hash -r", "termux-app-store version"],
            ),
            (
                "Package '<name>' not found",
                "Periksa ejaan dan perbarui index.",
                ["termux-app-store search <nama>", "termux-app-store update"],
            ),
            (
                "ModuleNotFoundError: textual",
                "Install atau upgrade Textual (8.0.0 ke atas, Python 3.9+).",
                ["pkg install python -y", "pip install --upgrade textual"],
            ),
            ("Permission denied", "Buat perintahnya executable.", ["chmod +x $PREFIX/bin/termux-app-store"]),
            (
                "Unsupported architecture",
                "Didukung: aarch64, armv7l, x86_64. Cek arsitekturmu, dan pakai build source jika binary tidak ada.",
                ["uname -m", "termux-app-store fix-install <pkg>"],
            ),
            (
                "Fast install gagal",
                "Tes mirror, bersihkan cache, lalu coba lagi. Pilihan terakhir: build dari source.",
                ["termux-app-store mirrors", "termux-app-store cache clear", "termux-app-store fix-install <pkg>"],
            ),
            (
                "SHA256 mismatch",
                "Biasanya unduhan rusak atau mirror belum diperbarui. Bersihkan cache lalu coba lagi. Jika berulang, laporkan (secara privat jika curiga dimanipulasi).",
                ["termux-app-store cache clear", "termux-app-store update"],
            ),
            (
                "apt: NO_PUBKEY / repository is not signed",
                "Tambahkan ulang repository agar signing key diunduh dan dicek lagi.",
                ["tasctl install-repo", "pkg update"],
            ),
            (
                "Could not resolve host / timeout",
                "Periksa koneksi dan coba mirror Termux lain.",
                ["termux-app-store mirrors", "termux-change-repo"],
            ),
            (
                "Build failed",
                "Scroll log dan baca error PERTAMA. Lalu periksa recipe-nya.",
                ["python doctor.py --pkg <pkg>", "./termux-build lint <pkg>"],
            ),
            (
                "Gagal total -- clean install",
                "Hapus semuanya lalu install lagi.",
                [
                    "pip uninstall termux-app-store",
                    "rm -rf $PREFIX/lib/.tas ~/.cache/termux-app-store",
                    "pip install termux-app-store",
                ],
            ),
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


def content_help(L):
    en = L == "en"
    if en:
        lines = section_header("GETTING HELP", tag("H"))
        lines += subsection("Before you ask")
        lines += numbered(
            [
                "Read Troubleshooting and FAQ in this guidebook",
                "Search existing issues and discussions on GitHub",
                "Update the app: termux-app-store update",
                "Run: tasctl doctor",
            ]
        )
        lines += subsection("Collect this information")
        lines += code_block(
            "termux-app-store version",
            "uname -m",
            "python --version",
            "pip show textual",
            "which termux-app-store",
            title="terminal",
        )
        lines += [""]
        lines += bullet(
            [
                "The exact command and the full error message",
                "How you installed (pip or tasctl) and whether you use TUI or CLI",
                "Your Termux and Android versions",
                "Remove tokens and private paths from logs before posting",
            ]
        )
        lines += subsection("Where to go")
        lines += bullet(
            [
                f"{B}Question or how-to{R}   -- GitHub Discussions, Q&A category",
                f"{B}Bug{R}                  -- GitHub Issues, Bug Report template",
                f"{B}Feature idea{R}          -- GitHub Issues, Feature Request template",
                f"{B}Package request{R}       -- GitHub Issues, Package Request template",
                f"{B}Security problem{R}      -- private only, see Security & Trust",
                f"{B}Accessibility barrier{R} -- issue titled 'accessibility', or email",
            ]
        )
        lines += [
            "",
            kv_row("Issues   :", REPO_URL + "/issues"),
            kv_row("Q&A      :", REPO_URL + "/discussions"),
            kv_row("Email    :", "gab288.gab288@passinbox.com"),
            "",
        ]
        lines += subsection("Documents in the repository")
        lines += [
            f"  {DIM}README, INSTALL, FAQ, TROUBLESHOOTING, SUPPORT, SECURITY, PRIVACY,{R}",
            f"  {DIM}ACCESSIBILITY, CONTRIBUTING, HOW_TO_UPLOAD{R}",
            "",
        ]
        lines += callout(
            "NOTE",
            "This project is maintained by volunteers, so no response time is guaranteed. Please be patient and respectful.",
            "note",
        )
    else:
        lines = section_header("MENDAPATKAN BANTUAN", tag("H"))
        lines += subsection("Sebelum bertanya")
        lines += numbered(
            [
                "Baca Troubleshooting dan FAQ di guidebook ini",
                "Cari issue dan discussion yang sudah ada di GitHub",
                "Perbarui aplikasi: termux-app-store update",
                "Jalankan: tasctl doctor",
            ]
        )
        lines += subsection("Kumpulkan informasi ini")
        lines += code_block(
            "termux-app-store version",
            "uname -m",
            "python --version",
            "pip show textual",
            "which termux-app-store",
            title="terminal",
        )
        lines += [""]
        lines += bullet(
            [
                "Perintah persisnya dan pesan error lengkap",
                "Cara install (pip atau tasctl) dan apakah memakai TUI atau CLI",
                "Versi Termux dan Android kamu",
                "Hapus token dan path pribadi dari log sebelum dikirim",
            ]
        )
        lines += subsection("Ke mana harus pergi")
        lines += bullet(
            [
                f"{B}Pertanyaan / cara pakai{R} -- GitHub Discussions, kategori Q&A",
                f"{B}Bug{R}                    -- GitHub Issues, template Bug Report",
                f"{B}Ide fitur{R}              -- GitHub Issues, template Feature Request",
                f"{B}Permintaan package{R}      -- GitHub Issues, template Package Request",
                f"{B}Masalah keamanan{R}        -- hanya privat, lihat Keamanan & Kepercayaan",
                f"{B}Hambatan aksesibilitas{R}  -- issue berjudul 'accessibility', atau email",
            ]
        )
        lines += [
            "",
            kv_row("Issues   :", REPO_URL + "/issues"),
            kv_row("Tanya    :", REPO_URL + "/discussions"),
            kv_row("Email    :", "gab288.gab288@passinbox.com"),
            "",
        ]
        lines += subsection("Dokumen di repository")
        lines += [
            f"  {DIM}README, INSTALL, FAQ, TROUBLESHOOTING, SUPPORT, SECURITY, PRIVACY,{R}",
            f"  {DIM}ACCESSIBILITY, CONTRIBUTING, HOW_TO_UPLOAD{R}",
            "",
        ]
        lines += callout(
            "CATATAN",
            "Proyek ini dikelola oleh relawan, jadi waktu respons tidak dijamin. Mohon bersabar dan tetap sopan.",
            "note",
        )
    lines.append("")
    return lines


def content_contributing(L):
    en = L == "en"
    if en:
        lines = section_header("CONTRIBUTING", tag("+"))
        lines += subsection("Accepted Contributions")
        lines += bullet(
            [
                "Add new packages (packages/<name>/build.sh)",
                "Fix existing build.sh files",
                "Fix CI / validation logic",
                "Improve CLI tools (termux-build, tasctl)",
                "Documentation, guides and translations",
                "Bug reports, reproductions and fixes",
                "Feature proposals",
                "Reviewing pull requests",
            ]
        )
        lines += subsection("Contribution Principles")
        lines += bullet(
            [
                f"{BCYN}Automation-first{R}  -- if it can be validated, it must be",
                f"{BCYN}Reproducibility{R}   -- builds must be deterministic",
                f"{BCYN}Transparency{R}      -- no hidden logic",
                f"{BCYN}Community-first{R}   -- breaking changes require discussion",
            ]
        )
        lines += subsection("Commit Message Convention")
        conventions = [
            ("pkg:", "new or updated package"),
            ("fix:", "bug fix"),
            ("ci:", "CI / workflow changes"),
            ("docs:", "documentation"),
            ("refactor:", "internal changes"),
            ("chore:", "maintenance"),
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
        lines += bullet(
            [
                f"{BRED}Do not{R} submit malicious code / malware",
                f"{BRED}Do not{R} submit binaries from local builds",
                f"{BRED}Do not{R} hardcode paths outside $PREFIX",
                f"{BRED}Do not{R} submit tools for brute-forcing, DDoS, backdoors or\ntracking people without a stated defensive use",
                f"{BRED}Do not{R} make breaking changes without discussion",
            ]
        )
        lines += [
            "",
            f"  {DIM}All PRs are automatically checked via GitHub Actions CI.{R}",
            f"  {DIM}PRs cannot be merged if CI fails.{R}",
            "",
            f"  {DIM}See CONTRIBUTING.md and CODE_OF_CONDUCT.md in the repository.{R}",
            "",
        ]
    else:
        lines = section_header("CARA KONTRIBUSI", tag("+"))
        lines += subsection("Kontribusi yang Diterima")
        lines += bullet(
            [
                "Tambah package baru (packages/<nama>/build.sh)",
                "Perbaiki build.sh yang ada",
                "Perbaiki CI / validation logic",
                "Improvement CLI (termux-build, tasctl)",
                "Dokumentasi, panduan, dan terjemahan",
                "Bug report, reproduksi, dan perbaikan",
                "Feature proposal",
                "Review pull request",
            ]
        )
        lines += subsection("Prinsip Kontribusi")
        lines += bullet(
            [
                f"{BCYN}Automation-first{R}  -- kalau bisa divalidasi, harus divalidasi",
                f"{BCYN}Reproducibility{R}   -- build harus deterministic",
                f"{BCYN}Transparency{R}      -- tidak ada hidden logic",
                f"{BCYN}Community-first{R}   -- breaking change harus diskusi dulu",
            ]
        )
        lines += subsection("Commit Message Convention")
        conventions = [
            ("pkg:", "package baru atau update"),
            ("fix:", "bug fix"),
            ("ci:", "CI / workflow changes"),
            ("docs:", "dokumentasi"),
            ("refactor:", "internal changes"),
            ("chore:", "maintenance"),
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
        lines += bullet(
            [
                f"{BRED}Jangan{R} submit kode berbahaya / malware",
                f"{BRED}Jangan{R} submit binary dari local build",
                f"{BRED}Jangan{R} hardcode path di luar $PREFIX",
                f"{BRED}Jangan{R} submit tool untuk brute-force, DDoS, backdoor, atau\nmelacak orang tanpa tujuan defensif yang jelas",
                f"{BRED}Jangan{R} breaking change tanpa diskusi",
            ]
        )
        lines += [
            "",
            f"  {DIM}Semua PR dicek otomatis via GitHub Actions CI.{R}",
            f"  {DIM}PR tidak bisa merge kalau CI gagal.{R}",
            "",
            f"  {DIM}Lihat CONTRIBUTING.md dan CODE_OF_CONDUCT.md di repository.{R}",
            "",
        ]
    return lines


def get_menu(L):
    en = L == "en"
    return [
        ("1", "About Termux App Store" if en else "Tentang Termux App Store", content_about),
        ("2", "How to Install" if en else "Cara Install", content_install),
        ("3", "How to Uninstall" if en else "Cara Uninstall", content_uninstall),
        ("4", "Using termux-app-store" if en else "Penggunaan termux-app-store", content_usage),
        ("5", "Using tasctl" if en else "Penggunaan tasctl", content_tasctl),
        ("6", "Using termux-build" if en else "Penggunaan termux-build", content_termux_build),
        ("7", "Using build-package.sh" if en else "Penggunaan build-package.sh", content_build_package),
        ("8", "How to Upload a Tool" if en else "Cara Upload Tool ke TAS", content_upload),
        ("9", "Guide to Writing build.sh" if en else "Panduan Menulis build.sh", content_buildsh),
        ("s", "Security & Trust" if en else "Keamanan & Kepercayaan", content_security),
        ("f", "FAQ" if en else "FAQ", content_faq),
        ("t", "Troubleshooting" if en else "Troubleshooting", content_troubleshoot),
        ("h", "Getting Help" if en else "Mendapatkan Bantuan", content_help),
        ("c", "Contributing" if en else "Cara Kontribusi", content_contributing),
        ("l", f"{DIM}Switch language / Ganti bahasa{R}", None),
        ("q", "Exit" if en else "Keluar", "quit"),
    ]


def banner(lang_label=""):
    cls()
    w = W()
    print(thick_rule(BCYN, w))
    title_text = f"{B}{BWHT}TERMUX APP STORE{R}  {DIM}-- Guidebook{R}"
    print(vcenter(title_text, w))
    sub_text = f"{DIM}github.com/djunekz/termux-app-store{R}"
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
        print(
            vcenter(
                f"  {DIM}[{R}{BCYN}{B}1{R}{DIM}]{R}  {B}English{R}          {DIM}[{R}{BCYN}{B}2{R}{DIM}]{R}  {B}Indonesia{R}  ",
                w,
            )
        )
        print()
        print(vcenter(f"{DIM}[{R}{BRED}{B}q{R}{DIM}]{R}  Exit / Keluar", w))
        print()
        print(thick_rule(DIM, w))
        print(f"  {DIM}Choice:{R} ", end="", flush=True)
        try:
            ch = input().strip().lower()
        except (EOFError, KeyboardInterrupt):
            ch = "q"
        if ch == "1":
            return "en"
        if ch == "2":
            return "id"
        if ch == "q":
            cls()
            print(f"\n  {BGRN}Goodbye / Sampai jumpa!{R}\n")
            sys.exit(0)


def main_menu(lang):
    while True:
        lang_label = "English" if lang == "en" else "Indonesia"
        menu = get_menu(lang)
        topic = "Choose a topic:" if lang == "en" else "Pilih topik:"
        prompt = "Type key then Enter" if lang == "en" else "Ketik tombol lalu Enter"
        bye = (
            f"\n  {BGRN}{B}Thanks for using Termux App Store!{R}\n"
            if lang == "en"
            else f"\n  {BGRN}{B}Terima kasih telah menggunakan Termux App Store!{R}\n"
        )
        unknown = "Unknown choice" if lang == "en" else "Pilihan tidak dikenali"

        banner(lang_label)
        print(f"  {B}{topic}{R}")
        print()

        w = W()
        main_items = [m for m in menu if m[0] not in ("l", "q")]
        special = [m for m in menu if m[0] in ("l", "q")]

        col_w = (w - 4) // 2
        mid = (len(main_items) + 1) // 2
        left = main_items[:mid]
        right = main_items[mid:]

        for i in range(max(len(left), len(right))):
            left_str = ""
            right_str = ""
            if i < len(left):
                k, lbl, _ = left[i]
                left_str = f"  {DIM}[{R}{BCYN}{B}{k}{R}{DIM}]{R}  {lbl}"
            if i < len(right):
                k, lbl, _ = right[i]
                right_str = f"  {DIM}[{R}{BCYN}{B}{k}{R}{DIM}]{R}  {lbl}"
            lv = vlen(left_str)
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
