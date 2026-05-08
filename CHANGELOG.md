# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to semantic versioning.


## [Unreleased]

### Added
- Package `merlin` v1.0.0 - Analyst website vulnerabillity scanner
- Package `bing-ip2hosts` v1.0.5 - bingip2hosts is a Bing.com web scraper that discovers websites by IP address
- Package `brutespray` v2.6.0 - Fast, multi-protocol credential brute-forcer. Parses Nmap, Nessus, and Nexpose output to automatically test default and custom credentials across 30+ protocols.
- Package `commix` v4.1 - Automated All-in-One OS Command Injection Exploitation Tool
- Package `xsstrike` v3.1.6 - Most advanced XSS scanner.
- Package `zerodoor` v1.0.0 - A script written lazily for generating cross-platform  backdoors on the go :) 
- Package `crowbar` v4.2 - Crowbar is brute forcing tool that can be used during penetration tests. It is developed to support protocols that are not currently supported by thc-hydra and other popular brute forcing tools. 
- Package `cupp` v1.0.0 - cupp — auto-packaged by termux-build-init
- Package `djangohunter` v1.0.0 - djangohunter — auto-packaged by termux-build-init
- Package `dnsrecon` v1.6.0 - DNS Enumeration Script
- Package `doona` v1.0.0 - Network based protocol fuzzer
- Package `dumpzilla` v1.0.0 - dumpzilla packaging for Kali Linux
- Package `termux-tui` v1.0.0 - A futuristic Jarvis-style terminal dashboard for Termux
- Package `aichat` v0.30.0 - All-in-one LLM CLI tool featuring Shell Assistant, Chat-REPL, RAG, AI Tools & Agents, with access to OpenAI, Claude, Gemini, Ollama, Groq, and more.
- Package `ttyper` v1.6.0 - Terminal-based typing test.
- Package `dalfox` v2.12.0 - Dalfox is a powerful open-source XSS scanner and utility focused on automation.
- Package `orchat` v1.4.6 - A powerful, feature-rich command-line interface for interacting with AI models through OpenRouter.
- Package `tere` v1.6.0 - Terminal file explorer
- Package `ssrfmap` v1.0.0 - Automatic SSRF fuzzer and exploitation tool
- TUI Command Palette (`Ctrl+P`) — added About and Contact Support menus
- TUI About menu — displays app version (read from `__version__` in `__init__.py`), Textual version, Python version, and original disclaimer
- TUI Contact Support menu — displays GitHub Issues, GitHub Discussions, Email, Official Repository, and disclaimer, with buttons to open browser directly
- TUI keyboard shortcuts: `Ctrl+R` refresh packages, `Ctrl+I` install selected, `Ctrl+Q` quit
- Package `bit` v1.1.2 - Bit is a modern Git CLI
- Package `broot` v1.56.2 - A new way to see and navigate directory trees
- Package `dust` v1.2.4 - A more intuitive version of du in rust
- Package `cloudflair` v1.0.0 - 🔎 Find origin servers of websites behind CloudFlare by using Internet-wide scan data from Censys.
- Package `holehe` v1.0.0 - holehe allows you to check if the mail is used on different sites like twitter, instagram and will retrieve information on sites with the forgotten password function.
- Package `photon` v1.3.0 - Incredibly fast crawler designed for OSINT.
- Package `xeuledoc` v1.0.0 - Fetch information about a public Google document.
- Package `viu` v1.6.1 - Terminal image viewer with native support for iTerm and Kitty
- Package `ytfzf` v2.6.2 - A posix script to find and watch youtube videos from the terminal. (Without API)
- Package `binwalk` v3.1.0 - Firmware Analysis Tool
- Package `dbd` v1.0.0 - Durandals Backdoor
- Package `dnsmap` v1.0.0 - fork of http://code.google.com/p/dnsmap/source/checkout
- Package `elpscrk` v1.0.0 - An Intelligent wordlist generator based on user profiling, permutations, and statistics. (Named after the same tool in Mr.Robot series S01E01)
- Package `eternal-scanner` v2.2 - An internet scanner for exploit CVE-2017-0144 (Eternal Blue) & CVE-2017-0145 (Eternal Romance)
- Package `evilginx2` v3.3.0 - Standalone man-in-the-middle attack framework used for phishing login credentials along with session cookies, allowing for the bypass of 2-factor authentication
- Package `fbvid` v1.0.0 - Facebook Video Downloader (CLI) For Linux Systems Coded in PHP

