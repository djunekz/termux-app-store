# How to Upload a Package to the Repository

Follow these steps to upload your tool or package to the Termux App Store repository.

## 1. Fork the Repository

- Open the target repository
- Click the `Fork` button (fork icon) at the top of the page
- Make sure the repository name is `termux-app-store`
- Click `Create fork`

## 2. Clone the Repository

```bash
git clone --depth 1 --single-branch --branch master https://github.com/YOUR_USERNAME/termux-app-store.git
cd termux-app-store
```

Replace `YOUR_USERNAME` with your GitHub username.

## 3. Create a New Branch

```bash
git checkout -b <package-name>
```

Example:

```bash
git checkout -b example
```

## 4. Create the Package Folder

General structure:

```text
packages/<package-name>/
             └── build.sh
```

Example:

```bash
mkdir -p packages/example
nano packages/example/build.sh
```

## 5. Fill in build.sh

- Use the `build.sh` template located in the `template/` folder
- Or generate it with the command `./termux-build template`
- The following metadata fields are required:

```bash
TERMUX_PKG_HOMEPAGE=
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER=""
TERMUX_PKG_VERSION=
TERMUX_PKG_SRCURL=
TERMUX_PKG_SHA256=
```

## 6. Validate the Package

Run the following checks before committing:

```bash
./termux-build lint packages/<package-name>
./termux-build doctor
./termux-build check-pr <package-name>
```

Make sure there are no errors ❌.

## 7. Commit Your Changes

```bash
git add packages/<package-name>
git commit -m "New package: <package-name>"
```

Example:

```bash
git add packages/example
git commit -m "New package: example"
```

## 8. Push to Your Fork

```bash
git push origin <package-name>
```

Example:

```bash
git push origin example
```

A link to open a Pull Request will appear in the terminal output.

## 9. Create a Pull Request (PR)

- Open your fork on GitHub
- Click **Compare & Pull Request**
- Briefly describe:
  - What the tool does
  - The upstream source
  - How to build/test it (if applicable)

## 10. Wait for Review

- A reviewer may request changes
- If changes are requested:
  - Edit the file(s)
  - Commit again
  - Push — the PR will update automatically

---

> **Important notes**
> - `termux-build` is for checking and reviewing only — it does not modify files or upload anything to GitHub
> - Do not upload compiled binaries from your local build
> - Make sure the source comes from the official upstream repository
