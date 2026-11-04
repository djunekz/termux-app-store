![[Termux App Store — Package Manager TUI untuk Termux](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — Cara Install Tool di Termux Tanpa Ribet](https://djunekz.github.io/termux-app-store/)

**Package manager TUI dan CLI yang local-first, dibangun khusus untuk Termux di Android, dengan instalasi binary terverifikasi checksum dan fallback build dari source. Seperti AUR, tapi untuk Termux.**

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


> **Local-first • Checksum-verified • Berbasis Source • Native Termux • Android Terminal**
> Install dan kelola package Termux — binary pre-built atau build dari source — tanpa root, tanpa akun, tanpa telemetri.

> Baca dengan bahasa lain: 🇬🇧 **[English](README.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

---

## Masalah yang sering kamu hadapi di Termux

Kalau kamu pengguna Termux, pasti pernah mengalami ini:

- Mau install tool dari GitHub, tapi harus `git clone`, `chmod +x`, `bash install.sh` satu per satu
- Tidak tahu tool apa saja yang tersedia untuk Termux selain yang ada di `pkg`
- Sudah install banyak tool, tapi susah melacak mana yang perlu diupdate
- Internet tidak stabil, tapi butuh install tool secara offline

**Termux App Store hadir untuk menyelesaikan semua itu.**

---

## Apa itu Termux App Store?

**Termux App Store** (`termux-app-store`) adalah **package manager TUI (Terminal User Interface)** dan **CLI** yang dibangun dengan Python ([Textual](https://github.com/Textualize/textual)). Memungkinkan pengguna Termux di Android untuk **menjelajah, menginstal, dan mengelola tools/paket** langsung di perangkat — tanpa akun, tanpa telemetri, tanpa root. Metadata paket dan unduhan memakai jaringan.

Mulai dari **v0.4.0**, Termux App Store hadir dengan **fast install engine**: paket diunduh sebagai binary `.deb` pre-built dari mirror pool (GitHub Pages, Cloudflare CDN, jsDelivr), dengan cache lokal `.deb` (TTL 7 hari) dan setiap `.deb`, termasuk dari cache, wajib cocok dengan SHA256 per arsitektur atau ditolak. SHA256 mendeteksi file rusak atau tidak cocok, bukan tanda tangan penerbit. Build dari source tetap tersedia via `fix-install` untuk kontrol penuh.

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
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
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

| Tombol / tombol keyboard | Fungsi |
|---|---|
| **Install / Update / Open** (`Ctrl+I`) | Tombol utama mengikuti paket: Install jika belum terpasang, Update jika ada versi baru, Open jika sudah terpasang dan terbaru. Open menjalankan tool (pilih command, isi argumen) dan kembali ke TUI setelah kamu menekan Enter |
| **Shortcut** (dialog Open) | Membuat skrip Termux:Widget di `~/.shortcuts` yang menjalankan tool dengan argumenmu |
| **Upgrade all** (banner update) | Banner menampilkan jumlah paket terpasang yang punya versi baru dan memasukkan semuanya ke antrean |
| **Cancel** (`Ctrl+X`) | Menghentikan download atau build source yang berjalan di titik aman berikutnya |
| `F4` | Riwayat aktivitas: install, update, hapus, dan jalankan |
| `F5` | Laporkan masalah: membuka form bug report yang sudah terisi |
| `Ctrl+R` / `Ctrl+Q` | Refresh paket / keluar |
| `Ctrl+P` | Command palette, termasuk menyalakan atau mematikan notifikasi (butuh Termux:API) |

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

| **Browser Paket (TUI)** Jelajahi paket dari folder `packages/` secara interaktif dengan keyboard & touchscreen.<br>**Fast Install Engine** Download `.deb` pre-built dari mirror pool — GitHub Pages, Cloudflare CDN, jsDelivr — dengan fallback otomatis.<br>**Binary Cache** Cache `.deb` lokal dengan TTL 7 hari; file cache diverifikasi ulang terhadap SHA256 per arsitektur sebelum setiap instalasi.<br>**Validator Build Cerdas** Mendeteksi dependensi Termux yang tidak didukung dengan badge status otomatis. | **Pencarian & Filter Real-time** Cari paket berdasarkan nama atau deskripsi — termasuk perintah CLI `search`/`find`.<br>**Install/Uninstall Multi-paket** Install atau hapus beberapa paket sekaligus dengan ringkasan output.<br>**Kelola Satu Klik** Install / update / uninstall Termux App Store sendiri via `./tasctl`.<br>**Privasi Utama** Tanpa akun, tanpa tracking, tanpa telemetri — tetap bisa dipakai dari data lokal yang sudah ada; mengambil metadata dan paket butuh jaringan. |
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
  Verifikasi SHA256         Probe mirror, pakai yang tercepat:
  (per arsitektur)          1. Cloudflare CDN
        │                   2. GitHub Pages
        ▼                   3. jsDelivr CDN
  dpkg -i                         │
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
| Build hanya berjalan atas perintah eksplisit | Local-first; jaringan dipakai untuk metadata dan unduhan |
| SHA256 wajib untuk setiap `.deb` (unduhan dan cache) | Sumber binary transparan dan bisa diaudit |

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
- Menghindari ketergantungan vendor
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

**Kata kunci:** cara install tool di termux · cara install aplikasi di termux · termux install tools tanpa root · package manager termux android · termux install tools dari github · termux package manager alternatif · AUR untuk termux · termux community tools · cara distribusi tool termux · bikin paket termux sendiri · termux tui android · termux cli android · termux install binary · termux deb installer · termux tools tanpa root · termux package manager Indonesia · install aplikasi di termux · termux community packages · termux build dari source · termux offline · custom repo termux · termux-app-store · termux-app-store djunekz · alternatif termux-packages · alternatif TUR termux · termux package browser · cara share tool termux · termux tool list indonesia · termux fast install · termux offline installer · termux app store github

---

**© Termux App Store — Dibuat untuk semua, oleh komunitas.**
