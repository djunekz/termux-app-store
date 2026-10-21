# Support

Welcome to the **Termux App Store** support guide.

This document explains where to get help, how to report a problem, and what
information to include so that maintainers and the community can respond
quickly. It applies to v0.9.1 and later.

---

## Quick Links

| I want to... | Go to |
|---|---|
| Fix a common problem myself | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Find a quick answer | [FAQ.md](FAQ.md) |
| Install or uninstall | [INSTALL.md](INSTALL.md) |
| Ask a question or get help | [Q&A Discussions](https://github.com/djunekz/termux-app-store/discussions/categories/q-a) |
| Report a bug | [Open an issue](https://github.com/djunekz/termux-app-store/issues/new/choose) (Bug Report) |
| Suggest a feature | [Open an issue](https://github.com/djunekz/termux-app-store/issues/new/choose) (Feature Request) |
| Ask for a package to be added | [Open an issue](https://github.com/djunekz/termux-app-store/issues/new/choose) (Package Request) |
| Submit my own package | [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md) |
| Report a security problem | [SECURITY.md](SECURITY.md) (private, never public) |
| Report an accessibility barrier | [ACCESSIBILITY.md](ACCESSIBILITY.md) |

---

## Before Asking for Help

Many problems are already documented or fixed. Please check the following
first:

1. Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md) and [FAQ.md](FAQ.md).
2. Search existing [issues](https://github.com/djunekz/termux-app-store/issues)
   and [discussions](https://github.com/djunekz/termux-app-store/discussions),
   including closed ones.
3. Update to the latest version and try again:
   ```bash
   pip install --upgrade termux-app-store
   termux-app-store update
   ```
4. Run the built-in diagnosis and read its output (see the next section).
5. If the problem is about a build, read the log output from the failed
   step. The first error is usually the real cause.

---

## Collect Diagnostic Information

Including the following details lets maintainers reproduce your problem
without a long back-and-forth.

```bash
termux-app-store version     # application version
uname -m                     # CPU architecture
python --version             # Python version
pip show textual             # Textual version (must be 8.0.0 or newer)
echo $PREFIX                 # Termux prefix
which termux-app-store       # which copy is being run
```

Then run the environment doctor. From the project folder:

```bash
./tasctl doctor                # installation and environment checks
python doctor.py --brief       # one line per check
python doctor.py --json        # machine-readable output, useful to attach
python doctor.py --pkg <name>  # deep check of one package's build.sh
```

`python doctor.py --fix` applies the fixes it can do automatically, for
example migrating an old repository entry. Run it without `--fix` first so
you know what will change.

Also include:

- The exact command you ran and the full error message or log output
- Whether you installed with `pip` or with `tasctl` / `install.sh`
- Whether you used the TUI or the CLI
- Your Termux version and Android version
- Whether the problem happens with one package or with all of them

Please remove tokens, passwords and private paths from logs before posting
them. Logs are public on GitHub.

---

## Bug Reports

Use the **Bug Report** issue template when:

- A command crashes or prints an unexpected error
- An install, upgrade or uninstall fails
- Checksum verification fails for a package that should be valid
- The TUI freezes, renders incorrectly or ignores input
- A package build fails in CI or on your device
- Documentation is wrong or out of date

A good report contains:

- A short, clear description of the problem
- Steps to reproduce, starting from a clean state if possible
- Expected behavior and actual behavior
- The diagnostic information listed above

Reports without enough detail may be closed until more information is
provided. They can be reopened at any time.

---

## Help and Questions

Use the **Support / Help Request** template or the
[Q&A discussion category](https://github.com/djunekz/termux-app-store/discussions/categories/q-a)
for:

- "How do I do X?" questions
- Help understanding an error message
- Choosing between binary install and source build
- Contribution guidance and best practices

Use Discussions for open-ended conversation and design ideas so the issue
tracker stays focused on actionable work. Blank issues are disabled, so
every issue must use one of the templates.

---

## Feature Requests

Use the **Feature Request** template for new tooling, workflow
improvements or validation enhancements. Explain:

- The problem you are trying to solve
- Why it benefits other users, not only you
- Alternatives you considered and their trade-offs

---

## Package Requests and Package Problems

- **Request a new package:** use the **Package Request** template.
- **Submit a package yourself:** follow [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)
  and the **Package Submission** template. Validate first with
  `./termux-build lint packages/<name>`.
- **A package fails to build or run:** open a Bug Report and include the
  package name, its version (`termux-app-store show <name>`) and the log.
- **A package misbehaves but installs fine:** the problem may be in the
  upstream software. Check the upstream project first. Bugs in third-party
  software are not handled here (see "What Is Not Support").
- **Outdated package version:** packages are checked against their upstream
  automatically every 12 hours. If a version is still behind after that,
  open an issue with the package name and the expected version.

Packages that describe credential brute-forcing, denial of service,
backdoor generation, or tracking of people without a stated defensive use
are not accepted into the catalog.

---

## Security Issues

**Do not report security issues in public issues or discussions.**

Report them privately:

- GitHub Security Advisories:
  [report a vulnerability](https://github.com/djunekz/termux-app-store/security/advisories/new)
- Email: gab288.gab288@passinbox.com

This includes suspected supply-chain problems, checksum bypasses, installer
hijacking, and any concern about the APT repository signing key. The key
fingerprint is published in [SECURITY.md](SECURITY.md). If the key shown
during installation does not match, stop and report it privately.

---

## Accessibility

If the CLI, the TUI or the documentation is hard to use because of an
accessibility barrier, tell us. See [ACCESSIBILITY.md](ACCESSIBILITY.md)
for current status, known limitations and how to report. Using the CLI
(`tas search`, `tas show`, `tas install`) is recommended if the full-screen
TUI does not work well with your setup.

---

## Private Contact

For matters that cannot be public (security, accessibility, conduct
concerns), email gab288.gab288@passinbox.com. For anything else, please use
GitHub so others with the same problem can find the answer.

---

## What Is Not Support

The following are out of scope:

- Unofficial forks, mirrors or repackaged installers. Always install from
  the official repository, `djunekz/termux-app-store`
- Environments modified in unsupported ways, for example an APT repository
  entry using `[trusted=yes]` or a replaced signing key
- Running with checksum or recipe verification disabled through
  `TERMUX_APP_STORE_ALLOW_UNVERIFIED_RECIPE` or
  `TERMUX_APP_STORE_ALLOW_UNVERIFIED_BUILD_SH` and then hitting problems
  caused by unreviewed scripts
- General Linux, Android or Termux troubleshooting that is not specific to
  Termux App Store (for those, see the official Termux documentation and
  community)
- Bugs in third-party software distributed through packages here
- Requests to remove safety checks such as SHA256 verification

---

## Response Expectations

This project is maintained by volunteers in their available time, so no
response time is guaranteed.

- Security reports are acknowledged within 72 hours, with an initial
  assessment within 7 days (see [SECURITY.md](SECURITY.md))
- Critical bugs, such as broken installs or failing signature
  verification, are prioritized
- Other issues are handled as time allows

Please do not post the same question in several places, and avoid
"bump" comments. Be patient and respectful, and follow the
[Code of Conduct](CODE_OF_CONDUCT.md).

---

## How You Can Help

- Improve or translate documentation
- Reproduce issues reported by others and share what you find
- Answer questions in Discussions
- Review pull requests and package submissions
- Report problems with clear, complete information

See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

---

## Supporting the Project

If Termux App Store is useful to you, you can support the maintainer
through the sponsor links on the repository page. Support is entirely
optional and does not affect how issues are prioritized.

---

## Related Documents

[README](README.md) | [INSTALL](INSTALL.md) | [FAQ](FAQ.md) |
[TROUBLESHOOTING](TROUBLESHOOTING.md) | [SECURITY](SECURITY.md) |
[PRIVACY](PRIVACY.md) | [ACCESSIBILITY](ACCESSIBILITY.md) |
[CONTRIBUTING](CONTRIBUTING.md) | [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md)

Maintainer: [@djunekz](https://github.com/djunekz)
