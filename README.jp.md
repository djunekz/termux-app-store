![[Termux App Store — TUI Package Manager for Termux](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)](https://github.com/user-attachments/assets/758d85c8-5654-422e-b345-ee6db5c27b1f)

# [Termux App Store — Termux 向け TUI & CLI パッケージマネージャー](https://djunekz.github.io/termux-app-store/)

**Android 上の Termux 向けにネイティブで構築された、ローカルファーストの TUI / CLI パッケージマネージャー。チェックサム検証付きのバイナリインストールとソースビルドのフォールバックに対応。**

> 他の言語: 🇬🇧 **[English](README.md)** | 🇮🇩 **[Bahasa Indonesia](README.id.md)** | 🇹🇭 **[ภาษาไทย](README.th.md)** | 🇨🇳 **[中文](README.ch.md)** | 🇻🇳 **[Tiếng Việt](README.vi.md)** | 🇮🇳 **[हिन्दी](README.in.md)**

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

> **ローカルファースト • チェックサム検証 • ソースベース • Termux ネイティブ • Android ターミナル**
> Termux パッケージのインストールと管理 — ビルド済みバイナリまたはソースビルド — root 不要、アカウント不要、テレメトリなし。

---

# Termux App Store とは？

**Termux App Store**（`termux-app-store`）は、Python（[Textual](https://github.com/Textualize/textual)）で作られた **TUI（Terminal User Interface）** と **CLI パッケージマネージャー**です。Android の Termux ユーザーが、端末上で直接 **ツール／パッケージを閲覧・インストール・管理**できます。アカウント、テレメトリ、root は不要です。パッケージのメタデータとダウンロードにはネットワークを使用します。

**v0.4.0** 以降、Termux App Store は **ファストインストールエンジン**に対応しています。パッケージはミラープール（GitHub Pages、Cloudflare CDN、jsDelivr）からビルド済み `.deb` バイナリとしてダウンロードされ、ローカルの `.deb` キャッシュ（TTL 7 日）が使われます。キャッシュ済みのものを含むすべての `.deb` はアーキテクチャごとの SHA256 と一致する必要があり、一致しない場合は拒否されます。SHA256 は破損や不一致の検出に使うもので、発行元の署名ではありません。ソースビルドは `fix-install` で引き続き利用できます。

**Termux 向けの代替パッケージマネージャー**として動作し、`build.sh` スクリプトを使ってコミュニティ製ツールをインストールできます。AUR（Arch User Repository）と発想は似ていますが、Android 上の Termux 専用に設計されています。

> **`termux-packages` や TUR（Termux User Repository）との違いは？**
>
> - `termux-packages` は Termux の公式リポジトリです。コアチームが管理し、PR の承認が必要で、広く使われているツールのみを受け付けます。
> - TUR は厳選された拡張で、こちらもコントリビューターのレビューが必要です。
> - **Termux App Store** は完全にコミュニティ主導です。誰でも `build.sh` を投稿でき、パッケージはビルド済み `.deb` またはソースビルドとして配布され、中央の承認ゲートはありません。Termux の上に重ねる、個人 + コミュニティのパッケージ層と考えてください。

> [!IMPORTANT]
> Termux App Store は **隠れた自動インストーラーではありません**。
> すべてのインストール（バイナリでもソースでも）は **ローカルで、透明性を保ち、ユーザーの完全な管理下で**実行されます。

---

# 対象ユーザー

| ユーザー | ユースケース |
|---|---|
| Termux ユーザー | 高速なバイナリインストール、またはソースビルドの完全な制御 |
| 開発者 | ビルド済み `.deb` やソースパッケージでツールを配布 |
| レビュアー・監査者 | ビルドスクリプトのレビューと検証 |
| メンテナー | 複数の Termux パッケージを一括管理 |

---

<div align="center">
<img src="https://github.com/user-attachments/assets/b03419bc-8efe-4ed0-9b61-fea5153e9f53" width="100%" alt="Termux App Store — Main View"/>

<br/><br/>
<H1>TUI インターフェース</H1>

| TUI メイン画面 | TUI インストール画面 | メニューパレット |
|:---:|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/fb9395f1-f943-44c5-b88f-be18e480fd26" width="400" alt="TUI Main Interface"/> | <img src="https://github.com/user-attachments/assets/a0ee7a15-95d2-4743-9f7e-90cd9e3388f7" width="400" alt="TUI Install Interface"/> | <img src="https://github.com/user-attachments/assets/ad760153-983f-4113-a465-2b682cb26b67" width="400" alt="Menu Palette Interface"/> |
| TUI メインメニュー | パッケージのインストール処理 | コマンドパレット |

> TUI は **タッチスクリーン**に完全対応した使いやすい設計です

---

<H1>CLI インターフェースとその他のツール対応</H1>

| その他のツール対応の CLI 表示 | Guidebook |
|:---:| :---: |
| https://github.com/user-attachments/assets/71c097b2-01a8-4c1c-9ffd-c26f29ee6ae6 | https://github.com/user-attachments/assets/b668a890-835f-4467-820a-988b1810c902 |


CLI インターフェースと対応ツール: `tasctl`, `termux-build`, `doctor.py`, `pkg-scaffold.py`, `build-package.sh`, `guidebook.py`

---

<H1>画面録画</H1>

| `termux-app-store` の TUI、CLI、その他のツール `tasctl`, `termux-build`, `guidebook.py` の録画 |
|:---:|
| <img src="https://github.com/user-attachments/assets/152c757f-d2a3-4f31-8174-2b857a3aad51" width="100%" alt="termux-app-store"/> | termux-app-store

</div>

---

# クイックインストールとアンインストール

> **[PyPI](https://pypi.org/project/termux-app-store/)** で公開中 — 検索でき、見つけやすくなっています。

### オプション 1（推奨）

```bash
pkg install python
pip install termux-app-store
```

### オプション 2（手動）

> 簡単な方法（メモリが限られている場合に推奨）

```bash
curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install
```

> git clone を使う方法（リポジトリ全体をダウンロード）

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh
```

インストール後に実行:

```bash
termux-app-store        # Open interactive TUI
termux-app-store -h     # Show CLI help
tas                     # Shorthand for termux-app-store
```

### アンインストール

```bash
pip uninstall termux-app-store
# or
./tasctl uninstall
```

---

# 使い方

### TUI — インタラクティブインターフェース

```bash
termux-app-store
# or shorthand:
tas
```

| キー / ボタン | 機能 |
|---|---|
| **Install / Update / Open**（`Ctrl+I`） | メインボタンはパッケージの状態に応じて変わります。未インストールなら Install、新しいバージョンがあれば Update、インストール済みで最新なら Open。Open はツールを実行し（コマンドの選択、引数の追加が可能）、Enter を押すと TUI に戻ります |
| **Shortcut**（Open ダイアログ） | 引数付きでツールを実行する Termux:Widget スクリプトを `~/.shortcuts` に作成します |
| **Upgrade all**（更新バナー） | バナーに更新可能なインストール済みパッケージの数が表示され、すべてをキューに追加します |
| **Cancel**（`Ctrl+X`） | 実行中のダウンロードまたはソースビルドを次の安全なタイミングで停止します |
| `F4` | アクティビティ履歴: インストール、更新、削除、起動 |
| `F5` | 問題を報告: 入力済みのバグ報告フォームを開きます |
| `Ctrl+R` / `Ctrl+Q` | パッケージの更新 / 終了 |
| `Ctrl+P` | コマンドパレット（通知のオン/オフを含む。Termux:API が必要） |

### CLI — 直接コマンド

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

# 機能

| **パッケージブラウザ（TUI）** `packages/` フォルダのパッケージを、キーボードとタッチ操作でインタラクティブに閲覧できます。<br>**ファストインストールエンジン** ミラープール（GitHub Pages、Cloudflare CDN、jsDelivr）からビルド済み `.deb` をダウンロードし、自動でフォールバックします。<br>**バイナリキャッシュ** TTL 7 日のローカル `.deb` キャッシュ。キャッシュ済みファイルもインストールのたびにアーキテクチャごとの SHA256 で再検証されます。キャッシュ済みパッケージは即座にインストールされます。<br>**スマートビルドバリデーター** 未対応の Termux 依存関係を検出し、ステータスバッジを自動表示します。 | **リアルタイム検索とフィルター** 名前や説明でパッケージを検索できます。`search`/`find` CLI コマンドも利用可能です。<br>**複数パッケージのインストール/削除** 1 つのコマンドで複数のパッケージをインストール・削除し、結果をまとめて表示します。<br>**ワンクリック管理** Termux App Store 自体のインストール / 更新 / 削除を `./tasctl` で行えます。<br>**プライバシー重視** アカウント、トラッキング、テレメトリなし。ローカルデータがあればそれで動作し、メタデータやパッケージの取得にはネットワークが必要です。 |
|---|---|

---

# ファストインストールの仕組み（v0.4.0+）

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

> ファストインストールが失敗した場合は、`fix-install <package>` で `build-package.sh` による完全なソースビルドを強制できます。

---

# パッケージの追加

Termux App Store のすべてのパッケージは、1 つの `build.sh` ファイルで定義されます。Arch Linux の PKGBUILD に似ていますが、Android 上の Termux 向けに調整されています。

すべてのパッケージには `build.sh` ファイルが**必須**です:

```
packages/<tool-name>/build.sh
```

### 最小 `build.sh` テンプレート

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
> 完全なテンプレートは `template/build.sh` を参照するか、`./termux-build template` を実行してください

### termux-build でパッケージを追加する

```bash
cd termux-app-store
./termux-build create your-tool-name
# or auto-create from a GitHub URL:
./termux-build init https://github.com/user/repo
```

> [!NOTE]
> 名前にスペースは使わず、`-` を使ってください。例: `my-tool-name`

---

# termux-build — ビルドと検証ツール

`termux-build` は検証とレビューを補助するツールであり、自動アップロードや自動公開のツールではありません。

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
> `termux-build` は **読み取りと検証のみ**を行います。ファイルの変更や GitHub へのアップロードは行いません。

---

# tasctl — Termux App Store コントローラー

`tasctl` は termux-app-store システムのコントローラーです。

```bash
./tasctl install       # Install Termux App Store (latest)
./tasctl update        # Update to latest version
./tasctl uninstall     # Remove Termux App Store
./tasctl doctor        # Diagnose environment
./tasctl self-update   # Update tasctl itself
./tasctl help          # Show help
```

---

# guidebook — Termux App Store のすべての情報

```bash
python guidebook.py
```

> [!NOTE]
> guidebook は現在、英語とインドネシア語の 2 言語に対応しています。

---

# パッケージを Termux コミュニティに配布する方法

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

> 詳細ガイド: [HOW_TO_UPLOAD.md](HOW_TO_UPLOAD.md)

---

# アーキテクチャ

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

> 詳細: [ARCHITECTURE.md](ARCHITECTURE.md)

---

# セキュリティとプライバシー

| **セキュリティ** | **プライバシー** |
|---|---|
| 追加の権限は不要 | アカウントや登録は不要 |
| ネットワークポートを開かない | 分析やトラッキングなし |
| バックグラウンドサービスなし | いかなるテレメトリもなし |
| ビルドはユーザーが明示的に実行したときのみ動作 | ローカルファースト。ネットワークはメタデータとダウンロードに使用 |
| すべての `.deb`（ダウンロードとキャッシュ）に SHA256 が必須 | バイナリの出所は透明で監査可能 |

> 詳細: [SECURITY.md](SECURITY.md) | [PRIVACY.md](PRIVACY.md) | [DISCLAIMER.md](DISCLAIMER.md) | [BINARY_DISCLAIMER.md](BINARY_DISCLAIMER.md)

---

# 開発とテスト

```bash
git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
pip install -e ".[dev]"
```

| コマンド | 機能 |
|---|---|
| `make test` または `pytest` | テストスイートを実行 |
| `make coverage` | カバレッジレポート付きでテストスイートを実行 |
| `make lint` | Ruff による lint とフォーマットのチェック |
| `make typecheck` | Mypy による型チェック |
| `make check` | lint、型チェック、テストをまとめて実行 |

依存関係は `uv.lock` で固定されています（`uv sync --extra dev`）。詳しいガイドは [CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。

---

# コントリビューション

あらゆる貢献を歓迎します！

| 貢献の方法 | 説明 |
|---|---|
| パッケージの追加 | 新しいツールパッケージを提出 |
| バグの報告 | GitHub で issue を作成 |
| PR の送信 | コードやドキュメントの改善 |
| PR のレビュー | 他の人の貢献の検証を手伝う |
| セキュリティ監査 | ビルドスクリプトのセキュリティを確認 |
| ドキュメントの改善 | ドキュメントの明確化や翻訳 |

> 詳細ガイド: [CONTRIBUTING.md](CONTRIBUTING.md)

---

# ヘルプとドキュメント

| ドキュメント | 説明 |
|---|---|
| [FAQ](FAQ.md) | よくある質問 |
| [TROUBLESHOOTING](TROUBLESHOOTING.md) | よくある問題の解決方法 |
| [HOW TO UPLOAD](HOW_TO_UPLOAD.md) | ツールのアップロード方法 |
| [CONTRIBUTING](CONTRIBUTING.md) | コントリビューションガイド |
| [SUPPORT](SUPPORT.md) | サポートの受け方 |
| [BINARY_DISCLAIMER](BINARY_DISCLAIMER.md) | バイナリ配布に関する注意 |

---

# 理念

> *「ローカルファースト。利便性よりコントロール。魔法より透明性。」*

Termux App Store は、次のようなユーザーのために作られています:

- 自分のデバイスで何が動いているかを完全に理解したい
- ビルドとソースを直接コントロールしたい
- ベンダーロックインを避けたい
- ツールを Termux コミュニティとオープンに共有したい

---

# ライセンス

このプロジェクトは **MIT License** のもとで公開されています。詳細は [LICENSE](LICENSE) を参照してください。

---

# メンテナー

**Djunekz** — Termux App Store の個人開発者・メンテナー

[![GitHub](https://img.shields.io/badge/GitHub-djunekz-3fb950?style=for-the-badge&logo=github)](https://github.com/djunekz)

---

# このプロジェクトを支援する

Termux App Store が役に立ったら:

- このリポジトリに **Star** を付ける — 他の人が見つけやすくなります
- Termux・Android のコミュニティで **共有**する
- Issues で **バグを報告**する
- あらゆる改善の **PR を送る**
- **スポンサー**: https://saweria.co/redHh

---

# スター履歴

<a href="https://www.star-history.com/?repos=djunekz%2Ftermux-app-store&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&theme=dark&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=djunekz/termux-app-store&type=date&legend=bottom-right&sealed_token=yxIBRg8O6CfVP9fzApqsHovR51Bu-9FS0C01LYEOvVBkXHNNIe-JOGKtHOqIq1X_KzE" />
 </picture>
</a>

---

# 関連プロジェクトとキーワード

> このプロジェクトは独立して開発されており、公式の [Termux](https://github.com/termux/termux-app) プロジェクトとは**無関係**です。

**検索キーワード:** termux app store · termux package manager · termux tui · termux cli · termux tools · android terminal package manager · termux custom packages · termux source build · termux binary install · termux deb installer · termux alternative · termux community packages · termux offline installer · termux-app-store djunekz · install packages termux android · alternative to termux-packages · alternative to TUR termux · how to distribute package termux · termux community repo · termux build from source android · create termux package · custom repo termux · tas command termux

---

**© Termux App Store — みんなのために、コミュニティが作っています。**
