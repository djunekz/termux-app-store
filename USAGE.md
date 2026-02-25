# Termux App Store — Usage

This repository ships two ways to use Termux App Store:

1) **Binary edition** (default when installing from the one-line installer)
2) **Source edition** (Python + Textual, fully auditable and offline-first)

The commands below work for both editions unless noted.

## TUI

Run:

```bash
termux-app-store
```

Key bindings:

- `/` focus search
- `i` install/upgrade selected package
- `u` uninstall selected package
- `o` open package homepage
- `r` refresh list
- `q` quit

## CLI

Show help:

```bash
termux-app-store -h
```

List packages:

```bash
termux-app-store list
termux-app-store list nmap
termux-app-store list --installed
termux-app-store list --updates
```

Show details:

```bash
termux-app-store show <package>
```

Install/build:

```bash
termux-app-store install <package>
```

Upgrade everything that is missing/outdated:

```bash
termux-app-store upgrade
```

Refresh remote index cache:

```bash
termux-app-store update
```

Diagnostics:

```bash
termux-app-store doctor
```
