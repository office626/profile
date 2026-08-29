#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""profile.yaml / portfolio.yaml から公開用ファイルを生成する。"""

import json
import os
import sys
import datetime
import html

try:
    import yaml
except ImportError:
    sys.exit("PyYAML が必要です: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_SRC = os.path.join(ROOT, "profile.yaml")
PORTFOLIO_SRC = os.path.join(ROOT, "portfolio.yaml")


def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_profile():
    d = load_yaml(PROFILE_SRC)
    warn = []
    meta = d.get("meta", {})
    if meta.get("github_user") in (None, "", "CHANGE-ME"):
        warn.append("meta.github_user が未設定です")
    today = datetime.date.today().isoformat()
    if str(meta.get("updated", "")) != today:
        warn.append(f"meta.updated が {meta.get('updated')} のままです（今日は {today}）")
    for w in warn:
        print("  ⚠  " + w)
    return d


def load_portfolio():
    if os.path.isfile(PORTFOLIO_SRC):
        return load_yaml(PORTFOLIO_SRC)
    return {"cases": [], "meta": {}}


def public_contacts(d):
    return [c for c in d.get("contacts", []) if c.get("public")]


def layer_labels(d, keys):
    L = d.get("layers", {})
    return [L[k]["label"] for k in (keys or []) if k in L]


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  ✓  {path}")


def shared_css():
    return """
:root {
  --ink: #16232E; --ink-soft: #4A5A66; --paper: #F2F1ED; --panel: #FBFAF7;
  --rule: #D8D5CC; --accent: #3F7A6E;
  --mincho: "Hiragino Mincho ProN", "Yu Mincho", "Noto Serif JP", serif;
  --gothic: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Noto Sans JP", sans-serif;
  --mono: ui-monospace, "SFMono-Regular", "Menlo", monospace;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--paper); color: var(--ink); font-family: var(--gothic);
  line-height: 1.85; font-size: 15.5px; -webkit-font-smoothing: antialiased; }
.wrap { max-width: 880px; margin: 0 auto; padding: 0 24px 96px; }
a { color: var(--accent); text-underline-offset: 3px; }
.topnav { padding: 16px 0; font-size: 13px; display: flex; gap: 16px; flex-wrap: wrap; }
.topnav a { text-decoration: none; font-family: var(--mono); letter-spacing: .06em; }
header { padding: 48px 0 40px; border-bottom: 1px solid var(--rule); }
.eyebrow { font-family: var(--mono); font-size: 11.5px; letter-spacing: .18em;
  color: var(--ink-soft); text-transform: uppercase; margin: 0 0 22px; }
h1 { font-family: var(--mincho); font-weight: 600; font-size: clamp(38px, 7vw, 60px);
  line-height: 1.15; margin: 0 0 6px; }
.kana { font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft); }
.tagline { font-family: var(--mincho); font-size: clamp(17px, 2.6vw, 21px);
  line-height: 1.8; margin: 28px 0 0; max-width: 36em; }
.affil-line { margin: 26px 0 0; color: var(--ink-soft); font-size: 14px; }
.affil-line strong { color: var(--ink); font-weight: 600; }
.avail { margin-top: 12px; font-size: 13px; color: var(--accent); }
section { padding: 48px 0 8px; border-bottom: 1px solid var(--rule); }
section:last-of-type { border-bottom: 0; }
h2 { font-family: var(--mincho); font-size: 21px; font-weight: 600; margin: 0 0 24px;
  letter-spacing: .08em; display: flex; align-items: baseline; gap: 14px; }
h2::after { content: ""; flex: 1; height: 1px; background: var(--rule); }
h3 { font-family: var(--mincho); font-size: 17px; margin: 0 0 8px; }
.lead { color: var(--ink-soft); font-size: 14.5px; margin: 0 0 20px; }
.audience-grid { display: grid; gap: 12px; }
.audience-card { background: var(--panel); border: 1px solid var(--rule); padding: 18px 20px; }
.audience-card strong { display: block; margin-bottom: 6px; font-size: 15px; }
.audience-card p { margin: 0; font-size: 13.5px; color: var(--ink-soft); }
.highlight-box { background: color-mix(in srgb, var(--accent) 8%, var(--panel));
  border: 1px solid color-mix(in srgb, var(--accent) 25%, var(--rule));
  border-left: 3px solid var(--accent); padding: 22px 24px; margin-bottom: 16px; }
.highlight-box h3 { color: var(--accent); font-size: 16px; margin-bottom: 10px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font-size: 11px; font-weight: 600; padding: 5px 9px; border-radius: 2px;
  color: var(--c); border: 1px solid color-mix(in srgb, var(--c) 35%, transparent);
  background: color-mix(in srgb, var(--c) 7%, transparent); }
.cards { display: grid; gap: 14px; }
.card { background: var(--panel); border: 1px solid var(--rule);
  border-left: 3px solid var(--accent); padding: 22px 24px; }
.card h3 { font-size: 18px; margin: 10px 0 8px; }
.card p { margin: 0; font-size: 14.5px; }
.proof { margin-top: 12px; padding-top: 10px; border-top: 1px dotted var(--rule);
  font-size: 12.5px; color: var(--ink-soft); }
.proof span { font-family: var(--mono); font-size: 10.5px; letter-spacing: .12em;
  display: block; margin-bottom: 3px; color: var(--accent); }
.timeline { list-style: none; margin: 0; padding: 0; }
.timeline > li { display: grid; grid-template-columns: 168px 1fr; gap: 24px; padding: 0 0 28px; }
.when { font-family: var(--mono); font-size: 12px; color: var(--ink-soft);
  padding-top: 5px; border-top: 2px solid var(--ink); }
.what h3 { font-size: 17px; margin: 0 0 6px; }
.what p { margin: 0 0 8px; font-size: 14px; color: var(--ink-soft); }
.plainlist { list-style: none; margin: 0; padding: 0; }
.plainlist li { padding: 10px 0; border-bottom: 1px dotted var(--rule); font-size: 14.5px; }
.plainlist .when { display: inline-block; width: 118px; border: 0; padding: 0; }
.creds { display: grid; gap: 28px; }
.credgroup h3 { font-family: var(--mono); font-size: 11.5px; letter-spacing: .16em;
  color: var(--accent); margin: 0 0 10px; padding-bottom: 8px; border-bottom: 1px solid var(--rule); }
.credgroup ul { margin: 0; padding-left: 1.15em; }
.credgroup li { font-size: 14px; margin-bottom: 6px; }
dl.contact { margin: 0; }
.row { display: grid; grid-template-columns: 118px 1fr; gap: 16px;
  padding: 10px 0; border-bottom: 1px dotted var(--rule); }
.row dt { font-family: var(--mono); font-size: 11.5px; color: var(--ink-soft); padding-top: 4px; }
.row dd { margin: 0; font-size: 14.5px; word-break: break-word; }
.pub-list li { margin-bottom: 10px; }
.case-mini { font-size: 13.5px; color: var(--ink-soft); margin-bottom: 14px; }
.case-mini strong { color: var(--ink); }
.form-grid { display: grid; gap: 14px; max-width: 560px; }
.form-grid label { display: block; font-size: 13px; margin-bottom: 4px; color: var(--ink-soft); }
.form-grid input, .form-grid textarea, .form-grid select {
  width: 100%; padding: 10px 12px; border: 1px solid var(--rule); border-radius: 2px;
  font: inherit; background: #fff; }
.form-grid textarea { min-height: 120px; resize: vertical; }
.btn { display: inline-block; padding: 12px 24px; background: var(--accent); color: #fff;
  border: 0; border-radius: 2px; font: inherit; cursor: pointer; }
.endnotes { color: var(--ink-soft); font-size: 12.5px; line-height: 1.9; }
.endnotes h2 { font-family: var(--mono); font-size: 11.5px; letter-spacing: .16em;
  color: var(--ink-soft); margin-bottom: 14px; }
.endnotes p { margin: 0 0 8px; }
footer { padding: 40px 0 96px; font-family: var(--mono); font-size: 11.5px; color: var(--ink-soft); }

/* --- 顧客属性別のアクセント（低彩度） --- */
[data-target="municipality"] { --c: #3D6B99; }
[data-target="enterprise"]   { --c: #2F4A6B; }
[data-target="sme"]          { --c: #3F7A6E; }
[data-target="support"]      { --c: #A9713C; }
[data-target="training"]     { --c: #6B5A8E; }

/* --- HERO --- */
.hero { padding: 40px 0 44px; border-bottom: 1px solid var(--rule); }
.hero h1 { font-size: clamp(30px, 6vw, 46px); line-height: 1.28; margin: 0 0 18px; }
.hero .sub { font-size: 15.5px; line-height: 1.9; max-width: 34em; margin: 0 0 24px; }
.hero .who { color: var(--ink-soft); font-size: 13.5px; line-height: 1.85; margin: 0 0 18px; }
.hero .who strong { color: var(--ink); font-size: 16px; font-family: var(--mincho);
  display: block; margin-bottom: 4px; }
.hero-top { display: flex; gap: 26px; align-items: flex-start; flex-wrap: wrap-reverse; }
.hero-body { flex: 1 1 380px; }
.domains { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 26px; padding: 0; list-style: none; }
.domains li { font-size: 12px; color: var(--ink-soft); border: 1px solid var(--rule);
  background: var(--panel); padding: 5px 10px; border-radius: 2px; }
.cta-row { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.btn.ghost { background: transparent; color: var(--accent);
  border: 1px solid color-mix(in srgb, var(--accent) 45%, var(--rule)); }
.btn.sm { padding: 8px 16px; font-size: 13px; }
.btn:hover { opacity: .88; }
.cta-note { font-size: 12.5px; color: var(--ink-soft); margin: 12px 0 0; }

/* --- 対象者カード --- */
.audience-grid { grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
.audience-card { border-top: 3px solid var(--c, var(--accent)); display: flex; flex-direction: column; }
.audience-card strong { font-family: var(--mincho); font-size: 16px; }
.audience-card p { flex: 1; margin-bottom: 12px; }
.audience-card .btn { align-self: flex-start; }

/* --- 相談例 --- */
.voice-grid { display: grid; gap: 10px; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
.voice { background: var(--panel); border: 1px solid var(--rule); border-radius: 2px;
  padding: 14px 16px; font-size: 14px; position: relative; }
.voice::before { content: "“"; font-family: var(--mincho); color: var(--accent);
  font-size: 22px; line-height: 1; margin-right: 4px; }
.closing { margin: 22px 0 0; font-size: 14.5px; font-weight: 600; }

/* --- サービスメニュー --- */
.filterbar { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 22px; }
.filterbar button { font: inherit; font-size: 13px; padding: 7px 15px; cursor: pointer;
  background: transparent; color: var(--ink-soft); border: 1px solid var(--rule); border-radius: 2px; }
.filterbar button[aria-pressed="true"] { background: var(--ink); color: #fff; border-color: var(--ink); }
.menu-grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
.menu-card { background: var(--panel); border: 1px solid var(--rule); border-top: 3px solid var(--c, var(--accent));
  padding: 20px 22px 22px; display: flex; flex-direction: column;
  transition: transform .15s ease, box-shadow .15s ease; }
.menu-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(22,35,46,.07); }
.menu-card.is-hidden { display: none; }
.menu-card .no { font-family: var(--mono); font-size: 10.5px; letter-spacing: .16em;
  color: var(--ink-soft); margin: 0 0 8px; }
.menu-card h3 { font-size: 17px; margin: 6px 0 8px; }
.menu-card .summary { font-size: 13.5px; color: var(--ink-soft); margin: 0 0 14px; }
.menu-card details { border-top: 1px dotted var(--rule); padding-top: 10px; margin-bottom: 12px; }
.menu-card details + details { margin-top: -4px; }
.menu-card summary { font-size: 12.5px; color: var(--accent); cursor: pointer; }
.menu-card details ul { margin: 8px 0 0; padding-left: 1.1em; font-size: 13px; color: var(--ink-soft); }
.menu-card details li { margin-bottom: 4px; }
.menu-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: auto 0 14px;
  padding-top: 12px; border-top: 1px solid var(--rule); }
.menu-meta dt { font-family: var(--mono); font-size: 10px; letter-spacing: .12em; color: var(--ink-soft); }
.menu-meta dd { margin: 2px 0 0; font-size: 14.5px; font-weight: 600; }
.menu-card .note { font-size: 12px; color: var(--ink-soft); margin: 0 0 12px; }
.menu-card .for { font-size: 13px; margin: 0 0 12px; padding-left: 1.1em; color: var(--ink-soft); }
.menu-card .for li { margin-bottom: 3px; }
.menu-card .flag { font-size: 12.5px; background: color-mix(in srgb, var(--accent) 9%, transparent);
  border-left: 2px solid var(--accent); padding: 8px 10px; margin: 0 0 12px; }
.menu-empty { color: var(--ink-soft); font-size: 14px; }

/* --- 発注までの流れ --- */
.steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
.steps li { background: var(--panel); border: 1px solid var(--rule); padding: 16px 18px; }
.steps .num { font-family: var(--mono); font-size: 10.5px; letter-spacing: .16em; color: var(--accent); }
.steps h3 { font-size: 15px; margin: 6px 0 6px; }
.steps p { margin: 0; font-size: 13px; color: var(--ink-soft); }

/* --- 発注条件早見表 --- */
.conditions { width: 100%; border-collapse: collapse; font-size: 14px; }
.conditions th, .conditions td { text-align: left; padding: 10px 12px;
  border-bottom: 1px dotted var(--rule); }
.conditions th { width: 42%; font-weight: 600; color: var(--ink); }
.conditions td { color: var(--ink-soft); }

/* --- 選ばれる理由 --- */
.reasons { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
.reason { border-top: 2px solid var(--ink); padding-top: 14px; }
.reason .num { font-family: var(--mono); font-size: 11px; letter-spacing: .16em; color: var(--accent); }
.reason h3 { font-size: 16px; margin: 6px 0 8px; }
.reason p { margin: 0; font-size: 13.5px; color: var(--ink-soft); }

/* --- 代表実績 --- */
.case-grid { display: grid; gap: 14px; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
.case-card { background: var(--panel); border: 1px solid var(--rule);
  border-left: 3px solid var(--accent); padding: 20px 22px; }
.case-card.is-hidden { display: none; }
.case-card h3 { font-size: 16px; margin: 10px 0 10px; }
.case-card dl { margin: 0; display: grid; grid-template-columns: 68px 1fr; gap: 4px 12px; }
.case-card dt { font-family: var(--mono); font-size: 10px; letter-spacing: .1em;
  color: var(--ink-soft); padding-top: 4px; }
.case-card dd { margin: 0; font-size: 13.5px; }
.case-card ul { margin: 10px 0 0; padding-left: 1.1em; font-size: 13px; }

/* --- 支援機関向け --- */
.taglist { display: flex; flex-wrap: wrap; gap: 8px; list-style: none; margin: 18px 0; padding: 0; }
.taglist li { font-size: 13px; background: #fff; border: 1px solid var(--rule); padding: 6px 12px; }

/* --- 常時表示CTA --- */
.sticky-cta { position: fixed; right: 24px; bottom: 24px; z-index: 20;
  box-shadow: 0 4px 16px rgba(22,35,46,.16); text-decoration: none; }
@media (max-width: 640px) {
  .timeline > li { grid-template-columns: 1fr; }
  .row { grid-template-columns: 1fr; }
  .wrap { padding-bottom: 120px; }
  .menu-meta { grid-template-columns: 1fr; gap: 6px; }
  .case-card dl { grid-template-columns: 1fr; gap: 0 0; }
  .case-card dt { padding-top: 8px; }
  .conditions, .conditions tbody, .conditions tr, .conditions th, .conditions td { display: block; }
  .conditions tr { border: 1px solid var(--rule); background: var(--panel);
    padding: 10px 12px; margin-bottom: 8px; }
  .conditions th, .conditions td { width: auto; border: 0; padding: 0; }
  .conditions td { margin-top: 2px; }
  .sticky-cta { right: 0; left: 0; bottom: 0; text-align: center; border-radius: 0; padding: 15px; }
}
"""


def chips_html(d, keys, e=html.escape):
    L = d.get("layers", {})
    return "".join(
        f'<span class="chip" style="--c:{L[k]["color"]}">{e(L[k]["label"])}</span>'
        for k in (keys or []) if k in L
    )


def build_offerings_html(d, proof_label="経験"):
    e = html.escape
    out = ""
    for x in d.get("offerings", []):
        proof = (
            f'<p class="proof"><span>{proof_label}</span>{e(x["proof"])}</p>'
            if x.get("proof") else ""
        )
        out += f"""<article class="card">
        <div class="chips">{chips_html(d, x.get('layers'), e)}</div>
        <h3>{e(x['title'])}</h3>
        <p>{e(x['body'].strip())}</p>{proof}</article>"""
    return out


def build_career_html(d):
    e = html.escape
    out = ""
    for c in d.get("career", []):
        out += f"""<li>
        <div class="when">{e(c.get('period') or '')}</div>
        <div class="what">
          <h3>{e(c['title'])}</h3>
          {f'<p class="org">{e(c["org"])}</p>' if c.get('org') else ''}
          {f'<p>{e(c["detail"])}</p>' if c.get('detail') else ''}
          <div class="chips">{chips_html(d, c.get('layers'), e)}</div>
        </div></li>"""
    return out


def build_media_html(mc):
    e = html.escape
    if not mc or not mc.get("items"):
        return ""
    items = ""
    for it in mc["items"]:
        date = f'<span class="when">{e(it.get("date", ""))}</span> ' if it.get("date") else ""
        media = (
            f' <span style="color:var(--ink-soft);font-size:13px">（{e(it["media"])}）</span>'
            if it.get("media") else ""
        )
        if it.get("url"):
            title = f'<a href="{e(it["url"])}">{e(it["title"])}</a>'
        else:
            title = e(it["title"])
        note = f' — {e(it["note"])}' if it.get("note") else ""
        items += f"<li>{date}{title}{media}{note}</li>"
    return (
        f'<h3 style="margin-top:28px">メディア掲載・取材</h3>'
        f'<p class="lead">{e(mc.get("intro", ""))}</p>'
        f'<ul class="plainlist pub-list">{items}</ul>'
    )


def cred_item_html(item, e):
    if isinstance(item, dict):
        label = item.get("label", "")
        url = item.get("url")
        if url:
            return f'<li><a href="{e(url)}">{e(label)}</a></li>'
        return f"<li>{e(label)}</li>"
    return f"<li>{e(item)}</li>"


def build_writings_html(wr):
    e = html.escape
    if not wr:
        return ""
    pages = ""
    if wr.get("author_pages"):
        pages = "<ul class='plainlist pub-list'>" + "".join(
            f'<li><a href="{e(p["url"])}">{e(p["label"])}</a></li>'
            for p in wr["author_pages"]
        ) + "</ul>"
    items = ""
    for it in wr.get("items", []):
        date = f'<span class="when">{e(it.get("date", ""))}</span> ' if it.get("date") else ""
        pub = (
            f' <span style="color:var(--ink-soft);font-size:13px">（{e(it["publication"])}）</span>'
            if it.get("publication") else ""
        )
        if it.get("url"):
            title = f'<a href="{e(it["url"])}">{e(it["title"])}</a>'
        else:
            title = e(it["title"])
        note = f' — {e(it["note"])}' if it.get("note") else ""
        items += f"<li>{date}{title}{pub}{note}</li>"
    body = pages
    if items:
        body += f'<ul class="plainlist pub-list">{items}</ul>'
    if not body:
        return ""
    return (
        f'<h3 style="margin-top:28px">執筆・コラム</h3>'
        f'<p class="lead">{e(wr.get("intro", ""))}</p>'
        f"{body}"
    )


def build_contact_form(d, prefix=""):
    e = html.escape
    cf = d.get("contact_form", {})
    action = e(cf.get("action", ""))
    if not action:
        return ""
    selects = ""
    for i, s in enumerate(cf.get("selects", [])):
        fid = f"{prefix}sel{i}"
        opts = "".join(f"<option>{e(o)}</option>" for o in s.get("options", []))
        suffix = "（任意）" if s.get("optional") else ""
        selects += (
            f'<div><label for="{fid}">{e(s["name"])}{suffix}</label>'
            f'<select id="{fid}" name="{e(s["name"])}">'
            f'<option value="">選択してください</option>{opts}</select></div>'
        )
    msg_label = e(cf.get("message_label", "ご相談内容"))
    msg_note = cf.get("message_note", "")
    note_html = f'<p class="cta-note">{e(msg_note)}</p>' if msg_note else ""
    return f"""
    <form class="form-grid" action="{action}" method="POST">
      <input type="hidden" name="_subject" value="プロフィールサイトからのお仕事のご相談">
      <input type="hidden" name="_captcha" value="false">
      <input type="text" name="_honey" style="display:none">
      <div><label for="{prefix}name">お名前 *</label><input id="{prefix}name" name="name" required></div>
      <div><label for="{prefix}org">団体・企業名</label><input id="{prefix}org" name="organization"></div>
      <div><label for="{prefix}email">メールアドレス *</label><input id="{prefix}email" name="email" type="email" required></div>
      {selects}
      <div><label for="{prefix}message">{msg_label} *</label>
        <textarea id="{prefix}message" name="message" required placeholder="現在の状況、解決したいこと、希望時期など"></textarea>
        {note_html}</div>
      <button class="btn" type="submit">送信する</button>
    </form>"""


def build_hero_html(d):
    e = html.escape
    b = d["basic"]
    h = d.get("hero", {})
    if not h:
        return ""
    photo = (
        f'<img src="{e(b["photo"])}" alt="{e(b["name_ja"])}" '
        f'style="width:132px;height:132px;object-fit:cover;border-radius:2px">'
        if b.get("photo") else ""
    )
    roles = "<br>".join(e(r) for r in h.get("roles", []))
    domains = "".join(f"<li>{e(x)}</li>" for x in h.get("domains", []))
    p, s = h.get("primary_cta", {}), h.get("secondary_cta", {})
    ctas = ""
    if p:
        ctas += f'<a class="btn" href="{e(p["href"])}">{e(p["label"])}</a>'
    if s:
        ctas += f'<a class="btn ghost" href="{e(s["href"])}">{e(s["label"])}</a>'
    note = f'<p class="cta-note">{e(h["note"])}</p>' if h.get("note") else ""
    return f"""
  <header class="hero">
    <div class="hero-top">
      <div class="hero-body">
        <p class="eyebrow">Consulting</p>
        <h1>{e(h.get('headline', ''))}</h1>
        <p class="sub">{e(h.get('sub', ''))}</p>
        <p class="who"><strong>{e(b['name_ja'])}</strong>{roles}</p>
        <ul class="domains">{domains}</ul>
        <div class="cta-row">{ctas}</div>
        {note}
      </div>
      {photo}
    </div>
  </header>"""


def build_targets_html(d):
    e = html.escape
    cards = ""
    for g in d.get("audience_guides", []):
        target = e(g.get("target", ""))
        cta = (
            f'<a class="btn ghost sm" href="#menu" '
            f'data-menu-filter="{target}">{e(g["cta"])}</a>'
            if g.get("cta") and target else ""
        )
        cards += (
            f'<div class="audience-card" id="{e(g.get("id",""))}" data-target="{target}">'
            f'<strong>{e(g["label"])}</strong><p>{e(g["summary"])}</p>{cta}</div>'
        )
    return cards


def build_problems_html(d):
    e = html.escape
    pr = d.get("problems", {})
    if not pr:
        return ""
    items = "".join(f'<div class="voice">{e(x)}</div>' for x in pr.get("items", []))
    return f"""
  <section id="problems">
    <h2>{e(pr.get('title', ''))}</h2>
    <p class="lead">{e(pr.get('intro', ''))}</p>
    <div class="voice-grid">{items}</div>
    <p class="closing">{e(pr.get('closing', ''))}</p>
  </section>"""


def build_menu_html(d):
    e = html.escape
    sm = d.get("service_menu", {})
    if not sm:
        return ""
    filters = "".join(
        f'<button type="button" data-filter="{e(f["key"])}" '
        f'aria-pressed="{"true" if f["key"] == "all" else "false"}">{e(f["label"])}</button>'
        for f in sm.get("filters", [])
    )
    cards = ""
    for m in sm.get("items", []):
        targets = " ".join(m.get("targets", []))
        primary = (m.get("targets") or ["sme"])[0]
        tags = "".join(f'<span class="chip">{e(t)}</span>' for t in m.get("tags", []))
        for_whom = "".join(f"<li>{e(x)}</li>" for x in (m.get("for_whom") or [])[:3])
        scope = "".join(f"<li>{e(x)}</li>" for x in m.get("scope", []))
        deliv = "".join(f"<li>{e(x)}</li>" for x in m.get("deliverables", []))
        flag = f'<p class="flag">{e(m["highlight"])}</p>' if m.get("highlight") else ""
        note = f'<p class="note">{e(m["price_note"])}</p>' if m.get("price_note") else ""
        audience = (
            f'<p class="note">主な対象：{e(m["audience"])}</p>' if m.get("audience") else ""
        )
        cta = e(m.get("cta", "このメニューについて相談する"))
        cards += f"""
      <article class="menu-card" data-targets="{e(targets)}" data-target="{e(primary)}">
        <p class="no">MENU {e(m.get('code',''))}</p>
        <div class="chips">{tags}</div>
        <h3>{e(m['title'])}</h3>
        <p class="summary">{e(m.get('summary',''))}</p>
        <p class="no">こんな課題に</p>
        <ul class="for">{for_whom}</ul>
        {flag}
        <details><summary>実施内容を見る</summary><ul>{scope}</ul></details>
        <details><summary>成果物を見る</summary><ul>{deliv}</ul></details>
        <dl class="menu-meta">
          <div><dt>PERIOD</dt><dd>{e(m.get('period',''))}</dd></div>
          <div><dt>PRICE</dt><dd>{e(m.get('price',''))}</dd></div>
        </dl>
        {note}{audience}
        <a class="btn sm" href="#contact">{cta}</a>
      </article>"""

    un = sm.get("undecided", {})
    undecided = ""
    if un:
        items = "".join(f"<li>{e(x)}</li>" for x in un.get("items", []))
        undecided = f"""
    <div class="highlight-box" style="margin-top:28px">
      <h3>{e(un.get('title',''))}</h3>
      <p>{e(un.get('body',''))}</p>
      <ol style="font-size:14px;color:var(--ink-soft)">{items}</ol>
      <a class="btn sm" href="#contact">{e(un.get('cta',''))}</a>
    </div>"""

    topics = "".join(f"<li>{e(t)}</li>" for t in d.get("training_topics", []))
    topics_block = (
        f'<details style="margin-top:20px"><summary style="font-size:13px;color:var(--accent);'
        f'cursor:pointer">講演・研修の演題例を見る</summary>'
        f'<ul style="font-size:14px;color:var(--ink-soft)">{topics}</ul></details>'
        if topics else ""
    )

    return f"""
  <section id="menu">
    <h2>{e(sm.get('title', ''))}</h2>
    <p class="lead">{e(sm.get('intro', ''))}</p>
    <div class="filterbar" id="menu-filter">{filters}</div>
    <div class="menu-grid" id="menu-grid">{cards}</div>
    <p class="menu-empty" hidden>該当するメニューはありません。個別に設計しますので、そのままご相談ください。</p>
    <p class="cta-note" style="margin-top:18px">{e(sm.get('price_note', ''))}</p>
    {topics_block}
    {undecided}
  </section>"""


def build_order_flow_html(d):
    e = html.escape
    of = d.get("order_flow", {})
    if not of:
        return ""
    steps = "".join(
        f'<li><span class="num">STEP {i}</span><h3>{e(s["label"])}</h3><p>{e(s["body"])}</p></li>'
        for i, s in enumerate(of.get("steps", []), 1)
    )
    note = f'<p class="closing">{e(of["note"])}</p>' if of.get("note") else ""
    return f"""
  <section id="flow">
    <h2>{e(of.get('title', '発注までの流れ'))}</h2>
    <ol class="steps">{steps}</ol>
    {note}
  </section>"""


def build_conditions_html(d):
    e = html.escape
    oc = d.get("order_conditions", {})
    if not oc:
        return ""
    rows = "".join(
        f'<tr><th scope="row">{e(r["item"])}</th><td>{e(r["value"])}</td></tr>'
        for r in oc.get("rows", [])
    )
    return f"""
  <section id="conditions">
    <h2>{e(oc.get('title', '発注条件早見表'))}</h2>
    <p class="lead">{e(oc.get('intro', ''))}</p>
    <table class="conditions"><tbody>{rows}</tbody></table>
  </section>"""


def build_why_html(d):
    e = html.escape
    w = d.get("why_reasons", {})
    if not w:
        return ""
    items = "".join(
        f'<div class="reason"><span class="num">{e(x.get("code",""))}</span>'
        f'<h3>{e(x["title"])}</h3><p>{e(x["body"])}</p></div>'
        for x in w.get("items", [])
    )
    return f"""
  <section id="why">
    <h2>{e(w.get('title', ''))}</h2>
    <div class="reasons">{items}</div>
  </section>"""


def build_support_orgs_html(d):
    e = html.escape
    s = d.get("support_orgs", {})
    if not s:
        return ""
    items = "".join(f"<li>{e(x)}</li>" for x in s.get("items", []))
    hi = f'<p class="flag" style="font-size:14px">{e(s["highlight"])}</p>' if s.get("highlight") else ""
    return f"""
  <section id="support-orgs" data-target="support">
    <h2>{e(s.get('title', ''))}</h2>
    <p>{e(s.get('body', ''))}</p>
    <ul class="taglist">{items}</ul>
    {hi}
    <a class="btn sm" href="#menu" data-menu-filter="support">支援機関向けメニューを見る</a>
  </section>"""


# テーマタグは案件名と対応サービス名だけを見る。本文まで拾うと大半の事例に
# 「計画」「支援」が含まれ、タグが機能しなくなるため。
PORTFOLIO_TAG_RULES = [
    ("スマートシティ", ("スマートシティ",)),
    ("AI・DX", ("AI", "DX", "デジタル", "オープンデータ", "システム", "ICT", "シビックテック", "データ")),
    ("研修", ("研修", "講義", "講演", "ワークショップ", "アイデアソン", "セッション")),
    ("経営企画", ("経営改善", "経営診断", "事業構想", "グループ経営", "ガバナンス", "会議体",
                  "ポリシー", "事業承継", "経営計画", "数値計画", "コーポレート")),
    ("地域づくり", ("地域", "まち", "商店街", "自治会", "市民", "住民", "復興", "コミュニティ")),
]

SUPPORT_ORG_WORDS = ("商工会", "金融機関", "保証協会", "よろず", "支援機関", "組合", "中央会", "専門家派遣")

PORTFOLIO_CATEGORY_TAGS = {
    "国・政策": ["自治体・行政"],
    "自治体": ["自治体・行政"],
    "大企業": ["大企業"],
    "大企業・自治体": ["大企業", "自治体・行政"],
    "中小企業": ["中小企業"],
    "NPO・地域活動": ["地域づくり"],
    "研修・講演": ["研修"],
}

MAX_CASE_TAGS = 3


def case_tags(c):
    """明示指定がなければ、分類と案件名からフィルタ用タグを組み立てる。"""
    if c.get("tags"):
        return list(c["tags"])
    tags = list(PORTFOLIO_CATEGORY_TAGS.get(c.get("category", ""), []))
    if any(w in f'{c.get("client", "")} {c.get("role", "")}' for w in SUPPORT_ORG_WORDS):
        tags.append("支援機関")
    theme = f'{c.get("title", "")} {c.get("related_service", "")}'
    for tag, words in PORTFOLIO_TAG_RULES:
        if len(tags) >= MAX_CASE_TAGS:
            break
        if tag not in tags and any(w in theme for w in words):
            tags.append(tag)
    return tags


def build_case_cards_html(portfolio, only_featured=False, limit=None):
    e = html.escape
    cases = portfolio.get("cases", [])
    if only_featured:
        picked = [c for c in cases if c.get("featured")]
        cases = picked or cases
    if limit:
        cases = cases[:limit]
    out = ""
    for c in cases:
        tags = case_tags(c)
        chips = "".join(f'<span class="chip" style="--c:#3F7A6E">{e(t)}</span>' for t in tags)
        rows = f'<dt>依頼者</dt><dd>{e(c.get("client",""))}</dd>'
        if c.get("issue"):
            rows += f'<dt>課題</dt><dd>{e(c["issue"])}</dd>'
        role = e(c.get("role", ""))
        rows += f'<dt>担当</dt><dd>{role}／{e(c.get("scope",""))}</dd>'
        if c.get("deliverables"):
            rows += f'<dt>成果物</dt><dd>{e(c["deliverables"])}</dd>'
        if c.get("result"):
            rows += f'<dt>実施成果</dt><dd>{e(c["result"])}</dd>'
        if c.get("outcome_after"):
            rows += f'<dt>その後</dt><dd>{e(c["outcome_after"])}</dd>'
        if c.get("period"):
            rows += f'<dt>期間</dt><dd>{e(c["period"])}</dd>'
        links = "".join(
            f'<li><a href="{e(l["url"])}">{e(l["label"])}</a></li>'
            for l in c.get("public_links", [])
        )
        links_block = f"<ul>{links}</ul>" if links else ""
        out += f"""
      <article class="case-card" data-tags="{e('|'.join(tags))}">
        <div class="chips">{chips}</div>
        <h3>{e(c['title'])}</h3>
        <dl>{rows}</dl>
        {links_block}
      </article>"""
    return out


FILTER_JS = """
(function () {
  function bind(barId, gridId, attr) {
    var bar = document.getElementById(barId);
    var grid = document.getElementById(gridId);
    if (!bar || !grid) return;
    var buttons = bar.querySelectorAll("button");
    function apply(key) {
      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", String(b.dataset.filter === key));
      });
      var shown = 0;
      grid.querySelectorAll("[" + attr + "]").forEach(function (card) {
        var hit = key === "all" ||
          card.getAttribute(attr).split(/[|\\s]+/).indexOf(key) !== -1;
        card.classList.toggle("is-hidden", !hit);
        if (hit) shown++;
      });
      var empty = grid.parentNode.querySelector(".menu-empty");
      if (empty) empty.hidden = shown > 0;
    }
    bar.addEventListener("click", function (ev) {
      var b = ev.target.closest("button");
      if (b) apply(b.dataset.filter);
    });
    bar.dataset.apply = "1";
    grid.filterApply = apply;
    var q = new URLSearchParams(location.search).get(barId === "menu-filter" ? "target" : "tag");
    var hash = (location.hash.split("?")[1] || "");
    var hq = new URLSearchParams(hash).get("target");
    if (q || hq) apply(q || hq);
  }
  bind("menu-filter", "menu-grid", "data-targets");
  bind("case-filter", "case-grid", "data-tags");

  document.querySelectorAll("[data-menu-filter]").forEach(function (a) {
    a.addEventListener("click", function (ev) {
      ev.preventDefault();
      var grid = document.getElementById("menu-grid");
      if (grid && grid.filterApply) grid.filterApply(a.dataset.menuFilter);
      var target = document.getElementById("menu");
      if (target) target.scrollIntoView({ behavior: "smooth" });
    });
  });
})();
"""


def build_html(d, portfolio):
    b = d["basic"]
    e = html.escape
    meta = d.get("meta", {})
    fe = d.get("free_entry", {})
    free_items = "".join(
        f'<div class="highlight-box"><h3>'
        f'{"<a href=\"" + e(it["url"]) + "\">" + e(it["title"]) + "</a>" if it.get("url") else e(it["title"])}'
        f'</h3><p>{e(it["body"])}</p></div>'
        for it in fe.get("items", [])
    )

    pubs = "<ul class='plainlist pub-list'>" + "".join(
        f'<li><a href="{e(p["url"])}">{e(p["title"])}</a>'
        f'{" — " + e(p["note"]) if p.get("note") else ""}</li>'
        for p in d.get("publications", [])
    ) + "</ul>"

    notes = "<ul class='plainlist pub-list'>" + "".join(
        f'<li><a href="{e(n["url"])}">{e(n["title"])}</a>'
        f'{" — " + e(n["theme"]) if n.get("theme") else ""}</li>'
        for n in d.get("featured_notes", [])
    ) + "</ul>"

    media_block = build_media_html(d.get("media_coverage", {}))
    writings_block = build_writings_html(d.get("writings", {}))

    affil = "".join(
        f'<li><span class="when">{e(x["since"])}</span><span>{e(x["name"])}</span></li>'
        for x in d.get("affiliations", [])
    )

    creds = ""
    for g in d.get("credentials", []):
        items = "".join(cred_item_html(i, e) for i in g["items"])
        creds += f'<div class="credgroup"><h3>{e(g["group"])}</h3><ul>{items}</ul></div>'

    fields = "".join(f"<li>{e(x)}</li>" for x in d.get("fields", []))

    contacts = ""
    for c in public_contacts(d):
        v = (
            f'<a href="{e(c["value"])}">{e(c["value"])}</a>'
            if c.get("link") else e(c["value"])
        )
        contacts += f'<div class="row"><dt>{e(c["label"])}</dt><dd>{v}</dd></div>'

    npo = d.get("npo_offering", {})
    eng = d.get("engagement", {})

    endn = d.get("endnotes", {})
    endnote_items = "".join(
        f'<p><strong>{e(n["label"])}：</strong>{e(n["body"])}</p>'
        for n in endn.get("items", [])
    )

    seo = d.get("seo", {})
    title = seo.get("title") or f"{b['name_ja']}｜{b['organization']}"
    desc = seo.get("description") or d["tagline"]
    site_url = f"https://{meta.get('github_user','')}.github.io/{meta.get('repo_name','profile')}/"
    og_image = seo.get("og_image") or b.get("photo", "")
    og_image_url = og_image if og_image.startswith("http") else site_url + og_image

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(site_url)}">
{f'<meta property="og:image" content="{e(og_image_url)}">' if og_image else ''}
<meta name="twitter:card" content="summary_large_image">
<style>{shared_css()}</style>
</head>
<body>
<div class="wrap">
  <nav class="topnav">
    <a href="#menu">サンプルメニュー</a>
    <a href="#flow">発注までの流れ</a>
    <a href="portfolio.html">実績・ポートフォリオ</a>
    <a href="#profile">プロフィール</a>
    <a href="#contact">お仕事のご相談</a>
  </nav>

  {build_hero_html(d)}

  <section id="targets">
    <h2>どのお立場の方ですか？</h2>
    <div class="audience-grid">{build_targets_html(d)}</div>
  </section>

  {build_problems_html(d)}

  {build_menu_html(d)}

  <section id="free-entry">
    <h2>{e(fe.get('headline', '無料相談の入り口'))}</h2>
    <p class="lead">{e(fe.get('intro', ''))}</p>
    {free_items}
    <h3 style="margin-top:28px">{e(npo.get('title', 'NPO・地域活動向け'))}</h3>
    <p style="font-size:14px;color:var(--ink-soft)">{e(npo.get('body', '').strip())}</p>
  </section>

  {build_order_flow_html(d)}

  {build_conditions_html(d)}

  {build_why_html(d)}

  <section id="cases">
    <h2>代表的な実績</h2>
    <p class="lead">ご発注の参考になる事例を抜粋しています。守秘義務のある案件は、依頼者・地域を特定できない形に整理しています。</p>
    <div class="case-grid">{build_case_cards_html(portfolio, only_featured=True, limit=10)}</div>
    <p style="margin-top:22px"><a href="portfolio.html">全実績を見る →</a></p>
  </section>

  {build_support_orgs_html(d)}

  <section id="profile">
    <h2>プロフィール・経歴</h2>
    <p class="lead">{e(d['intros']['medium'].strip())}</p>
    <ul class="timeline" style="margin-top:28px">{build_career_html(d)}</ul>
    <h3 style="margin-top:12px">支援領域と経験</h3>
    <div class="cards" style="margin-top:14px">{build_offerings_html(d)}</div>
  </section>

  <section id="credentials">
    <h2>資格・所属</h2>
    <div class="creds">{creds}</div>
    <h3 style="margin-top:28px">現在の所属</h3>
    <ul class="plainlist">{affil}</ul>
    <h3 style="margin-top:28px">主な活動分野</h3>
    <ul class="plainlist">{fields}</ul>
  </section>

  <section id="media">
    <h2>メディア・執筆</h2>
    <h3>代表的な記事（note）</h3>
    {notes}
    {media_block}
    {writings_block}
    <h3 style="margin-top:28px">公開成果物</h3>
    {pubs}
  </section>

  <section id="contact">
    <h2>お仕事のご相談</h2>
    <p class="lead">初回は30分程度のオンライン面談から承ります。相談したら必ず契約しなければならない、ということはありません。</p>
    {build_contact_form(d)}
    <h3 style="margin-top:36px">連絡先</h3>
    <dl class="contact">{contacts}</dl>
  </section>

  <section class="endnotes">
    <h2>{e(endn.get('title', '補足事項（参考情報）'))}</h2>
    {endnote_items}
    <p>{e(eng.get('fees', '').strip())}</p>
  </section>

  <footer>LAST UPDATED {e(str(meta.get('updated')))} ｜
    <a href="https://github.com/{e(meta.get('github_user',''))}/{e(meta.get('repo_name','profile'))}">Source</a>
  </footer>
