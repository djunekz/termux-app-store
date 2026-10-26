import html as html_lib
import json
import os
import re

version = os.environ.get("VERSION", "0.0.0")
total = os.environ.get("TOTAL", "0")
updated = os.environ.get("UPDATED", "")

try:
    with open("tools/index.json") as f:
        data = json.load(f)
    pkgs = data.get("packages", [])
except (OSError, ValueError):
    pkgs = []


def esc(value):
    text = str(value if value is not None else "")
    text = re.sub(r"[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0000FE0F]", "", text)
    return html_lib.escape(text, quote=True)


def package_text(value):
    if isinstance(value, (list, tuple)):
        return ", ".join(str(x) for x in value)
    return str(value or "")


rows = []
for p in pkgs:
    name = esc(p.get("package", ""))
    ver = esc(p.get("version", ""))
    desc = esc(p.get("description", ""))
    dep = esc(package_text(p.get("depends"))) or "&mdash;"
    homepage = esc(p.get("homepage", ""))
    rows.append(
        f'<tr data-search="{name.lower()} {ver.lower()} {desc.lower()} {dep.lower()}" data-package="{name}"><td>{name}</td><td>{ver}</td><td>{desc}</td><td>{dep}</td></tr>'
    )
pkg_rows = "\n".join(rows)

featured = []
for p in pkgs[:6]:
    name = esc(p.get("package", ""))
    ver = esc(p.get("version", ""))
    desc = esc(p.get("description", "No description provided."))
    deps = esc(package_text(p.get("depends")) or "No additional dependencies listed")
    homepage = str(p.get("homepage", "") or "")
    safe_home = esc(homepage) if homepage.startswith(("https://", "http://")) else ""
    link = (
        f'<a class="package-link" href="{safe_home}" target="_blank" rel="noopener noreferrer">Project homepage</a>'
        if safe_home
        else '<span class="package-link muted">Homepage not listed</span>'
    )
    copy_arg = html_lib.escape(json.dumps(str(p.get("package", ""))), quote=True)
    featured.append(
        f'<article class="package-card" data-search="{name.lower()} {ver.lower()} {desc.lower()} {deps.lower()}"><div class="package-card-top"><span class="package-name">{name}</span><span class="package-version">{ver}</span></div><p>{desc}</p><div class="package-meta"><span>Dependencies: {deps}</span></div><div class="package-card-actions"><button class="small-btn" type="button" onclick="copyText({copy_arg}, this)">Copy name</button>{link}</div></article>'
    )
featured_cards = "\n".join(featured)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Termux App Store | Package Discovery for Termux</title>
<meta name="description" content="Explore Termux App Store packages, installation instructions, repository information, and contribution guides.">
<meta name="theme-color" content="#0d1117">
<meta property="og:title" content="Termux App Store">
<meta property="og:description" content="Discover tools and packages for your Termux environment.">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#0d1117;
  --bg2:#161b22;
  --bg3:#21262d;
  --border:#30363d;
  --border2:#21262d;
  --text:#c9d1d9;
  --text-dim:#8b949e;
  --text-dimmer:#484f58;
  --blue:#58a6ff;
  --blue-light:#79c0ff;
  --green:#3fb950;
  --yellow:#e3b341;
  --purple:#d2a8ff;
  --cyan:#56d364;
}}
html{{scroll-behavior:smooth}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}}

/* NAV */
nav{{
  position:sticky;top:0;z-index:100;
  background:rgba(13,17,23,.95);
  border-bottom:1px solid var(--border);
  backdrop-filter:blur(8px);
  padding:0;
  width:100vw;max-width:100%;box-sizing:border-box;
}}
.nav-inner{{max-width:960px;margin:0 auto;display:flex;align-items:center;gap:0;width:100%;box-sizing:border-box;padding:0 12px}}
.nav-brand{{color:var(--blue);font-weight:bold;font-size:14px;padding:12px 0;margin-right:12px;white-space:nowrap;flex-shrink:0}}
.nav-brand span{{color:var(--green)}}
.nav-tabs{{display:flex;gap:0;overflow-x:auto;scrollbar-width:none;flex:1;min-width:0;-webkit-overflow-scrolling:touch}}
.nav-tabs::-webkit-scrollbar{{display:none}}
.nav-tab{{
  color:var(--text-dim);font-size:13px;
  padding:12px 10px;
  border-bottom:2px solid transparent;
  cursor:pointer;white-space:nowrap;
  transition:color .15s,border-color .15s,background .15s;
  text-decoration:none;display:block;
}}
.nav-tab:hover{{color:var(--text)}}
.nav-tab.active{{color:var(--blue);border-bottom-color:var(--blue);background:rgba(88,166,255,.15);border-radius:4px 4px 0 0}}

/* LAYOUT */
.wrap{{max-width:960px;margin:0 auto;padding:28px 20px 64px;overflow-x:hidden}}

/* SECTIONS */
.section{{display:none}}
.section.active{{display:block}}

