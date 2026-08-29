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
.lang-divider { margin: 64px 0 32px; padding-top: 48px; border-top: 3px double var(--rule);
  text-align: center; font-family: var(--mono); font-size: 12px; letter-spacing: .2em;
  color: var(--ink-soft); }
footer { padding: 40px 0 0; font-family: var(--mono); font-size: 11.5px; color: var(--ink-soft); }
@media (max-width: 640px) {
  .timeline > li { grid-template-columns: 1fr; }
  .row { grid-template-columns: 1fr; }
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


def build_contact_form(d):
    e = html.escape
    cf = d.get("contact_form", {})
    action = e(cf.get("action", ""))
    if not action:
        return ""
    return f"""
    <form class="form-grid" action="{action}" method="POST">
      <input type="hidden" name="_subject" value="プロフィールサイトからのお仕事のご相談">
      <input type="hidden" name="_captcha" value="false">
      <input type="text" name="_honey" style="display:none">
      <div><label for="name">お名前 *</label><input id="name" name="name" required></div>
      <div><label for="org">ご所属</label><input id="org" name="organization"></div>
      <div><label for="email">メールアドレス *</label><input id="email" name="email" type="email" required></div>
      <div><label for="type">ご相談の種類</label>
        <select id="type" name="inquiry_type">
          <option>自治体・行政</option><option>中小企業</option><option>大企業</option>
          <option>NPO・地域活動</option><option>研修・講演</option><option>その他</option>
        </select></div>
      <div><label for="message">ご相談内容 *</label>
        <textarea id="message" name="message" required placeholder="課題・希望時期・予算感など"></textarea></div>
      <button class="btn" type="submit">送信する</button>
    </form>"""


def build_html(d, portfolio):
    b = d["basic"]
    e = html.escape
    meta = d.get("meta", {})
    photo = (
        f'<img class="portrait" src="{e(b["photo"])}" alt="{e(b["name_ja"])}" '
        f'style="width:108px;height:108px;object-fit:cover;border-radius:2px;margin-bottom:20px">'
        if b.get("photo") else ""
    )

    audience = "".join(
        f'<div class="audience-card" id="{e(g.get("id",""))}">'
        f'<strong>{e(g["label"])}</strong><p>{e(g["summary"])}</p></div>'
        for g in d.get("audience_guides", [])
    )

    fe = d.get("free_entry", {})
    free_items = "".join(
        f'<div class="highlight-box"><h3>{e(it["title"])}</h3><p>{e(it["body"])}</p></div>'
        for it in fe.get("items", [])
    )

    pubs = "<ul class='plainlist pub-list'>" + "".join(
        f'<li><a href="{e(p["url"])}">{e(p["title"])}</a>'
        f'{" — " + e(p["note"]) if p.get("note") else ""}</li>'
        for p in d.get("publications", [])
    ) + "</ul>"

    cases_preview = ""
    for c in (portfolio.get("cases") or [])[:3]:
        cases_preview += (
            f'<p class="case-mini"><strong>{e(c["title"])}</strong> — '
            f'{e(c.get("client",""))}／{e(c.get("period",""))}。{e(c.get("result","")[:80])}…</p>'
        )

    affil = "".join(
        f'<li><span class="when">{e(x["since"])}</span><span>{e(x["name"])}</span></li>'
        for x in d.get("affiliations", [])
    )

    creds = ""
    for g in d.get("credentials", []):
        items = "".join(f"<li>{e(i)}</li>" for i in g["items"])
        creds += f'<div class="credgroup"><h3>{e(g["group"])}</h3><ul>{items}</ul></div>'

    fields = "".join(f"<li>{e(x)}</li>" for x in d.get("fields", []))
    training = "".join(f"<li>{e(t)}</li>" for t in d.get("training_topics", []))

    contacts = ""
    for c in public_contacts(d):
        v = (
            f'<a href="{e(c["value"])}">{e(c["value"])}</a>'
            if c.get("link") else e(c["value"])
        )
        contacts += f'<div class="row"><dt>{e(c["label"])}</dt><dd>{v}</dd></div>'

    npo = d.get("npo_offering", {})
    eng = d.get("engagement", {})
    pol = d.get("policies", {})
    ord_ent = d.get("ordering_entities", [])

    en = d.get("en", {})
    en_audience = "".join(
        f'<div class="audience-card"><strong>{e(g["label"])}</strong>'
        f'<p>{e(g["summary"])}</p></div>'
        for g in en.get("audience_guides", [])
    )

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(b['name_ja'])}｜{e(b['organization'])}</title>
<meta name="description" content="{e(d['tagline'])}">
<style>{shared_css()}</style>
</head>
<body>
<div class="wrap">
  <nav class="topnav">
    <a href="#services">サービス</a>
    <a href="portfolio.html">実績・ポートフォリオ</a>
    <a href="#contact">お仕事のご相談</a>
    <a href="#english">English</a>
  </nav>

  <header>
    <p class="eyebrow">Profile</p>
    {photo}
    <h1>{e(b['name_ja'])}</h1>
    <p class="kana">{e(b['name_kana'])} / {e(b['name_en'])}</p>
    <p class="tagline">{e(d['tagline'])}</p>
    <p class="affil-line">
      <strong>{e(b['organization'])}</strong>　{e(b['title'])}<br>
      {e(b['organization_note'])}<br>
      {e(b['hometown'])}／{e(b['base'])}
    </p>
    {f'<p class="avail">{e(meta.get("availability",""))}</p>' if meta.get("availability") else ''}
  </header>

  <section>
    <h2>どのお立場の方ですか？</h2>
    <div class="audience-grid">{audience}</div>
  </section>

  <section id="free-entry">
    <h2>{e(fe.get('headline', '無料相談の入り口'))}</h2>
    <p class="lead">{e(fe.get('intro', ''))}</p>
    {free_items}
  </section>

  <section>
    <h2>実績・公開成果物</h2>
    <p class="lead">匿名化した事例の詳細は<a href="portfolio.html">ポートフォリオページ</a>に掲載しています。</p>
    {cases_preview}
    <h3 style="margin-top:28px">公開成果物</h3>
    {pubs}
  </section>

  <section id="services">
    <h2>お任せいただけること</h2>
    <div class="cards">{build_offerings_html(d)}</div>
  </section>

  <section id="npo-menu">
    <h2>{e(npo.get('title', 'NPO・地域活動向け'))}</h2>
    <p>{e(npo.get('body', '').strip())}</p>
  </section>

  <section id="training">
    <h2>講演・研修の演題例</h2>
    <ul class="plainlist">{training}</ul>
  </section>

  <section>
    <h2>経歴</h2>
    <ul class="timeline">{build_career_html(d)}</ul>
  </section>

  <section>
    <h2>現在の所属</h2>
    <ul class="plainlist">{affil}</ul>
  </section>

  <section>
    <h2>資格・委嘱</h2>
    <div class="creds">{creds}</div>
  </section>

  <section>
    <h2>主な活動分野</h2>
    <ul class="plainlist">{fields}</ul>
  </section>

  <section>
    <h2>ご依頼の流れ・費用</h2>
    <ol>{''.join(f'<li>{e(s)}</li>' for s in eng.get('steps', []))}</ol>
    <p class="lead" style="margin-top:16px">{e(eng.get('fees', '').strip())}</p>
  </section>

  <section>
    <h2>方針</h2>
    <p><strong>中立性：</strong>{e(pol.get('neutrality', ''))}</p>
    <p><strong>守秘：</strong>{e(pol.get('confidentiality', ''))}</p>
    <p><strong>リモート：</strong>{e(pol.get('remote', ''))}</p>
  </section>

  <section>
    <h2>発注先の別</h2>
    <ul class="plainlist">{''.join(
        f'<li><strong>{e(o["entity"])}</strong> — {e(o["use_for"])}</li>'
        for o in ord_ent
    )}</ul>
    <p class="lead">{e(d.get("invoice_note", ""))}</p>
  </section>

  <section id="contact">
    <h2>連絡先・お仕事のご相談</h2>
    <dl class="contact">{contacts}</dl>
    <h3 style="margin-top:32px">お問い合わせフォーム</h3>
    <p class="lead">初回のご相談は30分程度のオンライン面談から承ります。</p>
    {build_contact_form(d)}
  </section>

  <div class="lang-divider" id="english">ENGLISH PROFILE</div>

  <header style="padding-top:24px;border:0">
    <h1 style="font-size:clamp(28px,5vw,42px)">{e(b['name_en'])}</h1>
    <p class="tagline">{e(en.get('tagline', ''))}</p>
    <p class="affil-line">{e(b['organization'])} — {e(b['title'])}</p>
  </header>

  <section>
    <h2>For whom</h2>
    <div class="audience-grid">{en_audience}</div>
  </section>

  <section>
    <h2>{e(en.get('section_titles', {}).get('offerings', 'Services'))}</h2>
    <p class="lead">{e(en.get('offerings_note', ''))}</p>
    <div class="cards">{build_offerings_html(d, 'Experience')}</div>
  </section>

  <section>
    <h2>{e(en.get('section_titles', {}).get('career', 'Career'))}</h2>
    <ul class="timeline">{build_career_html(d)}</ul>
  </section>

  <section>
    <h2>{e(en.get('section_titles', {}).get('contact', 'Contact'))}</h2>
    <dl class="contact">{contacts}</dl>
    {build_contact_form(d)}
  </section>

  <footer>LAST UPDATED {e(str(meta.get('updated')))} ｜
    <a href="https://github.com/{e(meta.get('github_user',''))}/{e(meta.get('repo_name','profile'))}">Source</a>
  </footer>
