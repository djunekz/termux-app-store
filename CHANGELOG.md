# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to semantic versioning.

---

## [Unreleased]

---

## [v0.1.4] - 2026-02-13
### Added
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
- Package `iptrack` v1.0.0
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