/* HERO */
.hero{{text-align:center;padding:48px 0 40px}}
.hero-logo{{font-size:11px;color:var(--blue);letter-spacing:.15em;text-transform:uppercase;margin-bottom:8px}}
.hero h1{{font-size:36px;font-weight:bold;color:var(--text);margin-bottom:8px;line-height:1.2}}
.hero h1 span{{color:var(--green)}}
.hero-sub{{color:var(--text-dim);font-size:14px;margin-bottom:28px}}
.hero-badges{{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-bottom:36px}}
.badge{{background:var(--bg2);color:var(--text-dim);border:1px solid var(--border);font-size:11px;padding:4px 12px;border-radius:20px}}
.badge.green{{background:#23863618;color:var(--green);border-color:#23863640}}
.badge.blue{{background:#1f6feb18;color:var(--blue);border-color:#1f6feb40}}
.badge.yellow{{background:#e3b34118;color:var(--yellow);border-color:#e3b34140}}
.hero-version{{
  display:inline-flex;align-items:center;gap:16px;
  background:var(--bg2);border:1px solid var(--border);border-radius:12px;
  padding:16px 28px;margin-bottom:36px;
}}
.hero-version-label{{color:var(--text-dimmer);font-size:11px;text-transform:uppercase;letter-spacing:.1em}}
.hero-version-num{{color:var(--green);font-size:28px;font-weight:bold}}
.hero-cta{{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}}
.btn{{
  font-family:'Courier New',monospace;
  font-size:13px;padding:10px 20px;border-radius:8px;
  border:1px solid transparent;cursor:pointer;
  text-decoration:none;display:inline-block;
  transition:all .15s;
}}
.btn-primary{{background:var(--green);color:#0d1117;border-color:var(--green);font-weight:bold}}
.btn-primary:hover{{background:#2ea043;border-color:#2ea043}}
.btn-outline{{background:transparent;color:var(--blue);border-color:var(--blue)}}
.btn-outline:hover{{background:#1f6feb18}}

/* CARDS */
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;margin:24px 0}}
.card{{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:20px}}
.card-icon{{font-size:24px;margin-bottom:10px}}
.card-title{{color:var(--text);font-weight:bold;font-size:14px;margin-bottom:6px}}
.card-desc{{color:var(--text-dim);font-size:12px;line-height:1.6}}

/* CODE BLOCKS */
.section-title{{color:var(--blue-light);font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:.1em;margin:32px 0 12px}}
.section-title:first-child{{margin-top:0}}
.code-block{{position:relative;margin-bottom:16px;width:100%;max-width:100%;box-sizing:border-box}}
.code-block pre{{
  background:var(--bg2);border:1px solid var(--border);border-radius:8px;
  padding:14px 72px 14px 14px;overflow-x:auto;font-size:12px;
}}
code{{color:#7ee787}}
.copy-btn{{
  position:absolute;top:8px;right:8px;
  background:var(--bg3);color:var(--text-dim);
  border:1px solid var(--border);border-radius:6px;
  padding:3px 9px;font-size:10px;font-family:'Courier New',monospace;
  cursor:pointer;transition:all .15s;white-space:nowrap;
}}
.copy-btn:hover{{background:var(--border);color:var(--text)}}
.copy-btn.copied{{color:var(--green);border-color:#2ea043}}
.code-label{{
  display:inline-block;background:var(--bg3);color:var(--text-dimmer);
  font-size:10px;text-transform:uppercase;letter-spacing:.1em;
  padding:2px 8px;border-radius:4px 4px 0 0;border:1px solid var(--border);
  border-bottom:none;margin-bottom:-1px;position:relative;z-index:1;
}}

/* CONTRIB MODE TITLE */
.contrib-mode-title{{font-size:13px;font-weight:bold;color:var(--text);margin:24px 0 8px;padding:6px 12px;background:var(--bg3);border:1px solid var(--border);border-radius:6px;display:inline-block}}

/* STEPS */
.steps{{margin:16px 0}}
.step{{display:flex;gap:16px;margin-bottom:20px;}}
.step-num{{
  flex-shrink:0;width:28px;height:28px;
  background:var(--bg3);border:1px solid var(--border);border-radius:50%;
  display:flex;align-items:center;justify-content:center;
  color:var(--blue);font-size:12px;font-weight:bold;
  margin-top:2px;
}}
.step-body{{flex:1;min-width:0;overflow:hidden}}
.step-title{{color:var(--text);font-size:13px;font-weight:bold;margin-bottom:6px}}
.step-desc{{color:var(--text-dim);font-size:12px;margin-bottom:8px;line-height:1.6}}
.step-note{{
  background:#e3b34110;border:1px solid #e3b34130;border-radius:6px;
  padding:8px 12px;font-size:12px;color:var(--yellow);margin-top:8px;
}}
.step-note-green{{
  background:#23863610;border:1px solid #23863630;border-radius:6px;
  padding:8px 12px;font-size:12px;color:var(--green);margin-top:8px;
}}

/* INSTALL OPTIONS */
.install-options{{display:grid;gap:16px;margin:16px 0}}
.install-option{{
  background:var(--bg2);border:1px solid var(--border);border-radius:10px;
  padding:20px;cursor:pointer;transition:border-color .2s,background .2s;
  overflow:hidden;max-width:100%;box-sizing:border-box}}
.install-option.open{{border-color:var(--blue);background:rgba(88,166,255,.04)}}
.install-option-header{{display:flex;align-items:center;gap:10px;margin-bottom:12px}}
.install-option-icon{{font-size:20px}}
.install-option-title{{color:var(--text);font-weight:bold;font-size:14px}}
.install-option-badge{{
  margin-left:auto;background:#23863618;color:var(--green);
  border:1px solid #23863640;font-size:10px;padding:2px 8px;border-radius:10px;
}}
.install-option-desc{{color:var(--text-dim);font-size:12px;margin-bottom:12px;word-break:break-word}}

/* TABLE */
.search-wrap{{margin-bottom:16px}}
.search-box{{
  width:100%;background:var(--bg2);border:1px solid var(--border);border-radius:8px;
  padding:10px 14px 10px 38px;color:var(--text);font-family:'Courier New',monospace;
  font-size:13px;outline:none;transition:border .15s;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' fill='none' stroke='%238b949e' stroke-width='2' viewBox='0 0 24 24'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:12px center;
}}
.search-box:focus{{border-color:var(--blue)}}
.search-box::placeholder{{color:var(--text-dimmer)}}
.search-count{{color:var(--text-dim);font-size:11px;margin-top:6px;min-height:16px}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
th{{
  text-align:left;padding:8px 12px;color:var(--text-dim);
  border-bottom:1px solid var(--border);font-weight:normal;
  font-size:11px;text-transform:uppercase;letter-spacing:.05em;
}}
td{{padding:7px 12px;border-bottom:1px solid var(--border2);vertical-align:top}}
td:first-child{{color:#7ee787;white-space:nowrap;font-weight:bold}}
td:nth-child(2){{color:var(--yellow);white-space:nowrap}}
td:nth-child(4){{color:var(--text-dimmer);font-size:11px}}
tr:hover td{{background:var(--bg2)}}
tr.hidden{{display:none}}

/* MISC */
a{{color:var(--blue);text-decoration:none}}
a:hover{{text-decoration:underline}}
.divider{{border:none;border-top:1px solid var(--border);margin:28px 0}}
.text-dim{{color:var(--text-dim);font-size:13px}}
.text-dimmer{{color:var(--text-dimmer)}}
.mt-4{{margin-top:16px}}
.info-box{{
  background:var(--bg2);border:1px solid var(--border);border-radius:8px;
  padding:16px 20px;margin:16px 0;
}}
.info-box p{{color:var(--text-dim);font-size:13px;line-height:1.7}}
.info-box p + p{{margin-top:8px}}
.arch-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:12px 0}}
.arch-item{{
  background:var(--bg3);border:1px solid var(--border);border-radius:6px;
  padding:8px 12px;text-align:center;color:var(--text-dim);font-size:12px;
}}

/* REQUIREMENTS */
.req-section{{margin:0 0 32px}}
.req-title{{color:var(--blue-light);font-size:11px;font-weight:bold;text-transform:uppercase;letter-spacing:.1em;margin-bottom:12px}}
.req-card{{
  background:var(--bg2);border:1px solid var(--border);border-radius:10px;
  padding:20px 24px;display:flex;align-items:center;gap:20px;flex-wrap:wrap;
}}
.req-left{{flex:1;min-width:200px}}
.req-app-name{{color:var(--green);font-size:16px;font-weight:bold;margin-bottom:4px}}
.req-app-desc{{color:var(--text-dim);font-size:12px;line-height:1.6;margin-bottom:6px}}
.req-meta{{color:var(--text-dimmer);font-size:11px}}
.btn-download{{
  flex-shrink:0;
  font-family:'Courier New',monospace;font-size:13px;font-weight:bold;
  background:var(--green);color:#0d1117;
  border:none;border-radius:8px;padding:10px 22px;
  text-decoration:none;display:inline-block;
  transition:background .15s;white-space:nowrap;
}}
.btn-download:hover{{background:#2ea043;text-decoration:none}}

footer{{
  border-top:1px solid var(--border2);padding:20px 0 0;
  color:var(--text-dimmer);font-size:12px;
  display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;
  margin-top:48px;
}}

@media(max-width:680px){{
  .nav-tabs{{flex:1;min-width:0;overflow-x:auto;-webkit-overflow-scrolling:touch}}
  .wrap{{padding:16px 14px 48px}}
  .hero{{padding:28px 0 24px}}
  .hero h1{{font-size:22px}}
  .hero-sub{{font-size:13px}}
  .hero-badges{{gap:6px;margin-bottom:20px}}
  .badge{{font-size:10px;padding:3px 9px}}
  .hero-cta{{gap:8px}}
  .btn{{font-size:12px;padding:9px 16px}}
  .hero-version{{flex-direction:column;gap:8px;padding:12px 16px}}
  .arch-grid{{grid-template-columns:repeat(2,1fr)}}
  .cards{{grid-template-columns:1fr;gap:12px}}
  .card{{padding:14px}}
  .section-title{{font-size:10px;margin:20px 0 10px}}
  .code-block{{margin-bottom:12px;width:100%}}
  .code-block pre{{font-size:11px;padding:11px 60px 11px 11px;overflow-x:auto}}
  .copy-btn{{font-size:9px;padding:3px 7px;top:7px;right:7px}}
  .code-label{{font-size:9px}}
  .install-options{{gap:12px;width:100%}}
  .install-option{{padding:14px;width:100%;box-sizing:border-box}}
  .install-option-header{{flex-wrap:nowrap}}
  .install-option-title{{font-size:13px}}
  .install-option-badge{{font-size:9px;white-space:nowrap}}
  .step{{gap:12px;margin-bottom:16px}}
  .step-num{{width:24px;height:24px;font-size:11px;flex-shrink:0}}
  .step-title{{font-size:13px}}
  .step-desc{{font-size:12px}}
  .step-note,.step-note-green{{font-size:11px;padding:7px 10px}}
  .info-box{{padding:14px 16px}}
  .info-box p{{font-size:12px}}
  .req-card{{padding:14px;gap:12px;flex-direction:column;align-items:flex-start}}
  .req-app-name{{font-size:14px}}
  .req-app-desc{{font-size:11px}}
  .btn-download{{font-size:12px;padding:9px 20px;align-self:stretch;text-align:center}}
  table{{font-size:11px}}
  th{{font-size:10px;padding:6px 8px}}
  td{{padding:5px 8px;word-break:break-word}}
  td:first-child{{white-space:normal}}
  td:nth-child(2){{white-space:normal}}
  .search-box{{font-size:12px;padding:9px 12px 9px 32px}}
  footer{{font-size:11px;flex-direction:column;gap:4px}}
  #tab-install .section-title ~ .code-block{{width:100%}}
}}

/* Extended discovery experience */
:root{{color-scheme:dark;--surface-raised:#1c232d;--accent-soft:rgba(88,166,255,.10)}}
.nav-inner{{max-width:1180px;gap:12px}}.nav-brand{{font-size:15px;text-decoration:none;letter-spacing:.04em}}.nav-brand span{{color:var(--text-dim);font-weight:500}}
.nav-tab{{padding:14px 11px;font-size:12px}}.theme-toggle{{border:1px solid var(--border);border-radius:7px;background:var(--bg2);color:var(--text-dim);padding:7px 10px;font-size:11px;cursor:pointer;white-space:nowrap}}
.wrap{{max-width:1180px;padding-top:32px}}.hero{{text-align:left;padding:60px 0 48px;max-width:880px}}.hero-logo{{letter-spacing:.18em}}.hero h1{{font-size:clamp(34px,5vw,58px);letter-spacing:-.045em;max-width:760px}}.hero-sub{{font-size:16px;max-width:640px;line-height:1.8}}.hero-badges{{justify-content:flex-start}}.hero-cta{{justify-content:flex-start}}.hero-version{{margin-left:0}}
.page-heading{{padding:30px 0 24px;max-width:760px}}.page-heading .eyebrow{{font-size:10px;letter-spacing:.18em;color:var(--green);font-weight:700;margin-bottom:12px}}.page-heading h1{{font-size:clamp(30px,4vw,46px);letter-spacing:-.04em;line-height:1.1;margin-bottom:14px}}.page-heading p{{color:var(--text-dim);font-size:15px;max-width:680px;line-height:1.8}}
.package-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:20px 0 28px}}.package-card{{background:linear-gradient(145deg,var(--bg2),var(--surface-raised));border:1px solid var(--border);border-radius:12px;padding:18px;display:flex;flex-direction:column;min-width:0;transition:transform .18s,border-color .18s}}.package-card:hover{{transform:translateY(-3px);border-color:#4b6178}}.package-card-top{{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px}}.package-name{{font-size:15px;font-weight:750;color:var(--green);overflow-wrap:anywhere}}.package-version{{font-size:10px;color:var(--yellow);border:1px solid var(--border);border-radius:5px;padding:3px 6px;white-space:nowrap}}.package-card p{{font-size:12px;color:var(--text-dim);line-height:1.75;overflow-wrap:anywhere;flex:1}}.package-meta{{font-size:10px;color:var(--text-dimmer);margin-top:14px;padding-top:10px;border-top:1px solid var(--border2);overflow-wrap:anywhere}}.package-card-actions{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:12px}}.small-btn{{background:var(--bg3);border:1px solid var(--border);border-radius:6px;color:var(--text);padding:6px 9px;font-size:10px;cursor:pointer}}.package-link{{font-size:11px}}.muted{{color:var(--text-dimmer)}}
.discover-toolbar{{display:flex;gap:12px;align-items:center;margin:8px 0}}.discover-toolbar .search-box{{flex:1}}.discover-toolbar .search-count{{white-space:nowrap}}.collection-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:16px 0}}.collection-card{{text-align:left;background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:16px;cursor:pointer;color:var(--text);display:flex;flex-direction:column;gap:9px;min-height:150px;transition:border-color .18s,transform .18s}}.collection-card:hover{{border-color:var(--blue);transform:translateY(-2px)}}.collection-kicker{{font-size:9px;letter-spacing:.12em;color:var(--blue);font-weight:700}}.collection-card strong{{font-size:14px}}.collection-card>span:last-child{{font-size:11px;line-height:1.65;color:var(--text-dim)}}
.guide-list{{display:grid;gap:12px;margin:12px 0 24px}}.guide-card{{display:grid;grid-template-columns:48px minmax(0,1fr);gap:16px;padding:22px;background:var(--bg2);border:1px solid var(--border);border-radius:11px}}.guide-number{{font-size:12px;color:var(--green);font-weight:700;letter-spacing:.08em;padding-top:3px}}.guide-card h2{{font-size:16px;margin-bottom:8px}}.guide-card p{{font-size:13px;line-height:1.8;color:var(--text-dim);max-width:760px}}.text-button{{display:inline-block;background:none;border:0;padding:10px 0 0;color:var(--blue);font-size:12px;cursor:pointer;text-decoration:none}}.guide-code{{display:inline-block;background:var(--bg);border:1px solid var(--border);border-radius:6px;padding:9px 12px;margin-top:12px;font:12px monospace;color:#7ee787}}
body.light-theme{{--bg:#f6f8fa;--bg2:#ffffff;--bg3:#eef2f6;--border:#d0d7de;--border2:#eaeef2;--text:#1f2328;--text-dim:#59636e;--text-dimmer:#737d87;--blue:#0969da;--blue-light:#0550ae;--green:#1a7f37;--yellow:#9a6700;--purple:#8250df;--surface-raised:#f0f4f8;color-scheme:light}}
body.light-theme nav{{background:rgba(246,248,250,.94)}}body.light-theme .hero h1{{color:var(--text)}}body.light-theme .btn-primary{{color:white}}
.section{{animation:section-in .2s ease-out}}@keyframes section-in{{from{{opacity:.45;transform:translateY(4px)}}to{{opacity:1;transform:translateY(0)}}}}
:focus-visible{{outline:2px solid var(--blue);outline-offset:3px}}button,a,input{{touch-action:manipulation}}
@media(max-width:900px){{.package-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.collection-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.nav-inner{{gap:6px}}}}
@media(max-width:600px){{.nav-inner{{padding:0 10px;flex-wrap:wrap}}.nav-brand{{padding:9px 0;margin-right:4px}}.nav-tabs{{order:2;flex-basis:100%;width:100%}}.nav-tab{{padding:10px 11px}}.theme-toggle{{margin-left:auto}}.wrap{{padding:18px 14px 48px}}.hero{{padding:34px 0 28px}}.hero h1{{font-size:34px}}.hero-sub{{font-size:13px}}.page-heading{{padding:20px 0}}.page-heading h1{{font-size:32px}}.package-grid{{grid-template-columns:1fr}}.collection-grid{{grid-template-columns:1fr 1fr}}.collection-card{{padding:12px;min-height:140px}}.discover-toolbar{{align-items:stretch;flex-direction:column;gap:5px}}.guide-card{{grid-template-columns:30px minmax(0,1fr);gap:10px;padding:16px}}.guide-card h2{{font-size:14px}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{scroll-behavior:auto!important;animation-duration:.01ms!important;transition-duration:.01ms!important}}}}

</style>
</head>
<body>

<nav>
  <div class="nav-inner">
    <a class="nav-brand" href="#home" onclick="showTab('home',this);return false">TAS <span>/ TERMUX APP STORE</span></a>
    <div class="nav-tabs">
      <a class="nav-tab active" data-tab="home" onclick="showTab('home',this)" href="#home">Overview</a>
      <a class="nav-tab" data-tab="discover" onclick="showTab('discover',this)" href="#discover">Discover</a>
      <a class="nav-tab" data-tab="packages" onclick="showTab('packages',this)" href="#packages">Packages</a>
      <a class="nav-tab" data-tab="install" onclick="showTab('install',this)" href="#install">Install</a>
      <a class="nav-tab" data-tab="guides" onclick="showTab('guides',this)" href="#guides">Guides</a>
      <a class="nav-tab" data-tab="contribute" onclick="showTab('contribute',this)" href="#contribute">Contribute</a>
      <a class="nav-tab" data-tab="repo" onclick="showTab('repo',this)" href="#repo">Repository</a>
      <button class="theme-toggle" type="button" onclick="toggleTheme()" aria-label="Toggle color theme">Theme</button>
    </div>
  </div>
</nav>

<div class="wrap">

<!-- ═══════════════ HOME ═══════════════ -->
<div id="tab-home" class="section active">
  <div class="hero">
    <div class="hero-logo">◈  Termux Package Repository</div>
    <h1><span>Termux App Store</span></h1>
    <p class="hero-sub">A local-first package manager for Termux on Android. Browse, build, and install community tools through a native TUI & CLI, with SHA-256-verified binaries, source builds, and no root required. Transparency over magic.<br>by <a href="https://github.com/djunekz">@djunekz</a></p>
    <div class="hero-badges">
      <span class="badge green">v{version}</span>
      <span class="badge blue">{total} packages</span>
      <span class="badge">aarch64</span>
      <span class="badge">arm</span>
      <span class="badge">x86_64</span>
      <span class="badge">i686</span>
    </div>
    <div class="hero-cta">
      <a class="btn btn-primary" onclick="showTab('install',document.querySelector('[onclick*=install]'))" href="#">Get Started</a>
      <a class="btn btn-outline" href="https://github.com/djunekz/termux-app-store">GitHub →</a>
    </div>
  </div>

  <div class="req-section">
    <div class="req-title">Requirements</div>
    <div class="req-card">
      <div class="req-left">
        <div class="req-app-name">Termux</div>
        <div class="req-app-desc">Android terminal emulator and Linux environment app. Required to run Termux App Store.</div>
        <div class="req-meta">v0.118.3 &nbsp;&middot;&nbsp; Universal APK &nbsp;&middot;&nbsp; ~100MB</div>
      </div>
      <a class="btn-download" href="https://github.com/termux/termux-app/releases/download/v0.118.3/termux-app_v0.118.3+github-debug_universal.apk">
        Download
      </a>
    </div>
  </div>

  <div class="cards">
    <div class="card">
      <div class="card-icon">▸</div>
      <div class="card-title">Fast &amp; Lightweight</div>
      <div class="card-desc">Built for Termux. Minimal dependencies, fast package resolution, and a clean TUI interface.</div>
    </div>
    <div class="card">
      <div class="card-icon">▸</div>
      <div class="card-title">{total} Packages</div>
      <div class="card-desc">A growing collection of tools, utilities, and apps — all packaged and ready to install via pkg.</div>
    </div>
    <div class="card">
      <div class="card-icon">▸</div>
      <div class="card-title">Multi-Architecture</div>
      <div class="card-desc">Full support for aarch64, arm, x86_64, and i686. Works on any Android device running Termux.</div>
    </div>
    <div class="card">
      <div class="card-icon">▸</div>
      <div class="card-title">Open &amp; Community</div>
      <div class="card-desc">Anyone can submit a package. Fork the repo, build your tool, open a PR — it's that simple.</div>
    </div>
  </div>

  <div class="section-title">Quick Install</div>
  <div class="code-block">
    <div class="code-label">shell</div>
    <pre><code>curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python')">copy</button>
  </div>

  <div class="section-title">Usage</div>
  <div class="code-block">
    <pre><code id="usage-code">pkg install termux-app-store     # install
pkg upgrade termux-app-store     # update to v{version}
pkg uninstall termux-app-store   # remove
termux-app-store                 # launch TUI
termux-app-store list            # show all {total} packages
termux-app-store install &lt;pkg&gt;   # install a package</code></pre>
    <button class="copy-btn" onclick="copyCode(this,document.getElementById('usage-code').innerText)">copy</button>
  </div>
</div>

<!-- ═══════════════ INSTALL ═══════════════ -->
<div id="tab-install" class="section">
  <div class="section-title">Install Termux App Store</div>
  <p class="text-dim" style="margin-bottom:20px">Choose one of the methods below. Method 1 (pkg) is recommended if you already have the repository configured.</p>

  <div class="install-options">

    <div class="install-option">
      <div class="install-option-header">
        <div class="install-option-icon">◈</div>
        <div class="install-option-title">Method 1 — pkg (Recommended)</div>
        <div class="install-option-badge">Recommended</div>
      </div>
      <div class="install-option-desc">Install via the official APT repository. Supports automatic upgrades with <code>pkg upgrade</code>.</div>
      <div class="code-block">
        <div class="code-label">step 1 — add repository</div>
        <pre><code>curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python</code></pre>
        <button class="copy-btn" onclick="copyCode(this,'curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python')">copy</button>
      </div>
      <div class="code-block">
        <div class="code-label">step 2 — install</div>
        <pre><code>pkg install termux-app-store</code></pre>
        <button class="copy-btn" onclick="copyCode(this,'pkg install termux-app-store')">copy</button>
      </div>
    </div>

    <div class="install-option">
      <div class="install-option-header">
        <div class="install-option-icon">◈</div>
        <div class="install-option-title">Method 2 — pip</div>
      </div>
      <div class="install-option-desc">Install directly from PyPI. Useful if you prefer pip-based package management.</div>
      <div class="code-block">
        <pre><code>pip install termux-app-store</code></pre>
        <button class="copy-btn" onclick="copyCode(this,'pip install termux-app-store')">copy</button>
      </div>
    </div>

    <div class="install-option">
      <div class="install-option-header">
        <div class="install-option-icon">◈</div>
        <div class="install-option-title">Method 3 — tasctl (bootstrap script)</div>
      </div>
      <div class="install-option-desc">One-line bootstrap using the tasctl installer. Downloads and sets up everything automatically.</div>
      <div class="code-block">
        <pre><code>curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install</code></pre>
        <button class="copy-btn" onclick="copyCode(this,'curl -fsSL https://raw.githubusercontent.com/djunekz/termux-app-store/master/tasctl | bash -s install')">copy</button>
      </div>
    </div>

    <div class="install-option">
      <div class="install-option-header">
        <div class="install-option-icon">◈</div>
        <div class="install-option-title">Method 4 — Manual (from source)</div>
      </div>
      <div class="install-option-desc">Clone the repository and run the install script manually. Useful for development or offline setups.</div>
      <div class="code-block">
        <pre><code>git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store
cd termux-app-store
bash install.sh</code></pre>
        <button class="copy-btn" onclick="copyCode(this,'git clone --depth 1 --single-branch --branch master https://github.com/djunekz/termux-app-store\ncd termux-app-store\nbash install.sh')">copy</button>
      </div>
    </div>

  </div>

  <hr class="divider">
  <div class="section-title">Update &amp; Remove</div>
  <div style="display:block;width:100%">
  <div class="code-block">
    <div class="code-label">update</div>
    <pre><code>pkg upgrade termux-app-store
# or via tasctl:
tasctl update</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'pkg upgrade termux-app-store')">copy</button>
  </div>
  <div class="code-block">
    <div class="code-label">remove</div>
    <pre><code>pkg uninstall termux-app-store
# or via tasctl:
tasctl uninstall</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'pkg uninstall termux-app-store')">copy</button>
  </div>
  </div>
</div>

<!-- DISCOVER -->
<div id="tab-discover" class="section">
  <div class="page-heading"><div class="eyebrow">EXPLORE THE CATALOG</div><h1>Find your next tool.</h1><p>Browse a curated starting point, then search the full catalog to find tools that fit your workflow.</p></div>
  <div class="discover-toolbar"><input class="search-box" id="discoverSearch" type="search" placeholder="Search featured packages..." oninput="filterCards()"><span class="search-count" id="discoverCount">Featured packages</span></div>
  <div class="package-grid" id="featuredGrid">{featured_cards}</div>
  <div class="info-box"><p><strong>Looking for something specific?</strong> Open the Packages section to search the complete index, including descriptions, versions, and dependencies.</p><p>Package order follows the source index. Featured placement does not indicate popularity, endorsement, or security review.</p></div>
  <div class="section-title">Explore by workflow</div>
  <div class="collection-grid">
    <button class="collection-card" onclick="searchPackages('python')"><span class="collection-kicker">01 / DEVELOPMENT</span><strong>Python and scripting</strong><span>Find packages mentioning Python, scripts, and automation.</span></button>
    <button class="collection-card" onclick="searchPackages('git')"><span class="collection-kicker">02 / WORKFLOW</span><strong>Version control</strong><span>Explore tools related to Git and source management.</span></button>
    <button class="collection-card" onclick="searchPackages('network')"><span class="collection-kicker">03 / CONNECTIVITY</span><strong>Networking tools</strong><span>Search the catalog for networking utilities.</span></button>
    <button class="collection-card" onclick="searchPackages('security')"><span class="collection-kicker">04 / SECURITY</span><strong>Security utilities</strong><span>Find relevant packages by their indexed descriptions.</span></button>
  </div>
</div>

<!-- GUIDES -->
<div id="tab-guides" class="section">
  <div class="page-heading"><div class="eyebrow">DOCUMENTATION</div><h1>Get more from Termux.</h1><p>Practical starting points for setting up the repository, installing packages, and keeping your environment maintainable.</p></div>
  <div class="guide-list">
    <article class="guide-card"><div class="guide-number">01</div><div><h2>Before you begin</h2><p>Install Termux from a trusted source and open the app before running repository setup commands. Keep your installation source consistent to avoid signature and update conflicts.</p><button class="text-button" onclick="showTab('install',document.querySelector('[data-tab=install]'))">View installation methods</button></div></article>
    <article class="guide-card"><div class="guide-number">02</div><div><h2>Set up the repository</h2><p>Use the recommended installation method in the Install section. Read each command before running it and verify that the repository setup completes without errors.</p><button class="text-button" onclick="showTab('repo',document.querySelector('[data-tab=repo]'))">Repository details</button></div></article>
    <article class="guide-card"><div class="guide-number">03</div><div><h2>Search and install packages</h2><p>Use the package catalog to check the package name, version, description, and listed dependencies. Package names must match the repository index.</p><button class="text-button" onclick="showTab('packages',document.querySelector('[data-tab=packages]'))">Browse all packages</button></div></article>
    <article class="guide-card"><div class="guide-number">04</div><div><h2>Keep packages updated</h2><p>Refresh package metadata before upgrading. If an installation fails, review the exact terminal output and confirm that your device architecture and repository configuration are supported.</p><div class="guide-code">pkg update && pkg upgrade</div></div></article>
    <article class="guide-card"><div class="guide-number">05</div><div><h2>Report a problem</h2><p>Include the package name, version, device architecture, relevant command, and complete error output when opening an issue. Remove tokens, passwords, and other private information first.</p><a class="text-button" href="https://github.com/djunekz/termux-app-store/issues" target="_blank" rel="noopener noreferrer">Open project issues</a></div></article>
  </div>
  <div class="info-box"><p><strong>Security note:</strong> Only install software you trust. Review project sources and permissions where applicable, and avoid running commands copied from untrusted sources without understanding what they do.</p></div>
</div>

<!-- ═══════════════ PACKAGES ═══════════════ -->
<div id="tab-packages" class="section">
  <div class="section-title">All Packages ({total})</div>
  <div class="search-wrap">
    <input class="search-box" type="text" id="searchInput" placeholder="Search packages by name or description..." oninput="filterTable()">
    <div class="search-count" id="searchCount"></div>
  </div>
  <table id="pkgTable">
    <thead><tr><th>Package</th><th>Version</th><th>Description</th><th>Depends</th></tr></thead>
    <tbody>
{pkg_rows}
    </tbody>
  </table>
</div>

<!-- ═══════════════ CONTRIBUTE ═══════════════ -->
<div id="tab-contribute" class="section">
  <div class="section-title">Distribute to Termux App Store</div>
  <div class="info-box">
    <p>Want to share your tool with the Termux community? Follow the steps below to package and submit it to this repository.</p>
    <p>All packages are reviewed via Pull Request before being added to the index.</p>
  </div>

  <div class="steps">
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <div class="step-title">Fork &amp; Clone the repository</div>
        <div class="step-desc">Fork the official repo on GitHub, then clone it to your Termux environment.</div>
        <div class="code-block">
          <pre><code>git clone --depth 1 --single-branch --branch master https://github.com/YOUR_USERNAME/termux-app-store
cd termux-app-store</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'git clone --depth 1 --single-branch --branch master https://github.com/YOUR_USERNAME/termux-app-store\ncd termux-app-store')">copy</button>
        </div>
        <div class="step-note">Replace <code>YOUR_USERNAME</code> with your GitHub username.</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">
        <div class="step-title">Create a new branch</div>
        <div class="step-desc">Always work on a separate branch before submitting a Pull Request.</div>
        <div class="code-block">
          <pre><code>git checkout -b &lt;your-branch&gt;</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'git checkout -b &lt;your-branch&gt;')">copy</button>
        </div>
      </div>
    </div>
  </div>

  <div class="contrib-mode-title">Automatic</div>
  <div class="steps">
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <div class="step-title">Init with termux-build or pkg-scaffold.py</div>
        <div class="step-desc">Run <code>./termux-build init</code> with your tool's repository URL to automatically scaffold the package.</div>
        <div class="code-block">
          <pre><code>./termux-build init &lt;url-your-repository&gt;</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'./termux-build init &lt;url-your-repository&gt;')">copy</button>
        </div>
        <div class="step-desc mt-4">Or use the <code>pkg-scaffold.py</code> wizard. It reads your repository, detects the build method, computes the SHA256 and writes <code>packages/&lt;your-tool-name&gt;/build.sh</code> for you.</div>
        <div class="code-block">
          <pre><code>python3 pkg-scaffold.py --from &lt;url-your-repository&gt;</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'python3 pkg-scaffold.py --from &lt;url-your-repository&gt;')">copy</button>
        </div>
        <div class="step-note">Run it from the repository root and review the generated <code>build.sh</code> before continuing.</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">
        <div class="step-title">Run and test your tool</div>
        <div class="step-desc">After init completes, try running your tool directly. If it does not run correctly, open an issue before proceeding.</div>
        <div class="step-note-green">If your tool runs correctly — skip to <strong>Commit &amp; Pull Request</strong> below.</div>
      </div>
    </div>
  </div>

  <div class="contrib-mode-title">Manual</div>
  <div class="steps">
    <div class="step">
      <div class="step-num">1</div>
      <div class="step-body">
        <div class="step-title">Generate a build.sh template</div>
        <div class="step-desc">Use the template generator to scaffold your <code>build.sh</code> file.</div>
        <div class="code-block">
          <pre><code>./termux-build template</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'./termux-build template')">copy</button>
        </div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">2</div>
      <div class="step-body">
        <div class="step-title">Create your package folder and build.sh</div>
        <div class="step-desc">Create a directory under <code>packages/</code> for your tool, then write your <code>build.sh</code> inside it.</div>
        <div class="code-block">
          <pre><code>mkdir packages/&lt;your-tool-name&gt;</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'mkdir packages/&lt;your-tool-name&gt;')">copy</button>
        </div>
        <div class="code-block">
          <div class="code-label">example build.sh</div>
          <pre><code>TERMUX_PKG_HOMEPAGE="https://github.com/you/your-tool"
TERMUX_PKG_DESCRIPTION="A short description of your tool"
TERMUX_PKG_VERSION="1.0.0"
TERMUX_PKG_DEPENDS="python"

termux_step_make_install() {{
  install -Dm755 your-tool "$TERMUX_PREFIX/bin/your-tool"
}}</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'TERMUX_PKG_HOMEPAGE=...')">copy</button>
        </div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">3</div>
      <div class="step-body">
        <div class="step-title">Validate with termux-build lint</div>
        <div class="step-desc">Run the linter to check your package definition for common errors before building.</div>
        <div class="code-block">
          <pre><code>./termux-build lint &lt;your-tool-name&gt;</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'./termux-build lint &lt;your-tool-name&gt;')">copy</button>
        </div>
        <div class="step-note">Fix any warnings or errors reported before proceeding.</div>
      </div>
    </div>

    <div class="step">
      <div class="step-num">4</div>
      <div class="step-body">
        <div class="step-title">Build and test your package</div>
        <div class="step-desc">Build the <code>.deb</code> package and verify it installs and runs correctly in Termux.</div>
        <div class="code-block">
          <pre><code>bash build-package.sh &lt;your-tool-name&gt;</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'bash build-package.sh &lt;your-tool-name&gt;')">copy</button>
        </div>
        <div class="step-note-green">If the tool runs correctly after building, you're ready to submit!</div>
      </div>
    </div>
  </div>

  <hr class="divider">
  <div class="section-title">Commit &amp; Open a Pull Request</div>
  <div class="steps">
    <div class="step">
      <div class="step-num">&#8594;</div>
      <div class="step-body">
        <div class="step-desc">Push your changes and open a PR targeting the <code>master</code> branch.</div>
        <div class="code-block">
          <pre><code>git add packages/&lt;your-tool-name&gt;/
git commit -m "feat: add &lt;your-tool-name&gt; package"
git push origin &lt;your-branch&gt;</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'git add packages/\ngit commit -m \"feat: add package\"\ngit push origin &lt;your-branch&gt;')">copy</button>
        </div>
        <div class="step-desc mt-4">Then open a Pull Request at:</div>
        <div class="code-block">
          <pre><code>https://github.com/djunekz/termux-app-store/pulls</code></pre>
          <button class="copy-btn" onclick="copyCode(this,'https://github.com/djunekz/termux-app-store/pulls')">copy</button>
        </div>
        <div class="step-note">Describe what your tool does and include a brief test result in the PR description.</div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════ REPO ═══════════════ -->
<div id="tab-repo" class="section">
  <div class="section-title">Repository Information</div>
  <div class="info-box">
    <p>This is an unofficial APT repository hosted on GitHub Pages. Add it to your Termux sources to install packages with <code>pkg</code>.</p>
  </div>

  <div class="section-title">Recommended: signed repository (one command)</div>
  <div class="code-block">
    <pre><code>curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python')">copy</button>
  </div>

  <div class="section-title">Manual setup &mdash; step 1: signing key</div>
  <div class="code-block">
    <pre><code>mkdir -p $PREFIX/etc/apt/keyrings &amp;&amp; curl -fsSL https://djunekz.github.io/termux-app-store/termux-app-store.gpg -o $PREFIX/etc/apt/keyrings/termux-app-store.gpg</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'mkdir -p $PREFIX/etc/apt/keyrings &amp;&amp; curl -fsSL https://djunekz.github.io/termux-app-store/termux-app-store.gpg -o $PREFIX/etc/apt/keyrings/termux-app-store.gpg')">copy</button>
  </div>

  <div class="section-title">Manual setup &mdash; step 2: repository entry</div>
  <div class="code-block">
    <pre><code>echo "deb [signed-by=$PREFIX/etc/apt/keyrings/termux-app-store.gpg] https://djunekz.github.io/termux-app-store termux main" &gt; $PREFIX/etc/apt/sources.list.d/tas.list</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'echo &quot;deb [signed-by=$PREFIX/etc/apt/keyrings/termux-app-store.gpg] https://djunekz.github.io/termux-app-store termux main&quot; &gt; $PREFIX/etc/apt/sources.list.d/tas.list')">copy</button>
  </div>
  <div class="info-box"><p>The repository metadata is GPG-signed (<code>InRelease</code> / <code>Release.gpg</code>). Do not use <code>[trusted=yes]</code>; it disables signature verification.</p></div>

  <div class="section-title">Supported Architectures</div>
  <div class="arch-grid">
    <div class="arch-item">aarch64</div>
    <div class="arch-item">arm</div>
    <div class="arch-item">x86_64</div>
    <div class="arch-item">i686</div>
  </div>

  <div class="section-title">Packages Index Endpoints</div>
  <div class="code-block">
    <pre><code>dists/termux/main/binary-aarch64/Packages
dists/termux/main/binary-arm/Packages
dists/termux/main/binary-x86_64/Packages
dists/termux/main/binary-i686/Packages</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'dists/termux/main/binary-aarch64/Packages')">copy</button>
  </div>

  <div class="section-title">Add / Remove Repository Manually</div>
  <div class="code-block">
    <div class="code-label">add</div>
    <pre><code>curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'curl -fsSL https://djunekz.github.io/termux-app-store/install-repo.py | python')">copy</button>
  </div>
  <div class="code-block">
    <div class="code-label">remove</div>
    <pre><code>rm $PREFIX/etc/apt/sources.list.d/tas.list
pkg update</code></pre>
    <button class="copy-btn" onclick="copyCode(this,'rm $PREFIX/etc/apt/sources.list.d/tas.list\npkg update')">copy</button>
  </div>

  <hr class="divider">
  <div class="section-title">Release Info</div>
  <div class="info-box">
    <p><strong style="color:var(--text)">Current version:</strong> <span style="color:var(--green)">v{version}</span></p>
    <p><strong style="color:var(--text)">Packages in index:</strong> <span style="color:var(--blue)">{total}</span></p>
    <p><strong style="color:var(--text)">Last updated:</strong> <span style="color:var(--text-dim)">{updated}</span></p>
    <p><strong style="color:var(--text)">Source:</strong> <a href="https://github.com/djunekz/termux-app-store">github.com/djunekz/termux-app-store</a></p>
  </div>
</div>

<footer>
  <span>Termux App Store &copy; <a href="https://github.com/djunekz">@djunekz</a></span>
  <span>Last updated: {updated}</span>
</footer>

</div><!-- /wrap -->

<script>
function showTab(id, el) {{
  const target = document.getElementById('tab-' + id);
  if (!target) return false;
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
  target.classList.add('active');
  const active = el || document.querySelector('[data-tab="' + id + '"]');
  if (active && active.classList.contains('nav-tab')) active.classList.add('active');
  if (history.replaceState) history.replaceState(null, '', '#' + id);
  window.scrollTo({{top:0,behavior:'smooth'}});
  return false;
}}

function copyText(text, btn) {{
  const done = () => {{ if (btn) {{ const old = btn.textContent; btn.textContent = 'Copied'; setTimeout(() => btn.textContent = old, 1400); }} }};
  if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done));
  else fallbackCopy(text, done);
}}
function fallbackCopy(text, callback) {{
  const field = document.createElement('textarea'); field.value = text; field.style.position = 'fixed'; field.style.opacity = '0'; document.body.appendChild(field); field.select();
  try {{ document.execCommand('copy'); callback(); }} catch (e) {{}} finally {{ field.remove(); }}
}}
function toggleTheme() {{
  const light = document.body.classList.toggle('light-theme');
  try {{ localStorage.setItem('tas-theme', light ? 'light' : 'dark'); }} catch (e) {{}}
}}
function searchPackages(query) {{
  showTab('packages', document.querySelector('[data-tab="packages"]'));
  const input = document.getElementById('searchInput'); input.value = query; filterTable();
}}
function filterCards() {{
  const q = document.getElementById('discoverSearch').value.toLowerCase().trim(); let visible = 0;
  document.querySelectorAll('#featuredGrid .package-card').forEach(card => {{ const match = card.dataset.search.includes(q); card.hidden = !match; if (match) visible++; }});
  document.getElementById('discoverCount').textContent = visible + ' featured package' + (visible === 1 ? '' : 's');
}}

function copyCode(btn, text) {{
  navigator.clipboard.writeText(text).then(() => {{
    btn.textContent = 'copied!';
    btn.classList.add('copied');
    setTimeout(() => {{ btn.textContent = 'copy'; btn.classList.remove('copied'); }}, 2000);
  }});
}}

function filterTable() {{
  const q = document.getElementById('searchInput').value.toLowerCase().trim();
  const rows = document.querySelectorAll('#pkgTable tbody tr');
  let visible = 0;
  rows.forEach(row => {{
    const haystack = row.dataset.search || row.textContent.toLowerCase();
    const match = haystack.includes(q);
    row.classList.toggle('hidden', !match);
    if (match) visible++;
  }});
  const countEl = document.getElementById('searchCount');
  countEl.textContent = q ? (visible + ' of ' + rows.length + ' packages match') : (rows.length + ' packages available');
}}

// Handle nav onclick properly
document.querySelectorAll('.nav-tab').forEach(tab => {{
  tab.addEventListener('click', e => e.preventDefault());
}});
try {{ if (localStorage.getItem('tas-theme') === 'light') document.body.classList.add('light-theme'); }} catch (e) {{}}
const initialTab = location.hash.replace('#', '');
if (initialTab && document.getElementById('tab-' + initialTab)) showTab(initialTab, document.querySelector('[data-tab="' + initialTab + '"]'));
if (document.getElementById('searchCount')) document.getElementById('searchCount').textContent = document.querySelectorAll('#pkgTable tbody tr').length + ' packages available';
</script>
</body>
</html>"""

print(html)
