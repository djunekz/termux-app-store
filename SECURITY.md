# Security Policy

Security is a core principle of **Termux App Store**.
This project provides tooling and infrastructure used to build and
validate Termux packages, therefore **supply-chain integrity** and
**trust** are critical.

---

## Supported Versions

Security fixes apply to:

- The `master` branch
- The latest stable release (if applicable)

Older versions may not receive security updates.

---

## Reporting a Vulnerability

**Do NOT report security issues via public GitHub issues.**

If you discover a vulnerability, please report it responsibly.

### How to Report

**Preferred — GitHub Security Advisories (private):**
[Click Here](https://github.com/djunekz/termux-app-store/security/advisories/new)

**Alternative — Private contact:**
gab288.gab288@passinbox.com

Provide as much detail as possible:

- Description of the issue
- Affected components
- Steps to reproduce
- Potential impact
- Suggested mitigation (if any)

---

## APT Repository Signing Key

The APT repository at `https://djunekz.github.io/termux-app-store` is
signed. `InRelease` and `Release.gpg` are produced by CI with the key
below, and clients verify them with `signed-by`.

| | |
|---|---|
| Owner | djunekz <gab288.gab288@passinbox.com> |
| Type | RSA 4096 |
| Primary key ID | `05D70CDBB6D80295` |
| Fingerprint | `D391 34A1 7771 7A5B EBEE AE71 05D7 0CDB B6D8 0295` |

Plain form for copy and paste:

```
D39134A177717A5BEBEEAE7105D70CDBB6D80295
```

The same fingerprint is pinned in `install-repo.py`, `tasctl` and
`doctor.py`. The installers refuse any key that is not exactly one primary
key with this fingerprint, so a replaced `termux-app-store.gpg` on the
download host is rejected. Compare the fingerprint above with the one shown
during installation, and never use `[trusted=yes]`.

Key rotation: a new key is introduced only through a reviewed commit that
updates the pinned fingerprint and this table. Report suspected key
compromise privately, as described above.

---

## Response Timeline

We aim to:

- Acknowledge reports within **72 hours**
- Provide an initial assessment within **7 days**
- Release a fix as soon as reasonably possible

Timelines may vary depending on severity.

---

## Automated Security Controls

This repository uses:

- Automated CI validation
- Script & build file linting
- Coverage checks for core tooling
- Controlled GitHub Actions workflows
- SHA256 integrity verification for all packages
- Official source verification (`verify_official_release`)

These measures reduce the risk of:

- Malicious packages
- Hidden build behavior
- Supply-chain attacks

---

## Scope of Security Issues

### In Scope

- Malicious code submissions
- Build script abuse
- CI pipeline manipulation
- Unauthorized data exfiltration
- Dependency or toolchain vulnerabilities
- SHA256 / integrity bypass
- Installer or updater hijacking

### Out of Scope

- Vulnerabilities in third-party software packaged by users
- User misconfiguration
- Unsupported forks or modified environments

---

## Confidentiality & Disclosure

- All security reports are handled privately
- Public disclosure occurs **only after mitigation**
- Credit will be given to reporters unless anonymity is requested

---

## Zero Tolerance Policy

The following will result in immediate action:

- Intentional backdoors
- Crypto miners
- Obfuscated malicious logic
- Supply-chain compromise attempts

Offending contributions will be removed and access revoked.

---

## Trust Model

Trust is earned through:

- Transparent contributions
- Reviewable changes
- Automated validation
- Consistent community behavior

Security is everyone's responsibility.

---

## Policy Changes

This security policy may be updated as the project evolves.
Significant changes will be documented and communicated publicly.

---

## Final Note

Security policies exist to protect:

- Contributors
- Users
- The broader Termux ecosystem

Responsible disclosure helps everyone.
