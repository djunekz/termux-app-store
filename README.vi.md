![[Termux App Store — TUI Package Manager](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — TUI & CLI Package Manager cho Termux](https://djunekz.github.io/termux-app-store/)

**Package manager TUI và CLI ưu tiên chạy cục bộ, được xây dựng riêng cho Termux trên Android, cài nhị phân có xác minh checksum và có phương án dự phòng build từ source.**

[![CI](https://github.com/djunekz/termux-app-store/actions/workflows/build.yml/badge.svg)](https://github.com/djunekz/termux-app-store/actions)
[![PyPI](https://img.shields.io/pypi/v/termux-app-store?style=flat&logo=pypi&color=3fb950&label=pypi)](https://pypi.org/project/termux-app-store/)
[![License](https://img.shields.io/badge/License-MIT-3fb950?style=flat)](LICENSE)
[![Stars](https://img.shields.io/github/stars/djunekz/termux-app-store?style=flat&logo=github&color=white&label=stars)](https://github.com/djunekz/termux-app-store/stargazers)

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
