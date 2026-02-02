# Termux App Store

![Release](https://img.shields.io/github/v/release/djunekz/termux-app-store?logo=iterm2&style=flat-square)
![License](https://img.shields.io/github/license/djunekz/termux-app-store?logo=open-source-initiative&style=flat-square)
![Issues](https://img.shields.io/github/issues/djunekz/termux-app-store?logo=openbugbounty&style=flat-square)
![PRs](https://img.shields.io/github/issues-pr/djunekz/termux-app-store?logo=git&style=flat-square)
![Downloads](https://img.shields.io/github/downloads/djunekz/termux-app-store/total?logo=abdownloadmanager&style=flat-square)
![Contributors](https://img.shields.io/github/contributors/djunekz/termux-app-store?logo=github&style=flat-square)
![Stars](https://img.shields.io/github/stars/djunekz/termux-app-store?logo=starship&style=flat-square)
![Forks](https://img.shields.io/github/forks/djunekz/termux-app-store?logo=refinedgithub&style=flat-square)

> 🧠 **Offline-first • Source-based • Binary-safe • Termux-native**

**Termux App Store** adalah **TUI (Terminal User Interface)** berbasis **Textual (Python)** yang memungkinkan pengguna Termux untuk **menelusuri, membangun, dan mengelola aplikasi** dari skrip build secara lokal — tanpa akun, tanpa telemetry, dan tanpa ketergantungan cloud.

---

## ✨ Fitur Utama

- 📦 **Package Browser (TUI)**  
  Jelajahi paket berbasis folder `packages/` secara interaktif

- 🧠 **Smart Build Validator**
  - Deteksi dependency tidak didukung Termux
  - Badge `UNSUPPORTED`, `UPDATE`, `INSTALLED`, `NEW`

- 🔍 **Search & Filter**
  Cari paket berdasarkan nama atau deskripsi secara real-time

- ⚙️ **One-Click Build**
  Install / update paket via `build-package.sh`

- 🧩 **Portable Execution**
  Dapat dijalankan dari direktori mana pun selama folder `termux-app-store/packages` tersedia

- 🧬 **Binary Release Ready**
  Source Python tersembunyi di balik binary (PyInstaller / Nuitka)

- 🧠 **Self-Healing Path Resolver**
  Auto-detect lokasi app meski folder dipindah atau di-rename

- 🔐 **Privacy-First**
  Tanpa akun, tanpa tracking, tanpa telemetry

---

## 🧱 Arsitektur
Detail: lihat [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🚀 Instalasi (Binary Release)

### Install via Installer (Disarankan)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/main/install.sh
```
Lalu jalankan:
```
termux-app-store
```
---

## 🧠 Cara Kerja
1. Aplikasi mencari folder termux-app-store/packages
2. Membaca metadata dari build.sh
3. Menampilkan paket di UI
4. Menjalankan build via build-package.sh
5. Menampilkan log & progress real-time

---

## 🧩 Struktur Package
Setiap package **WAJIB** memiliki:
```
packages/<name_tool>/build.sh
```
Contoh isi minimal file `build.sh`:
```.Text
TERMUX_PKG_HOMEPAGE=
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@author-repository"
TERMUX_PKG_VERSION=
TERMUX_PKG_SRCURL=
TERMUX_PKG_SHA256=
```
Contoh file `build.sh`:
berada di folder `template/build.sh`

---

## 🔴 Badge Status
- 🟢 NEW - Paket baru (<7 hari)
- 🟡 UPDATE - Versi tersedia lebih baru
- 🟢 INSTALLED - Versi sudah terpasang
- 🔴 UNSUPPORTED - Dependency tidak tersedia di Termux

---

## 🔐 Keamanan
- Tidak meminta permission tambahan
- Tidak membuka port
- Tidak menjalankan service background
- Build dijalankan atas perintah user
Detail lengkap: [SECURITY.md](SECURITY.md)

---

## 🛡️ Privasi
- Tanpa akun
- Tanpa analytics
- Tanpa telemetry
- Offline-first
Detail lengkap: [PRIVACY.md](PRIVACY.md)

---

## 🧪 Binary Disclaimer
Binary release:
- Dibangun dari source publik
- Tidak dimodifikasi pasca-build
- Dianjurkan verifikasi checksum
Detail lengkap: [DISCLAIMER.md](DISCLAIMER.md)

---

## 🤝 Kontribusi
Kontribusi sangat diterima!
- Tambah package
- Perbaiki build script
- Audit security
- Perbaiki dokumentasi
Panduan: [CONTRIBUTING.md](CONTRIBUTING.md)

---


## 📜 Lisensi
Proyek ini dilisensikan di bawah:
**MIT License**
Lihat file [LICENSE](LICENSE)

---

## 🧭 Roadmap
- [ ] Package rating
- [ ] Dependency graph visual
- [ ] Offline package cache
- [ ] Multi-arch prebuilt cache
- [ ] Plugin system

---

## ❓ FAQ & Bantuan
- **FAQ.md** [disini](FAQ.md)
- **TROUBLESHOOTING.md** [disini](TROUBLESHOOTING.md)

---

## 🧠 Filosofi
> “Local first. Control over convenience. Transparency over magic.”
Termux App Store dibuat untuk pengguna yang ingin:
- Memahami apa yang dijalankan
- Mengontrol build
- Menghindari vendor lock-in

---

## 👤 Maintainer / Developer
@djunekz
Independent Developer

---

## ⭐ Dukungan
Jika proyek ini membantu:
- ⭐ Star repo
- 🐛 Laporkan issue
- 🔀 Kirim PR

© Termux App Store — Built for everyone.
