![[Termux App Store — TUI Package Manager for Termux](https://github.com/djunekz/termux-app-store/blob/master/.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — TUI & CLI Package Manager for Termux](https://djunekz.github.io/termux-app-store/)

**The first offline-first, binary-safe TUI package manager built natively for Termux on Android.**

> Read in: 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

[![CI](https://github.com/djunekz/termux-app-store/actions/workflows/build.yml/badge.svg)](https://github.com/djunekz/termux-app-store/actions)
[![Codecov](https://codecov.io/github/djunekz/termux-app-store/branch/master/graph/badge.svg?token=357W4EP8G0)](https://codecov.io/github/djunekz/termux-app-store)
[![PyPI](https://img.shields.io/pypi/v/termux-app-store?style=flat&logo=pypi&color=3fb950&label=pypi)](https://pypi.org/project/termux-app-store/)
[![Version](https://badgen.net/github/release/djunekz/termux-app-store?icon=github&color=3fb950&label=release)](https://github.com/djunekz/termux-app-store/releases)
[![Downloads](https://img.shields.io/github/downloads/djunekz/termux-app-store/total?style=flat&logo=github&color=3fb950&logoColor=white)](https://github.com/djunekz/termux-app-store)
[![License](https://img.shields.io/badge/License-MIT-3fb950?style=flat&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Stars](https://badgen.net/github/stars/djunekz/termux-app-store?icon=github&color=white&label=stars)](https://github.com/djunekz/termux-app-store/stargazers)
[![Forks](https://badgen.net/github/forks/djunekz/termux-app-store?icon=github&color=white&label=forks)](https://github.com/djunekz/termux-app-store/network)
[![Issues](https://img.shields.io/badge/issues-open-3fb950?style=flat&logo=github&logoColor=white)](https://github.com/djunekz/termux-app-store/issues)
[![PRs](https://img.shields.io/github/issues-pr/djunekz/termux-app-store?style=flat&logo=git&logoColor=white&color=3fb950)](https://github.com/djunekz/termux-app-store/pulls)
[![Community Ready](https://img.shields.io/badge/Community-Ready-3fb950?style=flat&logo=github)](https://github.com/djunekz/termux-app-store)

> **Offline-first • Binary-safe • Source-based • Termux-native • Android Terminal**
> Install and manage Termux packages — pre-built binaries or source builds — no root, no account, no telemetry.

---

## What is Termux App Store?

**Termux App Store** (`termux-app-store`) is a **TUI (Terminal User Interface)** and **CLI package manager** built with Python ([Textual](https://github.com/Textualize/textual)) that lets Termux users on Android **browse, install, and manage tools/packages** directly on-device — no account, no telemetry, no cloud dependency, no root required.

Starting from **v0.4.0**, Termux App Store supports a **fast install engine**: packages are downloaded as pre-built `.deb` binaries from a mirror pool (GitHub Pages, Cloudflare CDN, jsDelivr), with local `.deb` caching (TTL 7 days) and per-arch SHA256 verification. Source builds remain available via `fix-install` for full control.

It works as an **alternative package manager for Termux**, letting you install community tools using verified `build.sh` scripts — similar in spirit to the AUR (Arch User Repository) but designed specifically for Termux on Android.

> **How is this different from `termux-packages` or TUR (Termux User Repository)?**
>
> - `termux-packages` is the official Termux repo — maintained by the core team, requires PR approval, and only accepts widely-used tools.
> - TUR is a curated extension, still requires contributor review.
> - **Termux App Store** is fully community-driven: anyone can submit a `build.sh`, packages are distributed as pre-built `.deb` or source builds, and there is no centralized approval gate. Think of it as a personal + community package layer on top of Termux.

> [!IMPORTANT]
> Termux App Store is **not a hidden auto-installer**.
> All installs — binary or source — run **locally, transparently, and under full user control**.

---

## Who Is It For?

| User | Use Case |
|---|---|
| Termux Users | Fast binary installs or full source-build control |
| Developers | Distribute tools via pre-built `.deb` or source packaging |
| Reviewers & Auditors | Review and validate build scripts |
| Maintainers | Manage multiple Termux packages at once |

---

## Screenshots

<div align="center">

<img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0.jpeg" width="74%" alt="Termux App Store — Main View"/>

<br/><br/>
<H1>Tui Interface</H1>

| TUI Main Interface | TUI Install Interface | Menu Palette |
|:---:|:---:|:---:|
| <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0main.jpg" width="220" alt="TUI Main Interface"/> | <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/1install.jpg" width="220" alt="TUI Install Interface"/> | <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/2pallete.jpg" width="220" alt="Menu Palette Interface"/> |
| TUI main menu | Package install process | Command palette |

> TUI User-friendly with full **touchscreen** support

---

<H1>CLI Interface</H1>

| Other tools support | CLI Install Interface | CLI View Interface |
|:---:|:---:|:---:|
| <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0tas-and-termux-build.jpg" width="220" alt="Other tools support"/> | <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0cli-install.jpg" width="220" alt="CLI Install Interface"/> | <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0cli-view.jpg" width="220" alt="CLI View Interface"/> |
| tasctl and termux-build | Package install process | CLI help, list and show |

---

<H1>GuideBook</H1>

| List menu | Menu about | Menu how to upload |
|:---:|:---:|:---:|
| <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0guide-menu.png" width="220" alt="List menu"/> | <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0guide-about.png" width="220" alt="Menu about"/> | <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/0guide-upload.png" width="220" alt="Menu how to upload"/> |
| GuideBook main menu | Information termux-app-store | Guide how to upload |

> GuideBook is a information, run: `python guidebook.py`

---

<H1>Screenrecord</H1>

| Record `termux-app-store` TUI, CLI, Other tool `tasctl`, `termux-build`, `guidebook.py` |
|:---:|
| <img src="https://github.com/djunekz/termux-app-store/blob/master/.assets/demo.gif" width="74%" alt="termux-app-store"/> | termux-app-store

</div>

---

## Quick Install and Uninstall

> Available on **[PyPI](https://pypi.org/project/termux-app-store/)** — searchable and indexed, easy to discover.

### Option 1 (Recommended)

```bash
pkg install python
pip install termux-app-store
```

### Option 2 (Manual)

> Simple (recommended if memory is limited)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> With git clone (downloads full repository)

```bash
git clone --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

After install, run:

```bash
termux-app-store        # Open interactive TUI
termux-app-store -h     # Show CLI help
tas                     # Shorthand for termux-app-store
```

### Uninstall

```bash
pip uninstall termux-app-store
# or
./tasctl uninstall
```

---

## Usage

### TUI — Interactive Interface

```bash
termux-app-store
# or shorthand:
tas
```

### CLI — Direct Commands

```bash
termux-app-store list                     # List all packages
termux-app-store show <package>           # Show package details
termux-app-store install <package>        # Fast install (pre-built .deb)
termux-app-store install pkg1 pkg2 pkg3   # Multi-package install
termux-app-store fix-install <package>    # Force source build (bypass fast install)
termux-app-store search <query>           # Search packages by name or description
termux-app-store update                   # Check for available updates
termux-app-store upgrade                  # Upgrade all packages
termux-app-store upgrade <package>        # Upgrade a specific package
termux-app-store uninstall <package>      # Uninstall a package
termux-app-store mirrors                  # Check mirror status
termux-app-store cache info               # Show binary cache info
termux-app-store cache clear              # Clear binary cache
termux-app-store version                  # Check latest version
termux-app-store help                     # Full help
```

---

## Features

| **Package Browser (TUI)** Browse packages from the `packages/` folder interactively with keyboard & touchscreen navigation.<br>**Fast Install Engine** Downloads pre-built `.deb` from mirror pool — GitHub Pages, Cloudflare CDN, jsDelivr — with automatic fallback.<br>**Binary Cache** Local `.deb` cache with 7-day TTL and per-arch SHA256 verification. Cached packages install instantly.<br>**Smart Build Validator** Detects unsupported Termux dependencies with automatic status badges. | **Real-time Search & Filter** Search packages by name or description — `search`/`find` CLI commands included.<br>**Multi-package Install/Uninstall** Install or remove several packages in one command with a summary output.<br>**One-Click Manage** Install / update / uninstall Termux App Store itself via `./tasctl`.<br>**Privacy-First** No account, no tracking, no telemetry — fully offline after mirror sync. |
|---|---|

---

## Package Status Badges

| Badge | Description |
|---|---|
| **NEW** | Newly added package (< 7 days) |
| **UPDATE** | A newer version is available |
| **INSTALLED** | Installed version is up-to-date |
| **UNSUPPORTED** | Dependency not available in Termux |

---

## How Fast Install Works (v0.4.0+)

```
termux-app-store install <package>
        │
        ▼
  Check local .deb cache (TTL 7 days)
        │ cache HIT          │ cache MISS
        ▼                    ▼
  Verify SHA256        Try mirrors in order:
  (per arch)           1. GitHub Pages (primary)
        │              2. Cloudflare CDN
        ▼              3. jsDelivr CDN
  dpkg -i              4. Raw GitHub (fallback)
                             │
                             ▼
                       Download .deb
                       Verify SHA256 (sha256_by_arch)
                       Cache locally
                       dpkg -i
```

> If fast install fails, use `fix-install <package>` to force a full source build via `build-package.sh`.

---

## Adding a Package

Every package in Termux App Store is defined by a single `build.sh` file — similar to how PKGBUILD works in Arch Linux, but adapted for Termux on Android.

Every package **must** have a `build.sh` file:

```
packages/<tool-name>/build.sh
```

### Minimal `build.sh` Template

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@your-github-username"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

> [!NOTE]
> See the full template in `template/build.sh` or run: `./termux-build template`

### Adding a Package using termux-build

```bash
cd termux-app-store
./termux-build create your-tool-name
# or auto-create from a GitHub URL:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> When naming, do not use spaces — use `-`. Example: `my-tool-name`

---

## termux-build — Build & Validation Tool

`termux-build` is a validation and reviewer helper tool — not an auto-upload or auto-publish tool.

```bash
./termux-build create <package>      # Create package for distribution
./termux-build init <url-repo>       # Auto-create and build package from GitHub URL
./termux-build lint <package>        # Lint a build script
./termux-build check-pr <package>    # Check PR readiness
./termux-build doctor                # Diagnose environment
./termux-build suggest <package>     # Get improvement suggestions
./termux-build explain <package>     # Detailed package explanation
./termux-build template              # Generate build.sh template
./termux-build guide                 # Contribution guide
```

> [!NOTE]
> `termux-build` **only reads and validates** — it does not modify files or upload to GitHub.

---

## tasctl — Termux App Store Controller

`tasctl` is the controller for the termux-app-store system.

```bash
./tasctl install       # Install Termux App Store (latest)
./tasctl update        # Update to latest version
./tasctl uninstall     # Remove Termux App Store
./tasctl doctor        # Diagnose environment
./tasctl self-update   # Update tasctl itself
./tasctl help          # Show help
```

---

## guidebook — All Information About Termux App Store

```bash
python guidebook.py
```

> [!NOTE]
> guidebook currently supports two languages: English and Bahasa Indonesia.

---

## How to Distribute Your Package to the Termux Community

```bash
# 1. Fork this repo
# 2. Add your package folder:
mkdir packages/your-tool-name
# 3. Create build.sh from the template or with termux-build:
./termux-build create your-tool-name
# or from a GitHub URL:
./termux-build init https://github.com/you/your-repo
# 4. Validate with termux-build:
./termux-build lint packages/your-tool-name
# 5. Submit a Pull Request
```

> Full guide: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

## Architecture

```
termux-app-store/
├── packages/              # All packages directory
│   └── <tool-name>/
│       └── build.sh       # Metadata & build script
├── template/
│   └── build.sh           # Package template
├── core/
│   ├── binary_core.py     # BinaryCache — local .deb cache + mirror download
│   ├── mirrors.py         # MirrorManager — mirror pool registry
│   ├── package.py         # Package dataclass
│   └── validator.py       # PackageValidator
├── utils/
│   └── installer.py       # install_from_binary / install_from_source helpers
├── tools/
│   └── mirrors.json       # Mirror registry (GitHub Pages, Cloudflare, jsDelivr, raw GitHub)
├── fast_install.py        # Fast install engine (.deb download + cache + SHA256 verify)
├── tasctl                 # TAS installer/updater/uninstaller
├── termux-build           # Validation & review tool
└── install.sh             # Main installer
```

> Full details: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Security & Privacy

| **Security** | **Privacy** |
|---|---|
| No extra permissions required | No account or registration |
| No network ports opened | No analytics or tracking |
| No background services running | No telemetry of any kind |
| Builds only run on explicit user command | Offline-first by design |
| SHA256 verification on all `.deb` downloads | Binary source is transparent and auditable |

> Full details: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

## Contributing

All contributions are welcome!

| How to Contribute | Description |
|---|---|
| Add a package | Submit a new tool package |
| Report a bug | Open an issue on GitHub |
| Send a PR | Code or documentation improvements |
| Review PRs | Help validate others' contributions |
| Security audit | Review build script security |
| Improve docs | Clarify or translate documentation |

> Full guide: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Help & Documentation

| Document | Description |
|---|---|
| [FAQ](FAQ.md) | Frequently asked questions |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | Solutions to common problems |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | How to upload your tool |
| [CONTRIBUTING](CONTRIBUTING.md) | Contribution guide |
| [SUPPORT](SUPPORT.md) | How to get support |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | Notes on binary distribution |

---

## Philosophy

> *"Local first. Control over convenience. Transparency over magic."*

Termux App Store is built for users who want to:

- Fully understand what runs on their device
- Control builds and sources directly
- Avoid vendor lock-in and cloud dependency
- Share tools openly with the Termux community

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## Maintainer

**Djunekz** — Independent & Official Developer

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

## Support This Project

If Termux App Store has been useful to you:

- **Star** this repo — helps others discover it
- **Share** it in Termux & Android communities
- **Report bugs** via Issues
- **Submit a PR** for any improvement
- **Sponsor**: https://saweria.co/redHh

---

## Star History

<a href="https://www.star-history.com/?repos=djunekz%2Ftermux-app-store&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=dUovvZ4qTYe6-3cHZJkYNy2Ht7VAKBtZfINRBBmyshGbxaZzlzoSXryXbqzfWJ_d6r5ma3kRriLK0UbG_jPcqTeJGX2t4AXm0nz3LMlfCy1ftHLi2Akcgg" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=dUovvZ4qTYe6-3cHZJkYNy2Ht7VAKBtZfINRBBmyshGbxaZzlzoSXryXbqzfWJ_d6r5ma3kRriLK0UbG_jPcqTeJGX2t4AXm0nz3LMlfCy1ftHLi2Akcgg" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=dUovvZ4qTYe6-3cHZJkYNy2Ht7VAKBtZfINRBBmyshGbxaZzlzoSXryXbqzfWJ_d6r5ma3kRriLK0UbG_jPcqTeJGX2t4AXm0nz3LMlfCy1ftHLi2Akcgg" />
 </picture>
</a>

---

## Related Projects & Keywords

> This project is independently developed and is **not affiliated with** the official [Termux](https://github.com/termux/termux-app) project.

**Search terms:** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — Built for everyone, by the community.**
