# Frequently Asked Questions (FAQ)

This document answers common questions about **Termux App Store**. It applies
to v0.9.1 and later.

Quick navigation: [General](#general) | [Installing the App](#installing-the-app)
| [Installing Packages](#installing-packages) | [Security and Trust](#security-and-trust)
| [Packages and Contributing](#packages-and-contributing) | [Troubleshooting and Help](#troubleshooting-and-help)

---

## General

### What is Termux App Store?

**Termux App Store** is a terminal package manager for Termux with two
interfaces: a full-screen TUI built with [Textual](https://textual.textualize.io)
and a CLI. It lets you browse, search, install, upgrade and remove community
tools on your Android device.

By default it installs pre-built `.deb` files that are checked against a
SHA256 checksum, and it falls back to building from a package's `build.sh`
when no verified binary is available.

### Is this an official Termux project?

No. Termux App Store is an independent project and is not affiliated with the
official Termux maintainers.

### How is it different from `pkg`, `termux-packages` and TUR?

- `pkg` installs from the official Termux repositories, which are maintained
  by the Termux team.
- TUR (Termux User Repository) is a separate curated repository with its own
  review process.
- Termux App Store is a community catalog. Anyone can submit a package
  recipe through a pull request, and recipes go through automated validation
  and review before they are published.

It works alongside `pkg`, not instead of it. Installed packages are normal
`.deb` packages managed by `dpkg`.

### What do the commands `termux-app-store` and `tas` do?

They are the same program. Run it with no arguments to open the TUI, or with
a command such as `list`, `search`, `install` or `upgrade` to use the CLI.
Run `termux-app-store help` for the full list.

### What is `tasctl`?

`tasctl` is the controller script for the app itself. It installs, updates
and uninstalls Termux App Store, adds or removes the APT repository
(`install-repo`, `uninstall-repo`), and runs an environment check (`doctor`).
It is not used to install packages.

### What is `termux-build`?

`termux-build` is a validation helper for contributors. It can create, lint,
explain and check package recipes. It only reads and validates; it does not
upload anything.

### Is the project open source?

Yes. The source code is on GitHub under the MIT license. The app itself is
written in Python and is distributed as a Python package. Pre-built `.deb`
files are a distribution format for packages, not closed-source software. See
[BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md).

### Who maintains it?

The project is maintained by [@djunekz](https://github.com/djunekz) with help
from community contributors.

---

## Installing the App

### Which installation method should I use?

Use `pip install termux-app-store` unless you have a reason not to. It is the
simplest and works on all supported architectures. `tasctl` is a good choice on
low-memory devices or if you also want the APT repository, and `install.sh`
installs the latest official release archive. See [INSTALL.md](INSTALL.md).

### Which CPU architectures are supported?

The documented architectures are `aarch64`, `armv7l` and `x86_64`. The
installer scripts also recognize `i686`, but support for it is not
guaranteed. Pre-built binaries are published per package and architecture, so
a package may be available for one architecture and not another. A source
build with `fix-install` can fill the gap.

### Is root required?

No. Termux App Store runs entirely in user space inside Termux.

### How do I update the app?

```bash
termux-app-store update
```

or `pip install --upgrade termux-app-store` or `tasctl update`, depending on
how you installed it.

### How do I uninstall it?

```bash
pip uninstall termux-app-store     # pip installs
tasctl uninstall                   # tasctl and install.sh installs
```

Packages you installed with it stay installed until you remove them with
`termux-app-store uninstall <package>`. See [INSTALL.md](INSTALL.md) for all
options.

### Can I move the project folder?

Yes. The app detects its own location, supports symlinks and repairs cached
paths if the folder is moved or renamed. If it does not recover, set
`TERMUX_APP_STORE_HOME` to the folder that contains `packages/`.

### Can I run it from any directory?

Yes. The launcher sets the location for you, so you can run it from anywhere.

---

## Installing Packages

### How does installing a package work?

`termux-app-store install <package>` downloads a pre-built `.deb` from the
fastest reachable mirror (Cloudflare CDN, GitHub Pages or jsDelivr), verifies
its SHA256 for your architecture, caches it and installs it with `dpkg`. If no
verified binary exists, the package is built from source instead.

### Why does it try binaries first now?

Binary installs are much faster and use less battery and storage than a build.
Source builds remain available as a fallback and with
`termux-app-store fix-install <package>`.

### What is the difference between `update` and `upgrade`?

- `update` refreshes the app core and the package index so you can see what is
  new or outdated.
- `upgrade` installs newer versions of packages you already have. Use
  `upgrade <package>` to upgrade just one.

### Can I install several packages at once?

Yes:

```bash
termux-app-store install tdoc ttyper aichat
termux-app-store uninstall tdoc ttyper
```

A summary is shown when it finishes.

### Does it work offline?

Partly. The interface works with data already on your device, but fetching
the index, downloading packages and building from source need the network.
A previously downloaded `.deb` can be reused from the cache (it is kept for 7
days) if its checksum can be verified.

### Where are things stored?

| Item | Location |
|---|---|
| Downloaded `.deb` files | `~/.cache/termux-app-store/debs/` |
| Package index and mirror data | `~/.cache/termux-app-store/` |
| Installation folder (tasctl, install.sh) | `$PREFIX/lib/.tas/` |
| Package recipes (source checkout) | `packages/<name>/build.sh` |

Check or clear the binary cache with `termux-app-store cache info` and
`termux-app-store cache clear`.

### What are mirrors?

Mirrors are alternative download locations for the package files. The app
tests them and uses the fastest one it can reach, then remembers the result
for 24 hours. Run `termux-app-store mirrors` to see their status.

### Why does an install seem to freeze?

Common reasons are a slow network, a large download or a compile step in
progress. Check the log panel for activity before cancelling. If it is really
stuck, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

### Does it modify my system?

It works inside the Termux environment and does not touch Android system
files. It does:

- Install packages with `dpkg` into the Termux prefix
- Store its own files and cache in your Termux home and `$PREFIX/lib/.tas`
- Add an APT repository entry and key if you use `tasctl install` or
  `install-repo` (a pip install does not add one by itself)

All of this can be undone, see [INSTALL.md](INSTALL.md#uninstall).

---

## Security and Trust

### Is it safe to use?

It includes several protections, but no tool can make third-party software
risk-free:

- Every `.deb` must match a per-architecture SHA256 or it is refused, including
  files already in the cache
- Recipes (`build.sh`) are checked against a checksum from the index before
  they are used
- The APT repository is signed, and clients verify it with `signed-by`
- The official installers refuse to run from an unofficial source
- Packages go through automated validation and review

You should still trust the source, and read a recipe before building from
source. Packages are third-party software maintained upstream.

### Does SHA256 prove a package is trustworthy?

No. SHA256 detects corruption and mismatched files. It is an integrity
check, not a publisher signature, and it cannot tell you whether the software
itself is safe.

### How do I check the APT signing key?

The expected fingerprint is published in [SECURITY.md](SECURITY.md) and is
also pinned in the installers:

```text
D39134A177717A5BEBEEAE7105D70CDBB6D80295
```

The installers add nothing if a downloaded key does not match it. Never use
`[trusted=yes]`.

### What data does it collect?

None. There is no account, no analytics and no telemetry. The network is used
to fetch the index, mirrors, checksums, `.deb` files and package sources, and
only when you run a command that needs it. See [PRIVACY.md](PRIVACY.md).

### Why were some packages removed from the catalog?

Packages whose descriptions state credential brute-forcing, denial of
service, backdoor generation or tracking of people without a stated defensive
use are not accepted, and some earlier entries were removed for this reason.
See [CONTRIBUTING.md](CONTRIBUTING.md) and [DISCLAIMER.md](DISCLAIMER.md).

### How do I report a security problem?

Privately, never in a public issue. Use a GitHub Security Advisory or email
gab288.gab288@passinbox.com. Details are in [SECURITY.md](SECURITY.md).

---

## Packages and Contributing

### Can I add my own packages?

To share a package with everyone, submit a pull request. Create a recipe at
`packages/<your-tool>/build.sh`, validate it, then open the PR:

```bash
./termux-build create your-tool
./termux-build lint packages/your-tool
```

Follow [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md). Use `-` instead of spaces in
package names.

Note that `termux-app-store update` removes local package folders that are not
in the official index, so do not keep unpublished recipes in `packages/` of an
installed copy.

### Can I request a package?

Yes. Open an issue with the **Package Request** template.

### How are package versions kept up to date?

An automated workflow checks packages against their upstream (GitHub releases
or tags and npm) twice a day and updates the version and checksum in the
recipe. Some packages opt out, and unusual sources are handled by hand. If a
version is behind for long, open an issue.

### How can I contribute?

Contributions are welcome: packages, bug fixes, documentation, translations,
reviews and testing. See [CONTRIBUTING.md](CONTRIBUTING.md) and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## Troubleshooting and Help

### Something does not work. What should I do first?

1. Update: `termux-app-store update`
2. Run the checks: `./tasctl doctor` or `python doctor.py`
3. Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### A pre-built install failed. Is there a fallback?

Yes. Use `termux-app-store fix-install <package>` to build from source.

### Is the TUI accessible?

The CLI is recommended for screen readers and keyboard-only use, because every
TUI action is also a command. Current limitations are documented honestly in
[ACCESSIBILITY.md](ACCESSIBILITY.md).

### Where can I report bugs, ask questions or request features?

- Bugs and requests: [GitHub Issues](https://github.com/djunekz/termux-app-store/issues)
- Questions: [Q&A Discussions](https://github.com/djunekz/termux-app-store/discussions/categories/q-a)
- Full guide: [SUPPORT.md](SUPPORT.md)

---

## Final Notes

If something feels broken:

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- Read [SUPPORT.md](SUPPORT.md) and open an issue with the details it asks for
- Or read the source, it is all on GitHub
