![[Termux App Store — TUI Package Manager for Termux](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)

# [Termux App Store — TUI & CLI Package Manager cho Termux](https://djunekz.github.io/termux-app-store/)

**Package manager TUI và CLI ưu tiên cục bộ, xây dựng native cho Termux trên Android, với cài đặt binary được xác minh checksum và phương án dự phòng build từ source.**

> Đọc bằng: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

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
> Cài đặt và quản lý gói Termux — binary dựng sẵn hoặc build từ source — không cần root, không cần tài khoản, không telemetry.

---

# Termux App Store là gì?

**Termux App Store** (`termux-app-store`) là một **TUI (Terminal User Interface)** và **CLI package manager** được xây dựng bằng Python ([Textual](https://github.com/Textualize/textual)), cho phép người dùng Termux trên Android **duyệt, cài đặt và quản lý công cụ/gói** ngay trên thiết bị — không cần tài khoản, không telemetry, không cần root. Metadata gói và việc tải xuống cần dùng mạng.

Bắt đầu từ **v0.4.0**, Termux App Store hỗ trợ **fast install engine**: các gói được tải về dưới dạng binary `.deb` dựng sẵn từ mirror pool (GitHub Pages, Cloudflare CDN, jsDelivr), với bộ nhớ đệm `.deb` cục bộ (TTL 7 ngày). Mọi tệp `.deb`, kể cả từ bộ nhớ đệm, đều phải khớp SHA256 theo từng kiến trúc, nếu không sẽ bị từ chối. SHA256 phát hiện tệp hỏng hoặc không khớp; đây không phải chữ ký của nhà phát hành. Vẫn có thể build từ source qua `fix-install`.

Đây là một **package manager thay thế cho Termux**, cho phép bạn cài đặt công cụ cộng đồng bằng các script `build.sh` — có tinh thần tương tự AUR (Arch User Repository) nhưng được thiết kế riêng cho Termux trên Android.

> **Khác gì so với `termux-packages` hoặc TUR (Termux User Repository)?**
>
> - `termux-packages` là repo chính thức của Termux — do nhóm phát triển cốt lõi duy trì, cần duyệt PR và chỉ nhận các công cụ được dùng rộng rãi.
> - TUR là phần mở rộng được tuyển chọn, vẫn cần người đóng góp review.
> - **Termux App Store** hoàn toàn do cộng đồng điều hành: ai cũng có thể gửi `build.sh`, gói được phân phối dưới dạng `.deb` dựng sẵn hoặc build từ source, và không có cổng phê duyệt tập trung. Hãy xem nó như một lớp gói cá nhân + cộng đồng đặt trên Termux.

> [!IMPORTANT]
> Termux App Store **không phải trình tự động cài đặt ẩn**.
> Mọi lượt cài đặt — binary hay source — đều chạy **cục bộ, minh bạch và hoàn toàn dưới sự kiểm soát của người dùng**.

---

# Dành cho ai?

| Người dùng | Trường hợp sử dụng |
|---|---|
| Người dùng Termux | Cài binary nhanh hoặc toàn quyền kiểm soát build từ source |
| Nhà phát triển | Phân phối công cụ qua `.deb` dựng sẵn hoặc đóng gói source |
| Người review & kiểm toán | Xem xét và xác thực script build |
| Người duy trì | Quản lý nhiều gói Termux cùng lúc |

---

<div align="center">
<img src="https://github.com/user-attachments/assets/b03419bc-8efe-4ed0-9b61-fea5153e9f53" width="100%" alt="Termux App Store — Main View"/>

<br/><br/>
<H1>Giao diện TUI</H1>

| Giao diện chính TUI | Giao diện cài đặt TUI | Menu Palette |
|:---:|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/fb9395f1-f943-44c5-b88f-be18e480fd26" width="400" alt="TUI Main Interface"/> | <img src="https://github.com/user-attachments/assets/a0ee7a15-95d2-4743-9f7e-90cd9e3388f7" width="400" alt="TUI Install Interface"/> | <img src="https://github.com/user-attachments/assets/ad760153-983f-4113-a465-2b682cb26b67" width="400" alt="Menu Palette Interface"/> |
| Menu chính của TUI | Quá trình cài đặt gói | Command palette |

> TUI thân thiện với người dùng, hỗ trợ đầy đủ **màn hình cảm ứng**

---

<H1>Giao diện CLI và các công cụ hỗ trợ khác</H1>

| Giao diện CLI và các công cụ hỗ trợ khác | Guidebook |
|:---:| :---: |
| https://github.com/user-attachments/assets/71c097b2-01a8-4c1c-9ffd-c26f29ee6ae6 | https://github.com/user-attachments/assets/b668a890-835f-4467-820a-988b1810c902 |


Giao diện CLI và công cụ hỗ trợ: `tasctl`, `termux-build`, `doctor.py`, `pkg-scaffold.py`, `build-package.sh`, `guidebook.py`

---

<H1>Quay màn hình</H1>

| Quay `termux-app-store` TUI, CLI và các công cụ khác `tasctl`, `termux-build`, `guidebook.py` |
|:---:|
| <img src="https://github.com/user-attachments/assets/152c757f-d2a3-4f31-8174-2b857a3aad51" width="100%" alt="termux-app-store"/> | termux-app-store

</div>

---

# Cài đặt và gỡ cài đặt nhanh

> Có trên **[PyPI](https://pypi.org/project/termux-app-store/)** — có thể tìm kiếm và đã được lập chỉ mục, dễ tìm thấy.

### Tùy chọn 1 (Khuyến nghị)

```bash
pkg install python
pip install termux-app-store
```

### Tùy chọn 2 (Thủ công)

> Đơn giản (khuyến nghị nếu bộ nhớ hạn chế)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> Dùng git clone (tải toàn bộ repository)

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

Sau khi cài đặt, chạy:

```bash
termux-app-store        # Open interactive TUI
termux-app-store -h     # Show CLI help
tas                     # Shorthand for termux-app-store
```

### Gỡ cài đặt

```bash
pip uninstall termux-app-store
# or
./tasctl uninstall
```

---

# Sử dụng

### TUI — Giao diện tương tác

```bash
termux-app-store
# or shorthand:
tas
```

| Phím / nút | Chức năng |
|---|---|
| **Install / Update / Open** (`Ctrl+I`) | Nút chính thay đổi theo gói: Install khi chưa cài, Update khi có phiên bản mới hơn, Open khi đã cài và là bản mới nhất. Open chạy công cụ (chọn lệnh, thêm đối số) rồi quay lại TUI sau khi bạn nhấn Enter |
| **Shortcut** (hộp thoại Open) | Tạo script Termux:Widget trong `~/.shortcuts` để chạy công cụ với các đối số của bạn |
| **Upgrade all** (banner cập nhật) | Banner hiển thị số gói đã cài có phiên bản mới hơn và đưa tất cả vào hàng đợi |
| **Cancel** (`Ctrl+X`) | Dừng quá trình tải xuống hoặc build source đang chạy tại điểm an toàn tiếp theo |
| `F4` | Lịch sử hoạt động: cài đặt, cập nhật, gỡ bỏ và khởi chạy |
| `F5` | Báo cáo sự cố: mở biểu mẫu báo lỗi đã điền sẵn |
| `Ctrl+R` / `Ctrl+Q` | Làm mới danh sách gói / thoát |
| `Ctrl+P` | Command palette, gồm bật hoặc tắt thông báo (cần Termux:API) |

### CLI — Lệnh trực tiếp

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

# Tính năng

| **Package Browser (TUI)** Duyệt các gói trong thư mục `packages/` một cách tương tác bằng bàn phím & màn hình cảm ứng.<br>**Fast Install Engine** Tải `.deb` dựng sẵn từ mirror pool — GitHub Pages, Cloudflare CDN, jsDelivr — với cơ chế dự phòng tự động.<br>**Binary Cache** Bộ nhớ đệm `.deb` cục bộ với TTL 7 ngày; tệp trong cache được xác minh lại SHA256 theo từng kiến trúc trước mỗi lần cài đặt. Gói đã cache được cài ngay lập tức.<br>**Smart Build Validator** Phát hiện các dependency Termux không được hỗ trợ với huy hiệu trạng thái tự động. | **Tìm kiếm & lọc thời gian thực** Tìm gói theo tên hoặc mô tả — có sẵn lệnh CLI `search`/`find`.<br>**Cài đặt/Gỡ nhiều gói** Cài hoặc gỡ nhiều gói bằng một lệnh, kèm tóm tắt kết quả.<br>**Quản lý một chạm** Cài đặt / cập nhật / gỡ chính Termux App Store qua `./tasctl`.<br>**Ưu tiên quyền riêng tư** Không tài khoản, không theo dõi, không telemetry. Hoạt động từ dữ liệu cục bộ khi đã có; việc tải metadata và gói cần mạng. |
|---|---|

---

# Fast Install hoạt động như thế nào (v0.4.0+)

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

> Nếu fast install thất bại, hãy dùng `fix-install <package>` để buộc build source đầy đủ qua `build-package.sh`.

---

# Thêm gói mới

Mỗi gói trong Termux App Store được định nghĩa bởi một tệp `build.sh` duy nhất — tương tự cách PKGBUILD hoạt động trong Arch Linux, nhưng được điều chỉnh cho Termux trên Android.

Mỗi gói **phải** có tệp `build.sh`:

```
packages/<tool-name>/build.sh
```

### Template `build.sh` tối thiểu

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
> Xem template đầy đủ tại `template/build.sh` hoặc chạy: `./termux-build template`

### Thêm gói bằng termux-build

```bash
cd termux-app-store
./termux-build create your-tool-name
# or auto-create from a GitHub URL:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> Khi đặt tên, không dùng khoảng trắng — hãy dùng `-`. Ví dụ: `my-tool-name`

---

# termux-build — Công cụ Build & Xác thực

`termux-build` là công cụ hỗ trợ xác thực và review — không phải công cụ tự động upload hay tự động publish.

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
> `termux-build` **chỉ đọc và xác thực** — không sửa đổi tệp và không upload lên GitHub.

---

# tasctl — Bộ điều khiển Termux App Store

`tasctl` là bộ điều khiển của hệ thống termux-app-store.

```bash
./tasctl install       # Install Termux App Store (latest)
./tasctl update        # Update to latest version
./tasctl uninstall     # Remove Termux App Store
./tasctl doctor        # Diagnose environment
./tasctl self-update   # Update tasctl itself
./tasctl help          # Show help
```

---

# guidebook — Toàn bộ thông tin về Termux App Store

```bash
python guidebook.py
```

> [!NOTE]
> guidebook hiện hỗ trợ hai ngôn ngữ: tiếng Anh và tiếng Indonesia.

---

# Cách phân phối gói của bạn đến cộng đồng Termux

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

> Hướng dẫn đầy đủ: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

# Kiến trúc

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

> Chi tiết đầy đủ: [ARCHITECTURE.md](ARCHITECTURE.md)

---

# Bảo mật & Quyền riêng tư

| **Bảo mật** | **Quyền riêng tư** |
|---|---|
| Không cần quyền bổ sung | Không cần tài khoản hay đăng ký |
| Không mở cổng mạng nào | Không phân tích hay theo dõi |
| Không có dịch vụ chạy nền | Không có telemetry dưới bất kỳ hình thức nào |
| Build chỉ chạy khi người dùng ra lệnh rõ ràng | Ưu tiên cục bộ; mạng dùng cho metadata và tải xuống |
| Bắt buộc SHA256 cho mọi `.deb` (tải xuống và cache) | Nguồn binary minh bạch và có thể kiểm toán |

> Chi tiết đầy đủ: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

# Phát triển và Kiểm thử

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
pip install -e ".[dev]"
```

| Lệnh | Chức năng |
|---|---|
| `make test` hoặc `pytest` | Chạy bộ kiểm thử |
| `make coverage` | Chạy bộ kiểm thử kèm báo cáo coverage |
| `make lint` | Kiểm tra lint và định dạng bằng Ruff |
| `make typecheck` | Kiểm tra kiểu bằng Mypy |
| `make check` | Chạy lint, kiểm tra kiểu và kiểm thử cùng lúc |

Các dependency được ghim trong `uv.lock` (`uv sync --extra dev`). Xem [CONTRIBUTING.md](CONTRIBUTING.md) để có hướng dẫn đầy đủ.

---

# Đóng góp

Mọi đóng góp đều được chào đón!

| Cách đóng góp | Mô tả |
|---|---|
| Thêm gói | Gửi một gói công cụ mới |
| Báo lỗi | Mở issue trên GitHub |
| Gửi PR | Cải thiện mã nguồn hoặc tài liệu |
| Review PR | Giúp xác thực đóng góp của người khác |
| Kiểm toán bảo mật | Xem xét tính bảo mật của script build |
| Cải thiện tài liệu | Làm rõ hoặc dịch tài liệu |

> Hướng dẫn đầy đủ: [CONTRIBUTING.md](CONTRIBUTING.md)

---

# Trợ giúp & Tài liệu

| Tài liệu | Mô tả |
|---|---|
| [FAQ](FAQ.md) | Câu hỏi thường gặp |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | Giải pháp cho các sự cố thường gặp |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | Cách upload công cụ của bạn |
| [CONTRIBUTING](CONTRIBUTING.md) | Hướng dẫn đóng góp |
| [SUPPORT](SUPPORT.md) | Cách nhận hỗ trợ |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | Lưu ý về phân phối binary |

---

# Triết lý

> *"Ưu tiên cục bộ. Kiểm soát hơn tiện lợi. Minh bạch hơn phép màu."*

Termux App Store được xây dựng cho những người dùng muốn:

- Hiểu rõ những gì chạy trên thiết bị của mình
- Kiểm soát trực tiếp việc build và source
- Tránh bị phụ thuộc vào nhà cung cấp
- Chia sẻ công cụ một cách cởi mở với cộng đồng Termux

---

# Giấy phép

Dự án này được cấp phép theo **MIT License** — xem [LICENSE](LICENSE) để biết chi tiết.

---

# Người duy trì

**Djunekz** — Nhà phát triển độc lập và người duy trì Termux App Store

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

# Ủng hộ dự án này

Nếu Termux App Store hữu ích với bạn:

- **Gắn sao** repo này — giúp người khác khám phá
- **Chia sẻ** trong cộng đồng Termux & Android
- **Báo lỗi** qua Issues
- **Gửi PR** cho bất kỳ cải tiến nào
- **Tài trợ**: https://saweria.co/redHh

---

# Lịch sử sao

<a href="https://www.star-history.com/?repos=djunekz%2Ftermux-app-store&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
 </picture>
</a>

---

# Dự án liên quan & Từ khóa

> Dự án này được phát triển độc lập và **không liên kết với** dự án [Termux](https://github.com/termux/termux-app) chính thức.

**Từ khóa tìm kiếm:** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — Được xây dựng cho mọi người, bởi cộng đồng.**
