![[Termux App Store — TUI Package Manager](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — TUI & CLI Package Manager cho Termux](https://djunekz.github.io/termux-app-store/)

**Package manager TUI và CLI ưu tiên chạy cục bộ, được xây dựng riêng cho Termux trên Android, cài nhị phân có xác minh checksum và có phương án dự phòng build từ source.**

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


> **Ưu tiên cục bộ • Xác minh checksum • Dựa trên source • Native Termux • Android Terminal**
> Cài đặt và quản lý gói Termux — nhị phân dựng sẵn hoặc build từ source — không root, không tài khoản, không theo dõi.

> Đọc bằng ngôn ngữ khác: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

---

## Termux App Store là gì?

**Termux App Store** là **package manager TUI & CLI** được xây dựng bằng Python ([Textual](https://github.com/Textualize/textual)), cho phép người dùng Termux trên Android **duyệt, cài đặt và quản lý công cụ/gói** trực tiếp trên thiết bị — không cần tài khoản, không có telemetry, không cần root. Việc lấy metadata và tải xuống cần mạng.

Từ **v0.4.0**, thêm **engine cài đặt nhanh**: tải xuống các file `.deb` nhị phân dựng sẵn từ nhóm mirror (GitHub Pages, Cloudflare CDN, jsDelivr), với bộ nhớ đệm `.deb` cục bộ (TTL 7 ngày) . Mọi file `.deb`, kể cả trong cache, phải khớp SHA256 theo kiến trúc, nếu không sẽ bị từ chối. SHA256 dùng để phát hiện file hỏng hoặc không khớp, không phải chữ ký của nhà phát hành. Vẫn có thể dùng `fix-install` để build từ source khi cần kiểm soát đầy đủ.

> [!IMPORTANT]
> Termux App Store **không phải là trình cài đặt tự động ẩn**.
> Tất cả các cài đặt — nhị phân hay source — đều chạy **cục bộ, minh bạch và hoàn toàn do người dùng kiểm soát**.

---

## Ảnh chụp màn hình

| TUI chính | TUI cài đặt | Command Palette |
|---|---|---|
| [![TUI Main](.assets/0main.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/0main.jpg) | [![TUI Install](.assets/1install.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/1install.jpg) | [![Menu Palette](.assets/2pallete.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/2pallete.jpg) |

---

## Cài đặt và gỡ cài đặt nhanh

### Tùy chọn 1 (Khuyến nghị)

```bash
pkg install python
pip install termux-app-store
```

### Tùy chọn 2 (Thủ công)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

Sau khi cài đặt:

```bash
termux-app-store    # Mở TUI tương tác
tas                 # Lệnh viết tắt
termux-app-store -h # Hiển thị trợ giúp CLI
```

### Gỡ cài đặt

```bash
pip uninstall termux-app-store
```

---

## Sử dụng

### TUI — Giao diện tương tác

```bash
termux-app-store
# hoặc viết tắt:
tas
```

### CLI — Lệnh trực tiếp

```bash
termux-app-store list                     # Liệt kê tất cả gói
termux-app-store show <gói>               # Xem chi tiết gói
termux-app-store install <gói>            # Cài đặt nhanh (file .deb dựng sẵn)
termux-app-store install pkg1 pkg2 pkg3   # Cài nhiều gói cùng lúc
termux-app-store fix-install <gói>        # Bắt buộc build từ source
termux-app-store search <từ khóa>         # Tìm kiếm gói
termux-app-store update                   # Kiểm tra bản cập nhật
termux-app-store upgrade                  # Nâng cấp tất cả gói
termux-app-store mirrors                  # Kiểm tra trạng thái mirror
termux-app-store cache info               # Thông tin bộ nhớ đệm
termux-app-store cache clear              # Xóa bộ nhớ đệm
termux-app-store version                  # Kiểm tra phiên bản mới nhất
termux-app-store help                     # Trợ giúp đầy đủ
```

---

## Cách hoạt động của Fast Install (v0.4.0+)

Từ v0.4.0, cài đặt mặc định tải xuống file `.deb` nhị phân dựng sẵn:

1. Kiểm tra bộ nhớ đệm `.deb` cục bộ (TTL 7 ngày)
2. Nếu không có cache, thử mirror theo thứ tự: GitHub Pages → Cloudflare CDN → jsDelivr CDN → raw GitHub
3. Xác minh SHA256 theo kiến trúc (`sha256_by_arch`)
4. Lưu cache cục bộ và cài đặt bằng `dpkg -i`

> Nếu cài đặt nhanh thất bại, dùng `fix-install <gói>` để build toàn bộ từ source qua `build-package.sh`.

---

## Huy hiệu trạng thái gói

| Huy hiệu | Mô tả |
|---|---|
| **NEW** | Gói mới thêm (trong 7 ngày) |
| **UPDATE** | Có phiên bản mới |
| **INSTALLED** | Đã cài và là bản mới nhất |
| **UNSUPPORTED** | Dependency không có sẵn trong Termux |

---

## Thêm gói mới

Mỗi gói được định nghĩa bởi một file `build.sh` duy nhất:

```
packages/<tên-công-cụ>/build.sh
```

### Template `build.sh` tối thiểu

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@tên-github-của-bạn"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

```bash
cd termux-app-store
./termux-build create tên-công-cụ
# hoặc tự động tạo từ GitHub URL:
./termux-build init https://github.com/user/repo
```

---

## Công cụ hỗ trợ

### termux-build

```bash
./termux-build create <gói>       # Tạo gói để phân phối
./termux-build init <url>         # Tự động tạo từ GitHub URL
./termux-build lint <gói>         # Kiểm tra build script
./termux-build doctor             # Chẩn đoán môi trường
./termux-build template           # Tạo template build.sh
```

### tasctl

```bash
./tasctl install       # Cài Termux App Store
./tasctl update        # Cập nhật phiên bản mới nhất
./tasctl uninstall     # Gỡ Termux App Store
./tasctl doctor        # Chẩn đoán môi trường
./tasctl self-update   # Tự cập nhật tasctl
```

---

## Bảo mật & Quyền riêng tư

- Không cần quyền bổ sung, không có dịch vụ chạy nền
- Không cần tài khoản, không đăng ký
- Không phân tích, không theo dõi, không telemetry
- Bắt buộc SHA256 cho mọi `.deb` (tải xuống và cache)
- Thiết kế ưu tiên cục bộ (cần mạng cho metadata và tải xuống)

> Chi tiết: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

## Giấy phép

**Giấy phép MIT** — xem [LICENSE](LICENSE) để biết chi tiết.

---

## Người duy trì

**Djunekz** — Nhà phát triển độc lập

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

**© Termux App Store — Được tạo ra cho mọi người, bởi cộng đồng.**
