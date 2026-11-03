![[Termux App Store — TUI Package Manager](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — TUI & CLI Package Manager สำหรับ Termux](https://djunekz.github.io/termux-app-store/)

**Package manager แบบ TUI และ CLI ที่เน้นการทำงานในเครื่อง สร้างมาเพื่อ Termux บน Android โดยเฉพาะ ติดตั้งไบนารีพร้อมตรวจสอบ checksum และมี fallback สร้างจาก source**

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


> **เน้นในเครื่อง • ตรวจสอบ checksum • ใช้ Source Code • Native บน Termux • Android Terminal**
> ติดตั้งและจัดการแพ็กเกจ Termux ได้โดยไม่ต้อง root ไม่ต้องมีบัญชี ไม่มีการติดตาม

> อ่านภาษาอื่น: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

---

## Termux App Store คืออะไร?

**Termux App Store** คือ **package manager แบบ TUI & CLI** ที่สร้างด้วย Python ([Textual](https://github.com/Textualize/textual)) ช่วยให้ผู้ใช้ Termux บน Android สามารถ**เรียกดู ติดตั้ง และจัดการเครื่องมือ/แพ็กเกจ**ได้โดยตรงบนอุปกรณ์ — ไม่ต้องมีบัญชี ไม่มีการติดตาม ไม่ต้อง root การดึงข้อมูลแพ็กเกจและการดาวน์โหลดใช้เครือข่าย

ตั้งแต่ **v0.4.0** เพิ่ม **Fast Install Engine**: ดาวน์โหลด `.deb` ไบนารีที่สร้างไว้ล่วงหน้าจากกลุ่มมิเรอร์ (GitHub Pages, Cloudflare CDN, jsDelivr) พร้อมแคช `.deb` ในเครื่อง (TTL 7 วัน) ไฟล์ `.deb` ทุกไฟล์ รวมถึงที่อยู่ในแคช ต้องตรงกับ SHA256 ตามสถาปัตยกรรม มิฉะนั้นจะถูกปฏิเสธ SHA256 ใช้ตรวจจับไฟล์เสียหรือไม่ตรงกัน ไม่ใช่ลายเซ็นของผู้เผยแพร่ หากต้องการควบคุมเต็มที่ยังสามารถใช้ `fix-install` เพื่อบิลด์จาก source code ได้

> [!IMPORTANT]
> Termux App Store **ไม่ใช่ตัวติดตั้งอัตโนมัติที่ซ่อนอยู่**
> การติดตั้งทั้งหมด — ไบนารีหรือ source — ทำงาน**ในเครื่อง โปร่งใส และภายใต้การควบคุมของผู้ใช้เสมอ**

---

## ภาพหน้าจอ

| TUI หลัก | TUI ติดตั้ง | Command Palette |
|---|---|---|
| [![TUI Main](.assets/0main.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/0main.jpg) | [![TUI Install](.assets/1install.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/1install.jpg) | [![Menu Palette](.assets/2pallete.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/2pallete.jpg) |

---

## ติดตั้งและถอนการติดตั้ง

### ตัวเลือก 1 (แนะนำ)

```bash
pkg install python
pip install termux-app-store
```

### ตัวเลือก 2 (ด้วยตนเอง)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

หลังติดตั้งแล้วรัน:

```bash
termux-app-store    # เปิด TUI แบบ interactive
tas                 # คำสั่งย่อ
termux-app-store -h # แสดง CLI help
```

### ถอนการติดตั้ง

```bash
pip uninstall termux-app-store
```

---

## วิธีใช้งาน

### TUI — อินเทอร์เฟซแบบ Interactive

```bash
termux-app-store
# หรือใช้คำสั่งย่อ:
tas
```

### CLI — คำสั่งโดยตรง

```bash
termux-app-store list                     # แสดงแพ็กเกจทั้งหมด
termux-app-store show <แพ็กเกจ>           # ดูรายละเอียดแพ็กเกจ
termux-app-store install <แพ็กเกจ>        # ติดตั้งเร็ว (ไฟล์ .deb สร้างไว้แล้ว)
termux-app-store install pkg1 pkg2 pkg3   # ติดตั้งหลายแพ็กเกจพร้อมกัน
termux-app-store fix-install <แพ็กเกจ>    # บังคับบิลด์จาก source
termux-app-store search <คำค้น>           # ค้นหาแพ็กเกจ
termux-app-store update                   # ตรวจสอบการอัปเดต
termux-app-store upgrade                  # อัปเกรดแพ็กเกจทั้งหมด
termux-app-store mirrors                  # ตรวจสอบสถานะมิเรอร์
termux-app-store cache info               # ดูข้อมูลแคช
termux-app-store cache clear              # ล้างแคช
termux-app-store version                  # ตรวจสอบเวอร์ชันล่าสุด
termux-app-store help                     # ความช่วยเหลือเต็ม
```

---

## วิธีทำงานของ Fast Install (v0.4.0+)

ตั้งแต่ v0.4.0 การติดตั้งจะดาวน์โหลด `.deb` ไบนารีที่สร้างไว้ล่วงหน้าโดยอัตโนมัติ:

1. ตรวจสอบแคช `.deb` ในเครื่อง (TTL 7 วัน)
2. หากไม่มีแคช ลองมิเรอร์ตามลำดับ: GitHub Pages → Cloudflare CDN → jsDelivr CDN → raw GitHub
3. ยืนยัน SHA256 ตามสถาปัตยกรรม (`sha256_by_arch`)
4. แคชในเครื่องและติดตั้งด้วย `dpkg -i`

> หาก fast install ล้มเหลว ใช้ `fix-install <แพ็กเกจ>` เพื่อบิลด์จาก source ด้วย `build-package.sh`

---

## สถานะแบดจ์ของแพ็กเกจ

| แบดจ์ | คำอธิบาย |
|---|---|
| **NEW** | แพ็กเกจเพิ่งเพิ่มใหม่ (ภายใน 7 วัน) |
| **UPDATE** | มีเวอร์ชันใหม่ |
| **INSTALLED** | ติดตั้งแล้วและเป็นเวอร์ชันล่าสุด |
| **UNSUPPORTED** | dependency ไม่รองรับใน Termux |

---

## การเพิ่มแพ็กเกจ

แต่ละแพ็กเกจกำหนดด้วยไฟล์ `build.sh` ไฟล์เดียว:

```
packages/<ชื่อเครื่องมือ>/build.sh
```

### เทมเพลต `build.sh` ขั้นต่ำ

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@ชื่อผู้ใช้ GitHub ของคุณ"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

```bash
cd termux-app-store
./termux-build create ชื่อเครื่องมือ
# หรือสร้างอัตโนมัติจาก GitHub URL:
./termux-build init https://github.com/user/repo
```

---

## เครื่องมือเสริม

### termux-build

```bash
./termux-build create <แพ็กเกจ>      # สร้างแพ็กเกจสำหรับเผยแพร่
./termux-build init <url>             # สร้างอัตโนมัติจาก GitHub URL
./termux-build lint <แพ็กเกจ>        # ตรวจสอบ build script
./termux-build doctor                 # วินิจฉัยสภาพแวดล้อม
./termux-build template               # สร้างเทมเพลต build.sh
```

### tasctl

```bash
./tasctl install       # ติดตั้ง Termux App Store
./tasctl update        # อัปเดตเป็นเวอร์ชันล่าสุด
./tasctl uninstall     # ลบ Termux App Store
./tasctl doctor        # วินิจฉัยสภาพแวดล้อม
./tasctl self-update   # อัปเดต tasctl เอง
```

---

## ความปลอดภัยและความเป็นส่วนตัว

- ไม่ต้องการสิทธิ์เพิ่มเติม ไม่มีบริการทำงานเบื้องหลัง
- ไม่ต้องมีบัญชี ไม่มีการลงทะเบียน
- ไม่มีการวิเคราะห์ ติดตาม หรือส่งข้อมูลเลย
- บังคับ SHA256 สำหรับ `.deb` ทุกไฟล์ (ดาวน์โหลดและแคช)
- ออกแบบให้เน้นการทำงานในเครื่อง (ใช้เครือข่ายสำหรับเมตาดาต้าและการดาวน์โหลด)

> รายละเอียด: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

## ลิขสิทธิ์

**MIT License** — ดูรายละเอียดที่ [LICENSE](LICENSE)

---

## ผู้ดูแล

**Djunekz** — นักพัฒนาอิสระ

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

**© Termux App Store — สร้างเพื่อทุกคน โดยชุมชน**
