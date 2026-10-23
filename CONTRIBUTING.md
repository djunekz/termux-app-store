# Contributing to Termux App Store

Thank you for your interest in contributing to **Termux App Store**
This project is a **community-driven infrastructure** for building and validating Termux packages.  
We welcome contributions of all kinds, as long as they follow the standards described below.

---

## Contribution Scope

You may contribute in one or more of the following areas:

- New Termux packages (`packages/<name>`)
- Improvements to existing `build.sh`
- CI / validation logic
- CLI tooling (`termux-build`, `tasctl`)
- Documentation & guides
- Bug reports & fixes
- Feature proposals

---

## Repository Structure Overview

```text
packages/
  └── <pkg-name>/
      └── build.sh
termux-build   # Core build tool
tasctl         # CLI controller
```

---

## Contribution Principles
All contributions must follow these principles:
1. **Automation-first** – If it can be validated, it must be validated.
2. **Reproducibility** – Builds must be deterministic.
3. **Transparency** – No hidden logic or obfuscation.
4. **Community-first** – No breaking changes without discussion.

---

## Adding a New Package
1. Package Layout
```text
packages/<pkg-name>/build.sh
```
or auto create build package
```text
./teemux-build create <pkg-name>
```
2. build.sh Requirements
- Must follow Termux packaging standards
- Must define:
 - TERMUX_PKG_HOMEPAGE
 - TERMUX_PKG_DESCRIPTION
 - TERMUX_PKG_LICENSE
 - TERMUX_PKG_VERSION
- Must NOT:
 - Download prebuilt binaries without verification
 - Use hardcoded paths outside $PREFIX
3. Validate Locally
```Sh
./termux-build lint <pkg-name>
./termux-build check-pr <pkg-name>
```
CI will reject PRs that fail validation.

---

## Setup
1. Fork and clone the repository
```Sh
git clone https://github.com/<your-username>/termux-app-store.git
cd termux-app-store
```
2. Create a virtual environment and install development dependencies
```Sh
python3 -m venv .venv
source .venv/bin/activate
make install
```
or with uv, using the committed `uv.lock`
```Sh
uv sync --extra dev
```
3. Copy the environment template when you need to override defaults
```Sh
cp .env.example .env
```
Python 3.9 or newer is required.

---

## Code Style
Python code is linted and formatted with [Ruff](https://docs.astral.sh/ruff/) and type checked with [mypy](https://mypy.readthedocs.io/). Configuration lives in `pyproject.toml`.
- Maximum line length is 120 characters
- Imports are sorted automatically
- Strings use double quotes
- Shell scripts must pass `bash -n` and `./termux-build lint <pkg-name>`

Run the checks locally before every commit:
```Sh
make lint
make typecheck
```
Apply automatic fixes and formatting:
```Sh
make format
```

---

## Testing
Tests are written with [pytest](https://docs.pytest.org/) and live in `tests/`.
```Sh
make test
```
or
```Sh
npm test
```
or directly
```Sh
python3 -m pytest
python3 -m pytest tests/test_package.py -k version
python3 -m pytest --cov=tools --cov=termux_app_store --cov-report=term
```
Run the full quality gate used by CI:
```Sh
make check
```
New features and bug fixes must include tests.

---

## CI & Quality Gates
All pull requests are automatically checked via GitHub Actions:
- Linting packages
- Ruff lint and format checks (`ruff.toml`)
- Mypy type checks
- Pytest suite
- Validating build.sh
- CLI behavior checks
- Python coverage enforcement
A pull request **cannot be merged** if any CI check fails.

---

## Commit Message Convention
Use clear and structured commit messages:
```text
<type>: <short description>

[optional body]
```
### Allowed Types
- pkg: New or updated package
- fix: Bug fix
- ci: CI / workflow changes
- docs: Documentation
- refactor: Internal changes
- chore: Maintenance
Example:
```text
pkg: add ripgrep package
fix: validate TERMUX_PKG_VERSION format
```

---

## Pull Request Guidelines
Before submitting a PR, ensure:
- [x] CI passes locally
- [x] No unrelated changes
- [x] Documentation updated (if applicable)
- [x] Commit history is clean
PR titles should be descriptive:
```text
pkg: add <package-name>
fix: correct build dependency detection
```

---

## Issue Labels & Workflow
Maintainers may assign labels such as:
- good first issue
- help wanted
- ci
- package
- discussion
Please follow the issue template when reporting bugs or requesting features.

---

## Breaking Changes Policy
Breaking changes must:
1. Be discussed via an issue first
2. Be clearly marked in the PR
3. Include migration notes (if applicable)

---

## Security & Trust
- Do NOT submit malicious code
- No malware scripts
- No backdoors
- Supply-chain integrity is critical
Security issues should **NOT** be reported publicly.
Use the contact method defined in [SECURITY.md](SECURITY.md).

---

## License Agreement
By contributing, you agree that your contributions will be licensed under the same license as this repository.

---

## Code of Conduct
All contributors must follow our [Code of Conduct](CODE_OF_CONDUCT.md).
Harassment, discrimination, or abuse will not be tolerated.

---

## Need Help?
- Open a [discussion](https://github.com/djunekz/termux-app-store/discussions)
- Open a [support request](https://github.com/djunekz/termux-app-store/issues)
- Or ask via an issue using the provided templates
We value **quality** over **quantity** and **collaboration** over speed.

---

## Welcome to the Termux App Store community
Your contribution helps build a better ecosystem for everyone.
