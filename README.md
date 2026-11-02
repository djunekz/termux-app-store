![[Termux App Store — TUI Package Manager for Termux](https://github.com/djunekz/termux-app-store/blob/master/.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — TUI & CLI Package Manager for Termux](https://djunekz.github.io/termux-app-store/)

**A local-first TUI and CLI package manager built natively for Termux on Android, with checksum-verified binary installs and a source-build fallback.**

> Read in: 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

<div align="center">

<a href="https://github.com/djunekz/termux-app-store/actions/workflows/build.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/build.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=CI" alt="CI"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/cli-ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/cli-ci.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=CLI" alt="CLI Validation"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/codeql.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/codeql.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=CodeQL" alt="CodeQL"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/lint-checker.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/lint-checker.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=Lint" alt="Lint"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/build-packages-debs.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/build-packages-debs.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=.deb%20build" alt="Build .deb"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/update_index.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/update_index.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=index" alt="Update Index"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/publish.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/publish.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=publish" alt="Publish to PyPI"/></a>
<br>
<a href="https://pypi.org/project/termux-app-store/"><img src="https://img.shields.io/pypi/v/termux-app-store?style=flat-square&labelColor=161b22&logo=pypi&logoColor=white&color=3fb950&label=pypi" alt="PyPI"/></a>
<a href="https://pypi.org/project/termux-app-store/"><img src="https://img.shields.io/pypi/dm/termux-app-store?style=flat-square&labelColor=161b22&logo=pypi&logoColor=white&color=3fb950&label=downloads" alt="PyPI downloads"/></a>
<a href="https://pypi.org/project/termux-app-store/"><img src="https://img.shields.io/pypi/pyversions/termux-app-store?style=flat-square&labelColor=161b22&logo=python&logoColor=white&color=3fb950" alt="Python"/></a>
<a href="https://github.com/djunekz/termux-app-store/releases"><img src="https://img.shields.io/github/v/release/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=release" alt="Release"/></a>
<a href="https://github.com/djunekz/termux-app-store/releases"><img src="https://img.shields.io/github/release-date/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=released" alt="Release date"/></a>
<a href="https://github.com/djunekz/termux-app-store/releases"><img src="https://img.shields.io/github/downloads/djunekz/termux-app-store/total?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=release%20downloads" alt="GitHub downloads"/></a>
<br>
<a href="https://codecov.io/github/djunekz/termux-app-store"><img src="https://img.shields.io/codecov/c/github/djunekz/termux-app-store/master?style=flat-square&labelColor=161b22&logo=codecov&logoColor=white&label=coverage" alt="Codecov"/></a>
<a href="https://www.repo-grade.com/report/djunekz/termux-app-store"><img src="https://www.repo-grade.com/api/badge/djunekz/termux-app-store" alt="RepoGrade"/></a>
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/lint-ruff-3fb950?style=flat-square&labelColor=161b22&logo=ruff&logoColor=white" alt="Ruff"/></a>
<a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/types-mypy-3fb950?style=flat-square&labelColor=161b22&logo=python&logoColor=white" alt="mypy"/></a>
<a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/tests-pytest-3fb950?style=flat-square&labelColor=161b22&logo=pytest&logoColor=white" alt="pytest"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/SECURITY.md"><img src="https://img.shields.io/badge/security-policy-3fb950?style=flat-square&labelColor=161b22&logo=github&logoColor=white" alt="Security Policy"/></a>
<br>
<a href="https://github.com/djunekz/termux-app-store/tree/master/packages"><img src="https://img.shields.io/badge/dynamic/json?style=flat-square&labelColor=161b22&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdjunekz%2Ftermux-app-store%2Fmaster%2Ftools%2Findex.json&query=%24.total&label=packages&color=3fb950&logo=gnometerminal&logoColor=white" alt="Packages"/></a>
<a href="https://termux.dev/"><img src="https://img.shields.io/badge/platform-Termux%20%7C%20Android-3fb950?style=flat-square&labelColor=161b22&logo=android&logoColor=white" alt="Platform"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/ARCHITECTURE.md"><img src="https://img.shields.io/badge/arch-aarch64%20%7C%20arm%20%7C%20x86__64%20%7C%20i686-3fb950?style=flat-square&labelColor=161b22&logo=arm&logoColor=white" alt="Architecture"/></a>
<a href="https://github.com/Textualize/textual"><img src="https://img.shields.io/badge/built%20with-Textual-3fb950?style=flat-square&labelColor=161b22&logo=python&logoColor=white" alt="Built with Textual"/></a>
<a href="https://github.com/djunekz/termux-app-store#readme"><img src="https://img.shields.io/badge/interface-TUI%20%7C%20CLI-3fb950?style=flat-square&labelColor=161b22&logo=gnubash&logoColor=white" alt="Interface"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/SECURITY.md"><img src="https://img.shields.io/badge/installs-SHA256%20verified-3fb950?style=flat-square&labelColor=161b22&logo=letsencrypt&logoColor=white" alt="Checksum verified"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/PRIVACY.md"><img src="https://img.shields.io/badge/root-not%20required-3fb950?style=flat-square&labelColor=161b22&logo=android&logoColor=white" alt="No root"/></a>
<br>
<a href="https://github.com/djunekz/termux-app-store/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3fb950?style=flat-square&labelColor=161b22&logo=opensourceinitiative&logoColor=white" alt="License"/></a>
<a href="https://github.com/djunekz/termux-app-store/stargazers"><img src="https://img.shields.io/github/stars/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Stars"/></a>
<a href="https://github.com/djunekz/termux-app-store/network/members"><img src="https://img.shields.io/github/forks/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Forks"/></a>
<a href="https://github.com/djunekz/termux-app-store/watchers"><img src="https://img.shields.io/github/watchers/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Watchers"/></a>
<a href="https://github.com/djunekz/termux-app-store/graphs/contributors"><img src="https://img.shields.io/github/contributors/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Contributors"/></a>
<a href="https://github.com/djunekz/termux-app-store/issues"><img src="https://img.shields.io/github/issues/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=issues" alt="Open issues"/></a>
<a href="https://github.com/djunekz/termux-app-store/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=closed" alt="Closed issues"/></a>
<a href="https://github.com/djunekz/termux-app-store/pulls"><img src="https://img.shields.io/github/issues-pr/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=git&logoColor=white&color=3fb950&label=PRs" alt="Pull requests"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-3fb950?style=flat-square&labelColor=161b22&logo=git&logoColor=white" alt="PRs welcome"/></a>
<br>
<a href="https://github.com/djunekz/termux-app-store/commits/master"><img src="https://img.shields.io/github/last-commit/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Last commit"/></a>
<a href="https://github.com/djunekz/termux-app-store/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=commits" alt="Commit activity"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/languages/top/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=python&logoColor=white&color=3fb950" alt="Top language"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/languages/count/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=languages" alt="Languages count"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/languages/code-size/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=code%20size" alt="Code size"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/repo-size/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=repo%20size" alt="Repo size"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/code%20of-conduct-3fb950?style=flat-square&labelColor=161b22&logo=contributorcovenant&logoColor=white" alt="Code of Conduct"/></a>

</div>

> **Local-first • Checksum-verified • Source-based • Termux-native • Android Terminal**
> Install and manage Termux packages — pre-built binaries or source builds — no root, no account, no telemetry.

---

## What is Termux App Store?

**Termux App Store** (`termux-app-store`) is a **TUI (Terminal User Interface)** and **CLI package manager** built with Python ([Textual](https://github.com/Textualize/textual)) that lets Termux users on Android **browse, install, and manage tools/packages** directly on-device — no account, no telemetry, no root required. Package metadata and downloads use the network.

Starting from **v0.4.0**, Termux App Store supports a **fast install engine**: packages are downloaded as pre-built `.deb` binaries from a mirror pool (GitHub Pages, Cloudflare CDN, jsDelivr), with local `.deb` caching (TTL 7 days). Every `.deb`, including cached ones, must match a per-arch SHA256 or it is refused. SHA256 detects corruption and mismatched files; it is not a publisher signature. Source builds remain available via `fix-install`.

It works as an **alternative package manager for Termux**, letting you install community tools using `build.sh` scripts — similar in spirit to the AUR (Arch User Repository) but designed specifically for Termux on Android.

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
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
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

| **Package Browser (TUI)** Browse packages from the `packages/` folder interactively with keyboard & touchscreen navigation.<br>**Fast Install Engine** Downloads pre-built `.deb` from mirror pool — GitHub Pages, Cloudflare CDN, jsDelivr — with automatic fallback.<br>**Binary Cache** Local `.deb` cache with 7-day TTL; cached files are re-verified against a per-arch SHA256 before every install. Cached packages install instantly.<br>**Smart Build Validator** Detects unsupported Termux dependencies with automatic status badges. | **Real-time Search & Filter** Search packages by name or description — `search`/`find` CLI commands included.<br>**Multi-package Install/Uninstall** Install or remove several packages in one command with a summary output.<br>**One-Click Manage** Install / update / uninstall Termux App Store itself via `./tasctl`.<br>**Privacy-First** No account, no tracking, no telemetry. Works from local data when already available; fetching metadata and packages needs the network. |
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
  Verify SHA256        Probe the mirrors, use the fastest:
  (per arch)           1. Cloudflare CDN
        │              2. GitHub Pages
        ▼              3. jsDelivr CDN
  dpkg -i                    │
                             ▼
                       Download .deb
                       Verify SHA256 (index sha256_by_arch, else the published .deb.sha256)
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
│   └── mirrors.json       # Mirror registry
├── fast_install.py        # Fast install engine (.deb download + cache + SHA256 verify)
├── store_common.py        # Shared logic: mirrors, app root, recipe and script verification
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
| Builds only run on explicit user command | Local-first; network used for metadata and downloads |
| SHA256 required for every `.deb` (download and cache) | Binary source is transparent and auditable |

> Full details: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

## Development and Testing

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
pip install -e ".[dev]"
```

| Command | What it does |
|---|---|
| `make test` or `pytest` | Run the test suite |
| `make coverage` | Run the test suite with a coverage report |
| `make lint` | Ruff lint and format check |
| `make typecheck` | Mypy type check |
| `make check` | Lint, type check and tests together |

Dependencies are pinned in `uv.lock` (`uv sync --extra dev`). See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

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
- Avoid vendor lock-in
- Share tools openly with the Termux community

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## Maintainer

**Djunekz** — Independent developer and maintainer of Termux App Store

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
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
 </picture>
</a>

---

## Related Projects & Keywords

> This project is independently developed and is **not affiliated with** the official [Termux](https://github.com/termux/termux-app) project.

**Search terms:** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — Built for everyone, by the community.**
