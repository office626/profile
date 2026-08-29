#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
profile.yaml から公開用ファイルをすべて生成する。

  $ python3 scripts/build.py

生成物:
  README.md            GitHubトップに表示されるプロフィール本体
  docs/index.html      GitHub Pages 用の1枚ページ（クライアントに見せる用）
  out/profile-full.md  詳細版（コピペ配布用）
  out/intro-short.txt  紹介文（短）
  out/intro-medium.txt 紹介文（中）
  out/intro-long.txt   紹介文（長）
  out/profile.json     機械可読版

注意:
  profile.yaml で public: false を付けた連絡先は、いっさい出力されない。
"""

import json
import os
import sys
import datetime
import html

try:
    import yaml
except ImportError:
    sys.exit(
        "PyYAML が必要です。次のコマンドでインストールしてください:\n"
        "    pip install pyyaml\n"
        "  （うまくいかない場合） pip3 install --user pyyaml"
    )

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "profile.yaml")


# --------------------------------------------------------------------------
# 読み込みとチェック
# --------------------------------------------------------------------------
def load():
    with open(SRC, encoding="utf-8") as f:
        d = yaml.safe_load(f)

    warn = []
    meta = d.get("meta", {})
    if meta.get("github_user") in (None, "", "CHANGE-ME"):
        warn.append("meta.github_user が未設定です（リンクが正しく生成されません）")
    today = datetime.date.today().isoformat()
    if str(meta.get("updated", "")) != today:
        warn.append(
            f"meta.updated が {meta.get('updated')} のままです（今日は {today}）。"
            "内容を変えたなら日付も更新してください。"
        )
    for w in warn:
        print("  ⚠  " + w)
    return d


def public_contacts(d):
    return [c for c in d.get("contacts", []) if c.get("public")]


def layer_labels(d, keys, lang="ja"):
    if lang == "ja":
        L = d.get("layers", {})
    else:
        L = d.get("en", {}).get("layers", {})
    return [L[k]["label"] for k in (keys or []) if k in L]


def localized(d, lang):
    """Return language-specific view used by generators."""
    b = d["basic"]
    if lang == "ja":
        return {
            "lang": "ja",
            "layers": d["layers"],
            "basic": b,
            "tagline": d["tagline"],
            "intros": d["intros"],
            "career": d.get("career", []),
            "affiliations": d.get("affiliations", []),
            "credentials": d.get("credentials", []),
            "fields": d.get("fields", []),
            "offerings": d.get("offerings", []),
            "ui": {
                "eyebrow": "Profile",
                "intro": "紹介文",
                "intro_note": "登壇者紹介や寄稿プロフィールにそのままお使いください",
                "offerings": "お任せいただけること",
                "offerings_legend": "それぞれの依頼が、どの立場の相手に効くかを示しています。",
                "proof": "根拠となる経験",
                "proof_prefix": "　根拠となる経験：",
                "career": "経歴",
                "affiliations": "現在の所属",
                "credentials": "資格・委嘱",
                "fields": "主な活動分野",
                "contact": "連絡先",
            },
        }
    e = d["en"]
    ja_offerings = d.get("offerings", [])
    en_offerings = []
    for i, item in enumerate(e.get("offerings", [])):
        layers = ja_offerings[i].get("layers", []) if i < len(ja_offerings) else []
        en_offerings.append({**item, "layers": layers})
    ja_career = d.get("career", [])
    en_career = []
    for i, item in enumerate(e.get("career", [])):
        layers = ja_career[i].get("layers", []) if i < len(ja_career) else []
        en_career.append({**item, "layers": layers})
    layers = {}
    for k, v in d.get("layers", {}).items():
        layers[k] = {**v, "label": e["layers"][k]["label"]}
    return {
        "lang": "en",
        "layers": layers,
        "basic": {**b, **e["basic"]},
        "tagline": e["tagline"],
        "intros": e["intros"],
        "career": en_career,
        "affiliations": e.get("affiliations", []),
        "credentials": e.get("credentials", []),
        "fields": e.get("fields", []),
        "offerings": en_offerings,
        "ui": {
            **e["ui"],
            "intro": "Introduction",
            "intro_note": "",
            "proof_prefix": "Relevant experience: ",
        },
    }


def localized_contacts(d, lang):
    if lang == "ja":
        return public_contacts(d)
    ui = d["en"]["ui"]
    contacts = []
    for c in public_contacts(d):
        if c["label"] == "オフィス":
            continue
        contacts.append(c)
    for office in ui.get("offices", []):
        contacts.append({
            "label": ui.get("office_label", "Office"),
            "value": office,
            "public": True,
            "link": False,
        })
    return contacts


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"  ✓  {path}")


# --------------------------------------------------------------------------
# README.md
# --------------------------------------------------------------------------
def build_readme_section(d, lang):
    loc = localized(d, lang)
    b = loc["basic"]
    ui = loc["ui"]
    o = []
    a = o.append

    if lang == "en":
        a("---")
        a("")
        a(f"# {b['name_en']}")
        a("")
    else:
        a(f"# {b['name_ja']}（{b['name_kana']} / {b['name_en']}）")
        a("")

    a(f"> {loc['tagline']}")
    a("")
    if lang == "ja" and b.get("photo"):
        a(f'<img src="{b["photo"]}" alt="{b["name_ja"]}" width="200">')
        a("")
    a(f"**{b['organization']}**　{b['title']}")
    a(f"{b['organization_note']}")
    a("")
    if lang == "ja":
        a(f"{b['hometown']}／{b['base']}")
    else:
        a(f"{b['hometown']} / {b['base']}")
    a("")
    if lang == "ja":
        a("---")
        a("")

    a(f"## {ui['intro']}")
    a("")
    if lang == "ja":
        a(f"<!-- {ui['intro_note']} -->")
        a("")
    a(loc["intros"]["medium"].strip())
    a("")
    if lang == "ja":
        a("より短い版・長い版は [`out/`](out/) にあります。")
        a("")

    a(f"## {ui['offerings']}")
    a("")
    for x in loc.get("offerings", []):
        tags = "　".join(f"`{t}`" for t in layer_labels(d, x.get("layers"), lang))
        a(f"### {x['title']}")
        if tags:
            a(tags)
        a("")
        a(x["body"].strip())
        if x.get("proof"):
            a("")
            a(f"{ui['proof_prefix']}{x['proof']}")
        a("")

    a(f"## {ui['career']}")
    a("")
    for c in loc.get("career", []):
        head = f"**{c['title']}**"
        if c.get("period"):
            head = f"**{c['period']}**　{c['title']}"
        a(f"- {head}")
        if c.get("org"):
            a(f"  　{c['org']}")
        if c.get("detail"):
            a(f"  　{c['detail']}")
    a("")

    a(f"## {ui['affiliations']}")
    a("")
    for x in loc.get("affiliations", []):
        a(f"- **{x['since']}**　{x['name']}")
    a("")

    a(f"## {ui['credentials']}")
    a("")
    for g in loc.get("credentials", []):
        a(f"### {g['group']}")
        a("")
        for i in g["items"]:
            a(f"- {i}")
        a("")

    a(f"## {ui['fields']}")
    a("")
    for x in loc.get("fields", []):
        a(f"- {x}")
    a("")

    a(f"## {ui['contact']}")
    a("")
    for c in localized_contacts(d, lang):
        v = f"<{c['value']}>" if c.get("link") else c["value"]
        a(f"- **{c['label']}**　{v}")
    a("")
    return o


def build_readme(d):
    meta = d["meta"]
    o = build_readme_section(d, "ja")
    o.extend(build_readme_section(d, "en"))
    o.append("---")
    o.append("")
    o.append(f"最終更新：{meta.get('updated')}　｜　"
               f"このページは [`profile.yaml`](profile.yaml) から自動生成しています。")
    return "\n".join(o) + "\n"


# --------------------------------------------------------------------------
# out/profile-full.md
# --------------------------------------------------------------------------
def build_full_md(d):
    b = d["basic"]
    o = []
    a = o.append
    a(f"# {b['name_ja']}　プロフィール（詳細版）")
    a("")
    a(f"{b['name_kana']}／{b['name_en']}")
    a("")
    a(f"{b['organization']}（{b['organization_note']}）　{b['title']}")
    a(f"{b['website']}")
    a("")
    a(f"{b['hometown']}。{b['base']}。")
    a("")
    a("## 経歴")
    a("")
    a(d["intros"]["long"].strip())
    a("")
    a("## 現在の所属")
    a("")
    for x in d.get("affiliations", []):
        a(f"- {x['since']}　{x['name']}")
    a("")
    for g in d.get("credentials", []):
        a(f"## {g['group']}")
        a("")
        for i in g["items"]:
            a(f"- {i}")
        a("")
    a("## 主な活動分野")
    a("")
    for x in d.get("fields", []):
        a(f"- {x}")
    a("")
    a("## 連絡先")
    a("")
    for c in public_contacts(d):
        a(f"- {c['label']}：{c['value']}")
    a("")
    return "\n".join(o) + "\n"


# --------------------------------------------------------------------------
# docs/index.html
# --------------------------------------------------------------------------
def build_html_lang_block(d, lang):
    loc = localized(d, lang)
    b = loc["basic"]
    L = loc["layers"]
    ui = loc["ui"]
    e = html.escape

    def chips(keys):
        out = []
        for k in keys or []:
            if k in L:
                out.append(
                    f'<span class="chip" style="--c:{L[k]["color"]}">{e(L[k]["label"])}</span>'
                )
        return "".join(out)

    legend = "".join(
        f'<span class="chip" style="--c:{v["color"]}">{e(v["label"])}</span>'
        for v in L.values()
    )

    offerings = ""
    for x in loc.get("offerings", []):
        proof = (
            f'<p class="proof"><span>{e(ui["proof"])}</span>{e(x["proof"])}</p>'
            if x.get("proof") else ""
        )
        offerings += f"""
      <article class="card">
        <div class="chips">{chips(x.get('layers'))}</div>
        <h3>{e(x['title'])}</h3>
        <p>{e(x['body'].strip())}</p>
        {proof}
      </article>"""

    career = ""
    for c in loc.get("career", []):
        career += f"""
      <li>
        <div class="when">{e(c.get('period') or '')}</div>
        <div class="what">
          <h3>{e(c['title'])}</h3>
          {f'<p class="org">{e(c["org"])}</p>' if c.get('org') else ''}
          {f'<p>{e(c["detail"])}</p>' if c.get('detail') else ''}
          <div class="chips">{chips(c.get('layers'))}</div>
        </div>
      </li>"""

    affil = "".join(
        f'<li><span class="when">{e(x["since"])}</span>'
        f'<span class="what">{e(x["name"])}</span></li>'
        for x in loc.get("affiliations", [])
    )

    creds = ""
    for g in loc.get("credentials", []):
        items = "".join(f"<li>{e(i)}</li>" for i in g["items"])
        creds += f'<div class="credgroup"><h3>{e(g["group"])}</h3><ul>{items}</ul></div>'

    fields = "".join(f"<li>{e(x)}</li>" for x in loc.get("fields", []))

    contacts = ""
    for c in localized_contacts(d, lang):
        v = (f'<a href="{e(c["value"])}">{e(c["value"])}</a>'
             if c.get("link") else e(c["value"]))
        contacts += f'<div class="row"><dt>{e(c["label"])}</dt><dd>{v}</dd></div>'

    if lang == "ja":
        hometown_base = f"{e(b['hometown'])}／{e(b['base'])}"
        header = f"""
  <header>
    <p class="eyebrow">{e(ui['eyebrow'])}</p>
    <h1>{e(b['name_ja'])}</h1>
    <p class="kana">{e(b['name_kana'])} &nbsp;/&nbsp; {e(b['name_en'])}</p>
    <p class="tagline">{e(loc['tagline'])}</p>
    <p class="affil-line">
      <strong>{e(b['organization'])}</strong>　{e(b['title'])}<br>
      {e(b['organization_note'])}<br>
      {hometown_base}
    </p>
  </header>"""
    else:
        hometown_base = f"{e(b['hometown'])} / {e(b['base'])}"
        header = f"""
  <div class="lang-divider" id="english"></div>
  <header class="lang-en">
    <p class="eyebrow">{e(ui['eyebrow'])} (English)</p>
    <h1>{e(b['name_en'])}</h1>
    <p class="kana">{e(b['name_ja'])} &nbsp;/&nbsp; {e(b['name_kana'])}</p>
    <p class="tagline">{e(loc['tagline'])}</p>
    <p class="affil-line">
      <strong>{e(b['organization'])}</strong> — {e(b['title'])}<br>
      {e(b['organization_note'])}<br>
      {hometown_base}
    </p>
  </header>"""

    return f"""{header}

  <section>
    <h2>{e(ui['offerings'])}</h2>
    <div class="legend">
      <p>{e(ui['offerings_legend'])}</p>
      <div class="chips">{legend}</div>
    </div>
    <div class="cards">{offerings}
    </div>
  </section>

  <section>
    <h2>{e(ui['career'])}</h2>
    <ul class="timeline">{career}
    </ul>
  </section>

  <section>
    <h2>{e(ui['affiliations'])}</h2>
    <ul class="plainlist">{affil}</ul>
  </section>

  <section>
    <h2>{e(ui['credentials'])}</h2>
    <div class="creds">{creds}</div>
  </section>

  <section>
    <h2>{e(ui['fields'])}</h2>
    <ul class="plainlist">{fields}</ul>
  </section>

  <section>
    <h2>{e(ui['contact'])}</h2>
    <dl class="contact">{contacts}</dl>
  </section>
