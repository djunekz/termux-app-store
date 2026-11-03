![[Termux App Store — TUI 包管理器](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — Termux TUI & CLI 包管理器](https://djunekz.github.io/termux-app-store/)

**专为 Android Termux 构建的本地优先的 TUI 和 CLI 包管理器，支持带校验和验证的二进制安装及源码构建回退。**

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
> 无需 root、无需账号、无遥测，安装和管理 Termux 包。

> 其他语言版本: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

---

## 什么是 Termux App Store？

**Termux App Store** 是一个用 Python ([Textual](https://github.com/Textualize/textual)) 构建的 **TUI & CLI 包管理器**，让 Android 上的 Termux 用户可以直接在设备上**浏览、安装和管理工具/包** — 无需账号、无遥测、无需 root。获取包元数据和下载需要网络。

从 **v0.4.0** 起，新增 **快速安装引擎**：从镜像池（GitHub Pages、Cloudflare CDN、jsDelivr）下载预构建 `.deb` 二进制文件，支持本地 `.deb` 缓存（TTL 7天）。包括缓存在内的每个 `.deb` 都必须匹配按架构的 SHA256，否则会被拒绝。SHA256 用于检测文件损坏或不匹配，并不是发布者签名。需要完全控制时，`fix-install` 仍可使用源码构建。

> [!IMPORTANT]
> Termux App Store **不是隐藏的自动安装程序**。
> 所有安装——无论是二进制还是源码构建——均**在本地透明运行，完全由用户控制**。

---

## 截图

<div align="center">

<img src=".assets/0.jpeg" width="74%" alt="Termux App Store — 主界面"/>

<br/><br/>
<H1>TUI界面</H1>

| TUI主界面 | TUI安装界面 | 菜单面板 |
|:---:|:---:|:---:|
| <img src=".assets/0main.jpg" width="220" alt="TUI Main Interface"/> | <img src=".assets/1install.jpg" width="220" alt="TUI Install Interface"/> | <img src=".assets/2pallete.jpg" width="220" alt="Menu Palette Interface"/> |
| TUI主菜单 | 软件包安装过程 | 命令面板 |

> TUI界面友好，完全支持**触摸屏**操作

---

<H1>CLI界面</H1>

| 其他工具支持 | CLI安装界面 | CLI查看界面 |
|:---:|:---:|:---:|
| <img src=".assets/0tas-and-termux-build.jpg" width="220" alt="Other tools support"/> | <img src=".assets/0cli-install.jpg" width="220" alt="CLI Install Interface"/> | <img src=".assets/0cli-view.jpg" width="220" alt="CLI View Interface"/> |
| tasctl和termux-build | 软件包安装过程 | CLI帮助、列表和显示 |

</div>

---

## 快速安装与卸载

### 方式 1（推荐）

```bash
pkg install python
pip install termux-app-store
```

### 方式 2（手动）

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

安装后运行：

```bash
termux-app-store    # 打开交互式 TUI
tas                 # 简写命令
termux-app-store -h # 显示 CLI 帮助
```

### 卸载

```bash
pip uninstall termux-app-store
```

---

## 使用方法

### TUI — 交互界面

```bash
termux-app-store
# 或简写：
tas
```

### CLI — 直接命令

```bash
termux-app-store list                     # 列出所有包
termux-app-store show <包名>              # 显示包详情
termux-app-store install <包名>           # 快速安装（预构建 .deb）
termux-app-store install pkg1 pkg2 pkg3   # 批量安装多个包
termux-app-store fix-install <包名>       # 强制源码构建
termux-app-store search <关键词>          # 搜索包
termux-app-store update                   # 检查可用更新
termux-app-store upgrade                  # 升级所有包
termux-app-store mirrors                  # 检查镜像状态
termux-app-store cache info               # 查看缓存信息
termux-app-store cache clear              # 清除缓存
termux-app-store version                  # 检查最新版本
termux-app-store help                     # 完整帮助
```

---

## 快速安装工作原理（v0.4.0+）

v0.4.0 起，安装默认下载预构建 `.deb` 二进制文件：

1. 检查本地 `.deb` 缓存（7天TTL）
2. 缓存未命中时，按顺序尝试镜像：GitHub Pages → Cloudflare CDN → jsDelivr CDN → raw GitHub
3. 按架构 SHA256 验证（`sha256_by_arch`）
4. 本地缓存后 `dpkg -i` 安装

> 如果快速安装失败，使用 `fix-install <包名>` 通过 `build-package.sh` 进行完整源码构建。

---

## 包状态标识

| 标识 | 说明 |
|---|---|
| **NEW** | 新增包（7天内） |
| **UPDATE** | 有新版本可用 |
| **INSTALLED** | 已安装且为最新 |
| **UNSUPPORTED** | Termux 中依赖不可用 |

---

## 添加包

每个包由单个 `build.sh` 文件定义：

```
packages/<工具名>/build.sh
```

### 最简 `build.sh` 模板

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@你的GitHub用户名"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

```bash
cd termux-app-store
./termux-build create 你的工具名
# 或从 GitHub URL 自动创建：
./termux-build init https://github.com/user/repo
```

---

## 辅助工具

### termux-build

```bash
./termux-build create <包名>      # 创建发布用包
./termux-build init <url>         # 从 GitHub URL 自动创建
./termux-build lint <包名>        # 检查构建脚本
./termux-build check-pr <包名>    # 检查 PR 准备情况
./termux-build doctor             # 诊断环境
./termux-build template           # 生成 build.sh 模板
```

### tasctl

```bash
./tasctl install       # 安装 Termux App Store
./tasctl update        # 更新到最新版本
./tasctl uninstall     # 删除 Termux App Store
./tasctl doctor        # 诊断环境
./tasctl self-update   # 更新 tasctl 本身
```

---

## 安全与隐私

- 无需额外权限，无后台服务
- 无账号、无注册
- 无分析、无追踪、无遥测
- 每个 `.deb`（下载和缓存）都强制要求 SHA256
- 本地优先设计（元数据和下载需要网络）

> 详情: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

## 许可证

**MIT 许可证** — 详见 [LICENSE](LICENSE)。

---

## 维护者

**Djunekz** — 独立开发者

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

**© Termux App Store — 为社区而建，由社区共创。**