</div>
<a class="btn sticky-cta" href="#contact">仕事について相談する</a>
<script>{FILTER_JS}</script>
</body>
</html>"""


PORTFOLIO_FILTERS = [
    "すべて", "自治体・行政", "大企業", "中小企業", "支援機関",
    "AI・DX", "スマートシティ", "研修", "地域づくり", "経営企画",
]


def build_portfolio_html(portfolio, profile):
    e = html.escape
    meta = portfolio.get("meta", {})
    pm = profile.get("meta", {})
    b = profile.get("basic", {})
    cases = portfolio.get("cases", [])
    used = {t for c in cases for t in case_tags(c)}
    counts = {t: sum(1 for c in cases if t in case_tags(c)) for t in used}
    filters = ""
    for label in PORTFOLIO_FILTERS:
        if label != "すべて" and label not in used:
            continue
        key = "all" if label == "すべて" else label
        n = len(cases) if label == "すべて" else counts[label]
        filters += (
            f'<button type="button" data-filter="{e(key)}" '
            f'aria-pressed="{"true" if key == "all" else "false"}">{e(label)}'
            f'<span style="opacity:.6"> {n}</span></button>'
        )

    title = f"実績・ポートフォリオ｜{b.get('name_ja', '土屋俊博')}"
    desc = "自治体・大企業・中小企業・支援機関向けに実施した支援事例を、依頼者を特定できない形に整理して掲載しています。"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="article">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<style>{shared_css()}</style>
</head>
<body>
<div class="wrap">
  <nav class="topnav">
    <a href="index.html">← プロフィールに戻る</a>
    <a href="index.html#menu">サンプルメニュー</a>
    <a href="#contact">お仕事のご相談</a>
  </nav>
  <header class="hero">
    <p class="eyebrow">Portfolio</p>
    <h1 style="font-size:clamp(30px,6vw,44px)">実績・ポートフォリオ</h1>
    <p class="sub">{e(meta.get('intro','').strip())}</p>
    <div class="cta-row">
      <a class="btn ghost" href="index.html#menu">相談できるメニューを見る</a>
    </div>
  </header>
  <section id="cases">
    <div class="filterbar" id="case-filter">{filters}</div>
    <div class="case-grid" id="case-grid">{build_case_cards_html(portfolio)}</div>
  </section>
  <section id="contact">
    <h2>お仕事のご相談</h2>
    <p class="lead">事例の詳細や、類似案件のご相談を承ります。まだ依頼内容が決まっていない段階でも構いません。</p>
    {build_contact_form(profile, prefix="pf-")}
  </section>
  <footer>LAST UPDATED {e(str(meta.get('updated', pm.get('updated'))))}</footer>
</div>
<a class="btn sticky-cta" href="#contact">仕事について相談する</a>
<script>{FILTER_JS}</script>
</body>
</html>"""


