# Frequently Asked Questions (FAQ)

This document answers common questions about **Termux App Store**.

---

## ❓ What is Termux App Store?

**Termux App Store** is a terminal-based (TUI) package manager for Termux that:
- Builds packages from source
- Uses `build.sh` definitions
- Provides a modern Textual UI
- Supports binary and developer modes

It is **not** an alternative to `pkg`, but a **source-based app store**.

---

## ❓ Is this an official Termux project?

No.

Termux App Store is an **independent project** and is **not affiliated** with
the official Termux maintainers.

---

## ❓ Is it safe to use?

Yes, provided that:
- You trust the source repository
- You review `build.sh` files if using developer mode

Binary releases are prebuilt and intended for convenience.

---

## ❓ Why are some packages marked UNSUPPORTED?

A package is marked **UNSUPPORTED** when it depends on libraries that:
- Do not exist in Termux
- Require system-level components (e.g. `systemd`)
- Are desktop-only (e.g. `gtk2`, legacy `sdl`)

This is a **feature**, not a bug.

---

## ❓ Can I force install an unsupported package?

No (by default).

Unsupported packages are blocked to prevent broken builds and system damage.
Advanced users may modify `build.sh` at their own risk.

---

## ❓ Why does it build from source instead of downloading binaries?

Because:
- Termux environments differ across devices
- Source builds ensure compatibility
- Some tools have no official Termux binaries

Binary releases are only for **Termux App Store itself**, not the packages.

---

## ❓ Does it work offline?

Partially.

- UI works offline
- Installing packages requires internet access

---

## ❓ Where are packages stored?

Packages are located inside:
```Text
termux-app-store/packages
```
Each package must contain a valid `build.sh`.

---

## ❓ Can I add my own packages?

Yes.

Simply create:
```Text
packages/your-tool/build.sh
```
Restart the app and it will appear automatically.

---

## ❓ Can I move the termux-app-store folder?

Yes.

The app:
- Detects its own location
- Supports symlinks
- Self-heals cached paths if moved or renamed

---

## ❓ Can I run it from anywhere?

Yes.

As long as the `packages/` directory exists next to the app root,
it can be executed from any directory.

---

## ❓ Why is the Python source hidden in binary releases?

Binary releases are used to:
- Prevent casual source scraping
- Protect internal logic
- Improve startup speed
- Simplify installation

The project remains open-source on GitHub.

---

## ❓ Is this project open source?

Yes.

The source code is available on GitHub under the project license.
Binary releases are a distribution format, not closed-source software.

---

## ❓ Can I contribute?

Absolutely.

See:
- `CONTRIBUTING.md` [here](CONTRIBUTING.md)
- `CODE_OF_CONDUCT.md` [here](CODE_OF_CONDUCT.md)

Pull requests, issues, and discussions are welcome.

---

## ❓ What architectures are supported?

Currently:
- `aarch64`
- `armv7l`
- `x86_64`

---

## ❓ Why does installation freeze sometimes?

Common reasons:
- Slow network
- Large source download
- Compilation step in progress

Check the log panel for activity.

---

## ❓ Is root required?

No.

Termux App Store runs **entirely in user space**.

---

## ❓ Does it modify my system?

No system files are modified.

Only:
- Termux user directories
- Installed packages via `pkg`

---

## ❓ Where can I report bugs or request features?

GitHub Issues:
https://github.com/djunekz/termux-app-store/issues

---

## ❓ Who maintains this project?

Maintained by **@djunekz**.

---

## ❤️ Final Notes

If something feels broken:
- Check `TROUBLESHOOTING.md` [here](TROUBLESHOOTING.md)
- Open an issue
- Or read the source 😉