### Fixed
- `termux-build-init.sh` — `detect_entrypoint()` step 3: regex in `sed` for parsing `AC_INIT(...)` from `configure.ac` was malformed (`\[\?\([^],)]*\)\]`), causing m4 macro internals like `m4_defn([package_name])` to leak into the entrypoint result (e.g. detected as `m4-defn-package` instead of the actual binary name); regex corrected to `\[*\([^]],)]*\)` and an output validation guard added to reject strings containing `m4_`, `defn`, `$`, `(`, `)`, or `@`
- `termux-build-init.sh` — `scan_python_declared_deps()`: lines starting with `-` in `requirements.txt` (e.g. `-i https://pypi.org/simple`, `--index-url`, `-r`, `-f`) were not filtered and leaked into pip dependency list; added `[[ "$line" =~ ^[[:space:]]*- ]] && continue` guard before processing
- `termux-build-init.sh` — `map_python_dep()`: `socketserver` (lowercase, Python 3 stdlib module) was not in the stdlib filter list, causing it to be included as a pip install target; added to stdlib whitelist alongside `SocketServer`
- `termux-build-init.sh` — `make_install_block()` autotools case: no `termux_step_make_install()` was generated in the output `build.sh`, so `build-package.sh` fell back to auto-detect mode which incorrectly picked the `compile` helper file (an automake utility) instead of the actual built binary; a proper `termux_step_make_install()` using `make install PREFIX=` is now always emitted for autotools packages
- `build-package.sh` — `bash -n "$BUILD_SH"` exit code was silently lost: the result was captured into `_SYNTAX_ERR=$(...)` which always sets `$?` to 0, so syntax errors in `build.sh` were never caught; fixed by capturing exit code separately into `_SYNTAX_EXIT=$?`
- `build-package.sh` — `TERMUX_PKG_DEPENDS` was split via `tr` into a plain string `_DEPS_NORMALIZED` then used unquoted in `for` loop and `pkg install`, causing incorrect word splitting when package names contained spaces or special characters; replaced with `mapfile -t _DEPS_ARRAY` and `"${_DEPS_ARRAY[@]}"` throughout
- `build-package.sh` — `local _pd` used inside a `| while read` subshell within `_check_rust_env()`; semantically wrong outside a direct function body; removed `local`, variable now declared plainly as `_pd=$(dirname "$_ct")`
- `build-package.sh` — staging paths were inconsistent: ELF, npm, and auto-detect modes used `$WORK_DIR/pkg/$PREFIX` (double slash since `PREFIX` starts with `/`), while custom install mode used `$WORK_DIR/pkg$PREFIX` (correct); standardized all paths to `$WORK_DIR/pkg$PREFIX` to ensure all staged files land in the same directory tree that `dpkg-deb` packages
- `build-package.sh` — `dpkg-deb --build ... | tee "$DPKG_LOG"` caused `DPKG_EXIT` to always be 0 because the `if` condition evaluated the exit code of `tee` (always succeeds), not `dpkg-deb`; even with `set -o pipefail` active this pattern is unreliable; replaced with direct redirect `> "$DPKG_LOG"` and explicit `DPKG_EXIT=$?` capture
- `build-package.sh` — `termux_step_pre_configure()` defined in `build.sh` (e.g. running `autoreconf -fi` for autotools packages) was never called by `build-package.sh`, causing autotools builds to fail at `./configure` with missing generated files; added an explicit call block before `termux_step_make()` that `cd`s into `$SRC_ROOT` and invokes the function when declared
- `termux-build-init.sh` — all color variables now use `$'\033[...'` syntax so escape sequences are correctly interpreted by `printf` and `echo`; previously colors appeared as raw text like `\033[97m`
- `termux-build-init.sh` — Unicode characters in banner (`·`) and status tags (`✓`, `─`) now render correctly instead of showing as `\u00b7`, `\u2713`, `\u2500`
- `termux-build-init.sh` — output style unified with `build-package.sh`: same colors, same tag format `[✓]` `[INFO]` `[!]` `[FAIL]`, same `— Section —` style, same `─` line separator
- `termux-build-init.sh` — fail message "Cek nama branch atau pastikan repo tidak private" translated to English and reformatted to match tag style
- `build-package.sh` — `_line_heavy()` and `_line_thin()` fixed: replaced `tr ' ' '─'` with `printf '%.0s─' $(seq 1 $w)` to correctly render multi-byte Unicode separator characters
- `termux-build-init.sh` — when `INSTALL_METHOD=unknown`, tool now detects if the repo is a build-scripts/patch collection (contains `scripts/`, `patches/`, or `cmake/` directories with no runnable file in root) and sets `_BUILD_SCRIPTS_ONLY=true`
- `termux-build-init.sh` — when `INSTALL_METHOD=unknown` and repo is build-scripts only, a red warning box is shown: *"This repo is not a standalone tool — packaging will produce a .deb with no usable command"*; prompt defaults to **N** (abort)
- `termux-build-init.sh` — when `INSTALL_METHOD=unknown` but repo is not build-scripts only, a yellow warning box is shown: *"Could not detect build system — edit build.sh manually before test build"*; prompt also defaults to **N**
- `termux-build-init.sh` — test build is automatically skipped when `INSTALL_METHOD=unknown`; user is shown a message to edit `build.sh` first before running `bash build-package.sh <name>`
- `termux-build-init.sh` — `detect_method()` wrong priority: `Makefile` was checked before `pyproject.toml`, causing Python repos that also have a `Makefile` (e.g. `parllama`) to be detected as `make` method and fail with `No makefile found`
- `termux-build-init.sh` — `map_python_dep()` had many incorrect pip package names and stdlib modules slipping through: `yaml` → `PyYAML`, `click_default_group` → `click-default-group`, `xdg_base_dirs` → `xdg-base-dirs`, `dotenv` → `python-dotenv`; `asyncio`, `bisect`, `toml` should be filtered as stdlib
- `termux-build-init.sh` — `pip install .` used `--no-deps` so dependencies declared in `pyproject.toml` were not installed, causing `ModuleNotFoundError` at runtime (e.g. `elia`: `click_default_group` not installed)
- `termux-build-init.sh` — `pip_extra_cmd` installed all dependencies in one batch with `|| true`, so if one package name was wrong the entire batch failed silently
- `build-package.sh` — auto-detect mode: ELF binary check now runs **before** `cp`, preventing `Permission denied` errors when zip contains compiled executables
- `build-package.sh` — auto-detect mode: ELF binaries are now installed directly to `bin/` using `install -m755` instead of `cp -r` of the entire repo
- `build-package.sh` — auto-detect mode: non-ELF files retain `cp -r` to `lib/` with a file-by-file fallback in case any individual file fails to copy
- `build-package.sh` — `termux_step_make()` only ran `cd` to source when `TERMUX_PKG_BUILD_IN_SRC=true`; now always `cd "$SRC_ROOT"` before running make
- `termux_app_store.py` — `Input` search bar was placed outside `#body`, so on maximize only the search bar appeared and the left/right panels were not visible
- `termux_app_store.py` — `on_mount` used `await asyncio.to_thread(self.load_packages, True)` which blocked the initial render, causing the UI to appear blank on startup while waiting for GitHub fetch to complete
- `termux_app_store.py` — `ContactScreen` crashed with `MarkupError` because the `[link=https://...]` tag is not supported by Rich markup; URLs containing `://` were parsed incorrectly
- `termux_app_store_cli.py` — display CLI new interface

