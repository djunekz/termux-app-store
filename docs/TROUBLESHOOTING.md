# Troubleshooting

This document helps you diagnose and fix common problems when using
**Termux App Store**.

---

## 🚫 Command Not Found

### ❌ Error
`termux-app-store: command not found`
### ✅ Solution
Restart Termux, then try again:
```
hash -r
termux-app-store
```
If the issue persists, verify the symlink exists:
```
ls $PREFIX/bin/termux-app-store
```
If missing, reinstall using the official installer.

---

## 📦 Packages Not Found

### ❌ Error
`packages/ not found`
### 🔍 Cause
The `packages/` directory cannot be located.
This usually happens when:
- The project folder was partially copied
- The directory structure was modified incorrectly
- Running a developer build without the packages folder
### ✅ Solution
Ensure the structure exists:
```Text
termux-app-store/
├── packages/
│   └── <package-name>/
│       └── build.sh
```
Then restart the app.
> Binary users normally never see this error.

---

## 🧠 Unsupported Package

### ❌ Symptom
- Package shows as UNSUPPORTED
- Installation is blocked or skipped
### 🔍 Cause
The package depends on libraries not available in Termux (e.g. sdl, gtk2, systemd).
### ✅ Solution
This is intentional.
Options:
- Choose another package
- Modify `build.sh` to use Termux-supported dependencies
- Wait for a compatible port

---

## 🧪 Build Failed

### ❌ Symptom
Installation stops with errors in the log panel.
### 🔍 Common Causes
- Missing dependency
- Invalid `build.sh`
- Network interruption
- Upstream source removed
### ✅ Solution
Scroll the log panel and check:
- Missing package names
- 404 download errors
- Compilation failures
Then:
- Fix `build.sh` (developer mode)
- Or report the issue on GitHub

---

## 🔐 Permission Denied

### ❌ Error
`Permission denied`
### ✅ Solution
Ensure the binary is executable:
```Bash
chmod +x $PREFIX/bin/termux-app-store
```

---

## 🧱 Architecture Not Supported

### ❌ Error
```Text
Unsupported architecture
```
### 🔍 Cause
Your device CPU is not supported by current releases.
### ✅ Solution
Check your architecture:
```Bash
uname -m
```
Supported:
- aarch64
- armv7l
- x86_64

---

## 🐍 Python / Textual Errors (Developer Mode Only)

### ❌ Error
```Text
ModuleNotFoundError: textual```
### ✅ Solution
Install dependencies manually:
```Bash
pkg install python -y
pip install textual
```
> Binary users should not encounter this issue.

---

## 🖥 UI Issues

### ❌ Symptoms
- Right panel not updating
- ENTER key does nothing
- UI freezes during install
### 🔍 Causes
- Terminal too small
- Outdated Termux
- Interrupted background process
### ✅ Solution
- Resize terminal
- Restart Termux
- Avoid running multiple installs simultaneously

---

## 🔄 Cache / Path Issues

### ❌ Symptom
App fails after moving the project directory.
### ✅ Solution
Termux App Store automatically self-heals.
If needed, restart the app or reinstall.

---

## 🌐 Network Issues

### ❌ Error
```Text
curl: (6) Could not resolve host
```
### ✅ Solution
- Check internet connection
- Change mirror:
```Bash
termux-change-repo
```

---

## 🧹 Clean Reinstall
If everything fails:
```Bash
rm -f $PREFIX/bin/termux-app-store
rm -rf $PREFIX/lib/.tas
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/main/install.sh | bash
```
---

## 🐞 Reporting Bugs
Before opening an issue, include:
- Termux version
- Architecture (`uname -m`)
- Error message or log output
- Whether using binary or source mode
Open issues at: [Click for issue here](https://github.com/djunekz/termux-app-store/issues)
---

## ❤️ Support
Maintainer: [@djunekz](https://github.com/djunekz)
Community contributions are welcome.