"""


def build_html(d):
    b = d["basic"]
    e = html.escape
    photo = (f'<img class="portrait" src="../{e(b["photo"])}" alt="{e(b["name_ja"])}">'
             if b.get("photo") else "")
    ja_block = build_html_lang_block(d, "ja")
    if photo:
        ja_block = ja_block.replace("<header>", f"<header>\n    {photo}", 1)
    en_block = build_html_lang_block(d, "en")

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(b['name_ja'])}｜{e(b['organization'])}</title>
<meta name="description" content="{e(d['tagline'])}">
<meta property="og:title" content="{e(b['name_ja'])}｜{e(b['organization'])}">
<meta property="og:description" content="{e(d['tagline'])}">
<meta property="og:type" content="profile">
<style>
:root {{
  --ink:      #16232E;
  --ink-soft: #4A5A66;
  --paper:    #F2F1ED;
  --panel:    #FBFAF7;
  --rule:     #D8D5CC;
  --accent:   #3F7A6E;
  --mincho: "Hiragino Mincho ProN", "Yu Mincho", "YuMincho", "Noto Serif JP", serif;
  --gothic: "Hiragino Sans", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Noto Sans JP", sans-serif;
  --mono: ui-monospace, "SFMono-Regular", "Menlo", monospace;
  --serif-en: Georgia, "Times New Roman", "Noto Serif", serif;
  --sans-en: system-ui, -apple-system, "Segoe UI", sans-serif;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--paper); color: var(--ink);
  font-family: var(--gothic); line-height: 1.85;
  font-size: 15.5px; letter-spacing: .01em;
  -webkit-font-smoothing: antialiased;
}}
.wrap {{ max-width: 880px; margin: 0 auto; padding: 0 24px 96px; }}
a {{ color: var(--accent); text-underline-offset: 3px; }}
a:focus-visible, .chip:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px; }}

/* ---- header ---- */
header {{ padding: 72px 0 40px; border-bottom: 1px solid var(--rule); }}
.eyebrow {{
  font-family: var(--mono); font-size: 11.5px; letter-spacing: .18em;
  color: var(--ink-soft); text-transform: uppercase; margin: 0 0 22px;
}}
h1 {{
  font-family: var(--mincho); font-weight: 600;
  font-size: clamp(38px, 7vw, 60px); line-height: 1.15;
  margin: 0 0 6px; letter-spacing: .04em;
}}
.kana {{ font-family: var(--mono); font-size: 12.5px; color: var(--ink-soft); letter-spacing: .12em; }}
.tagline {{
  font-family: var(--mincho); font-size: clamp(17px, 2.6vw, 21px);
  line-height: 1.8; margin: 28px 0 0; max-width: 34em; color: var(--ink);
}}
.affil-line {{ margin: 26px 0 0; color: var(--ink-soft); font-size: 14px; }}
.affil-line strong {{ color: var(--ink); font-weight: 600; }}
.portrait {{ width: 108px; height: 108px; object-fit: cover; border-radius: 2px; margin: 0 0 24px; }}

.lang-divider {{
  margin: 72px 0 0; padding-top: 8px;
  border-top: 3px solid var(--ink);
}}
.lang-en {{
  font-family: var(--sans-en);
}}
.lang-en h1, .lang-en h2, .lang-en h3, .lang-en .tagline {{
  font-family: var(--serif-en);
}}
.lang-en .kana {{ font-family: var(--mono); }}

/* ---- section ---- */
section {{ padding: 56px 0 8px; border-bottom: 1px solid var(--rule); }}
section:last-of-type {{ border-bottom: 0; }}
h2 {{
  font-family: var(--mincho); font-size: 21px; font-weight: 600;
  margin: 0 0 28px; letter-spacing: .08em; display: flex; align-items: baseline; gap: 14px;
}}
h2::after {{ content: ""; flex: 1; height: 1px; background: var(--rule); }}
.lang-en h2 {{ font-family: var(--serif-en); letter-spacing: .04em; }}

/* ---- layer chips: this page's through-line ---- */
.chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.chip {{
  font-size: 11px; font-weight: 600; letter-spacing: .06em; line-height: 1;
  padding: 5px 9px 6px; border-radius: 2px;
  color: var(--c); border: 1px solid color-mix(in srgb, var(--c) 35%, transparent);
  background: color-mix(in srgb, var(--c) 7%, transparent); white-space: nowrap;
}}
.legend {{ margin: -14px 0 30px; }}
.legend p {{ font-size: 12.5px; color: var(--ink-soft); margin: 0 0 10px; }}

/* ---- offerings ---- */
.cards {{ display: grid; gap: 14px; }}
.card {{
  background: var(--panel); border: 1px solid var(--rule);
  border-left: 3px solid var(--accent); padding: 24px 26px;
}}
.card h3 {{ font-family: var(--mincho); font-size: 19px; margin: 12px 0 10px; letter-spacing: .03em; }}
.lang-en .card h3 {{ font-family: var(--serif-en); }}
.card p {{ margin: 0; font-size: 14.5px; }}
.proof {{
  margin-top: 14px !important; padding-top: 12px; border-top: 1px dotted var(--rule);
  font-size: 12.5px; color: var(--ink-soft);
}}
.proof span {{
  font-family: var(--mono); font-size: 10.5px; letter-spacing: .12em;
  display: block; margin-bottom: 3px; color: var(--accent);
}}

/* ---- timeline ---- */
.timeline {{ list-style: none; margin: 0; padding: 0; }}
.timeline > li {{ display: grid; grid-template-columns: 168px 1fr; gap: 24px; padding: 0 0 34px; }}
.when {{
  font-family: var(--mono); font-size: 12px; color: var(--ink-soft);
  letter-spacing: .04em; padding-top: 5px; border-top: 2px solid var(--ink);
}}
.what h3 {{ font-family: var(--mincho); font-size: 17.5px; margin: 0 0 6px; letter-spacing: .03em; }}
.lang-en .what h3 {{ font-family: var(--serif-en); }}
.what p {{ margin: 0 0 10px; font-size: 14px; color: var(--ink-soft); }}
.what .org {{ font-size: 13px; margin-bottom: 6px; }}

.plainlist {{ list-style: none; margin: 0; padding: 0; }}
.plainlist li {{ padding: 11px 0; border-bottom: 1px dotted var(--rule); font-size: 14.5px; }}
.plainlist li:last-child {{ border-bottom: 0; }}
.plainlist .when {{ display: inline-block; width: 118px; border: 0; padding: 0; }}

.creds {{ display: grid; gap: 34px; }}
.credgroup h3 {{
  font-family: var(--mono); font-size: 11.5px; letter-spacing: .16em; color: var(--accent);
  margin: 0 0 12px; padding-bottom: 8px; border-bottom: 1px solid var(--rule);
}}
.credgroup ul {{ margin: 0; padding-left: 1.15em; }}
.credgroup li {{ font-size: 14px; margin-bottom: 7px; }}

dl.contact {{ margin: 0; }}
.row {{ display: grid; grid-template-columns: 118px 1fr; gap: 16px; padding: 11px 0; border-bottom: 1px dotted var(--rule); }}
.row dt {{ font-family: var(--mono); font-size: 11.5px; letter-spacing: .1em; color: var(--ink-soft); padding-top: 4px; }}
.row dd {{ margin: 0; font-size: 14.5px; word-break: break-all; }}

footer {{ padding: 40px 0 0; font-family: var(--mono); font-size: 11.5px; color: var(--ink-soft); letter-spacing: .06em; }}

@media (max-width: 640px) {{
  .timeline > li {{ grid-template-columns: 1fr; gap: 10px; }}
  .when {{ display: inline-block; }}
  .row {{ grid-template-columns: 1fr; gap: 2px; }}
  header {{ padding-top: 48px; }}
}}
@media (prefers-reduced-motion: no-preference) {{
  section, header > * {{ animation: rise .5s ease both; }}
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(8px); }} }}
}}
</style>
</head>
<body>
<div class="wrap">

{ja_block}
{en_block}

  <footer>LAST UPDATED {e(str(d['meta'].get('updated')))}</footer>
</div>
</body>
</html>
"""


# --------------------------------------------------------------------------
def main():
    print("profile.yaml を読み込みます…")
    d = load()

    write("README.md", build_readme(d))
    write("docs/index.html", build_html(d))
    write("out/profile-full.md", build_full_md(d))
    for k, name in (("short", "intro-short"), ("medium", "intro-medium"), ("long", "intro-long")):
        write(f"out/{name}.txt", d["intros"][k].strip() + "\n")

    pub = dict(d)
    pub["contacts"] = public_contacts(d)
    write("out/profile.json", json.dumps(pub, ensure_ascii=False, indent=2) + "\n")

    print("\n完了しました。docs/index.html をブラウザで開くと表示を確認できます。")


if __name__ == "__main__":
    main()