### Changed
- `pkg-scaffold.py` — auto-detect build method from repo file tree via GitHub API before Step 4 (checks for `Cargo.toml`, `go.mod`, `package.json`, `pyproject.toml`, `setup.py`, `CMakeLists.txt`, `Makefile`, `Gemfile`, etc.)
- `pkg-scaffold.py` — auto-detected method is pre-selected as default in the build method menu, user just presses Enter to confirm
- `pkg-scaffold.py` — default branch is fetched dynamically from GitHub API (`default_branch` field), so repos using `master`, `main`, or any custom branch are handled correctly; `"main"` is only used as fallback when offline
- `pkg-scaffold.py` — Step 5 (entrypoint) is automatically skipped for methods that don't need it (`cargo`, `go`, `npm`, `cmake`, `make`, `pip`), with a short message explaining the skip
- `pkg-scaffold.py` — warning displayed in Next Steps when `python-script` method is selected, reminding user to verify the entrypoint file exists and suggesting the correct method if build fails
- `build-termux-repo.yml` — nav bar: fixed horizontal overflow on mobile; `nav-inner` now uses `width:100%; box-sizing:border-box; overflow:hidden`
- `build-termux-repo.yml` — nav tabs now use `flex:1; min-width:0; overflow-x:auto` so tabs scroll horizontally instead of clipping the viewport
- `build-termux-repo.yml` — active nav tab now has a blue background highlight with top border radius for visual clarity
- `build-termux-repo.yml` — `.wrap` container now has `overflow-x:hidden` to prevent code blocks and cards from leaking outside the page on mobile
- `build-termux-repo.yml` — `.install-option` cards now have `overflow:hidden; box-sizing:border-box` to stay within screen bounds
- `build-termux-repo.yml` — `.step-body` now uses `min-width:0; overflow:hidden` to prevent flex children from overflowing on the Contribute page
- `build-termux-repo.yml` — Contribute page restructured: Fork & Clone and Create Branch steps moved above Automatic/Manual sections as shared prerequisites
- `build-termux-repo.yml` — Contribute page: "Automatic" and "Manual" section labels no longer use emoji icons
- `build-termux-repo.yml` — Contribute page: `./termux-build template` command no longer requires `<your-tool-name>` argument
- `build-termux-repo.yml` — Contribute page: `git push origin master` corrected to `git push origin <your-branch>`
- `build-termux-repo.yml` — Contribute page: removed `# Fork via GitHub UI, then:` comment from code block
- `build-termux-repo.yml` — Contribute page: `git checkout -b <your-branch>` added as a dedicated step after clone
- `termux_app_store_cli.py` — redesigned CLI output: all messages indented 2 spaces for cleaner alignment
- `termux_app_store_cli.py` — replaced `[*]`, `[✔]`, `[✗]`, `[!]` prefix tags with clean `✔` `✗` `↑` symbols
- `termux_app_store_cli.py` — `cmd_install` and `cmd_uninstall` now display a `─` bordered header section
- `termux_app_store_cli.py` — `cmd_version` redesigned with `━` box border showing installed and latest versions
- `termux_app_store_cli.py` — `cmd_show` redesigned with `━` box border for package details
- `termux_app_store_cli.py` — `cmd_help` restructured into a bordered box with grouped command sections
- `termux_app_store_cli.py` — `cmd_list` footer changed from inline total to a separate line with `─` separator
- `termux_app_store_cli.py` — `cmd_upgrade` list and summary now use bordered sections with `─` separators
- `termux_app_store_cli.py` — all status/progress messages shortened and made consistent across commands
- `tasctl` sync with pypi for update and wrapper
- `termux_app_store_cli.py` sync tasctl and pypi
- Package `termux-tui` v1.0.2 - Updated metadata
- `termux-build-init.sh` — `pip install .` now tries with full deps first, falls back to `--no-build-isolation`, then finally `--no-deps` as last resort
- `termux-build-init.sh` — each pip dependency is now installed individually with a warning per failed package instead of silent batch failure
- `termux-build-init.sh` — `make` block now has a guard: if no `Makefile` is found in the working directory, automatically falls back to pip if `pyproject.toml` exists
- `termux-build-init.sh` — added new mappings in `map_python_dep()`: `xdg_base_dirs`, `click_default_group`, `sqlmodel`, `tiktoken`, `humanize`, `textual`, `cv2`, `PIL`, `sklearn`, `skimage`, `nacl`, `pyzmq`, `attr`, `flask_restful`, and more
- `termux_app_store.py` — `Input` search moved inside `#left` panel so maximize works correctly
- `termux_app_store.py` — CSS fixed: `Screen` gets `layout: vertical`, `#left` and `#right` get proper `height: 1fr`
- `termux_app_store.py` — `on_mount` now renders immediately from local cache, then fetches GitHub index in background via `run_worker` without freezing the UI
- `termux_app_store.py` — Command Palette replaced from Textual default menus (Maximize, Keys, Screenshot, Theme) with: Refresh packages, Install selected, Show installed, Update all, Open homepage, Clear log, About, Contact Support
- `termux_app_store.py` — contact email corrected: `gab288.gab288@gmail.com` → `gab288.gab288@passinbox.com`
- `termux_app_store.py` — `ContactScreen` added Discussions button to open GitHub Discussions directly in browser