</div>
</body>
</html>"""


def build_portfolio_html(portfolio, profile):
    e = html.escape
    meta = portfolio.get("meta", {})
    pm = profile.get("meta", {})
    cases_html = ""
    for c in portfolio.get("cases", []):
        links = ""
        for lnk in c.get("public_links", []):
            links += f'<li><a href="{e(lnk["url"])}">{e(lnk["label"])}</a></li>'
        links_block = f"<ul>{links}</ul>" if links else ""
        cases_html += f"""
        <article class="card">
          <div class="chips"><span class="chip" style="--c:#3F7A6E">{e(c.get('category',''))}</span></div>
          <h3>{e(c['title'])}</h3>
          <p><strong>クライアント：</strong>{e(c.get('client',''))}</p>
          <p><strong>関与：</strong>{e(c.get('role',''))}（{e(c.get('period',''))}）</p>
          <p><strong>内容：</strong>{e(c.get('scope',''))}</p>
          <p><strong>成果：</strong>{e(c.get('result',''))}</p>
          {links_block}
        </article>"""

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>実績・ポートフォリオ｜土屋俊博</title>
<style>{shared_css()}</style>
</head>
<body>
<div class="wrap">
  <nav class="topnav"><a href="index.html">← プロフィールに戻る</a></nav>
  <header>
    <p class="eyebrow">Portfolio</p>
    <h1>実績・ポートフォリオ</h1>
    <p class="lead">{e(meta.get('intro','').strip())}</p>
  </header>
  <section>
    <div class="cards">{cases_html}</div>
  </section>
  <section id="contact">
    <h2>お仕事のご相談</h2>
    <p class="lead">事例の詳細や類似案件のご相談は、<a href="index.html#contact">プロフィールページのフォーム</a>からお送りください。</p>
    {build_contact_form(profile)}
  </section>
  <footer>LAST UPDATED {e(str(meta.get('updated', pm.get('updated'))))}</footer>
</div>
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
    fe = d.get("free_entry", {})
    a(f"## {fe.get('headline', '')}")
    a("")
    a(fe.get("intro", ""))
    a("")
    for it in fe.get("items", []):
        a(f"- **{it['title']}** — {it['body']}")
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
    write("out/profile.json", json.dumps(pub, ensure_ascii=False, indent=2) + "\n")

    print("\n完了しました。")


if __name__ == "__main__":
    main()