def build_readme(d, portfolio):
    b = d["basic"]
    meta = d["meta"]
    o = []
    a = o.append

    a(f"# {b['name_ja']}（{b['name_kana']} / {b['name_en']}）")
    a("")
    a(f"> {d['tagline']}")
    a("")
    a(f"**{b['organization']}**　{b['title']}")
    a(f"{b['organization_note']}")
    a("")
    a(f"📄 **公開ページ:** https://{meta.get('github_user')}.github.io/{meta.get('repo_name')}/")
    a(f"📁 **ポートフォリオ:** https://{meta.get('github_user')}.github.io/{meta.get('repo_name')}/portfolio.html")
    a("")
    a("---")
    a("")
    a("## どのお立場の方ですか？")
    a("")
    for g in d.get("audience_guides", []):
        a(f"- **{g['label']}** — {g['summary']}")
    a("")
    sm = d.get("service_menu", {})
    if sm.get("items"):
        a(f"## {sm.get('title', 'サンプルメニュー')}")
        a("")
        a(sm.get("intro", ""))
        a("")
        a("| # | メニュー | 主な対象 | 標準期間 | 費用目安 |")
        a("|---|---|---|---|---|")
        for m in sm["items"]:
            tags = "／".join(m.get("tags", []))
            a(
                f"| {m.get('code','')} | {m['title']} | {tags} | "
                f"{m.get('period','')} | {m.get('price','')} |"
            )
        a("")
        a(sm.get("price_note", ""))
        a("")
    of = d.get("order_flow", {})
    if of.get("steps"):
        a(f"## {of.get('title', '発注までの流れ')}")
        a("")
        for i, s in enumerate(of["steps"], 1):
            a(f"{i}. **{s['label']}** — {s['body']}")
        a("")
        if of.get("note"):
            a(of["note"])
            a("")
    oc = d.get("order_conditions", {})
    if oc.get("rows"):
        a(f"## {oc.get('title', '発注条件早見表')}")
        a("")
        a("| 項目 | 対応 |")
        a("|---|---|")
        for r in oc["rows"]:
            a(f"| {r['item']} | {r['value']} |")
        a("")
    fe = d.get("free_entry", {})
    a(f"## {fe.get('headline', '')}")
    a("")
    a(fe.get("intro", ""))
    a("")
    for it in fe.get("items", []):
        if it.get("url"):
            a(f"- [{it['title']}]({it['url']}) — {it['body']}")
        else:
            a(f"- **{it['title']}** — {it['body']}")
    a("")
    mc = d.get("media_coverage", {})
    if mc.get("items"):
        a("## メディア掲載・取材")
        a("")
        a(mc.get("intro", ""))
        a("")
        for it in mc["items"]:
            line = f"- {it.get('date', '—')} / {it.get('media', '')}"
            if it.get("url"):
                line += f" — [{it['title']}]({it['url']})"
            else:
                line += f" — {it['title']}"
            if it.get("note"):
                line += f" — {it['note']}"
            a(line)
        a("")
    wr = d.get("writings", {})
    if wr.get("items") or wr.get("author_pages"):
        a("## 執筆・コラム")
        a("")
        a(wr.get("intro", ""))
        a("")
        for p in wr.get("author_pages", []):
            a(f"- [{p['label']}]({p['url']})")
        if wr.get("author_pages") and wr.get("items"):
            a("")
        for it in wr.get("items", []):
            line = f"- {it.get('date', '—')} / {it.get('publication', '')}"
            if it.get("url"):
                line += f" — [{it['title']}]({it['url']})"
            else:
                line += f" — {it['title']}"
            if it.get("note"):
                line += f" — {it['note']}"
            a(line)
        a("")
    a("## お任せいただけること")
    a("")
    for x in d.get("offerings", []):
        a(f"### {x['title']}")
        a("")
        a(x["body"].strip())
        if x.get("proof"):
            a("")
            a(f"　経験：{x['proof']}")
        a("")
    a("## 経歴")
    a("")
    for c in d.get("career", []):
        head = f"**{c['period']}**　{c['title']}" if c.get("period") else f"**{c['title']}**"
        a(f"- {head}")
        if c.get("detail"):
            a(f"  　{c['detail']}")
    a("")
    a("## 連絡先")
    a("")
    for c in public_contacts(d):
        v = f"<{c['value']}>" if c.get("link") else c["value"]
        a(f"- **{c['label']}**　{v}")
    a("")
    endn = d.get("endnotes", {})
    if endn.get("items"):
        a(f"## {endn.get('title', '補足事項（参考情報）')}")
        a("")
        for n in endn["items"]:
            a(f"- {n['label']}：{n['body']}")
        a("")
    a(f"最終更新：{meta.get('updated')}")
    return "\n".join(o) + "\n"


def build_full_md(d):
    b = d["basic"]
    o = [f"# {b['name_ja']}　プロフィール（詳細版）", "", d["intros"]["long"].strip(), ""]
    for c in public_contacts(d):
        o.append(f"- {c['label']}：{c['value']}")
    return "\n".join(o) + "\n"


def main():
    print("profile.yaml を読み込みます…")
    d = load_profile()
    portfolio = load_portfolio()

    write("README.md", build_readme(d, portfolio))
    write("docs/index.html", build_html(d, portfolio))
    write("docs/portfolio.html", build_portfolio_html(portfolio, d))
    write("out/profile-full.md", build_full_md(d))
    for k, name in (("short", "intro-short"), ("medium", "intro-medium"), ("long", "intro-long")):
        write(f"out/{name}.txt", d["intros"][k].strip() + "\n")

    pub = dict(d)
    pub["contacts"] = public_contacts(d)
    pub.pop("contact_form", None)
    write("out/profile.json", json.dumps(pub, ensure_ascii=False, indent=2) + "\n")

    print("\n完了しました。")


if __name__ == "__main__":
    main()