### Update
- `termux-build-init.sh` - Update and fixed scan repo, fixed generate build.sh
- Package `cybertuz` v1.0.1 → v1.0.2-1
- Package `tdoc` v1.0.6 → v2.0.0
- Package `termux-sync` v0.1.0 → v1.1.0
- Package `ani-cli` v4.11 → v4.13
- Package `termux-tui` v1.0.0 → v1.0.1
- Package `zora` v1.2.2 → v2.0.0

---

## [v0.2.6] - 2026-04-23
### Added
- New menu `termux-build init` for auto create and build package
- New file termux-build-init.sh in directory tools for auto create and build package
- Package `auxscan` v1.0.0 - Vulnerability Scanner to automate certain tasks, improve
- Package `clickjacking-tester` v1.0.0 - A python script designed to check if the website if vulnerable of clickjacking and create a poc
- Package `cmseek` v1.1.3 - CMS Detection and Exploitation suite - Scan WordPress, Joomla, Drupal and over 180 other CMSs
- Package `cmsmap` v1.0.0 - CMSmap is a python open source CMS scanner that automates the process of detecting security flaws of the most popular CMSs. 
- Package `gemail-hack` v1.0.0 - python script for Hack gmail account brute force
- Package `ghosttrack` v1.0.0 - Useful tool to track location or mobile number
- Package `goblinwordgenerator` v1.0.0 - Python wordlist generator 
- Package `hammer` v1.0.0 - Ddos attack tool for termux
- Package `hash-buster` v1.0.0 - hash-buster — auto-packaged by termux-build-init
- Package `ht-wps-breaker` v1.0.0 - HT-WPS Breaker (High Touch WPS Breaker)
- Package `hunner` v1.0.0 - Hacking framework
- Package `instareporter` v1.0.0 - Instagram Mass Reporting Tool
- Package `ip-tracker` v1.0.0 - Track anyones IP just opening a link!
- Package `ipgeolocation` v2.0.4 - Retrieve IP Geolocation information
- Package `lazymux` v1.0.0 - termux tool installer
- Package `termux-ai` v1.0.0 - Interactive AI tool for Termux with 10+ providers and 50+ image models
- Package `userfinder` v1.0.0 - userfinder — auto-packaged by termux-build-init
- Package `termux-sync` v0.1.0 - OpenSource Backup and restore your entire Termux environment across devices.
- Package `lalin` v1.0.0 - this script automatically install any package for pentest with uptodate tools , and lazy command for run the tools like lazynmap , install another and update to new #actually for lazy people hahaha #and Lalin is remake the lazykali with fixed bugs , added new features and uptodate tools . Its compatible with the latest release of Kali (Rolling)
- Package `myserver` v1.0.0 - myserver — auto-packaged by termux-build-init
- Package `parsero` v1.0.0 - Parsero | Robots.txt audit tool
- Package `red-hawk` v1.0.0 - All in one tool for Information Gathering, Vulnerability Scanning and Crawling. A must have tool for all penetration testers
- Package `sublist3r` v1.1 - Fast subdomains enumeration tool for penetration testers
- Package `termuxalpine` v1.0.0 - Use TermuxAlpine.sh calling to install Alpine Linux in Termux on Android. This setup script will attempt to set Alpine Linux up in your Termux environment.
- Package `the-eye` v1.0.0 - Simple security surveillance script for linux distributions.

