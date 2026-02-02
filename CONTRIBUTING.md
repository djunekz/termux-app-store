# Contributing to Termux App Store

Thanks for your interest in contributing.

This project is focused on **stability, simplicity, and correctness**.
Please read this guide before opening issues or pull requests.

---

## 📌 Scope of Contributions

Contributions are welcome in the following areas:

- 🐛 Bug fixes
- 🧠 Logic improvements
- 📦 Package definitions (`packages/*`)
- 🧪 Build system improvements
- 🧾 Documentation fixes
- ⚡ Performance improvements

Out-of-scope contributions may be closed without discussion.

---

## 🐞 Reporting Bugs

Before opening an issue:

1. Make sure you are using the **latest version**
2. Check existing issues (open & closed)
3. Reproduce the problem

When reporting a bug, include:

- Termux version
- Architecture (`uname -m`)
- Python version
- Textual version
- Exact error output / traceback
- Steps to reproduce

Low-effort or incomplete bug reports may be ignored.

---

## ✨ Feature Requests

Feature requests are welcome **only if they meet these criteria**:

- Clearly solve a real problem
- Do not overcomplicate the UI
- Do not reduce performance or stability
- Fit the philosophy of the project

Please explain **why** the feature is needed, not just **what** it does.

---

## 🔧 Development Setup

### Requirements

- Termux
- Python ≥ 3.10
- `textual`
- Standard Unix tools (`bash`, `coreutils`, `git`)

### Run from source

```bash
git clone https://github.com/djunekz/termux-app-store
cd termux-app-store
chnod +x install.sh
./install.sh
```
