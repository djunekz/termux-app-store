# Troubleshooting

This document helps you diagnose and fix common problems when using
**Termux App Store**. It applies to v0.9.1 and later.

If your problem is not listed here, see [SUPPORT.md](SUPPORT.md) for how to
ask for help.

---

## Table of Contents

1. [Start Here: Quick Diagnosis](#start-here-quick-diagnosis)
2. [Command Not Found](#command-not-found)
3. [Wrong Copy Is Running or Version Looks Old](#wrong-copy-is-running-or-version-looks-old)
4. [Permission Denied](#permission-denied)
5. [Unsupported Architecture](#unsupported-architecture)
6. [Python and Textual Errors](#python-and-textual-errors)
7. [Package Not Found](#package-not-found)
8. [Fast Install Fails](#fast-install-fails)
9. [Checksum Errors](#checksum-errors)
10. [Source Build Fails](#source-build-fails)
11. [APT Repository and Signing Key Problems](#apt-repository-and-signing-key-problems)
12. [Network Issues](#network-issues)
13. [UI Issues](#ui-issues)
14. [Moved Folder, Cache and Path Issues](#moved-folder-cache-and-path-issues)
15. [Clean Reinstall](#clean-reinstall)
16. [Reporting a Bug](#reporting-a-bug)

---

## Start Here: Quick Diagnosis

Run these first. They solve or explain most problems.

```bash
termux-app-store version     # installed version
uname -m                     # CPU architecture
which termux-app-store       # which copy runs
termux-app-store mirrors     # are the download mirrors reachable?
```

Then run the environment doctor from the project folder:

```bash
./tasctl doctor              # installation checks
python doctor.py             # full diagnosis
python doctor.py --brief     # one line per check
python doctor.py --fix       # also apply automatic fixes
python doctor.py --pkg <name>  # deep check of one package's build.sh
```

The doctor checks the system, Python, required tools, the TAS installation,
the APT repository entry, the project layout, leftover builds and network
reachability. Run it without `--fix` first so you can see what would change.

Keep the tools current, because many problems are fixed in newer releases:

```bash
pip install --upgrade termux-app-store
termux-app-store update
```

---

## Command Not Found

### Error

```text
termux-app-store: command not found
```

### Solution

Clear the shell command cache, then try again:

```bash
hash -r
termux-app-store version
```

If it still fails, check whether the program exists:

```bash
ls $PREFIX/bin/termux-app-store
ls $PREFIX/bin/tas
```

If you installed with pip, confirm it is installed and reinstall if needed:

```bash
pip show termux-app-store
pip install --force-reinstall termux-app-store
```

If you installed with `tasctl` or `install.sh` and the file is missing,
reinstall (see [Clean Reinstall](#clean-reinstall)). Opening a new Termux
session also refreshes the path.

---

## Wrong Copy Is Running or Version Looks Old

### Symptom

- `termux-app-store version` shows an older version after you upgraded
- Behavior does not match the documentation
- Both `pip` and `tasctl` were used to install at different times

### Cause

The pip install and the `tasctl` / `install.sh` install can both place a
`termux-app-store` command in `$PREFIX/bin`. The one that was written last
is the one that runs.

### Solution

```bash
which termux-app-store
termux-app-store version
```

Pick one install method and remove the other, then reinstall with the method
you chose:

```bash
pip uninstall termux-app-store      # remove the pip copy
./tasctl uninstall                  # remove the tasctl copy
```

See [Clean Reinstall](#clean-reinstall) for the full steps.

---

## Permission Denied

### Error

```text
Permission denied
```

### Solution

Make sure the command is executable:

```bash
chmod +x $PREFIX/bin/termux-app-store
```

If the error appears while writing files, confirm you are running Termux as
its normal user and not through another environment such as a proot
session. Termux App Store runs entirely in user space and never needs root.

If you see this while adding the APT repository key or entry, see
[APT Repository and Signing Key Problems](#apt-repository-and-signing-key-problems).

---

## Unsupported Architecture

### Error

```text
Unsupported architecture
```

### Cause

Your device CPU is not supported by the current releases.

### Solution

Check your architecture:

```bash
uname -m
```

Documented as supported:

- `aarch64` (recommended)
- `armv7l`
- `x86_64`

Some packages are published as pre-built binaries only for certain
architectures. If a pre-built `.deb` is not available for your architecture,
use a source build instead:

```bash
termux-app-store fix-install <package>
```

---

## Python and Textual Errors

### Error

```text
ModuleNotFoundError: No module named 'textual'
```

or the TUI fails to start with a Textual-related error.

### Cause

Termux App Store needs Python 3.9 or newer and Textual 8.0.0 or newer. A
pip install pulls Textual in automatically. Running from a source checkout
does not.

### Solution

```bash
pkg install python -y
pip install --upgrade textual
```

Check the versions:

```bash
python --version
pip show textual
```

If you run from source, start the app from the project folder with:

```bash
python termux_app_store/main.py
```

The CLI does not need a working Textual setup for most commands, so
`termux-app-store list` and `termux-app-store install <package>` can still be
used while you fix the TUI.

---

## Package Not Found

### Error

```text
Package '<name>' not found.
```

### Solution

1. Check the spelling and search for the package:
   ```bash
   termux-app-store search <part-of-name>
   termux-app-store list
   ```
2. Package names use `-`, never spaces, for example `my-tool-name`.
3. Refresh the package index. The index is cached for about one hour:
   ```bash
   termux-app-store update
   ```
4. If the package was added very recently, wait for the index to be
   regenerated and try again.

### Error

```text
packages/ not found
```

### Cause

This only happens when running from a source checkout whose `packages/`
folder is missing, for example after a partial copy.

### Solution

Make sure the structure exists, then restart:

```text
termux-app-store/
  packages/
    <package-name>/
      build.sh
```

Users who installed with `pip` or the installer normally never see this error.

---

## Fast Install Fails

`termux-app-store install <package>` downloads a pre-built `.deb`, checks its
SHA256, caches it and installs it with `dpkg`. If any step fails, try these in
order.

### The pre-built .deb is not available

```text
Verified pre-built .deb not available for this package/arch
```

No trusted checksum or binary exists for your package and architecture, so
the binary was refused. The installer falls back to a source build. You can
also request it directly:

```bash
termux-app-store fix-install <package>
```

### A mirror is slow or unreachable

```bash
termux-app-store mirrors
```

This tests the mirrors in the pool: Cloudflare CDN, GitHub Pages and
jsDelivr. The fastest reachable one is used and remembered for 24 hours. If
all fail, see [Network Issues](#network-issues).

### The cached file is bad

A cached `.deb` is deleted automatically if it is older than 7 days or does
not match its checksum. To clear the whole cache manually:

```bash
termux-app-store cache info
termux-app-store cache clear
```

### dpkg install failed

```text
dpkg install failed
```

A dependency is probably missing. Repair and retry:

```bash
apt-get install -f
termux-app-store install <package>
```

If it still fails, the file may not match your device. Use
`termux-app-store fix-install <package>` to build from source.

---

## Checksum Errors

### Error

```text
SHA256 mismatch - file corrupt or tampered
```

### Cause

The downloaded or cached `.deb` does not match the expected SHA256. This is
usually a corrupted or partial download, a stale mirror, or a package that was
just rebuilt while the mirror still served the old file.

### Solution

1. Clear the cache and retry:
   ```bash
   termux-app-store cache clear
   termux-app-store update
   termux-app-store install <package>
   ```
2. Try again later. Mirrors can take time to catch up after a rebuild.
3. Use a source build:
   ```bash
   termux-app-store fix-install <package>
   ```
4. If the mismatch is repeatable, open a Bug Report with the package name,
   version, architecture and the full message. If you suspect tampering,
   report it privately instead, as described in [SECURITY.md](SECURITY.md).

Note: SHA256 detects corruption and mismatched files. It is an integrity
check, not a publisher signature.

---

## Source Build Fails

Source builds use `build-package.sh` and the package's `build.sh`.

### Install stops with errors in the log

Common causes:

- A missing dependency
- An invalid or outdated `build.sh`
- Network interruption or an HTTP 404 on the source download
- The upstream source was removed or moved
- A checksum in `build.sh` no longer matches the upstream file

Scroll the log and look at the first error, not the last. Then:

- Install the missing package named in the log with `pkg install <name>`
- Retry, in case the network was interrupted
- Run `python doctor.py --pkg <name>` to check the recipe
- Report it as a Bug Report if the recipe itself is broken

### build-package.sh not found

```text
build-package.sh not found.
```

Update the application. The script ships inside the pip package, so this
usually means an old or incomplete install:

```bash
pip install --upgrade termux-app-store
termux-app-store update
```

### build-package.sh checksum or syntax error

```text
build-package.sh SHA256 mismatch - refusing to run it
build-package.sh failed bash syntax check - refusing to run it
```

The script was not trusted, so it was not executed. This is a safety feature.
Update to the latest release and retry. Do not bypass it unless you have read
the script yourself.

### Recipe refused: no checksum in the index

```text
Refresh the package index, or set TERMUX_APP_STORE_ALLOW_UNVERIFIED_RECIPE=1
after reviewing the recipe.
```

A package recipe (`build.sh`) is downloaded only when it matches the
`recipe_sha256` published in the index. First refresh the index:

```bash
termux-app-store update
```

Only set `TERMUX_APP_STORE_ALLOW_UNVERIFIED_RECIPE=1` (or
`TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH=1`) if you have read the script
and accept the risk. These options are not supported configurations.

### Dependencies could not be installed

```text
FATAL ... missing dependencies
```

The build installs the packages named in `TERMUX_PKG_DEPENDS` and retries up
to five times with a delay. It stops if any are still missing, instead of
failing later with errors such as `cargo: command not found`,
`go: command not found` or `npm: command not found`.

Typical causes are a slow or rate-limited Termux mirror (HTTP 429) or a
mirror that is mid-update. Fix:

```bash
pkg update
termux-change-repo
```

Then run the install again.

---

## APT Repository and Signing Key Problems

Termux App Store also publishes a signed APT repository so packages can be
installed with `pkg install`. The repository entry is:

```text
deb [signed-by=$PREFIX/etc/apt/keyrings/termux-app-store.gpg] https://djunekz.github.io/termux-app-store termux main
```

Add it with one of:

```bash
curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python
./tasctl install-repo
```

Remove it with `./tasctl uninstall-repo`.

### Signature warnings during `pkg update`

```text
NO_PUBKEY ...
The repository ... is not signed.
Release.gpg / InRelease ... could not be verified
```

The signing key is missing or the entry is outdated. Re-add the repository,
which downloads and validates the key again:

```bash
./tasctl install-repo
pkg update
```

Or let the doctor repair it:

```bash
python doctor.py --fix
```

### Old entry with trusted=yes

Earlier versions used `deb [trusted=yes]`, which disables signature
checking. Current versions migrate it to `signed-by`. The doctor reports it
as a warning and `--fix` migrates it. Do not add `[trusted=yes]` yourself.

### The installer rejected the key

The installer accepts only a key that is exactly one primary key with the
pinned fingerprint:

```text
D39134A177717A5BEBEEAE7105D70CDBB6D80295
```

If the key is rejected, nothing is added and the repository is never
installed unsigned. This can mean a corrupted download or a replaced file on
the download host. Retry once. If it is rejected again, do not work around
it. Compare the fingerprint with [SECURITY.md](SECURITY.md) and report it
privately.

### "Repository added, but pkg update failed"

The repository entry was written, but `pkg update` returned an error. This is
usually a network or mirror problem unrelated to the repository itself. Fix
the error shown above that message, then run:

```bash
pkg update
```

### Remove the repository completely

```bash
./tasctl uninstall-repo
```

This removes `tas.list` and the keyring file, then runs `pkg update`.

---

## Network Issues

### Error

```text
curl: (6) Could not resolve host
```

or downloads that stall or time out.

### Solution

- Check your internet connection and DNS
- Test the download mirrors:
  ```bash
  termux-app-store mirrors
  ```
- Change the Termux package mirror, which also helps with HTTP 429
  responses:
  ```bash
  termux-change-repo
  pkg update
  ```
- Retry later if a mirror or GitHub is having an outage
- If you use a VPN, proxy or restrictive network, try without it

Package metadata and downloads always need the network. The interface itself
works offline, and cached `.deb` files that pass checksum verification can
be reinstalled without a download.

---

## UI Issues

### Symptoms

- The right panel does not update
- ENTER does nothing
- The screen freezes during an install
- Text or borders look broken

### Causes

- The terminal window is too small
- An outdated Termux or Textual
- A background process was interrupted
- Several installs are running at once

### Solution

- Enlarge the terminal or reduce the font size
- Restart Termux, then reopen the TUI
- Run one install at a time
- Update Textual: `pip install --upgrade textual`
- Use the CLI instead. Every TUI action also exists as a command:
  ```bash
  termux-app-store search <query>
  termux-app-store show <package>
  termux-app-store install <package>
  ```

Keyboard shortcuts in the TUI: `Ctrl+R` refresh, `Ctrl+I` install selected,
`Ctrl+Q` quit. In many terminals `Ctrl+I` is the same key as `Tab`, so it may
not work as install. Use the Termux extra keys row for `Ctrl`, `Tab` and
arrow keys. See [ACCESSIBILITY.md](ACCESSIBILITY.md) for more.

---

## Moved Folder, Cache and Path Issues

### Symptom

The app fails after you moved or renamed the project folder, or it keeps
using stale data.

### Solution

The app detects its own location and repairs cached paths automatically. If
it does not, restart it. If a source checkout still fails, point it at the
right folder:

```bash
export TERMUX_APP_STORE_HOME=/path/to/termux-app-store
```

The folder must contain `packages/`. Run `./tasctl doctor` to check this
setting.

The cache lives in `~/.cache/termux-app-store/` (or under `$XDG_CACHE_HOME`
if you set it):

| Item | Purpose | Lifetime |
|---|---|---|
| `debs/` | Downloaded `.deb` files | 7 days |
| `index.json` | Package index | 1 hour |
| `best-mirror.json` | Fastest mirror | 24 hours |
| `path.json` | Remembered app location | until it changes |

To reset the binary cache safely, use `termux-app-store cache clear`. To
reset everything, delete the folder:

```bash
rm -rf ~/.cache/termux-app-store
```

---

## Clean Reinstall

If everything else fails, remove and reinstall.

### pip install

```bash
pip uninstall termux-app-store
pip install termux-app-store
```

### tasctl install

```bash
./tasctl uninstall
```

or remove manually:

```bash
rm -f $PREFIX/bin/termux-app-store
rm -rf $PREFIX/lib/.tas
```

Then install again:

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

Optionally clear cached data as well:

```bash
rm -rf ~/.cache/termux-app-store
```

Always install from the official repository, `djunekz/termux-app-store`. The
installer refuses to continue when it cannot confirm the official source.

---

## Reporting a Bug

Before opening an issue, collect:

- `termux-app-store version`
- Architecture (`uname -m`), Termux version and Android version
- How you installed (`pip` or `tasctl`)
- The exact command and the full error output
- The result of `./tasctl doctor` or `python doctor.py --brief`

Remove any private information from logs, then open an issue:
[Open an issue](https://github.com/djunekz/termux-app-store/issues/new/choose)

For security problems, do not use public issues. See
[SECURITY.md](SECURITY.md).

---

## Related Documents

[SUPPORT](SUPPORT.md) | [FAQ](FAQ.md) | [INSTALL](INSTALL.md) |
[SECURITY](SECURITY.md) | [ACCESSIBILITY](ACCESSIBILITY.md)

Maintainer: [@djunekz](https://github.com/djunekz)
