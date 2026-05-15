![[Termux App Store — TUI 包管理器](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — Termux TUI & CLI 包管理器](https://djunekz.github.io/termux-app-store/)

**专为 Android Termux 构建的首个离线优先、二进制安全的 TUI 包管理器。**

[![CI](https://github.com/djunekz/termux-app-store/actions/workflows/build.yml/badge.svg)](https://github.com/djunekz/termux-app-store/actions)
[![PyPI](https://img.shields.io/pypi/v/termux-app-store?style=flat&logo=pypi&color=3fb950&label=pypi)](https://pypi.org/project/termux-app-store/)
[![License](https://img.shields.io/badge/License-MIT-3fb950?style=flat)](LICENSE)
[![Stars](https://img.shields.io/github/stars/djunekz/termux-app-store?style=flat&logo=github&color=white&label=stars)](https://github.com/djunekz/termux-app-store/stargazers)

> **离线优先 • 二进制安全 • 基于源码 • Termux 原生 • Android 终端**
> 无需 root、无需账号、无遥测，安装和管理 Termux 包。

> 其他语言版本: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

---

## 什么是 Termux App Store？

**Termux App Store** 是一个用 Python ([Textual](https://github.com/Textualize/textual)) 构建的 **TUI & CLI 包管理器**，让 Android 上的 Termux 用户可以直接在设备上**浏览、安装和管理工具/包** — 无需账号、无遥测、无云依赖、无需 root。

从 **v0.4.0** 起，新增 **快速安装引擎**：从镜像池（GitHub Pages、Cloudflare CDN、jsDelivr）下载预构建 `.deb` 二进制文件，支持本地 `.deb` 缓存（TTL 7天）和按架构 SHA256 验证。需要完全控制时，`fix-install` 仍可使用源码构建。

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
- 所有 `.deb` 下载均进行 SHA256 验证
- 离线优先设计

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
