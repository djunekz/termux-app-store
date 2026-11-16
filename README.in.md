![[Termux App Store — TUI Package Manager for Termux](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)

# [Termux App Store — Termux के लिए TUI & CLI Package Manager](https://djunekz.github.io/termux-app-store/)

**Android पर Termux के लिए नेटिव रूप से बना लोकल-फ़र्स्ट TUI और CLI package manager, जिसमें चेकसम-वेरिफ़ाइड बाइनरी इंस्टॉल और सोर्स-बिल्ड फ़ॉलबैक है।**

> इन भाषाओं में पढ़ें: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)**

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

> **लोकल-फ़र्स्ट • चेकसम-वेरिफ़ाइड • सोर्स-आधारित • Termux-नेटिव • Android टर्मिनल**
> Termux पैकेज इंस्टॉल और मैनेज करें — प्री-बिल्ट बाइनरी या सोर्स बिल्ड — बिना root, बिना अकाउंट, बिना टेलीमेट्री।

---

# Termux App Store क्या है?

**Termux App Store** (`termux-app-store`) एक **TUI (Terminal User Interface)** और **CLI package manager** है जो Python ([Textual](https://github.com/Textualize/textual)) से बना है। यह Android पर Termux उपयोगकर्ताओं को सीधे डिवाइस पर **टूल/पैकेज ब्राउज़, इंस्टॉल और मैनेज** करने देता है — बिना अकाउंट, बिना टेलीमेट्री, बिना root। पैकेज मेटाडेटा और डाउनलोड के लिए नेटवर्क का उपयोग होता है।

**v0.4.0** से Termux App Store में **फ़ास्ट इंस्टॉल इंजन** है: पैकेज मिरर पूल (GitHub Pages, Cloudflare CDN, jsDelivr) से प्री-बिल्ट `.deb` बाइनरी के रूप में डाउनलोड होते हैं, और लोकल `.deb` कैश (TTL 7 दिन) इस्तेमाल होता है। कैश वाली फ़ाइलों सहित हर `.deb` का प्रति-आर्किटेक्चर SHA256 से मेल खाना ज़रूरी है, वरना वह अस्वीकार कर दी जाती है। SHA256 खराब या बेमेल फ़ाइलों का पता लगाता है; यह पब्लिशर का सिग्नेचर नहीं है। सोर्स बिल्ड `fix-install` से अब भी उपलब्ध हैं।

यह **Termux के लिए एक वैकल्पिक package manager** की तरह काम करता है, जिससे आप `build.sh` स्क्रिप्ट के ज़रिए कम्युनिटी टूल इंस्टॉल कर सकते हैं — भावना में AUR (Arch User Repository) जैसा, लेकिन Android पर Termux के लिए ख़ास तौर पर डिज़ाइन किया गया।

> **यह `termux-packages` या TUR (Termux User Repository) से कैसे अलग है?**
>
> - `termux-packages` Termux का आधिकारिक रेपो है — कोर टीम द्वारा मेंटेन किया जाता है, PR की मंज़ूरी चाहिए, और केवल व्यापक रूप से इस्तेमाल होने वाले टूल स्वीकार किए जाते हैं।
> - TUR एक क्यूरेटेड एक्सटेंशन है, जिसमें अब भी कंट्रीब्यूटर रिव्यू ज़रूरी है।
> - **Termux App Store** पूरी तरह कम्युनिटी-संचालित है: कोई भी `build.sh` सबमिट कर सकता है, पैकेज प्री-बिल्ट `.deb` या सोर्स बिल्ड के रूप में वितरित होते हैं, और कोई केंद्रीय अनुमोदन गेट नहीं है। इसे Termux के ऊपर एक निजी + कम्युनिटी पैकेज लेयर समझें।

> [!IMPORTANT]
> Termux App Store **कोई छिपा हुआ ऑटो-इंस्टॉलर नहीं है**।
> सभी इंस्टॉल — बाइनरी हों या सोर्स — **लोकल, पारदर्शी और उपयोगकर्ता के पूर्ण नियंत्रण में** चलते हैं।

---

# यह किसके लिए है?

| उपयोगकर्ता | उपयोग का मामला |
|---|---|
| Termux उपयोगकर्ता | तेज़ बाइनरी इंस्टॉल या सोर्स बिल्ड पर पूरा नियंत्रण |
| डेवलपर | प्री-बिल्ट `.deb` या सोर्स पैकेजिंग से टूल वितरित करना |
| रिव्यूअर और ऑडिटर | बिल्ड स्क्रिप्ट की समीक्षा और सत्यापन |
| मेंटेनर | एक साथ कई Termux पैकेज मैनेज करना |

---

<div align="center">
<img src="https://github.com/user-attachments/assets/b03419bc-8efe-4ed0-9b61-fea5153e9f53" width="100%" alt="Termux App Store — Main View"/>

<br/><br/>
<H1>TUI इंटरफ़ेस</H1>

| TUI मुख्य इंटरफ़ेस | TUI इंस्टॉल इंटरफ़ेस | मेनू पैलेट |
|:---:|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/fb9395f1-f943-44c5-b88f-be18e480fd26" width="400" alt="TUI Main Interface"/> | <img src="https://github.com/user-attachments/assets/a0ee7a15-95d2-4743-9f7e-90cd9e3388f7" width="400" alt="TUI Install Interface"/> | <img src="https://github.com/user-attachments/assets/ad760153-983f-4113-a465-2b682cb26b67" width="400" alt="Menu Palette Interface"/> |
| TUI मुख्य मेनू | पैकेज इंस्टॉल प्रक्रिया | कमांड पैलेट |

> TUI उपयोगकर्ता-अनुकूल है और पूर्ण **टचस्क्रीन** सपोर्ट के साथ आता है

---

<H1>CLI इंटरफ़ेस और अन्य टूल्स का सपोर्ट</H1>

| अन्य टूल्स सपोर्ट वाला CLI व्यू | Guidebook |
|:---:| :---: |
| https://github.com/user-attachments/assets/71c097b2-01a8-4c1c-9ffd-c26f29ee6ae6 | https://github.com/user-attachments/assets/b668a890-835f-4467-820a-988b1810c902 |


CLI इंटरफ़ेस और टूल्स सपोर्ट: `tasctl`, `termux-build`, `doctor.py`, `pkg-scaffold.py`, `build-package.sh`, `guidebook.py`

---

<H1>स्क्रीन रिकॉर्डिंग</H1>

| `termux-app-store` TUI, CLI और अन्य टूल `tasctl`, `termux-build`, `guidebook.py` की रिकॉर्डिंग |
|:---:|
| <img src="https://github.com/user-attachments/assets/152c757f-d2a3-4f31-8174-2b857a3aad51" width="100%" alt="termux-app-store"/> | termux-app-store

</div>

---

# त्वरित इंस्टॉल और अनइंस्टॉल

> **[PyPI](https://pypi.org/project/termux-app-store/)** पर उपलब्ध — खोजने योग्य और इंडेक्स्ड, आसानी से मिल जाता है।

### विकल्प 1 (अनुशंसित)

```bash
pkg install python
pip install termux-app-store
```

### विकल्प 2 (मैन्युअल)

> आसान तरीका (मेमोरी सीमित हो तो अनुशंसित)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> git clone के साथ (पूरा रिपॉज़िटरी डाउनलोड होता है)

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

इंस्टॉल के बाद चलाएँ:

```bash
termux-app-store        # Open interactive TUI
termux-app-store -h     # Show CLI help
tas                     # Shorthand for termux-app-store
```

### अनइंस्टॉल

```bash
pip uninstall termux-app-store
# or
./tasctl uninstall
```

---

# उपयोग

### TUI — इंटरेक्टिव इंटरफ़ेस

```bash
termux-app-store
# or shorthand:
tas
```

| कुंजी / बटन | क्या करता है |
|---|---|
| **Install / Update / Open** (`Ctrl+I`) | मुख्य बटन पैकेज की स्थिति के अनुसार बदलता है: इंस्टॉल न होने पर Install, नया वर्शन होने पर Update, इंस्टॉल और अप-टू-डेट होने पर Open। Open टूल चलाता है (कमांड चुनें, आर्गुमेंट जोड़ें) और Enter दबाने के बाद TUI में लौट आता है |
| **Shortcut** (Open डायलॉग) | `~/.shortcuts` में एक Termux:Widget स्क्रिप्ट बनाता है जो आपके आर्गुमेंट के साथ टूल चलाती है |
| **Upgrade all** (अपडेट बैनर) | बैनर दिखाता है कि कितने इंस्टॉल्ड पैकेजों का नया वर्शन उपलब्ध है और उन सभी को कतार में डाल देता है |
| **Cancel** (`Ctrl+X`) | चल रहे डाउनलोड या सोर्स बिल्ड को अगले सुरक्षित बिंदु पर रोक देता है |
| `F4` | गतिविधि इतिहास: इंस्टॉल, अपडेट, हटाना और लॉन्च |
| `F5` | समस्या रिपोर्ट करें: पहले से भरा हुआ बग रिपोर्ट फ़ॉर्म खोलता है |
| `Ctrl+R` / `Ctrl+Q` | पैकेज रीफ़्रेश करें / बाहर निकलें |
| `Ctrl+P` | कमांड पैलेट, जिसमें नोटिफ़िकेशन चालू/बंद करना भी शामिल है (Termux:API चाहिए) |

### CLI — सीधे कमांड

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

# विशेषताएँ

| **Package Browser (TUI)** कीबोर्ड और टचस्क्रीन नेविगेशन के साथ `packages/` फ़ोल्डर के पैकेज इंटरैक्टिव रूप से ब्राउज़ करें।<br>**Fast Install Engine** मिरर पूल — GitHub Pages, Cloudflare CDN, jsDelivr — से प्री-बिल्ट `.deb` डाउनलोड करता है, ऑटोमैटिक फ़ॉलबैक के साथ।<br>**Binary Cache** 7 दिन के TTL वाला लोकल `.deb` कैश; कैश की फ़ाइलें हर इंस्टॉल से पहले प्रति-आर्किटेक्चर SHA256 से दोबारा जाँची जाती हैं। कैश किए गए पैकेज तुरंत इंस्टॉल होते हैं।<br>**Smart Build Validator** असमर्थित Termux डिपेंडेंसी का पता लगाता है और अपने-आप स्टेटस बैज दिखाता है। | **रियल-टाइम सर्च और फ़िल्टर** नाम या विवरण से पैकेज खोजें — `search`/`find` CLI कमांड भी शामिल हैं।<br>**मल्टी-पैकेज इंस्टॉल/अनइंस्टॉल** एक ही कमांड से कई पैकेज इंस्टॉल या हटाएँ, सारांश आउटपुट के साथ।<br>**वन-क्लिक मैनेजमेंट** `./tasctl` से Termux App Store को ख़ुद इंस्टॉल / अपडेट / अनइंस्टॉल करें।<br>**प्राइवेसी-फ़र्स्ट** कोई अकाउंट नहीं, कोई ट्रैकिंग नहीं, कोई टेलीमेट्री नहीं। डेटा पहले से मौजूद हो तो लोकल डेटा से काम करता है; मेटाडेटा और पैकेज लाने के लिए नेटवर्क चाहिए। |
|---|---|

---

# फ़ास्ट इंस्टॉल कैसे काम करता है (v0.4.0+)

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

> अगर फ़ास्ट इंस्टॉल विफल हो, तो `build-package.sh` से पूरा सोर्स बिल्ड ज़बरदस्ती चलाने के लिए `fix-install <package>` का उपयोग करें।

---

# पैकेज जोड़ना

Termux App Store का हर पैकेज एक अकेली `build.sh` फ़ाइल से परिभाषित होता है — Arch Linux के PKGBUILD जैसा, लेकिन Android पर Termux के लिए अनुकूलित।

हर पैकेज में `build.sh` फ़ाइल **होनी ही चाहिए**:

```
packages/<tool-name>/build.sh
```

### न्यूनतम `build.sh` टेम्पलेट

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
> पूरा टेम्पलेट `template/build.sh` में देखें या चलाएँ: `./termux-build template`

### termux-build से पैकेज जोड़ना

```bash
cd termux-app-store
./termux-build create your-tool-name
# or auto-create from a GitHub URL:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> नाम रखते समय स्पेस का उपयोग न करें — `-` का उपयोग करें। उदाहरण: `my-tool-name`

---

# termux-build — बिल्ड और वैलिडेशन टूल

`termux-build` एक वैलिडेशन और रिव्यूअर सहायक टूल है — ऑटो-अपलोड या ऑटो-पब्लिश टूल नहीं।

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
> `termux-build` **केवल पढ़ता और वैलिडेट करता है** — यह फ़ाइलें नहीं बदलता और GitHub पर अपलोड नहीं करता।

---

# tasctl — Termux App Store कंट्रोलर

`tasctl` termux-app-store सिस्टम का कंट्रोलर है।

```bash
./tasctl install       # Install Termux App Store (latest)
./tasctl update        # Update to latest version
./tasctl uninstall     # Remove Termux App Store
./tasctl doctor        # Diagnose environment
./tasctl self-update   # Update tasctl itself
./tasctl help          # Show help
```

---

# guidebook — Termux App Store की पूरी जानकारी

```bash
python guidebook.py
```

> [!NOTE]
> guidebook फ़िलहाल दो भाषाओं को सपोर्ट करता है: अंग्रेज़ी और इंडोनेशियाई।

---

# अपना पैकेज Termux कम्युनिटी तक कैसे पहुँचाएँ

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

> पूरी गाइड: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

# आर्किटेक्चर

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

> पूरा विवरण: [ARCHITECTURE.md](ARCHITECTURE.md)

---

# सुरक्षा और गोपनीयता

| **सुरक्षा** | **गोपनीयता** |
|---|---|
| किसी अतिरिक्त अनुमति की ज़रूरत नहीं | अकाउंट या रजिस्ट्रेशन नहीं |
| कोई नेटवर्क पोर्ट नहीं खुलता | कोई एनालिटिक्स या ट्रैकिंग नहीं |
| कोई बैकग्राउंड सर्विस नहीं चलती | किसी भी तरह की टेलीमेट्री नहीं |
| बिल्ड केवल उपयोगकर्ता के स्पष्ट आदेश पर चलते हैं | लोकल-फ़र्स्ट; नेटवर्क मेटाडेटा और डाउनलोड के लिए इस्तेमाल होता है |
| हर `.deb` (डाउनलोड और कैश) के लिए SHA256 अनिवार्य | बाइनरी का स्रोत पारदर्शी और ऑडिट योग्य है |

> पूरा विवरण: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

# डेवलपमेंट और टेस्टिंग

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
pip install -e ".[dev]"
```

| कमांड | क्या करता है |
|---|---|
| `make test` या `pytest` | टेस्ट सूट चलाएँ |
| `make coverage` | कवरेज रिपोर्ट के साथ टेस्ट सूट चलाएँ |
| `make lint` | Ruff लिंट और फ़ॉर्मैट जाँच |
| `make typecheck` | Mypy टाइप जाँच |
| `make check` | लिंट, टाइप जाँच और टेस्ट एक साथ |

डिपेंडेंसी `uv.lock` में पिन की गई हैं (`uv sync --extra dev`)। पूरी गाइड के लिए [CONTRIBUTING.md](CONTRIBUTING.md) देखें।

---

# योगदान

सभी योगदानों का स्वागत है!

| योगदान का तरीका | विवरण |
|---|---|
| पैकेज जोड़ें | नया टूल पैकेज सबमिट करें |
| बग रिपोर्ट करें | GitHub पर issue खोलें |
| PR भेजें | कोड या दस्तावेज़ीकरण में सुधार |
| PR रिव्यू करें | दूसरों के योगदान को वैलिडेट करने में मदद करें |
| सुरक्षा ऑडिट | बिल्ड स्क्रिप्ट की सुरक्षा की समीक्षा करें |
| दस्तावेज़ सुधारें | दस्तावेज़ों को स्पष्ट करें या अनुवाद करें |

> पूरी गाइड: [CONTRIBUTING.md](CONTRIBUTING.md)

---

# सहायता और दस्तावेज़ीकरण

| दस्तावेज़ | विवरण |
|---|---|
| [FAQ](FAQ.md) | अक्सर पूछे जाने वाले प्रश्न |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | आम समस्याओं के समाधान |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | अपना टूल कैसे अपलोड करें |
| [CONTRIBUTING](CONTRIBUTING.md) | योगदान गाइड |
| [SUPPORT](SUPPORT.md) | सहायता कैसे पाएँ |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | बाइनरी वितरण पर नोट्स |

---

# दर्शन

> *"लोकल फ़र्स्ट। सुविधा से ऊपर नियंत्रण। जादू से ऊपर पारदर्शिता।"*

Termux App Store उन उपयोगकर्ताओं के लिए बनाया गया है जो:

- पूरी तरह समझना चाहते हैं कि उनके डिवाइस पर क्या चल रहा है
- बिल्ड और सोर्स को सीधे नियंत्रित करना चाहते हैं
- वेंडर लॉक-इन से बचना चाहते हैं
- टूल्स को Termux कम्युनिटी के साथ खुले रूप से साझा करना चाहते हैं

---

# लाइसेंस

यह प्रोजेक्ट **MIT License** के तहत लाइसेंस प्राप्त है — विवरण के लिए [LICENSE](LICENSE) देखें।

---

# अनुरक्षक

**Djunekz** — Termux App Store के स्वतंत्र डेवलपर और अनुरक्षक

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

# इस प्रोजेक्ट का समर्थन करें

अगर Termux App Store आपके काम आया है:

- इस रेपो को **Star** करें — दूसरों को इसे खोजने में मदद मिलती है
- Termux और Android कम्युनिटी में इसे **शेयर** करें
- Issues के ज़रिए **बग रिपोर्ट** करें
- किसी भी सुधार के लिए **PR भेजें**
- **स्पॉन्सर**: https://saweria.co/redHh

---

# स्टार इतिहास

<a href="https://www.star-history.com/?repos=djunekz%2Ftermux-app-store&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
 </picture>
</a>

---

# संबंधित प्रोजेक्ट और कीवर्ड

> यह प्रोजेक्ट स्वतंत्र रूप से विकसित किया गया है और आधिकारिक [Termux](https://github.com/termux/termux-app) प्रोजेक्ट से **संबद्ध नहीं** है।

**खोज शब्द:** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — सबके लिए, कम्युनिटी द्वारा बनाया गया।**
