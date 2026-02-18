<div align="center">

<img src=".assets/0.jpeg" width="420" alt="Termux App Store — TUI Package Manager for Termux"/>

<br/>

# Termux App Store

**The first offline-first, source-based TUI package manager built natively for Termux.**

[![CI](https://github.com/djunekz/termux-app-store/actions/workflows/build.yml/badge.svg)](https://github.com/djunekz/termux-app-store/actions)
[![Codecov](https://codecov.io/github/djunekz/termux-app-store/branch/master/graph/badge.svg?token=357W4EP8G0)](https://codecov.io/github/djunekz/termux-app-store)
[![Release](https://img.shields.io/github/v/release/djunekz/termux-app-store.svg?style=flat&logo=iterm2&color=3fb950)](https://github.com/djunekz/termux-app-store/releases)
[![Downloads](https://img.shields.io/github/downloads/djunekz/termux-app-store/total?style=flat&logo=abdownloadmanager&logoColor=white&color=3fb950)](https://github.com/djunekz/termux-app-store)
[![License](https://img.shields.io/github/license/djunekz/termux-app-store.svg?style=flat&color=3fb950)](LICENSE)

[![Stars](https://img.shields.io/github/stars/djunekz/termux-app-store?logo=starship&color=3fb950&logoColor=black)](https://github.com/djunekz/termux-app-store/stargazers)
[![Forks](https://img.shields.io/github/forks/djunekz/termux-app-store?logo=refinedgithub&color=3fb950)](https://github.com/djunekz/termux-app-store/network)
[![Issues](https://img.shields.io/github/issues/djunekz/termux-app-store?style=flat&logo=openbugbounty&logoColor=white&color=3fb950)](https://github.com/djunekz/termux-app-store/issues)
[![PRs](https://img.shields.io/github/issues-pr/djunekz/termux-app-store?style=flat&logo=git&logoColor=white&color=3fb950)](https://github.com/djunekz/termux-app-store/pulls)
[![Contributors](https://img.shields.io/github/contributors/djunekz/termux-app-store?style=flat&logo=github&logoColor=white&color=3fb950)](https://github.com/djunekz/termux-app-store/graphs/contributors)
[![Community Ready](https://img.shields.io/badge/Community-Ready-3fb950?style=flat&logo=github)](https://github.com/djunekz/termux-app-store)

> 🧠 **Offline-first &nbsp;•&nbsp; Source-based &nbsp;•&nbsp; Binary-safe &nbsp;•&nbsp; Termux-native**

</div>

---

## 📖 Apa itu Termux App Store?

**Termux App Store** adalah **TUI (Terminal User Interface)** berbasis Python ([Textual](https://github.com/Textualize/textual)) dan CLI yang memungkinkan pengguna Termux untuk **menelusuri, membangun, dan mengelola tool/aplikasi** langsung dari perangkat Android — tanpa akun, tanpa telemetry, dan tanpa ketergantungan cloud.

> [!IMPORTANT]
> Termux App Store **bukan repository biner terpusat** dan **bukan installer otomatis tersembunyi**.
> Semua build dijalankan **secara lokal, transparan, dan atas kendali penuh pengguna**.

---

## 👥 Untuk Siapa?

| Pengguna | Kegunaan |
|---|---|
| 📱 Pengguna Termux | Kontrol penuh atas build & package |
| 🛠️ Developer | Distribusikan tool via source-based packaging |
| 🔍 Reviewer & Auditor | Review dan validasi build script |
| 📦 Maintainer | Kelola banyak package Termux sekaligus |

---

## 📱 Screenshot

<div align="center">

<img src=".assets/0.jpeg" width="74%" alt="Termux App Store — Tampilan Utama"/>

<br/><br/>

| Main Interface | Install Interface | Menu Palette |
|:---:|:---:|:---:|
| <img src=".assets/0main.jpg" width="220" alt="Main Interface"/> | <img src=".assets/1install.jpg" width="220" alt="Install Interface"/> | <img src=".assets/2pallete.jpg" width="220" alt="Menu Palette Interface"/> |
| TUI menu utama | Proses install package | Command palette |

> ✨ User-friendly dengan dukungan **touchscreen** penuh

</div>

---

## 🚀 Instalasi Cepat

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/main/install.sh | bash
```

Setelah instalasi, jalankan:

```bash
termux-app-store        # Buka TUI interaktif
termux-app-store -h     # Lihat bantuan CLI
```

---

## 🖥️ Penggunaan

### TUI — Antarmuka Interaktif
```bash
termux-app-store
```

### CLI — Perintah Langsung

```bash
termux-app-store list                  # Daftar semua package
termux-app-store show <package>        # Detail package
termux-app-store install <package>     # Build & install package
termux-app-store update                # Update index package
termux-app-store upgrade               # Upgrade semua package
termux-app-store upgrade <package>     # Upgrade package tertentu
termux-app-store version               # Cek versi terbaru
termux-app-store help                  # Bantuan lengkap
```

---

## ✨ Fitur Utama

<table>
<tr>
<td width="50%">

**📦 Package Browser (TUI)**
Jelajahi paket dari folder `packages/` secara interaktif dengan navigasi keyboard & touchscreen.

**🧠 Smart Build Validator**
Deteksi dependency yang tidak didukung Termux, lengkap dengan badge status otomatis.

**🔍 Search & Filter Real-time**
Cari paket berdasarkan nama atau deskripsi secara instan tanpa reload.

**⚡ One-Click Build**
Install atau update paket cukup satu klik via `build-package.sh`.

</td>
<td width="50%">

**✅ One-Click Validator**
Cek validasi package sebelum distribusi via `./termux-build`.

**🛠️ One-Click Manage**
Install / update / uninstall Termux App Store itu sendiri via `./tasctl`.

**🧬 Self-Healing Path Resolver**
Auto-detect lokasi app meski folder dipindah atau di-rename.

**🔐 Privacy-First**
Tanpa akun, tanpa tracking, tanpa telemetry — offline sepenuhnya.

</td>
</tr>
</table>

---

## 🔴 Badge Status Package

| Badge | Keterangan |
|---|---|
| 🟢 **NEW** | Package baru (< 7 hari) |
| 🟡 **UPDATE** | Versi lebih baru tersedia |
| 🟢 **INSTALLED** | Versi terpasang sudah terkini |
| 🔴 **UNSUPPORTED** | Dependency tidak tersedia di Termux |

---

## 🧩 Cara Menambahkan Package

Setiap package **wajib** memiliki file `build.sh`:

```
packages/<nama_tool>/build.sh
```

### Template Minimal `build.sh`

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@username-github"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

> 💡 Lihat template lengkap di folder `template/build.sh`
> atau jalankan: `./termux-build template`

---

## 🛠️ termux-build — Validation Tool

**termux-build** adalah tool validasi dan helper untuk reviewer — bukan tool upload atau publish otomatis.

```bash
./termux-build lint <package>        # Lint build script
./termux-build check-pr <package>    # Cek kesiapan PR
./termux-build doctor                # Diagnosis environment
./termux-build suggest <package>     # Saran perbaikan
./termux-build explain <package>     # Penjelasan detail package
./termux-build template              # Generate template build.sh
./termux-build guide                 # Panduan kontribusi
```

> [!NOTE]
> termux-build **hanya membaca dan memvalidasi** — tidak mengubah file, tidak build otomatis, tidak upload ke GitHub.

---

## 🏗️ Arsitektur

```
termux-app-store/
├── packages/              # Direktori semua package
│   └── <nama_tool>/
│       └── build.sh       # Metadata & build script
├── template/
│   └── build.sh           # Template package
├── tasctl                 # Installer/updater/uninstaller TAS
├── termux-build           # Validation & review tool
└── install.sh             # Installer utama
```

> 📄 Detail lengkap: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🔐 Keamanan & Privasi

<table>
<tr>
<td width="50%">

**🔐 Keamanan**
- Tidak meminta permission tambahan
- Tidak membuka port jaringan
- Tidak menjalankan service background
- Build hanya berjalan atas perintah eksplisit user

</td>
<td width="50%">

**🛡️ Privasi**
- Tanpa akun atau registrasi
- Tanpa analytics atau pelacakan
- Tanpa telemetry apapun
- Offline-first by design

</td>
</tr>
</table>

> 📄 [SECURITY.md](SECURITY.md) &nbsp;|&nbsp; [PRIVACY.md](PRIVACY.md) &nbsp;|&nbsp; [DISCLAIMER.md](DISCLAIMER.md)

---

## 📦 Upload Tool ke Termux App Store

Ingin mendistribusikan tool kamu ke komunitas Termux?

**Keuntungan upload tool:**
- Tool bisa diunduh banyak pengguna Termux
- Update cukup dengan mengubah `version` dan `sha256` di `build.sh`
- Tool muncul di TUI dengan badge status otomatis

**Cara upload:**

```bash
# 1. Fork repo ini
# 2. Tambahkan folder package kamu:
mkdir packages/nama-tool-kamu
# 3. Buat build.sh sesuai template
# 4. Validasi dengan termux-build:
./termux-build lint packages/nama-tool-kamu
# 5. Submit Pull Request
```

> 📄 Panduan lengkap: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

## 🤝 Kontribusi

Semua bentuk kontribusi sangat disambut!

| Cara Berkontribusi | Keterangan |
|---|---|
| 📦 Tambah package | Submit package tool baru |
| 🐛 Laporkan bug | Buat issue di GitHub |
| 🔀 Kirim PR | Perbaikan code atau dokumentasi |
| 🔍 Review PR | Bantu validasi kontribusi orang lain |
| 🔐 Audit security | Review keamanan build script |
| 📝 Perbaiki docs | Perjelas atau terjemahkan dokumentasi |

> 📄 Panduan lengkap: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## ❓ Bantuan & Dokumentasi

| Dokumen | Keterangan |
|---|---|
| [FAQ.md](FAQ.md) | Pertanyaan yang sering diajukan |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Solusi masalah umum |
| [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md) | Cara upload tool |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Panduan kontribusi |
| [SUPPORT.md](SUPPORT.md) | Cara mendapatkan bantuan |

---

## 🧠 Filosofi

> *"Local first. Control over convenience. Transparency over magic."*

Termux App Store dibuat untuk pengguna yang ingin:
- Memahami sepenuhnya apa yang dijalankan di perangkat mereka
- Mengontrol build dan source secara langsung
- Menghindari vendor lock-in dan ketergantungan cloud
- Berbagi tool dengan komunitas Termux secara terbuka

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat [LICENSE](LICENSE) untuk detail.

---

## 👤 Maintainer

<div align="center">

**Djunekz** — Independent & Official Developer

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

</div>

---

## ⭐ Dukung Proyek Ini

Jika Termux App Store berguna untukmu:

- ⭐ **Star** repo ini — membantu orang lain menemukannya
- 🧩 **Bagikan** ke komunitas Termux & Android
- 🐛 **Laporkan bug** via Issues
- 🔀 **Kirim PR** untuk perbaikan apapun

---

<div align="center">

**© Termux App Store — Built for everyone, by the community.**

*termux · termux app store · termux package manager · termux tui · android terminal tools · termux tools · termux packages · termux cli*

</div>