### Changed
- Package `bashxt` v2.2 - Updated metadata
- Package `cybertuz` v1.0.1 - Updated metadata
- Package `impulse` v1.0.0 - Updated metadata
- Package `pymaker` v1.0.0 - Updated metadata
- Package `fd` v10.4.2 - Updated metadata
- Package `ani-cli` v4.11 - Updated metadata

### Update
- Update core `termux-app-store` to textual new version 8.2.3
- Update fixed bug CLI - ensure build package, fetch index fallback to index cache, load package from disk, load package, load all packages
- Package `aura` v0.8.2 → v0.10.0
- Package `fd` v10.3.0 → v10.4.2
- Package `ani-cli` v4.10 → v4.11
- Package `uv` v0.10.4 → v0.11.7
- Package `sigit` v2.0-pre → v2.0

---

## [v0.2.4] - 2026-04-07
### Update
- Change log message format in CLI
- Repack and download build-package for installer package
- Fixed bug not found `build-package` before install package
- Fixed bug installer in TUI and CLI
- Fixed fetch bug version
- Auto update core to source with `termux-app-store update`
- Update formating docs
- Update source version to `__init__.py` or `pyproject.toml`
- Update support installer manual (git clone) or auto (pip install)
- Fixed crash launcher and intaller packages

---

