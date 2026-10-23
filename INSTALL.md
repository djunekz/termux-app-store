# Installation Guide

This document explains how to install, update and remove **Termux App Store**
on Termux. It applies to v0.9.1 and later.

---

## Requirements

- Termux on Android (latest version recommended)
- An internet connection
- Python 3.9 or newer (installed with `pkg install python`)
- Textual 8.0.0 or newer (installed automatically by pip and by the installers)
- One of these CPU architectures:
  - `aarch64` (recommended)
  - `armv7l`
  - `x86_64`

Check your architecture with `uname -m`. No root access is needed.

---

## Choose an Installation Method

| Method | Best for | What you get |
|---|---|---|
| Option 1: pip | Most users | Python package from PyPI, `termux-app-store` and `tas` commands |
| Option 2: tasctl | Low-memory devices, or when you also want the APT repository | Shallow clone of the repository in `$PREFIX/lib/.tas`, APT repository entry, `tasctl` command |
| Option 3: install.sh | When you want an official release archive | Latest release archive, checksum-verified, in `$PREFIX/lib/.tas`, plus `tasctl` |

Use only one method at a time. Mixing methods can leave two copies of the
`termux-app-store` command on your system (see
[Troubleshooting](TROUBLESHOOTING.md#wrong-copy-is-running-or-version-looks-old)).

---

## Option 1: pip (Recommended)

```bash
pkg install python
pip install termux-app-store
```

The package is published on [PyPI](https://pypi.org/project/termux-app-store/).
If pip refuses with an "externally-managed-environment" message, add the same
flag the project's own installers use:

```bash
pip install termux-app-store --break-system-packages
```

---

## Option 2: tasctl

Simple, and good when memory is limited because it does not download the full
repository history:

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

Or, from a clone of the repository:

```bash
git clone --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
./tasctl install
```

`tasctl install` checks that you are using the official source, installs
`git`, `python` and `textual` if missing, makes a shallow clone into
`$PREFIX/lib/.tas`, adds the signed APT repository, creates the launcher
and links `tasctl` into `$PREFIX/bin`. An existing installation is moved to a
backup folder named `.tas.bak.<timestamp>` before the new one is put in place.

---

## Option 3: install.sh

```bash
git clone --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

`install.sh` does not use the cloned files. It downloads the latest official
release archive from GitHub, verifies its SHA256 checksum, extracts it to
`$PREFIX/lib/.tas`, creates the launcher and links `tasctl`. It stops with an
error if the source cannot be confirmed as `djunekz/termux-app-store`, and it
refuses to continue on a checksum mismatch. It supports `aarch64`, `arm`
(`armv7l` and `armv8l`), `x86_64` and `i686`.

If a previous installation exists, it is replaced. When run from a terminal
you are asked to confirm first.

---

## After Installation

Verify it works:

```bash
termux-app-store version
```

Then start using it:

```bash
termux-app-store              # open the interactive TUI
tas                           # shorthand for termux-app-store
termux-app-store -h           # CLI help
```

Common first commands:

```bash
termux-app-store update               # refresh the package index
termux-app-store list                 # list all packages
termux-app-store search <query>       # search by name or description
termux-app-store show <package>       # show package details
termux-app-store install <package>    # fast install (pre-built .deb)
```

---

## How Packages Are Installed

Installing the app and installing packages are separate steps.

- **Fast install (default):** `install` downloads a pre-built `.deb` from the
  mirror pool (Cloudflare CDN, GitHub Pages, jsDelivr), checks its SHA256 for
  your architecture, caches it for 7 days and installs it with `dpkg`. A
  cached file is checked again before every install.
- **Source build (fallback):** if no verified binary exists for your package
  and architecture, or if you ask for it with
  `termux-app-store fix-install <package>`, the package is built from its
  `build.sh` using `build-package.sh`.

`build-package.sh` ships inside the pip package, so source builds work after a
pip install without any extra download.

SHA256 is an integrity check that detects corrupted or mismatched files. It
is not a publisher signature. See [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md).

---

## Optional: APT Repository

Packages can also be installed with plain `pkg install` by adding the signed
APT repository. `./tasctl install` does this for you. For other installs:

```bash
curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python
```

or, if you have `tasctl`:

```bash
tasctl install-repo
```

The repository entry uses `signed-by`, never `trusted=yes`:

```text
deb [signed-by=$PREFIX/etc/apt/keyrings/termux-app-store.gpg] https://djunekz.github.io/termux-app-store termux main
```

The installer accepts only a signing key with this exact fingerprint, and adds
nothing if the key does not match:

```text
D39134A177717A5BEBEEAE7105D70CDBB6D80295
```

Compare it with [SECURITY.md](SECURITY.md). To remove the repository:

```bash
tasctl uninstall-repo
```

---

## Update

Use whichever matches how you installed:

```bash
termux-app-store update        # update the app core (pip upgrade in pip mode) and refresh the index
pip install --upgrade termux-app-store
tasctl update                  # for tasctl installs; in pip mode it runs the pip upgrade
termux-app-store upgrade       # upgrade all installed packages that have a newer version
termux-app-store upgrade <package>
```

---

## What Gets Installed and Where

| Item | Location |
|---|---|
| Launcher command | `$PREFIX/bin/termux-app-store` |
| Shorthand command (pip) | `$PREFIX/bin/tas` |
| Controller | `$PREFIX/bin/tasctl` (tasctl and install.sh installs) |
| Installation folder (tasctl, install.sh) | `$PREFIX/lib/.tas/` |
| Install record | `$PREFIX/lib/.tas/.installed` |
| Downloaded `.deb` cache | `~/.cache/termux-app-store/debs/` |
| Index and mirror cache | `~/.cache/termux-app-store/` |
| APT repository entry (optional) | `$PREFIX/etc/apt/sources.list.d/tas.list` |
| APT signing key (optional) | `$PREFIX/etc/apt/keyrings/termux-app-store.gpg` |

The launcher sets `TERMUX_APP_STORE_HOME` to the installation folder, so the
app finds its files no matter where you run it from.

---

## Running from Source (Developers)

For development or review you can run the project directly from a checkout:

```bash
git clone https://github.com/djunekz/termux-app-store
cd termux-app-store
pkg install python -y
pip install --upgrade textual
python termux_app_store/main.py            # open the TUI
python termux_app_store/main.py list       # run a CLI command
```

Run the tests with:

```bash
pip install -e ".[dev]"
make test
```

Optional environment overrides are listed in `.env.example`. Dependencies are pinned in `uv.lock` (`uv sync --extra dev`).

This mode is intended for developers. Normal users should use Option 1.

---

## Packages Directory

A source checkout needs a `packages/` folder next to the app root:

```text
termux-app-store/
  packages/
    package1/
      build.sh
    package2/
      build.sh
  build-package.sh
```

The app locates this folder even if the project is moved or renamed. Note that
`termux-app-store update` removes local package folders that are not in the
official index, so keep your own work-in-progress packages in a separate
branch or folder. See [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md) to contribute one.

---

## Security Notice

- Install only from the official repository, `djunekz/termux-app-store`, or
  from PyPI
- Do not download the app or its binaries from third-party sources
- The official installers verify the source, and `install.sh` verifies the
  release checksum
- Do not add the APT repository with `[trusted=yes]`
- Read a package's `build.sh` before building it from source

See [SECURITY.md](SECURITY.md) for the full policy and how to report a problem.

---

## Troubleshooting

Short answers for the most common install problems. For the full guide, see
[TROUBLESHOOTING.md](TROUBLESHOOTING.md).

**command not found: termux-app-store**

```bash
hash -r
ls $PREFIX/bin/termux-app-store
```

If the file is missing, reinstall with your chosen method.

**Unsupported architecture**

Your CPU is not supported by the current releases. Check it with `uname -m`.

**Permission denied**

```bash
chmod +x $PREFIX/bin/termux-app-store
```

**No module named textual**

```bash
pip install --upgrade textual
```

**build-package.sh not found**

```bash
pip install --upgrade termux-app-store
termux-app-store update
```

**Diagnose the environment**

```bash
./tasctl doctor
python doctor.py --brief
```

---

## Uninstall

### Option 1: installed with pip

```bash
pip uninstall termux-app-store
```

### Option 2: installed with tasctl or install.sh

```bash
tasctl uninstall
```

This removes the launcher, the installation folder and the APT repository
entry. You can also run it from the project folder as `./tasctl uninstall`.

### Option 3: uninstall script

From the project folder, `bash uninstall.sh` asks for confirmation, then
removes the binaries, the installation folder, the environment variables it
added to your shell configuration and the cache folder
`~/.cache/termux-app-store`.

### Option 4: manual removal

```bash
rm -f $PREFIX/bin/termux-app-store
rm -f $PREFIX/bin/tasctl
rm -rf $PREFIX/lib/.tas
rm -rf ~/.cache/termux-app-store
```

### Things uninstalling the app does not do

- Packages you installed through Termux App Store stay installed. Remove them
  first if you want them gone: `termux-app-store uninstall <package>`
- A pip uninstall leaves the cache and any APT repository entry in place.
  Remove the entry with `tasctl uninstall-repo` and the cache with
  `rm -rf ~/.cache/termux-app-store`

---

## Support

- Guide: [SUPPORT.md](SUPPORT.md)
- Issues: [GitHub Issues](https://github.com/djunekz/termux-app-store/issues)
- Maintainer: [@djunekz](https://github.com/djunekz)
- Email: gab288.gab288@passinbox.com
