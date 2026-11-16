![[Termux App Store — TUI Package Manager for Termux](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)

# [Termux App Store — TUI & CLI Package Manager สำหรับ Termux](https://djunekz.github.io/termux-app-store/)

**package manager แบบ TUI และ CLI ที่เน้นในเครื่อง สร้างมาเพื่อ Termux บน Android โดยเฉพาะ พร้อมการติดตั้งไบนารีที่ตรวจสอบ checksum และ build จากซอร์สสำรอง**

> อ่านใน: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

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
> ติดตั้งและจัดการแพ็กเกจ Termux — ไบนารีสำเร็จรูปหรือ build จากซอร์ส — ไม่ต้อง root ไม่ต้องมีบัญชี ไม่มี telemetry

---

# Termux App Store คืออะไร?

**Termux App Store** (`termux-app-store`) คือ **TUI (Terminal User Interface)** และ **CLI package manager** ที่สร้างด้วย Python ([Textual](https://github.com/Textualize/textual)) ช่วยให้ผู้ใช้ Termux บน Android **เรียกดู ติดตั้ง และจัดการเครื่องมือ/แพ็กเกจ** ได้โดยตรงบนอุปกรณ์ — ไม่ต้องมีบัญชี ไม่มี telemetry ไม่ต้อง root โดยข้อมูลเมตาของแพ็กเกจและการดาวน์โหลดจะใช้เครือข่าย

ตั้งแต่ **v0.4.0** เป็นต้นไป Termux App Store รองรับ **fast install engine**: แพ็กเกจจะถูกดาวน์โหลดเป็นไบนารี `.deb` สำเร็จรูปจาก mirror pool (GitHub Pages, Cloudflare CDN, jsDelivr) พร้อมแคช `.deb` ในเครื่อง (TTL 7 วัน) ทุกไฟล์ `.deb` รวมถึงที่อยู่ในแคช ต้องตรงกับ SHA256 ของแต่ละสถาปัตยกรรม มิฉะนั้นจะถูกปฏิเสธ SHA256 ใช้ตรวจจับไฟล์เสียหายหรือไม่ตรงกัน แต่ไม่ใช่ลายเซ็นของผู้เผยแพร่ ยังคง build จากซอร์สได้ผ่าน `fix-install`

ใช้งานเป็น **package manager ทางเลือกสำหรับ Termux** ให้คุณติดตั้งเครื่องมือจากชุมชนด้วยสคริปต์ `build.sh` — มีแนวคิดคล้าย AUR (Arch User Repository) แต่ออกแบบมาเพื่อ Termux บน Android โดยเฉพาะ

> **ต่างจาก `termux-packages` หรือ TUR (Termux User Repository) อย่างไร?**
>
> - `termux-packages` คือ repo ทางการของ Termux — ดูแลโดยทีมหลัก ต้องได้รับการอนุมัติ PR และรับเฉพาะเครื่องมือที่ใช้กันอย่างแพร่หลาย
> - TUR คือส่วนขยายที่คัดสรรแล้ว ยังต้องผ่านการรีวิวจากผู้ร่วมพัฒนา
> - **Termux App Store** ขับเคลื่อนโดยชุมชนเต็มรูปแบบ: ใครก็ส่ง `build.sh` ได้ แพ็กเกจแจกจ่ายเป็น `.deb` สำเร็จรูปหรือ build จากซอร์ส และไม่มีขั้นตอนอนุมัติจากส่วนกลาง ลองมองว่าเป็นชั้นแพ็กเกจส่วนตัว + ชุมชนที่ซ้อนบน Termux

> [!IMPORTANT]
> Termux App Store **ไม่ใช่ตัวติดตั้งอัตโนมัติที่ซ่อนอยู่**
> การติดตั้งทั้งหมด — ไบนารีหรือซอร์ส — ทำงาน **ในเครื่อง โปร่งใส และอยู่ภายใต้การควบคุมของผู้ใช้อย่างเต็มที่**

---

# เหมาะกับใคร?

| ผู้ใช้ | กรณีใช้งาน |
|---|---|
| ผู้ใช้ Termux | ติดตั้งไบนารีได้เร็ว หรือควบคุมการ build จากซอร์สได้เต็มที่ |
| นักพัฒนา | แจกจ่ายเครื่องมือผ่าน `.deb` สำเร็จรูปหรือแพ็กเกจซอร์ส |
| ผู้รีวิวและผู้ตรวจสอบ | ตรวจและยืนยันสคริปต์ build |
| ผู้ดูแล | จัดการแพ็กเกจ Termux หลายตัวพร้อมกัน |

---

<div align="center">
<img src="https://github.com/user-attachments/assets/b03419bc-8efe-4ed0-9b61-fea5153e9f53" width="100%" alt="Termux App Store — Main View"/>

<br/><br/>
<H1>อินเทอร์เฟซ TUI</H1>

| หน้าหลัก TUI | หน้าติดตั้ง TUI | เมนู Palette |
|:---:|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/fb9395f1-f943-44c5-b88f-be18e480fd26" width="400" alt="TUI Main Interface"/> | <img src="https://github.com/user-attachments/assets/a0ee7a15-95d2-4743-9f7e-90cd9e3388f7" width="400" alt="TUI Install Interface"/> | <img src="https://github.com/user-attachments/assets/ad760153-983f-4113-a465-2b682cb26b67" width="400" alt="Menu Palette Interface"/> |
| เมนูหลักของ TUI | ขั้นตอนการติดตั้งแพ็กเกจ | Command palette |

> TUI ใช้งานง่าย รองรับ **หน้าจอสัมผัส** เต็มรูปแบบ

---

<H1>อินเทอร์เฟซ CLI และเครื่องมืออื่นที่รองรับ</H1>

| มุมมอง CLI และเครื่องมืออื่นที่รองรับ | Guidebook |
|:---:| :---: |
| https://github.com/user-attachments/assets/71c097b2-01a8-4c1c-9ffd-c26f29ee6ae6 | https://github.com/user-attachments/assets/b668a890-835f-4467-820a-988b1810c902 |


อินเทอร์เฟซ CLI และเครื่องมือที่รองรับ: `tasctl`, `termux-build`, `doctor.py`, `pkg-scaffold.py`, `build-package.sh`, `guidebook.py`

---

<H1>บันทึกหน้าจอ</H1>

| บันทึก `termux-app-store` TUI, CLI และเครื่องมืออื่น `tasctl`, `termux-build`, `guidebook.py` |
|:---:|
| <img src="https://github.com/user-attachments/assets/152c757f-d2a3-4f31-8174-2b857a3aad51" width="100%" alt="termux-app-store"/> | termux-app-store

</div>

---

# ติดตั้งและถอนการติดตั้งอย่างรวดเร็ว

> มีให้ใช้งานบน **[PyPI](https://pypi.org/project/termux-app-store/)** — ค้นหาและหาเจอได้ง่าย

### ตัวเลือก 1 (แนะนำ)

```bash
pkg install python
pip install termux-app-store
```

### ตัวเลือก 2 (ด้วยตนเอง)

> แบบง่าย (แนะนำหากหน่วยความจำจำกัด)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> ด้วย git clone (ดาวน์โหลดทั้งรีโพซิทอรี)

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

หลังติดตั้ง ให้รัน:

```bash
termux-app-store        # Open interactive TUI
termux-app-store -h     # Show CLI help
tas                     # Shorthand for termux-app-store
```

### ถอนการติดตั้ง

```bash
pip uninstall termux-app-store
# or
./tasctl uninstall
```

---

# วิธีใช้งาน

### TUI — อินเทอร์เฟซแบบ Interactive

```bash
termux-app-store
# or shorthand:
tas
```

| ปุ่ม / คีย์ | ทำอะไร |
|---|---|
| **Install / Update / Open** (`Ctrl+I`) | ปุ่มหลักเปลี่ยนตามสถานะแพ็กเกจ: Install เมื่อยังไม่ได้ติดตั้ง, Update เมื่อมีเวอร์ชันใหม่กว่า, Open เมื่อติดตั้งแล้วและเป็นเวอร์ชันล่าสุด Open จะรันเครื่องมือ (เลือกคำสั่ง ใส่อาร์กิวเมนต์) แล้วกลับสู่ TUI หลังกด Enter |
| **Shortcut** (กล่องโต้ตอบ Open) | สร้างสคริปต์ Termux:Widget ใน `~/.shortcuts` ที่รันเครื่องมือพร้อมอาร์กิวเมนต์ของคุณ |
| **Upgrade all** (แบนเนอร์อัปเดต) | แบนเนอร์แสดงจำนวนแพ็กเกจที่ติดตั้งไว้และมีเวอร์ชันใหม่กว่า พร้อมเข้าคิวอัปเกรดทั้งหมด |
| **Cancel** (`Ctrl+X`) | หยุดการดาวน์โหลดหรือการ build จากซอร์สที่กำลังทำงาน ณ จุดที่ปลอดภัยถัดไป |
| `F4` | ประวัติกิจกรรม: การติดตั้ง อัปเดต ลบ และเปิดใช้งาน |
| `F5` | รายงานปัญหา: เปิดแบบฟอร์มรายงานบั๊กที่กรอกข้อมูลไว้แล้ว |
| `Ctrl+R` / `Ctrl+Q` | รีเฟรชแพ็กเกจ / ออก |
| `Ctrl+P` | Command palette รวมถึงเปิด/ปิดการแจ้งเตือน (ต้องใช้ Termux:API) |

### CLI — คำสั่งโดยตรง

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

# คุณสมบัติ

| **Package Browser (TUI)** เรียกดูแพ็กเกจจากโฟลเดอร์ `packages/` แบบโต้ตอบ ด้วยคีย์บอร์ดและหน้าจอสัมผัส<br>**Fast Install Engine** ดาวน์โหลด `.deb` สำเร็จรูปจาก mirror pool — GitHub Pages, Cloudflare CDN, jsDelivr — พร้อมสำรองอัตโนมัติ<br>**Binary Cache** แคช `.deb` ในเครื่อง TTL 7 วัน ไฟล์ในแคชจะถูกตรวจ SHA256 ของแต่ละสถาปัตยกรรมซ้ำก่อนติดตั้งทุกครั้ง แพ็กเกจที่แคชไว้ติดตั้งได้ทันที<br>**Smart Build Validator** ตรวจจับ dependency ของ Termux ที่ไม่รองรับ พร้อมแบดจ์สถานะอัตโนมัติ | **ค้นหาและกรองแบบเรียลไทม์** ค้นหาแพ็กเกจตามชื่อหรือคำอธิบาย — มีคำสั่ง CLI `search`/`find` ด้วย<br>**ติดตั้ง/ถอนหลายแพ็กเกจ** ติดตั้งหรือลบหลายแพ็กเกจในคำสั่งเดียว พร้อมสรุปผล<br>**จัดการในคลิกเดียว** ติดตั้ง / อัปเดต / ถอน Termux App Store เองผ่าน `./tasctl`<br>**ความเป็นส่วนตัวมาก่อน** ไม่ต้องมีบัญชี ไม่ติดตาม ไม่มี telemetry ใช้ข้อมูลในเครื่องได้เมื่อมีอยู่แล้ว การดึงข้อมูลเมตาและแพ็กเกจต้องใช้เครือข่าย |
|---|---|

---

# Fast Install ทำงานอย่างไร (v0.4.0+)

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

> หาก fast install ล้มเหลว ให้ใช้ `fix-install <package>` เพื่อบังคับ build จากซอร์สเต็มรูปแบบผ่าน `build-package.sh`

---

# การเพิ่มแพ็กเกจ

ทุกแพ็กเกจใน Termux App Store กำหนดด้วยไฟล์ `build.sh` เพียงไฟล์เดียว — คล้ายกับ PKGBUILD ใน Arch Linux แต่ปรับให้เหมาะกับ Termux บน Android

ทุกแพ็กเกจ **ต้อง** มีไฟล์ `build.sh`:

```
packages/<tool-name>/build.sh
```

### เทมเพลต `build.sh` ขั้นต่ำ

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
> ดูเทมเพลตฉบับเต็มได้ที่ `template/build.sh` หรือรัน: `./termux-build template`

### การเพิ่มแพ็กเกจด้วย termux-build

```bash
cd termux-app-store
./termux-build create your-tool-name
# or auto-create from a GitHub URL:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> ตอนตั้งชื่อ ห้ามเว้นวรรค — ให้ใช้ `-` เช่น `my-tool-name`

---

# termux-build — เครื่องมือ Build และตรวจสอบ

`termux-build` เป็นเครื่องมือช่วยตรวจสอบและรีวิว — ไม่ใช่เครื่องมืออัปโหลดหรือเผยแพร่อัตโนมัติ

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
> `termux-build` **อ่านและตรวจสอบเท่านั้น** — ไม่แก้ไขไฟล์และไม่อัปโหลดไป GitHub

---

# tasctl — ตัวควบคุม Termux App Store

`tasctl` คือตัวควบคุมของระบบ termux-app-store

```bash
./tasctl install       # Install Termux App Store (latest)
./tasctl update        # Update to latest version
./tasctl uninstall     # Remove Termux App Store
./tasctl doctor        # Diagnose environment
./tasctl self-update   # Update tasctl itself
./tasctl help          # Show help
```

---

# guidebook — ข้อมูลทั้งหมดเกี่ยวกับ Termux App Store

```bash
python guidebook.py
```

> [!NOTE]
> ปัจจุบัน guidebook รองรับสองภาษา: อังกฤษและภาษาอินโดนีเซีย

---

# วิธีแจกจ่ายแพ็กเกจของคุณให้ชุมชน Termux

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

> คู่มือฉบับเต็ม: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

# สถาปัตยกรรม

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

> รายละเอียดทั้งหมด: [ARCHITECTURE.md](ARCHITECTURE.md)

---

# ความปลอดภัยและความเป็นส่วนตัว

| **ความปลอดภัย** | **ความเป็นส่วนตัว** |
|---|---|
| ไม่ต้องขอสิทธิ์เพิ่มเติม | ไม่ต้องมีบัญชีหรือสมัครสมาชิก |
| ไม่เปิดพอร์ตเครือข่าย | ไม่มีการวิเคราะห์หรือติดตาม |
| ไม่มีบริการทำงานเบื้องหลัง | ไม่มี telemetry ใดๆ |
| Build ทำงานเมื่อผู้ใช้สั่งอย่างชัดเจนเท่านั้น | เน้นในเครื่อง; ใช้เครือข่ายสำหรับข้อมูลเมตาและการดาวน์โหลด |
| ต้องมี SHA256 สำหรับทุก `.deb` (ดาวน์โหลดและแคช) | แหล่งที่มาของไบนารีโปร่งใสและตรวจสอบได้ |

> รายละเอียดทั้งหมด: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

# การพัฒนาและการทดสอบ

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
pip install -e ".[dev]"
```

| คำสั่ง | ทำอะไร |
|---|---|
| `make test` หรือ `pytest` | รันชุดทดสอบ |
| `make coverage` | รันชุดทดสอบพร้อมรายงาน coverage |
| `make lint` | ตรวจ lint และรูปแบบด้วย Ruff |
| `make typecheck` | ตรวจชนิดข้อมูลด้วย Mypy |
| `make check` | lint ตรวจชนิดข้อมูล และทดสอบพร้อมกัน |

Dependency ถูกล็อกไว้ใน `uv.lock` (`uv sync --extra dev`) ดูคู่มือฉบับเต็มได้ที่ [CONTRIBUTING.md](CONTRIBUTING.md)

---

# การมีส่วนร่วม

ยินดีรับทุกการมีส่วนร่วม!

| วิธีมีส่วนร่วม | คำอธิบาย |
|---|---|
| เพิ่มแพ็กเกจ | ส่งแพ็กเกจเครื่องมือใหม่ |
| รายงานบั๊ก | เปิด issue บน GitHub |
| ส่ง PR | ปรับปรุงโค้ดหรือเอกสาร |
| รีวิว PR | ช่วยตรวจสอบงานของผู้อื่น |
| ตรวจสอบความปลอดภัย | ตรวจความปลอดภัยของสคริปต์ build |
| ปรับปรุงเอกสาร | ทำให้เอกสารชัดเจนขึ้นหรือช่วยแปล |

> คู่มือฉบับเต็ม: [CONTRIBUTING.md](CONTRIBUTING.md)

---

# ความช่วยเหลือและเอกสาร

| เอกสาร | คำอธิบาย |
|---|---|
| [FAQ](FAQ.md) | คำถามที่พบบ่อย |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | วิธีแก้ปัญหาที่พบบ่อย |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | วิธีอัปโหลดเครื่องมือของคุณ |
| [CONTRIBUTING](CONTRIBUTING.md) | คู่มือการมีส่วนร่วม |
| [SUPPORT](SUPPORT.md) | วิธีขอรับการสนับสนุน |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | หมายเหตุเกี่ยวกับการแจกจ่ายไบนารี |

---

# ปรัชญา

> *"Local first. การควบคุมมาก่อนความสะดวก. ความโปร่งใสมาก่อนเวทมนตร์"*

Termux App Store สร้างขึ้นสำหรับผู้ใช้ที่ต้องการ:

- เข้าใจอย่างถ่องแท้ว่าอะไรทำงานบนอุปกรณ์ของตน
- ควบคุมการ build และซอร์สได้โดยตรง
- หลีกเลี่ยงการผูกติดกับผู้ให้บริการรายเดียว
- แบ่งปันเครื่องมือกับชุมชน Termux อย่างเปิดเผย

---

# ลิขสิทธิ์

โปรเจกต์นี้ใช้สัญญาอนุญาต **MIT License** — ดูรายละเอียดที่ [LICENSE](LICENSE)

---

# ผู้ดูแล

**Djunekz** — นักพัฒนาอิสระและผู้ดูแล Termux App Store

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

# สนับสนุนโปรเจกต์นี้

หาก Termux App Store เป็นประโยชน์กับคุณ:

- **กดดาว** repo นี้ — ช่วยให้คนอื่นค้นพบ
- **แบ่งปัน** ในชุมชน Termux และ Android
- **รายงานบั๊ก** ผ่าน Issues
- **ส่ง PR** สำหรับการปรับปรุงใดๆ
- **สนับสนุน**: https://saweria.co/redHh

---

# ประวัติดาว

<a href="https://www.star-history.com/?repos=djunekz%2Ftermux-app-store&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
 </picture>
</a>

---

# โปรเจกต์ที่เกี่ยวข้องและคีย์เวิร์ด

> โปรเจกต์นี้พัฒนาอย่างอิสระและ **ไม่ได้เกี่ยวข้องกับ** โปรเจกต์ [Termux](https://github.com/termux/termux-app) อย่างเป็นทางการ

**คำค้นหา:** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — สร้างเพื่อทุกคน โดยชุมชน**
