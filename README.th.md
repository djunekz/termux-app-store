![[Termux App Store — TUI Package Manager](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — TUI & CLI Package Manager สำหรับ Termux](https://djunekz.github.io/termux-app-store/)

**Package manager แบบ TUI และ CLI ที่เน้นการทำงานในเครื่อง สร้างมาเพื่อ Termux บน Android โดยเฉพาะ ติดตั้งไบนารีพร้อมตรวจสอบ checksum และมี fallback สร้างจาก source**

[![CI](https://github.com/djunekz/termux-app-store/actions/workflows/build.yml/badge.svg)](https://github.com/djunekz/termux-app-store/actions)
[![PyPI](https://img.shields.io/pypi/v/termux-app-store?style=flat&logo=pypi&color=3fb950&label=pypi)](https://pypi.org/project/termux-app-store/)
[![License](https://img.shields.io/badge/License-MIT-3fb950?style=flat)](LICENSE)
[![Stars](https://img.shields.io/github/stars/djunekz/termux-app-store?style=flat&logo=github&color=white&label=stars)](https://github.com/djunekz/termux-app-store/stargazers)

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
