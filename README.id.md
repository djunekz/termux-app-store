![[Termux App Store — Package Manager TUI untuk Termux](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — Package Manager TUI & CLI untuk Termux](https://djunekz.github.io/termux-app-store/)

**Package manager TUI pertama yang offline-first dan binary-safe, dibangun khusus untuk Termux di Android.**

[![CI](https://github.com/djunekz/termux-app-store/actions/workflows/build.yml/badge.svg)](https://github.com/djunekz/termux-app-store/actions)
[![Codecov](https://codecov.io/github/djunekz/termux-app-store/branch/master/graph/badge.svg?token=357W4EP8G0)](https://codecov.io/github/djunekz/termux-app-store)
[![PyPI](https://img.shields.io/pypi/v/termux-app-store?style=flat&logo=pypi&color=3fb950&label=pypi)](https://pypi.org/project/termux-app-store/)
[![Versi](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fapi.github.com%2Frepos%2Fdjunekz%2Ftermux-app-store%2Ftags&query=%24%5B0%5D.name&style=flat&logo=github&color=3fb950&label=rilis)](https://github.com/djunekz/termux-app-store/releases)
[![Unduhan](https://img.shields.io/github/downloads/djunekz/termux-app-store/total?style=flat&logo=github&color=3fb950&logoColor=white)](https://github.com/djunekz/termux-app-store)
[![Lisensi](https://img.shields.io/badge/Lisensi-MIT-3fb950?style=flat&logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Stars](https://img.shields.io/github/stars/djunekz/termux-app-store?style=flat&logo=github&color=white&label=stars&cacheSeconds=3600)](https://github.com/djunekz/termux-app-store/stargazers)
[![Forks](https://img.shields.io/github/forks/djunekz/termux-app-store?style=flat&logo=github&color=white&cacheSeconds=3600)](https://github.com/djunekz/termux-app-store/network)
[![Issues](https://img.shields.io/badge/issues-open-3fb950?style=flat&logo=github&logoColor=white)](https://github.com/djunekz/termux-app-store/issues)
[![PRs](https://img.shields.io/github/issues-pr/djunekz/termux-app-store?style=flat&logo=git&logoColor=white&color=3fb950)](https://github.com/djunekz/termux-app-store/pulls)
[![Komunitas](https://img.shields.io/badge/Komunitas-Terbuka-3fb950?style=flat&logo=github)](https://github.com/djunekz/termux-app-store)

> **Offline-first • Binary-safe • Berbasis Source • Native Termux • Android Terminal**
> Install dan kelola package Termux — binary pre-built atau build dari source — tanpa root, tanpa akun, tanpa telemetri.

> Baca dengan bahasa lain: 🇬🇧 **[English](README.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

---

## Apa itu Termux App Store?

**Termux App Store** (`termux-app-store`) adalah **package manager TUI (Terminal User Interface)** dan **CLI** yang dibangun dengan Python ([Textual](https://github.com/Textualize/textual)). Memungkinkan pengguna Termux di Android untuk **menjelajah, menginstal, dan mengelola tools/paket** langsung di perangkat — tanpa akun, tanpa telemetri, tanpa koneksi cloud, tanpa root.

Mulai dari **v0.4.0**, Termux App Store hadir dengan **fast install engine**: paket diunduh sebagai binary `.deb` pre-built dari mirror pool (GitHub Pages, Cloudflare CDN, jsDelivr), dengan cache lokal `.deb` (TTL 7 hari) dan verifikasi SHA256 per arsitektur. Build dari source tetap tersedia via `fix-install` untuk kontrol penuh.

Proyek ini bekerja sebagai **alternatif package manager untuk Termux**, memungkinkan kamu menginstal tools komunitas dari source menggunakan skrip `build.sh` yang terverifikasi — mirip semangat AUR (Arch User Repository) tapi dirancang khusus untuk Termux di Android.

> **Apa bedanya dengan `termux-packages` dan TUR (Termux User Repository)?**
>
> - `termux-packages` adalah repo resmi Termux — dikelola tim inti, butuh approval PR, hanya menerima tools populer.
> - TUR adalah ekstensi kurasi, tetap butuh review kontributor.
> - **Termux App Store** sepenuhnya digerakkan komunitas: siapa pun bisa submit `build.sh`, paket didistribusikan sebagai `.deb` pre-built atau build dari source, tanpa gerbang approval terpusat.

> [!IMPORTANT]
> Termux App Store **bukan auto-installer tersembunyi**.
> Semua instalasi — binary maupun source — berjalan **secara lokal, transparan, dan sepenuhnya di bawah kendali pengguna**.

---

## Untuk Siapa?

| Pengguna | Kebutuhan |
|---|---|
| Pengguna Termux | Install binary cepat atau kontrol penuh build dari source |
| Developer | Distribusi tools via `.deb` pre-built atau source packaging |
| Reviewer & Auditor | Memeriksa dan memvalidasi skrip build |
| Maintainer | Mengelola banyak paket Termux sekaligus |

---

## Tangkapan Layar

<div align="center">

<img src=".assets/0.jpeg" width="74%" alt="Termux App Store — Tampilan Utama"/>

<br/><br/>
<H1>Antarmuka TUI</H1>

| TUI Utama | TUI Install | Menu Palette |
|:---:|:---:|:---:|
| <img src=".assets/0main.jpg" width="220" alt="TUI Main Interface"/> | <img src=".assets/1install.jpg" width="220" alt="TUI Install Interface"/> | <img src=".assets/2pallete.jpg" width="220" alt="Menu Palette Interface"/> |
| Menu utama TUI | Proses install paket | Command palette |

> TUI ramah pengguna dengan dukungan **touchscreen** penuh

---

<H1>Antarmuka CLI</H1>

| Dukungan tools lain | CLI Install | CLI View |
|:---:|:---:|:---:|
| <img src=".assets/0tas-and-termux-build.jpg" width="220" alt="Other tools support"/> | <img src=".assets/0cli-install.jpg" width="220" alt="CLI Install Interface"/> | <img src=".assets/0cli-view.jpg" width="220" alt="CLI View Interface"/> |
| tasctl dan termux-build | Proses install paket | CLI help, list dan show |

---

<H1>GuideBook</H1>

| Daftar menu | Menu tentang | Menu cara upload |
|:---:|:---:|:---:|
| <img src=".assets/0guide-menu.png" width="220" alt="List menu"/> | <img src=".assets/0guide-about.png" width="220" alt="Menu about"/> | <img src=".assets/0guide-upload.png" width="220" alt="Menu how to upload"/> |
| Menu utama GuideBook | Informasi termux-app-store | Panduan cara upload |

> GuideBook adalah panduan informasi, jalankan: `python guidebook.py`

</div>

### Demo Video

| Rekaman `termux-app-store` TUI, CLI, tools lain `tasctl`, `termux-build`, `guidebook.py` |
|---|
| [![termux-app-store demo](.assets/demo.gif)](https://github.com/djunekz/termux-app-store/blob/master/.assets/demo.gif) |

---

## Cara Install dan Uninstall

> Tersedia di **[PyPI](https://pypi.org/project/termux-app-store/)** — bisa langsung diinstall via pip.

### Pilihan 1 (Direkomendasikan)

```bash
pkg install python
pip install termux-app-store
```

### Pilihan 2 (Manual)

> Sederhana (cocok jika memori terbatas)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> Dengan git clone (untuk download semua file repository)

```bash
git clone --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

Setelah install, jalankan:

```bash
termux-app-store        # Buka TUI interaktif
termux-app-store -h     # Tampilkan bantuan CLI
tas                     # Perintah singkat untuk termux-app-store
```

### Uninstall

```bash
pip uninstall termux-app-store
# atau
./tasctl uninstall
```

---

## Cara Penggunaan

### TUI — Antarmuka Interaktif

```bash
termux-app-store
# atau perintah singkat:
tas
```

### CLI — Perintah Langsung

```bash
termux-app-store list                       # Tampilkan semua paket
termux-app-store show <paket>               # Lihat detail paket
termux-app-store install <paket>            # Fast install (binary .deb pre-built)
termux-app-store install pkg1 pkg2 pkg3     # Install beberapa paket sekaligus
termux-app-store fix-install <paket>        # Paksa build dari source
termux-app-store search <kata-kunci>        # Cari paket berdasarkan nama atau deskripsi
termux-app-store update                     # Cek pembaruan yang tersedia
termux-app-store upgrade                    # Upgrade semua paket
termux-app-store upgrade <paket>            # Upgrade paket tertentu
termux-app-store uninstall <paket>          # Hapus paket
termux-app-store mirrors                    # Cek status mirror
termux-app-store cache info                 # Info binary cache
termux-app-store cache clear                # Bersihkan binary cache
termux-app-store version                    # Cek versi terbaru
termux-app-store help                       # Bantuan lengkap
```

---

## Fitur Unggulan

| **Browser Paket (TUI)** Jelajahi paket dari folder `packages/` secara interaktif dengan keyboard & touchscreen.<br>**Fast Install Engine** Download `.deb` pre-built dari mirror pool — GitHub Pages, Cloudflare CDN, jsDelivr — dengan fallback otomatis.<br>**Binary Cache** Cache `.deb` lokal dengan TTL 7 hari dan verifikasi SHA256 per arsitektur. Paket yang sudah di-cache langsung diinstall.<br>**Validator Build Cerdas** Mendeteksi dependensi Termux yang tidak didukung dengan badge status otomatis. | **Pencarian & Filter Real-time** Cari paket berdasarkan nama atau deskripsi — termasuk perintah CLI `search`/`find`.<br>**Install/Uninstall Multi-paket** Install atau hapus beberapa paket sekaligus dengan ringkasan output.<br>**Kelola Satu Klik** Install / update / uninstall Termux App Store sendiri via `./tasctl`.<br>**Privasi Utama** Tanpa akun, tanpa tracking, tanpa telemetri — sepenuhnya offline setelah sinkronisasi mirror. |
|---|---|

---

## Badge Status Paket

| Badge | Keterangan |
|---|---|
| **NEW** | Paket baru ditambahkan (< 7 hari) |
| **UPDATE** | Versi baru tersedia |
| **INSTALLED** | Versi terpasang sudah terbaru |
| **UNSUPPORTED** | Dependensi tidak tersedia di Termux |

---

## Cara Kerja Fast Install (v0.4.0+)

```
termux-app-store install <paket>
        │
        ▼
  Cek cache .deb lokal (TTL 7 hari)
        │ cache HIT              │ cache MISS
        ▼                        ▼
  Verifikasi SHA256         Coba mirror secara berurutan:
  (per arsitektur)          1. GitHub Pages (utama)
        │                   2. Cloudflare CDN
        ▼                   3. jsDelivr CDN
  dpkg -i                   4. Raw GitHub (fallback)
                                 │
                                 ▼
                           Download .deb
                           Verifikasi SHA256 (sha256_by_arch)
                           Cache lokal
                           dpkg -i
```

> Jika fast install gagal, gunakan `fix-install <paket>` untuk memaksa build penuh dari source via `build-package.sh`.

---

## Cara Membuat Paket Sendiri

Setiap paket di Termux App Store hanya butuh satu file `build.sh` — mirip cara kerja PKGBUILD di Arch Linux, tapi disesuaikan untuk Termux.

Setiap paket **wajib** memiliki file `build.sh`:

```
packages/<nama-tool>/build.sh
```

### Template Minimal `build.sh`

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@username-github-kamu"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

> [!NOTE]
> Lihat template lengkap di `template/build.sh` atau jalankan: `./termux-build template`

### Membuat Paket dengan `termux-build`

```bash
cd termux-app-store
./termux-build create nama-tool-kamu
# atau auto-create dari URL GitHub:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> Jangan gunakan spasi dalam penamaan — gunakan tanda `-`. Contoh: `tool-buatan-saya`

---

## termux-build — Tool Validasi dan Build

`termux-build` adalah tool bantu validasi dan review — bukan auto-upload atau auto-publish.

```bash
./termux-build create <paket>      # Buat paket untuk distribusi
./termux-build init <url-repo>     # Auto buat dan build paket dari URL GitHub
./termux-build lint <paket>        # Lint skrip build
./termux-build check-pr <paket>    # Cek kesiapan PR
./termux-build doctor              # Diagnosa environment
./termux-build suggest <paket>     # Saran perbaikan paket
./termux-build explain <paket>     # Penjelasan detail paket
./termux-build template            # Generate template build.sh
./termux-build guide               # Panduan kontribusi
```

> [!NOTE]
> `termux-build` **hanya membaca dan memvalidasi** — tidak memodifikasi file atau upload ke GitHub.

---

## tasctl — Termux App Store Controller

```bash
./tasctl install       # Install Termux App Store (terbaru)
./tasctl update        # Update ke versi terbaru
./tasctl uninstall     # Hapus Termux App Store
./tasctl doctor        # Diagnosa environment
./tasctl self-update   # Update tasctl itu sendiri
./tasctl help          # Tampilkan bantuan
```

---

## guidebook — Panduan Lengkap

```bash
python guidebook.py
```

> [!NOTE]
> guidebook saat ini mendukung dua bahasa: Bahasa Indonesia dan English.

---

## Cara Distribusi Package ke Komunitas Termux

```bash
# 1. Fork repo ini di GitHub
# 2. Tambahkan folder paket kamu:
mkdir packages/nama-tool-kamu
# 3. Buat build.sh dari template atau dengan termux-build:
./termux-build create nama-tool-kamu
# atau dari URL GitHub:
./termux-build init https://github.com/kamu/repo-kamu
# 4. Validasi sebelum submit:
./termux-build lint packages/nama-tool-kamu
# 5. Submit Pull Request ke repo ini
```

> Panduan lengkap: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

## Arsitektur

```
termux-app-store/
├── packages/              # Direktori semua paket
│   └── <nama-tool>/
│       └── build.sh       # Metadata & skrip build
├── template/
│   └── build.sh           # Template paket
├── core/
│   ├── binary_core.py     # BinaryCache — cache .deb lokal + unduh dari mirror
│   ├── mirrors.py         # MirrorManager — registry pool mirror
│   ├── package.py         # Package dataclass
│   └── validator.py       # PackageValidator
├── utils/
│   └── installer.py       # Helper install_from_binary / install_from_source
├── tools/
│   └── mirrors.json       # Registry mirror (GitHub Pages, Cloudflare, jsDelivr, raw GitHub)
├── fast_install.py        # Fast install engine (unduh .deb + cache + verifikasi SHA256)
├── tasctl                 # Installer/updater/uninstaller TAS
├── termux-build           # Tool validasi & review
└── install.sh             # Installer utama
```

> Detail lengkap: [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Keamanan & Privasi

| **Keamanan** | **Privasi** |
|---|---|
| Tidak butuh izin tambahan | Tanpa akun atau registrasi |
| Tidak membuka port jaringan | Tanpa analitik atau tracking |
| Tidak ada layanan berjalan di background | Tanpa telemetri apapun |
| Build hanya berjalan atas perintah eksplisit | Offline-first by design |
| Verifikasi SHA256 pada semua unduhan `.deb` | Sumber binary transparan dan bisa diaudit |

> Detail lengkap: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

## Kontribusi

Semua kontribusi sangat disambut!

| Cara Berkontribusi | Keterangan |
|---|---|
| Tambah paket | Submit tool paket baru |
| Laporkan bug | Buka issue di GitHub |
| Kirim PR | Perbaikan kode atau dokumentasi |
| Review PR | Bantu validasi kontribusi orang lain |
| Audit keamanan | Review keamanan skrip build |
| Perbaiki dokumentasi | Perjelas atau terjemahkan dokumentasi |

> Panduan lengkap: [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Bantuan & Dokumentasi

| Dokumen | Keterangan |
|---|---|
| [FAQ](FAQ.md) | Pertanyaan yang sering ditanyakan |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | Solusi masalah umum |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | Cara upload tool kamu |
| [CONTRIBUTING](CONTRIBUTING.md) | Panduan kontribusi |
| [SUPPORT](SUPPORT.md) | Cara mendapat bantuan |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | Catatan distribusi binary |

---

## Filosofi

> *"Lokal lebih utama. Kontrol di atas kemudahan. Transparansi di atas keajaiban."*

Termux App Store dibangun untuk pengguna yang ingin:

- Benar-benar memahami apa yang berjalan di perangkat mereka
- Mengontrol build dan sumber secara langsung
- Menghindari ketergantungan vendor dan cloud
- Berbagi tools secara terbuka dengan komunitas Termux

---

## Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat [LICENSE](LICENSE) untuk detail.

---

## Maintainer

**Djunekz** — Developer Independen & Resmi

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

## Dukung Proyek Ini

Jika Termux App Store bermanfaat untukmu:

- **Beri bintang** repo ini — membantu orang lain menemukannya
- **Bagikan** di komunitas Termux & Android Indonesia
- **Laporkan bug** via Issues
- **Submit PR** untuk perbaikan apapun
- **Sponsor**: https://saweria.co/redHh

---

## Kata Kunci Pencarian

> Proyek ini dikembangkan secara independen dan **tidak berafiliasi** dengan proyek resmi [Termux](https://github.com/termux/termux-app).

**Kata kunci:** termux app store · package manager termux · alternatif termux-packages · alternatif TUR termux · cara install tools termux · cara distribusi package termux · cara share tool di termux · bikin paket termux sendiri · termux tui android · termux cli android · termux install binary · termux deb installer · termux tools tanpa root · termux package manager Indonesia · install aplikasi di termux · termux community packages · termux build dari source · termux offline · custom repo termux · termux-app-store djunekz · perintah tas termux

---

**© Termux App Store — Dibuat untuk semua, oleh komunitas.**
