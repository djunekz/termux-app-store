![[Termux App Store — TUI Package Manager for Termux](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)

# [Termux App Store — 适用于 Termux 的 TUI & CLI 包管理器](https://djunekz.github.io/termux-app-store/)

**专为 Android 上的 Termux 原生构建的本地优先 TUI 与 CLI 包管理器，支持校验和验证的二进制安装，并提供源码构建作为回退。**

> 其他语言: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

<div align="center">

<a href="https://github.com/djunekz/termux-app-store/actions/workflows/build.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/build.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=CI" alt="CI"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/cli-ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/cli-ci.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=CLI" alt="CLI Validation"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/codeql.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/codeql.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=CodeQL" alt="CodeQL"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/lint-checker.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/lint-checker.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=Lint" alt="Lint"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/build-packages-debs.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/build-packages-debs.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=.deb%20build" alt="Build .deb"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/update_index.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/update_index.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=index" alt="Update Index"/></a>
<a href="https://github.com/djunekz/termux-app-store/actions/workflows/publish.yml"><img src="https://img.shields.io/github/actions/workflow/status/djunekz/termux-app-store/publish.yml?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white&label=publish" alt="Publish to PyPI"/></a>
<br>
<a href="https://pypi.org/project/termux-app-store/"><img src="https://img.shields.io/pypi/v/termux-app-store?style=flat-square&labelColor=161b22&logo=pypi&logoColor=white&color=3fb950&label=pypi" alt="PyPI"/></a>
<a href="https://pypi.org/project/termux-app-store/"><img src="https://img.shields.io/pypi/dm/termux-app-store?style=flat-square&labelColor=161b22&logo=pypi&logoColor=white&color=3fb950&label=downloads" alt="PyPI downloads"/></a>
<a href="https://pypi.org/project/termux-app-store/"><img src="https://img.shields.io/pypi/pyversions/termux-app-store?style=flat-square&labelColor=161b22&logo=python&logoColor=white&color=3fb950" alt="Python"/></a>
<a href="https://github.com/djunekz/termux-app-store/releases"><img src="https://img.shields.io/github/v/release/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=release" alt="Release"/></a>
<a href="https://github.com/djunekz/termux-app-store/releases"><img src="https://img.shields.io/github/release-date/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=released" alt="Release date"/></a>
<a href="https://github.com/djunekz/termux-app-store/releases"><img src="https://img.shields.io/github/downloads/djunekz/termux-app-store/total?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=release%20downloads" alt="GitHub downloads"/></a>
<br>
<a href="https://codecov.io/github/djunekz/termux-app-store"><img src="https://img.shields.io/codecov/c/github/djunekz/termux-app-store/master?style=flat-square&labelColor=161b22&logo=codecov&logoColor=white&label=coverage" alt="Codecov"/></a>
<a href="https://www.repo-grade.com/report/djunekz/termux-app-store"><img src="https://www.repo-grade.com/api/badge/djunekz/termux-app-store" alt="RepoGrade"/></a>
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/lint-ruff-3fb950?style=flat-square&labelColor=161b22&logo=ruff&logoColor=white" alt="Ruff"/></a>
<a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/types-mypy-3fb950?style=flat-square&labelColor=161b22&logo=python&logoColor=white" alt="mypy"/></a>
<a href="https://docs.pytest.org/"><img src="https://img.shields.io/badge/tests-pytest-3fb950?style=flat-square&labelColor=161b22&logo=pytest&logoColor=white" alt="pytest"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/SECURITY.md"><img src="https://img.shields.io/badge/security-policy-3fb950?style=flat-square&labelColor=161b22&logo=github&logoColor=white" alt="Security Policy"/></a>
<br>
<a href="https://github.com/djunekz/termux-app-store/tree/master/packages"><img src="https://img.shields.io/badge/dynamic/json?style=flat-square&labelColor=161b22&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdjunekz%2Ftermux-app-store%2Fmaster%2Ftools%2Findex.json&query=%24.total&label=packages&color=3fb950&logo=gnometerminal&logoColor=white" alt="Packages"/></a>
<a href="https://termux.dev/"><img src="https://img.shields.io/badge/platform-Termux%20%7C%20Android-3fb950?style=flat-square&labelColor=161b22&logo=android&logoColor=white" alt="Platform"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/ARCHITECTURE.md"><img src="https://img.shields.io/badge/arch-aarch64%20%7C%20arm%20%7C%20x86__64%20%7C%20i686-3fb950?style=flat-square&labelColor=161b22&logo=arm&logoColor=white" alt="Architecture"/></a>
<a href="https://github.com/Textualize/textual"><img src="https://img.shields.io/badge/built%20with-Textual-3fb950?style=flat-square&labelColor=161b22&logo=python&logoColor=white" alt="Built with Textual"/></a>
<a href="https://github.com/djunekz/termux-app-store#readme"><img src="https://img.shields.io/badge/interface-TUI%20%7C%20CLI-3fb950?style=flat-square&labelColor=161b22&logo=gnubash&logoColor=white" alt="Interface"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/SECURITY.md"><img src="https://img.shields.io/badge/installs-SHA256%20verified-3fb950?style=flat-square&labelColor=161b22&logo=letsencrypt&logoColor=white" alt="Checksum verified"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/PRIVACY.md"><img src="https://img.shields.io/badge/root-not%20required-3fb950?style=flat-square&labelColor=161b22&logo=android&logoColor=white" alt="No root"/></a>
<br>
<a href="https://github.com/djunekz/termux-app-store/blob/master/LICENSE"><img src="https://img.shields.io/badge/license-MIT-3fb950?style=flat-square&labelColor=161b22&logo=opensourceinitiative&logoColor=white" alt="License"/></a>
<a href="https://github.com/djunekz/termux-app-store/stargazers"><img src="https://img.shields.io/github/stars/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Stars"/></a>
<a href="https://github.com/djunekz/termux-app-store/network/members"><img src="https://img.shields.io/github/forks/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Forks"/></a>
<a href="https://github.com/djunekz/termux-app-store/watchers"><img src="https://img.shields.io/github/watchers/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Watchers"/></a>
<a href="https://github.com/djunekz/termux-app-store/graphs/contributors"><img src="https://img.shields.io/github/contributors/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Contributors"/></a>
<a href="https://github.com/djunekz/termux-app-store/issues"><img src="https://img.shields.io/github/issues/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=issues" alt="Open issues"/></a>
<a href="https://github.com/djunekz/termux-app-store/issues?q=is%3Aissue+is%3Aclosed"><img src="https://img.shields.io/github/issues-closed/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=closed" alt="Closed issues"/></a>
<a href="https://github.com/djunekz/termux-app-store/pulls"><img src="https://img.shields.io/github/issues-pr/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=git&logoColor=white&color=3fb950&label=PRs" alt="Pull requests"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-3fb950?style=flat-square&labelColor=161b22&logo=git&logoColor=white" alt="PRs welcome"/></a>
<br>
<a href="https://github.com/djunekz/termux-app-store/commits/master"><img src="https://img.shields.io/github/last-commit/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950" alt="Last commit"/></a>
<a href="https://github.com/djunekz/termux-app-store/graphs/commit-activity"><img src="https://img.shields.io/github/commit-activity/m/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=github&logoColor=white&color=3fb950&label=commits" alt="Commit activity"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/languages/top/djunekz/termux-app-store?style=flat-square&labelColor=161b22&logo=python&logoColor=white&color=3fb950" alt="Top language"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/languages/count/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=languages" alt="Languages count"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/languages/code-size/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=code%20size" alt="Code size"/></a>
<a href="https://github.com/djunekz/termux-app-store"><img src="https://img.shields.io/github/repo-size/djunekz/termux-app-store?style=flat-square&labelColor=161b22&color=3fb950&label=repo%20size" alt="Repo size"/></a>
<a href="https://github.com/djunekz/termux-app-store/blob/master/CODE_OF_CONDUCT.md"><img src="https://img.shields.io/badge/code%20of-conduct-3fb950?style=flat-square&labelColor=161b22&logo=contributorcovenant&logoColor=white" alt="Code of Conduct"/></a>

</div>

> **本地优先 • 校验和验证 • 基于源码 • Termux 原生 • Android 终端**
> 安装和管理 Termux 软件包 — 预编译二进制或源码构建 — 无需 root、无需账号、无遥测。

---

# 什么是 Termux App Store？

**Termux App Store**（`termux-app-store`）是一个用 Python（[Textual](https://github.com/Textualize/textual)）构建的 **TUI（终端用户界面）** 和 **CLI 包管理器**，让 Android 上的 Termux 用户可以直接在设备上**浏览、安装和管理工具/软件包** — 无需账号、无遥测、无需 root。软件包元数据和下载需要使用网络。

从 **v0.4.0** 开始，Termux App Store 支持**快速安装引擎**：软件包从镜像池（GitHub Pages、Cloudflare CDN、jsDelivr）下载为预编译的 `.deb` 二进制文件，并带有本地 `.deb` 缓存（TTL 7 天）。每个 `.deb`（包括缓存中的）都必须与对应架构的 SHA256 匹配，否则将被拒绝。SHA256 用于检测文件损坏或不匹配，不是发布者签名。仍可通过 `fix-install` 进行源码构建。

它是一个 **Termux 的替代包管理器**，让你可以使用 `build.sh` 脚本安装社区工具 — 理念类似 AUR（Arch User Repository），但专为 Android 上的 Termux 设计。

> **这与 `termux-packages` 或 TUR（Termux User Repository）有什么不同？**
>
> - `termux-packages` 是 Termux 官方仓库 — 由核心团队维护，需要 PR 审批，且只接受广泛使用的工具。
> - TUR 是精选的扩展仓库，仍然需要贡献者审核。
> - **Termux App Store** 完全由社区驱动：任何人都可以提交 `build.sh`，软件包以预编译 `.deb` 或源码构建的方式分发，没有集中的审批关卡。可以把它看作 Termux 之上的个人 + 社区软件包层。

> [!IMPORTANT]
> Termux App Store **不是隐藏的自动安装器**。
> 所有安装 — 无论二进制还是源码 — 都**在本地运行、透明，并完全由用户掌控**。

---

# 适合谁使用？

| 用户 | 使用场景 |
|---|---|
| Termux 用户 | 快速二进制安装，或完全掌控源码构建 |
| 开发者 | 通过预编译 `.deb` 或源码包分发工具 |
| 审阅者与审计员 | 审阅并验证构建脚本 |
| 维护者 | 同时管理多个 Termux 软件包 |

---

<div align="center">
<img src="https://github.com/user-attachments/assets/b03419bc-8efe-4ed0-9b61-fea5153e9f53" width="100%" alt="Termux App Store — Main View"/>

<br/><br/>
<H1>TUI 界面</H1>

| TUI 主界面 | TUI 安装界面 | 菜单面板 |
|:---:|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/fb9395f1-f943-44c5-b88f-be18e480fd26" width="400" alt="TUI Main Interface"/> | <img src="https://github.com/user-attachments/assets/a0ee7a15-95d2-4743-9f7e-90cd9e3388f7" width="400" alt="TUI Install Interface"/> | <img src="https://github.com/user-attachments/assets/ad760153-983f-4113-a465-2b682cb26b67" width="400" alt="Menu Palette Interface"/> |
| TUI 主菜单 | 软件包安装过程 | 命令面板 |

> TUI 界面友好，完整支持**触摸屏**

---

<H1>CLI 界面与其他工具支持</H1>

| 其他工具支持的 CLI 视图 | Guidebook |
|:---:| :---: |
| https://github.com/user-attachments/assets/71c097b2-01a8-4c1c-9ffd-c26f29ee6ae6 | https://github.com/user-attachments/assets/b668a890-835f-4467-820a-988b1810c902 |


CLI 界面与工具支持：`tasctl`、`termux-build`、`doctor.py`、`pkg-scaffold.py`、`build-package.sh`、`guidebook.py`

---

<H1>录屏</H1>

| 录制 `termux-app-store` 的 TUI、CLI 以及其他工具 `tasctl`、`termux-build`、`guidebook.py` |
|:---:|
| <img src="https://github.com/user-attachments/assets/152c757f-d2a3-4f31-8174-2b857a3aad51" width="100%" alt="termux-app-store"/> | termux-app-store

</div>

---

# 快速安装与卸载

> 已上架 **[PyPI](https://pypi.org/project/termux-app-store/)** — 可搜索、已收录，方便发现。

### 方式 1（推荐）

```bash
pkg install python
pip install termux-app-store
```

### 方式 2（手动）

> 简单方式（内存有限时推荐）

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> 使用 git clone（下载完整仓库）

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

安装后运行：

```bash
termux-app-store        # Open interactive TUI
termux-app-store -h     # Show CLI help
tas                     # Shorthand for termux-app-store
```

### 卸载

```bash
pip uninstall termux-app-store
# or
./tasctl uninstall
```

---

# 使用方法

### TUI — 交互界面

```bash
termux-app-store
# or shorthand:
tas
```

| 按键 / 按钮 | 作用 |
|---|---|
| **Install / Update / Open**（`Ctrl+I`） | 主按钮随软件包状态变化：未安装时为 Install，有新版本时为 Update，已安装且为最新时为 Open。Open 会运行该工具（可选择命令、添加参数），按 Enter 后返回 TUI |
| **Shortcut**（Open 对话框） | 在 `~/.shortcuts` 中创建 Termux:Widget 脚本，用你的参数运行该工具 |
| **Upgrade all**（更新横幅） | 横幅显示有新版本的已安装软件包数量，并将它们全部加入队列 |
| **Cancel**（`Ctrl+X`） | 在下一个安全点停止正在进行的下载或源码构建 |
| `F4` | 活动历史：安装、更新、卸载和启动 |
| `F5` | 报告问题：打开已预填的 Bug 报告表单 |
| `Ctrl+R` / `Ctrl+Q` | 刷新软件包 / 退出 |
| `Ctrl+P` | 命令面板，包括开启或关闭通知（需要 Termux:API） |

### CLI — 直接命令

```bash
termux-app-store list                     # List all packages
termux-app-store show <package>           # Show package details
termux-app-store install <package>        # Fast install (pre-built .deb)
termux-app-store install pkg1 pkg2 pkg3   # Multi-package install
termux-app-store fix-install <package>    # Force source build (bypass fast install)
termux-app-store search <query>           # Search packages by name or description
termux-app-store update                   # Check for available updates
termux-app-store upgrade                  # Upgrade all packages
termux-app-store upgrade <package>        # Upgrade a specific package
termux-app-store uninstall <package>      # Uninstall a package
termux-app-store mirrors                  # Check mirror status
termux-app-store cache info               # Show binary cache info
termux-app-store cache clear              # Clear binary cache
termux-app-store version                  # Check latest version
termux-app-store help                     # Full help
```

---

# 功能特性

| **软件包浏览器（TUI）** 通过键盘和触摸屏交互式浏览 `packages/` 文件夹中的软件包。<br>**快速安装引擎** 从镜像池 — GitHub Pages、Cloudflare CDN、jsDelivr — 下载预编译 `.deb`，并自动回退。<br>**二进制缓存** 本地 `.deb` 缓存，TTL 7 天；每次安装前都会按架构重新校验缓存文件的 SHA256。已缓存的软件包可即时安装。<br>**智能构建验证器** 检测不受支持的 Termux 依赖，并自动显示状态标识。 | **实时搜索与过滤** 按名称或描述搜索软件包 — 同时提供 `search`/`find` CLI 命令。<br>**多包安装/卸载** 一条命令安装或移除多个软件包，并输出汇总。<br>**一键管理** 通过 `./tasctl` 安装 / 更新 / 卸载 Termux App Store 本身。<br>**隐私优先** 无账号、无追踪、无遥测。本地已有数据时可离线使用；获取元数据和软件包需要网络。 |
|---|---|

---

# 快速安装的工作原理（v0.4.0+）

```
termux-app-store install <package>
        │
        ▼
  Check local .deb cache (TTL 7 days)
        │ cache HIT          │ cache MISS
        ▼                    ▼
  Verify SHA256        Probe the mirrors, use the fastest:
  (per arch)           1. Cloudflare CDN
        │              2. GitHub Pages
        ▼              3. jsDelivr CDN
  dpkg -i                    │
                             ▼
                       Download .deb
                       Verify SHA256 (index sha256_by_arch, else the published .deb.sha256)
                       Cache locally
                       dpkg -i
```

> 如果快速安装失败，请使用 `fix-install <package>` 通过 `build-package.sh` 强制进行完整的源码构建。

---

# 添加软件包

Termux App Store 中的每个软件包都由一个 `build.sh` 文件定义 — 类似 Arch Linux 的 PKGBUILD，但针对 Android 上的 Termux 做了调整。

每个软件包**必须**有一个 `build.sh` 文件：

```
packages/<tool-name>/build.sh
```

### 最简 `build.sh` 模板

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@your-github-username"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

> [!NOTE]
> 完整模板见 `template/build.sh`，或运行：`./termux-build template`

### 使用 termux-build 添加软件包

```bash
cd termux-app-store
./termux-build create your-tool-name
# or auto-create from a GitHub URL:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> 命名时不要使用空格 — 请使用 `-`。例如：`my-tool-name`

---

# termux-build — 构建与验证工具

`termux-build` 是验证和审阅辅助工具 — 不是自动上传或自动发布工具。

```bash
./termux-build create <package>      # Create package for distribution
./termux-build init <url-repo>       # Auto-create and build package from GitHub URL
./termux-build lint <package>        # Lint a build script
./termux-build check-pr <package>    # Check PR readiness
./termux-build doctor                # Diagnose environment
./termux-build suggest <package>     # Get improvement suggestions
./termux-build explain <package>     # Detailed package explanation
./termux-build template              # Generate build.sh template
./termux-build guide                 # Contribution guide
```

> [!NOTE]
> `termux-build` **只读取和验证** — 不会修改文件，也不会上传到 GitHub。

---

# tasctl — Termux App Store 控制器

`tasctl` 是 termux-app-store 系统的控制器。

```bash
./tasctl install       # Install Termux App Store (latest)
./tasctl update        # Update to latest version
./tasctl uninstall     # Remove Termux App Store
./tasctl doctor        # Diagnose environment
./tasctl self-update   # Update tasctl itself
./tasctl help          # Show help
```

---

# guidebook — 关于 Termux App Store 的全部信息

```bash
python guidebook.py
```

> [!NOTE]
> guidebook 目前支持两种语言：英语和印度尼西亚语。

---

# 如何向 Termux 社区分发你的软件包

```bash
# 1. Fork this repo
# 2. Add your package folder:
mkdir packages/your-tool-name
# 3. Create build.sh from the template or with termux-build:
./termux-build create your-tool-name
# or from a GitHub URL:
./termux-build init https://github.com/you/your-repo
# 4. Validate with termux-build:
./termux-build lint packages/your-tool-name
# 5. Submit a Pull Request
```

> 完整指南：[HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

# 架构

```
termux-app-store/
├── packages/              # All packages directory
│   └── <tool-name>/
│       └── build.sh       # Metadata & build script
├── template/
│   └── build.sh           # Package template
├── core/
│   ├── binary_core.py     # BinaryCache — local .deb cache + mirror download
│   ├── mirrors.py         # MirrorManager — mirror pool registry
│   ├── package.py         # Package dataclass
│   └── validator.py       # PackageValidator
├── utils/
│   └── installer.py       # install_from_binary / install_from_source helpers
├── tools/
│   └── mirrors.json       # Mirror registry
├── fast_install.py        # Fast install engine (.deb download + cache + SHA256 verify)
├── store_common.py        # Shared logic: mirrors, app root, recipe and script verification
├── tasctl                 # TAS installer/updater/uninstaller
├── termux-build           # Validation & review tool
└── install.sh             # Main installer
```

> 详细说明：[ARCHITECTURE.md](ARCHITECTURE.md)

---

# 安全与隐私

| **安全** | **隐私** |
|---|---|
| 无需额外权限 | 无需账号或注册 |
| 不开放网络端口 | 无分析或追踪 |
| 无后台服务运行 | 无任何形式的遥测 |
| 构建仅在用户明确下达命令时运行 | 本地优先；网络仅用于元数据和下载 |
| 每个 `.deb`（下载和缓存）都必须通过 SHA256 | 二进制来源透明且可审计 |

> 详细说明：[SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

# 开发与测试

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
pip install -e ".[dev]"
```

| 命令 | 作用 |
|---|---|
| `make test` 或 `pytest` | 运行测试套件 |
| `make coverage` | 运行测试套件并生成覆盖率报告 |
| `make lint` | Ruff 代码检查与格式检查 |
| `make typecheck` | Mypy 类型检查 |
| `make check` | 同时运行 lint、类型检查和测试 |

依赖版本锁定在 `uv.lock` 中（`uv sync --extra dev`）。完整指南请参阅 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

# 参与贡献

欢迎所有形式的贡献！

| 贡献方式 | 说明 |
|---|---|
| 添加软件包 | 提交新的工具软件包 |
| 报告 Bug | 在 GitHub 上提交 issue |
| 发送 PR | 改进代码或文档 |
| 审阅 PR | 帮助验证他人的贡献 |
| 安全审计 | 审查构建脚本的安全性 |
| 改进文档 | 完善或翻译文档 |

> 完整指南：[CONTRIBUTING.md](CONTRIBUTING.md)

---

# 帮助与文档

| 文档 | 说明 |
|---|---|
| [FAQ](FAQ.md) | 常见问题 |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | 常见问题的解决方案 |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | 如何上传你的工具 |
| [CONTRIBUTING](CONTRIBUTING.md) | 贡献指南 |
| [SUPPORT](SUPPORT.md) | 如何获得支持 |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | 关于二进制分发的说明 |

---

# 理念

> *“本地优先。掌控胜于便利。透明胜于魔法。”*

Termux App Store 为以下用户而生：

- 完全了解自己设备上运行的内容
- 直接掌控构建过程和源码
- 避免供应商锁定
- 与 Termux 社区公开分享工具

---

# 许可证

本项目采用 **MIT 许可证** — 详见 [LICENSE](LICENSE)。

---

# 维护者

**Djunekz** — Termux App Store 的独立开发者与维护者

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

# 支持本项目

如果 Termux App Store 对你有帮助：

- 给本仓库点 **Star** — 帮助更多人发现它
- 在 Termux 和 Android 社区中**分享**
- 通过 Issues **报告 Bug**
- 为任何改进**提交 PR**
- **赞助**：https://saweria.co/redHh

---

# Star 历史

<a href="https://www.star-history.com/?repos=djunekz%2Ftermux-app-store&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
 </picture>
</a>

---

# 相关项目与关键词

> 本项目为独立开发，与官方 [Termux](https://github.com/termux/termux-app) 项目**没有隶属关系**。

**搜索关键词：** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — 由社区为所有人打造。**
