# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to semantic versioning.


## [Unreleased]

### Update
- Package `tdoc` v1.0.5 → v1.0.6

### Added
- Package `basic` v1.0.0 - Simulator Terminal learning basic command for beginner
- Package `userfinder` v1.0 - OSINT tool for finding profiles by username

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