## [v0.2.3] - 2026-04-06
### Update
- Update system core `termux-app-store update`
- Support installer with `pip install termux-app-store`
- `main.py` `termux_app_store.py` `termux_app_store_cli.py` resolve app
- Package `tdoc` v1.0.5 → v1.0.6
- Package `basic` v1.0.0 → v1.0.2

### Added
- Package `basic` v1.0.0 - Simulator Terminal learning basic command for beginner
- Package `cybertuz` v1.0.1 - Comprehensive Educational Learning Platform for Termux

### Changed
- Package `basic` v1.2.0 - Updated metadata

### Remove
- All ilegal packages

---

## [v0.1.7] - 2026-03-02
### Added
- Added an `uninstall button` to the text-based user interface (TUI)
- Package `bashxt` v2.2 - basic command, code color, shortcut keyboar, etc information
- Package `aura` v0.8.2 - Adaptive Unified Runtime Assistant
- Package `tx` v1.0.0 - Advance Terminal Editor Ultimate
- Package `aircrack-ng` v1.7 - aircrack-ng for termux package
- Package `ani-cli` v4.10 - A cli tool to browse and play anime
- Package `fd` v10.3.0 - A simple, fast and user-friendly alternative to find
- Package `lux` v0.24.1 - Fast and simple video download library and CLI tool written in Go
- Package `maskphish` v2.0 - URL Making Technology to the world for the very tool for Phishing.
- Package `zx` v8.8.5 - A tool for writing better scripts
- Package `bower` v1.8.12 - A package manager for the web
- Package `infoooze` v1.1.9 - A OSINT tool which helps you to quickly find information effectively.
- Package `pnpm` v10.30.1 - Fast, disk space efficient package manager
- Package `sigit` v2.0-pre - SIGIT - Simple Information Gathering Toolkit
- Package `tuifimanager` v5.2.6 - A terminal-based TUI file manager
- Package `uv` v0.10.4 - An extremely fast Python package and project manager, written in Rust.
- Package `zorabuilder` v1.0.0 - Builder python standalone ELF

### Changed
- Package `impulse` v1.0.0 - Updated metadata
- Package `iptrack` v1.0.0 - Updated metadata
- Package `pymaker` v1.0.0 - Updated metadata
- Package `zora` v1.0.0 - Updated metadata
- Package `zoracrypter` v1.0.0 - Updated metadata
- Package `zoravuln` v1.0.0 - Updated metadata
- Package `ghostrack` v1.0.0 - Updated metadata
- Package `tdoc` v1.0.5 - Updated metadata

