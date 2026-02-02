# Installation Guide

This document explains how to install **Termux App Store** on Termux.

The recommended method is using the official installer script, which installs
the binary release and hides internal implementation details.

---

## 📋 Requirements

- Termux (latest version recommended)
- Internet connection
- One of the following architectures:
  - `aarch64` (recommended)
  - `armv7l`
  - `x86_64`

> No manual Python or Textual setup is required when using the binary release.

---

## 🚀 Quick Install (Recommended)

Run the following command inside Termux:

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/main/install.sh```

### After installation, run:
`termux-app-store`
---

## 🔍 What the Installer Does
The installer will:
- Detect your CPU architecture automatically
- Download the correct binary release
- Install it into a hidden directory:
```
$PREFIX/lib/.tas/```
- Create a symlink:
```
$PREFIX/bin/termux-app-store```
- Make the app runnable from anywhere
You do not need to know where the internal files are located.
---

## 📦 Binary Mode (Default)
By default, Termux App Store runs as a prebuilt binary:
- Source code is not required at runtime
- Python files are not exposed
- Prevents accidental modification
- Faster startup
This is intentional.
---

## 🧠 Python Fallback Mode (Advanced)
If you are running from source (not recommended for normal users):
### Install dependencies manually
```
pkg install python -y
pip install --upgrade textual
```
### Run manually
```
cd termux-app-store
python termux-app-store.py
```
This mode is intended for developers only.
---

## 🗂 Packages Directory Requirement
Termux App Store requires a packages/ directory inside the project root.
### Structure example:
```Text
termux-app-store/
├── packages/
│   ├── package1/
│   │   └── build.sh
│   └── package2/
│       └── build.sh
└── build-package.sh
```
The app will automatically locate this directory even if the project folder is moved or renamed.

## ❗ Troubleshooting
### command not found: termux-app-store
Restart Termux or run:
```Bash
hash -r
```
### Unsupported architecture
If you see:
```Text
Unsupported architecture
```
Your device is not supported yet.

### Permission denied
Make sure $PREFIX/bin is writable:
```Bash
chmod +x $PREFIX/bin/termux-app-store
```
---

## 🔐 Security Notice
- Always install from the official GitHub repository
- Do not download binaries from third-party sources
- Verify release checksums if provided
See [SECURITY.md](SECURITY.md) for details.
---

## 🧾 Uninstall
To remove Termux App Store:
```Bash
rm -f $PREFIX/bin/termux-app-store
rm -rf $PREFIX/lib/.tas
```
---

## 📎 Support
Issues: GitHub Issues
Maintainer: [@djunekz](https://github.com/djunekz)
Email Support: gab288.gab288@passinbox.com
