![[Termux App Store — TUI Package Manager](.assets/00.jpeg)](https://github.com/djunekz/termux-app-store/raw/master/.assets/00.jpeg)

# [Termux App Store — Termux के लिए TUI & CLI Package Manager](https://djunekz.github.io/termux-app-store/)

**Android पर Termux के लिए बनाया गया लोकल-फ़र्स्ट TUI और CLI पैकेज मैनेजर, चेकसम-वेरिफ़ाइड बाइनरी इंस्टॉल और सोर्स-बिल्ड फ़ॉलबैक के साथ।**

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


> **लोकल-फ़र्स्ट • चेकसम-वेरिफ़ाइड • सोर्स-आधारित • Termux-नेटिव • Android Terminal**
> Termux पैकेज इंस्टॉल करें और प्रबंधित करें — बिना root, बिना account, बिना tracking के।

> अन्य भाषाओं में पढ़ें: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇯🇵 **[日本語](README.jp.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)**

---

## Termux App Store क्या है?

**Termux App Store** Python ([Textual](https://github.com/Textualize/textual)) से बना एक **TUI & CLI पैकेज मैनेजर** है जो Android पर Termux उपयोगकर्ताओं को सीधे डिवाइस पर **टूल्स/पैकेज ब्राउज़ करने, इंस्टॉल करने और प्रबंधित करने** की सुविधा देता है — बिना account, बिना telemetry, बिना root। पैकेज मेटाडेटा और डाउनलोड के लिए नेटवर्क का उपयोग होता है।

**v0.4.0** से **फ़ास्ट इंस्टॉल इंजन** जोड़ा गया है: मिरर पूल (GitHub Pages, Cloudflare CDN, jsDelivr) से पहले से बने `.deb` बाइनरी फ़ाइलें डाउनलोड होती हैं, लोकल `.deb` कैश (TTL 7 दिन) के साथ। कैश सहित हर `.deb` का आर्किटेक्चर-वाइज SHA256 से मेल खाना ज़रूरी है, वरना उसे अस्वीकार कर दिया जाता है। SHA256 फ़ाइल के खराब या बेमेल होने का पता लगाता है; यह प्रकाशक का हस्ताक्षर नहीं है। पूर्ण नियंत्रण के लिए `fix-install` से सोर्स बिल्ड भी उपलब्ध है।

> [!IMPORTANT]
> Termux App Store **कोई छिपा हुआ ऑटो-इंस्टॉलर नहीं है**।
> सभी इंस्टॉलेशन — बाइनरी या सोर्स — **लोकल, पारदर्शी और पूरी तरह उपयोगकर्ता के नियंत्रण में** चलते हैं।

---

## स्क्रीनशॉट

| TUI मुख्य | TUI इंस्टॉल | Command Palette |
|---|---|---|
| [![TUI Main](.assets/0main.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/0main.jpg) | [![TUI Install](.assets/1install.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/1install.jpg) | [![Menu Palette](.assets/2pallete.jpg)](https://github.com/djunekz/termux-app-store/blob/master/.assets/2pallete.jpg) |

---

## इंस्टॉल और अनइंस्टॉल

### विकल्प 1 (अनुशंसित)

```bash
pkg install python
pip install termux-app-store
```

### विकल्प 2 (मैन्युअल)

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

इंस्टॉल के बाद चलाएं:

```bash
termux-app-store    # इंटरेक्टिव TUI खोलें
tas                 # शॉर्टहैंड कमांड
termux-app-store -h # CLI सहायता दिखाएं
```

### अनइंस्टॉल

```bash
pip uninstall termux-app-store
```

---

## उपयोग

### TUI — इंटरेक्टिव इंटरफ़ेस

```bash
termux-app-store
# या शॉर्टहैंड:
tas
```

### CLI — सीधे कमांड

```bash
termux-app-store list                     # सभी पैकेज सूचीबद्ध करें
termux-app-store show <पैकेज>             # पैकेज विवरण दिखाएं
termux-app-store install <पैकेज>          # फ़ास्ट इंस्टॉल (पहले से बना .deb)
termux-app-store install pkg1 pkg2 pkg3   # कई पैकेज एक साथ इंस्टॉल करें
termux-app-store fix-install <पैकेज>      # सोर्स बिल्ड को मजबूर करें
termux-app-store search <कीवर्ड>          # पैकेज खोजें
termux-app-store update                   # उपलब्ध अपडेट जांचें
termux-app-store upgrade                  # सभी पैकेज अपग्रेड करें
termux-app-store mirrors                  # मिरर स्थिति जांचें
termux-app-store cache info               # कैश जानकारी देखें
termux-app-store cache clear              # कैश साफ़ करें
termux-app-store version                  # नवीनतम संस्करण जांचें
termux-app-store help                     # पूरी सहायता
```

---

## फ़ास्ट इंस्टॉल कैसे काम करता है (v0.4.0+)

v0.4.0 से, इंस्टॉलेशन डिफ़ॉल्ट रूप से पहले से बने `.deb` बाइनरी डाउनलोड करती है:

1. लोकल `.deb` कैश जांचें (TTL 7 दिन)
2. कैश मिस होने पर मिरर क्रम से आज़माएं: GitHub Pages → Cloudflare CDN → jsDelivr CDN → raw GitHub
3. आर्किटेक्चर-वाइज SHA256 वेरिफ़िकेशन (`sha256_by_arch`)
4. लोकल में कैश करें और `dpkg -i` से इंस्टॉल करें

> फ़ास्ट इंस्टॉल विफल होने पर, `build-package.sh` के ज़रिए पूरा सोर्स बिल्ड करने के लिए `fix-install <पैकेज>` इस्तेमाल करें।

---

## पैकेज स्टेटस बैज

| बैज | विवरण |
|---|---|
| **NEW** | नया जोड़ा गया पैकेज (7 दिनों के अंदर) |
| **UPDATE** | नया संस्करण उपलब्ध है |
| **INSTALLED** | इंस्टॉल है और अप-टू-डेट है |
| **UNSUPPORTED** | Termux में dependency उपलब्ध नहीं |

---

## पैकेज जोड़ना

हर पैकेज एक `build.sh` फ़ाइल से परिभाषित होता है:

```
packages/<टूल-का-नाम>/build.sh
```

### न्यूनतम `build.sh` टेम्पलेट

```bash
TERMUX_PKG_HOMEPAGE=""
TERMUX_PKG_DESCRIPTION=""
TERMUX_PKG_LICENSE=""
TERMUX_PKG_MAINTAINER="@आपका-github-username"
TERMUX_PKG_VERSION=""
TERMUX_PKG_SRCURL=""
TERMUX_PKG_SHA256=""
```

```bash
cd termux-app-store
./termux-build create आपके-टूल-का-नाम
# या GitHub URL से ऑटो-क्रिएट करें:
./termux-build init https://github.com/user/repo
```

---

## सहायक टूल्स

### termux-build

```bash
./termux-build create <पैकेज>      # वितरण के लिए पैकेज बनाएं
./termux-build init <url>           # GitHub URL से ऑटो-क्रिएट करें
./termux-build lint <पैकेज>        # बिल्ड स्क्रिप्ट की जांच करें
./termux-build doctor               # पर्यावरण डायग्नोज़ करें
./termux-build template             # build.sh टेम्पलेट जनरेट करें
```

### tasctl

```bash
./tasctl install       # Termux App Store इंस्टॉल करें
./tasctl update        # नवीनतम संस्करण में अपडेट करें
./tasctl uninstall     # Termux App Store हटाएं
./tasctl doctor        # पर्यावरण डायग्नोज़ करें
./tasctl self-update   # tasctl खुद को अपडेट करे
```

---

## सुरक्षा और गोपनीयता

- अतिरिक्त अनुमति की ज़रूरत नहीं, कोई बैकग्राउंड सर्विस नहीं
- कोई account नहीं, कोई registration नहीं
- कोई analytics, tracking या telemetry नहीं
- हर `.deb` (डाउनलोड और कैश) के लिए SHA256 अनिवार्य
- लोकल-फ़र्स्ट डिज़ाइन (मेटाडेटा और डाउनलोड के लिए नेटवर्क का उपयोग)

> विवरण: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

## लाइसेंस

**MIT लाइसेंस** — विवरण के लिए [LICENSE](LICENSE) देखें।

---

## अनुरक्षक

**Djunekz** — स्वतंत्र डेवलपर

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

**© Termux App Store — सभी के लिए बनाया गया, समुदाय द्वारा।**