### Update
- Package `zora` v1.0.0 → v1.2.0

---

## [v0.1.6] - 2026-02-18
### Added
- index.json for based
- update_index workflows
- package_manager for index
- build for index

### Update
- `termux-app-store` new interface (CLI)
- `termux-app-store` feature index based
- System `update` and `upgrade`
- Installer interface
- Uninstaller interface
- Auto CLI workflows for PR (Pull Request)
- Colors `termux-build`
- Auto install / update / uninstall with `tasctl`

### Fixed
- Fixed build-package for installing package
- Fixed renovate workflows
- Fixed update log workflows
- Fixed PR Checker workflows
- Fixed Lint Cheker workflows

---

## [v0.1.4] - 2026-02-13
### Added
- Package `impulse` v1.0.0
- Package `zoracrypter` v1.0.0
- Package `zora` v1.0.0
- Package `ghostrack` v1.0.0
- Package `iptrack` v1.0.0
- `termux-build create` for easy create packages and build.sh
- `termux-build lint <package>` for check validation
- `termux-build doctor` for check error

### Update
- New interface (TUI and CLI)
  - command:
    - `termux-app-store` (Open interface)
    - `termux-app-store help`
    - `termuc-app-store list`
    - `termux-app-store show <package>`
    - `termux-app-store update`
    - `termux-app-store upgrade` (Upgrade all outdated installed)
    - `termux-app-store upgrade <package>`
    - `termux-app-store version`
  - short command
    - `termux-app-store -h` = help
    - `termux-app-store -v` = version
    - `termux-app-store i or -i <package> = install package
    - `termux-app-store -l or -L` = list package
- Auto CLI workflows for PR (Pull Request)
- Colors `termux-build`
- Auto install / update / uninstall with `tasctl`

### Fixed
- Fixed build-package for installing package
- Fixed error renovate workflows
- Fixed update log workflows
- Fixed PR Checker workflows
- Fixed Lint Checker workflows

---

## [v0.1.2] - 2026-02-10
### Added
- Package `pymaker` v1.0.0
- Package `baxter` v1.2.4
- termux-build for check lint, check-pr, and etc
- Package browser with search and live preview
- tasctl for install, uninstall, update termux-app-store
- Auto-detection of system architecture
- file uninstall.sh
- Portable path resolver (works via symlink, binary, or any directory)
- Self-healing package path detection
- Support architecture aarch64, arm, x86_64, i686
- Progress bar and live build log panel
- Status badges: INSTALLED
- Status information: maintainer

### Fixed
- List panel not updating preview on ENTER
- ProgressBar API misuse causing runtime crash
- Failure when running outside project root directory
- Crash when directory is missing or relocated
- Fast render

### Changed
- Improved package scanning logic
- Safer subprocess handling for build output
- More robust UI refresh behavior during installation

---

## [v0.1.0] - 2026-02-02
### Added
- Package `webshake` v1.0.2
- Package `termstyle` v1.0.0
- Package `tdoc` v1.0.5
- Package `pmcli` v0.1.0
- Package `encrypt` v1.1
- Textual-based TUI application for Termux
- Package browser with search and live preview
- Install / Update workflow using `build-package.sh`
- Auto-detection of system architecture
- Portable path resolver (works via symlink, binary, or any directory)
- Self-healing package path detection
- Inline CSS embedded in Python (no external CSS dependency)
- Progress bar and live build log panel
- Status badges: `NEW`, `INSTALLED`, `UPDATE`

### Fixed
- List panel not updating preview on ENTER
- ProgressBar API misuse causing runtime crash
- Failure when running outside project root directory
- Crash when `packages/` directory is missing or relocated

### Changed
- Improved package scanning logic
- Safer subprocess handling for build output
- More robust UI refresh behavior during installation

### Planned
- Binary distribution via GitHub Releases
- Automatic dependency validation for unsupported Termux packages
- UI badge for `UNSUPPORTED` packages
- Pre-build validation for `build.sh`

---

## [v0.0.1] - 2026-01-xx
### Initial
- Internal prototype
- Local-only execution
