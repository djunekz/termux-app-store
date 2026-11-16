![[Termux App Store — TUI Package Manager for Termux](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)

# [Termux App Store — Package Manager TUI & CLI untuk Termux](https://djunekz.github.io/termux-app-store/)

**Package manager TUI dan CLI yang local-first, dibangun native untuk Termux di Android, dengan instalasi binary terverifikasi checksum dan fallback build dari source.**

> Baca dalam: 🇬🇧 **[English](README.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

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

> **Local-first • Terverifikasi checksum • Berbasis source • Native Termux • Terminal Android**
> Install dan kelola paket Termux — binary pre-built atau build dari source — tanpa root, tanpa akun, tanpa telemetri.

---

# Apa itu Termux App Store?

**Termux App Store** (`termux-app-store`) adalah **TUI (Terminal User Interface)** dan **package manager CLI** yang dibangun dengan Python ([Textual](https://github.com/Textualize/textual)), memungkinkan pengguna Termux di Android untuk **menjelajah, menginstal, dan mengelola tools/paket** langsung di perangkat — tanpa akun, tanpa telemetri, tanpa root. Metadata paket dan unduhan menggunakan jaringan.

Mulai dari **v0.4.0**, Termux App Store mendukung **fast install engine**: paket diunduh sebagai binary `.deb` pre-built dari mirror pool (GitHub Pages, Cloudflare CDN, jsDelivr), dengan cache `.deb` lokal (TTL 7 hari). Setiap `.deb`, termasuk yang dari cache, harus cocok dengan SHA256 per arsitektur, jika tidak akan ditolak. SHA256 mendeteksi file yang rusak atau tidak cocok; ini bukan tanda tangan penerbit. Build dari source tetap tersedia lewat `fix-install`.

Ini bekerja sebagai **package manager alternatif untuk Termux**, memungkinkan kamu menginstal tools komunitas menggunakan skrip `build.sh` — mirip semangat AUR (Arch User Repository), tetapi dirancang khusus untuk Termux di Android.

> **Apa bedanya dengan `termux-packages` atau TUR (Termux User Repository)?**
>
> - `termux-packages` adalah repo resmi Termux — dikelola tim inti, butuh persetujuan PR, dan hanya menerima tools yang banyak dipakai.
> - TUR adalah ekstensi yang dikurasi, tetap butuh review kontributor.
> - **Termux App Store** sepenuhnya digerakkan komunitas: siapa pun bisa mengirim `build.sh`, paket didistribusikan sebagai `.deb` pre-built atau build dari source, dan tidak ada gerbang persetujuan terpusat. Anggap saja sebagai lapisan paket personal + komunitas di atas Termux.

> [!IMPORTANT]
> Termux App Store **bukan auto-installer tersembunyi**.
> Semua instalasi — binary maupun source — berjalan **secara lokal, transparan, dan sepenuhnya di bawah kendali pengguna**.

---

# Untuk Siapa?

| Pengguna | Kebutuhan |
|---|---|
| Pengguna Termux | Install binary cepat atau kontrol penuh build dari source |
| Developer | Distribusi tools lewat `.deb` pre-built atau source packaging |
| Reviewer & Auditor | Meninjau dan memvalidasi skrip build |
| Maintainer | Mengelola banyak paket Termux sekaligus |

---

<div align="center">
<img src="https://github.com/user-attachments/assets/b03419bc-8efe-4ed0-9b61-fea5153e9f53" width="100%" alt="Termux App Store — Main View"/>

<br/><br/>
<H1>Antarmuka TUI</H1>

| Antarmuka Utama TUI | Antarmuka Install TUI | Menu Palette |
|:---:|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/fb9395f1-f943-44c5-b88f-be18e480fd26" width="400" alt="TUI Main Interface"/> | <img src="https://github.com/user-attachments/assets/a0ee7a15-95d2-4743-9f7e-90cd9e3388f7" width="400" alt="TUI Install Interface"/> | <img src="https://github.com/user-attachments/assets/ad760153-983f-4113-a465-2b682cb26b67" width="400" alt="Menu Palette Interface"/> |
| Menu utama TUI | Proses install paket | Command palette |

> TUI ramah pengguna dengan dukungan **layar sentuh** penuh

---

<H1>Antarmuka CLI dan Dukungan Tools Lain</H1>

| Tampilan CLI dan dukungan tools lain | Guidebook |
|:---:| :---: |
| https://github.com/user-attachments/assets/71c097b2-01a8-4c1c-9ffd-c26f29ee6ae6 | https://github.com/user-attachments/assets/b668a890-835f-4467-820a-988b1810c902 |


Antarmuka CLI dan dukungan tools: `tasctl`, `termux-build`, `doctor.py`, `pkg-scaffold.py`, `build-package.sh`, `guidebook.py`

---

<H1>Rekaman Layar</H1>

| Rekaman `termux-app-store` TUI, CLI, tools lain `tasctl`, `termux-build`, `guidebook.py` |
|:---:|
| <img src="https://github.com/user-attachments/assets/152c757f-d2a3-4f31-8174-2b857a3aad51" width="100%" alt="termux-app-store"/> | termux-app-store

</div>

---

# Install dan Uninstall Cepat

> Tersedia di **[PyPI](https://pypi.org/project/termux-app-store/)** — bisa dicari dan terindeks, mudah ditemukan.

### Pilihan 1 (Direkomendasikan)

```bash
pkg install python
pip install termux-app-store
```

### Pilihan 2 (Manual)

> Sederhana (direkomendasikan jika memori terbatas)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> Dengan git clone (mengunduh seluruh repositori)

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

Setelah install, jalankan:

```bash
termux-app-store        # Open interactive TUI
termux-app-store -h     # Show CLI help
tas                     # Shorthand for termux-app-store
```

### Uninstall

```bash
pip uninstall termux-app-store
# or
./tasctl uninstall
```

---

# Cara Penggunaan

### TUI — Antarmuka Interaktif

```bash
termux-app-store
# or shorthand:
tas
```

| Tombol / key | Fungsinya |
|---|---|
| **Install / Update / Open** (`Ctrl+I`) | Tombol utama mengikuti kondisi paket: Install jika belum terpasang, Update jika ada versi lebih baru, Open jika sudah terpasang dan terbaru. Open menjalankan tool (pilih perintah, tambahkan argumen) lalu kembali ke TUI setelah kamu menekan Enter |
| **Shortcut** (dialog Open) | Membuat skrip Termux:Widget di `~/.shortcuts` yang menjalankan tool dengan argumenmu |
| **Upgrade all** (banner update) | Banner menampilkan jumlah paket terpasang yang punya versi lebih baru dan mengantrekan semuanya |
| **Cancel** (`Ctrl+X`) | Menghentikan unduhan atau build source yang sedang berjalan pada titik aman berikutnya |
| `F4` | Riwayat aktivitas: install, update, penghapusan, dan peluncuran |
| `F5` | Laporkan masalah: membuka formulir laporan bug yang sudah terisi |
| `Ctrl+R` / `Ctrl+Q` | Refresh paket / keluar |
| `Ctrl+P` | Command palette, termasuk notifikasi aktif atau nonaktif (butuh Termux:API) |

### CLI — Perintah Langsung

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

# Fitur

| **Package Browser (TUI)** Jelajahi paket dari folder `packages/` secara interaktif dengan navigasi keyboard & layar sentuh.<br>**Fast Install Engine** Mengunduh `.deb` pre-built dari mirror pool — GitHub Pages, Cloudflare CDN, jsDelivr — dengan fallback otomatis.<br>**Binary Cache** Cache `.deb` lokal dengan TTL 7 hari; file cache diverifikasi ulang terhadap SHA256 per arsitektur sebelum setiap install. Paket yang sudah di-cache terpasang seketika.<br>**Smart Build Validator** Mendeteksi dependensi Termux yang tidak didukung dengan badge status otomatis. | **Pencarian & Filter Real-time** Cari paket berdasarkan nama atau deskripsi — termasuk perintah CLI `search`/`find`.<br>**Install/Uninstall Multi-paket** Pasang atau hapus beberapa paket dalam satu perintah dengan ringkasan hasil.<br>**Kelola dengan Satu Klik** Install / update / uninstall Termux App Store itu sendiri lewat `./tasctl`.<br>**Privasi Utama** Tanpa akun, tanpa pelacakan, tanpa telemetri. Bekerja dari data lokal jika sudah tersedia; mengambil metadata dan paket membutuhkan jaringan. |
|---|---|

---

# Cara Kerja Fast Install (v0.4.0+)

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

> Jika fast install gagal, gunakan `fix-install <package>` untuk memaksa build source penuh lewat `build-package.sh`.

---

# Menambahkan Paket

Setiap paket di Termux App Store didefinisikan oleh satu file `build.sh` — mirip cara kerja PKGBUILD di Arch Linux, tetapi disesuaikan untuk Termux di Android.

Setiap paket **wajib** memiliki file `build.sh`:

```
packages/<tool-name>/build.sh
```

### Template Minimal `build.sh`

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
> Lihat template lengkap di `template/build.sh` atau jalankan: `./termux-build template`

### Menambahkan Paket dengan termux-build

```bash
cd termux-app-store
./termux-build create your-tool-name
# or auto-create from a GitHub URL:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> Saat memberi nama, jangan gunakan spasi — gunakan `-`. Contoh: `my-tool-name`

---

# termux-build — Tool Build & Validasi

`termux-build` adalah tool bantu validasi dan review — bukan tool upload atau publish otomatis.

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
> `termux-build` **hanya membaca dan memvalidasi** — tidak mengubah file dan tidak mengunggah ke GitHub.

---

# tasctl — Termux App Store Controller

`tasctl` adalah controller untuk sistem termux-app-store.

```bash
./tasctl install       # Install Termux App Store (latest)
./tasctl update        # Update to latest version
./tasctl uninstall     # Remove Termux App Store
./tasctl doctor        # Diagnose environment
./tasctl self-update   # Update tasctl itself
./tasctl help          # Show help
```

---

# guidebook — Semua Informasi tentang Termux App Store

```bash
python guidebook.py
```

> [!NOTE]
> guidebook saat ini mendukung dua bahasa: Inggris dan Bahasa Indonesia.

---

# Cara Mendistribusikan Paket ke Komunitas Termux

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

> Panduan lengkap: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

# Arsitektur

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

> Detail lengkap: [ARCHITECTURE.md](ARCHITECTURE.md)

---

# Keamanan & Privasi

| **Keamanan** | **Privasi** |
|---|---|
| Tidak butuh izin tambahan | Tanpa akun atau registrasi |
| Tidak membuka port jaringan | Tanpa analitik atau pelacakan |
| Tidak ada layanan latar belakang | Tanpa telemetri dalam bentuk apa pun |
| Build hanya berjalan atas perintah eksplisit pengguna | Local-first; jaringan dipakai untuk metadata dan unduhan |
| SHA256 wajib untuk setiap `.deb` (unduhan dan cache) | Sumber binary transparan dan dapat diaudit |

> Detail lengkap: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

# Pengembangan dan Pengujian

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
pip install -e ".[dev]"
```

| Perintah | Fungsinya |
|---|---|
| `make test` atau `pytest` | Menjalankan test suite |
| `make coverage` | Menjalankan test suite beserta laporan coverage |
| `make lint` | Pengecekan lint dan format Ruff |
| `make typecheck` | Pengecekan tipe Mypy |
| `make check` | Lint, pengecekan tipe, dan test sekaligus |

Dependensi dikunci di `uv.lock` (`uv sync --extra dev`). Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan lengkap.

---

# Kontribusi

Semua kontribusi diterima dengan senang hati!

| Cara Berkontribusi | Deskripsi |
|---|---|
| Tambah paket | Kirim paket tool baru |
| Laporkan bug | Buka issue di GitHub |
| Kirim PR | Perbaikan kode atau dokumentasi |
| Review PR | Bantu memvalidasi kontribusi orang lain |
| Audit keamanan | Tinjau keamanan skrip build |
| Perbaiki dokumentasi | Perjelas atau terjemahkan dokumentasi |

> Panduan lengkap: [CONTRIBUTING.md](CONTRIBUTING.md)

---

# Bantuan & Dokumentasi

| Dokumen | Deskripsi |
|---|---|
| [FAQ](FAQ.md) | Pertanyaan yang sering diajukan |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | Solusi untuk masalah umum |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | Cara mengunggah tool kamu |
| [CONTRIBUTING](CONTRIBUTING.md) | Panduan kontribusi |
| [SUPPORT](SUPPORT.md) | Cara mendapatkan dukungan |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | Catatan tentang distribusi binary |

---

# Filosofi

> *"Local first. Kendali di atas kenyamanan. Transparansi di atas sihir."*

Termux App Store dibuat untuk pengguna yang ingin:

- Memahami sepenuhnya apa yang berjalan di perangkat mereka
- Mengontrol build dan source secara langsung
- Menghindari vendor lock-in
- Berbagi tools secara terbuka dengan komunitas Termux

---

# Lisensi

Proyek ini dilisensikan di bawah **MIT License** — lihat [LICENSE](LICENSE) untuk detail.

---

# Maintainer

**Djunekz** — Developer independen dan maintainer Termux App Store

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

# Dukung Proyek Ini

Jika Termux App Store bermanfaat untukmu:

- **Beri bintang** repo ini — membantu orang lain menemukannya
- **Bagikan** di komunitas Termux & Android
- **Laporkan bug** lewat Issues
- **Kirim PR** untuk perbaikan apa pun
- **Sponsor**: https://saweria.co/redHh

---

# Riwayat Bintang

<a href="https://www.star-history.com/?repos=djunekz%2Ftermux-app-store&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
 </picture>
</a>

---

# Proyek Terkait & Kata Kunci

> Proyek ini dikembangkan secara independen dan **tidak berafiliasi dengan** proyek resmi [Termux](https://github.com/termux/termux-app).

**Kata kunci pencarian:** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — Dibuat untuk semua orang, oleh komunitas.**
