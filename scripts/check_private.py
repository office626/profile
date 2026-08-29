"""生成物に非公開の連絡先が混ざっていないか確認する（CI と同じ判定）。"""
import pathlib
import re
import sys

import yaml

contacts = yaml.safe_load(open("profile.yaml", encoding="utf-8")).get("contacts", [])
priv = [c["value"] for c in contacts if not c.get("public")]
shown = [c["value"] for c in contacts if c.get("public")]

targets = (
    list(pathlib.Path(".").glob("README.md"))
    + list(pathlib.Path("docs").rglob("*"))
    + list(pathlib.Path("out").rglob("*"))
)

fail = 0
for p in targets:
    if not p.is_file():
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    # 問い合わせフォームの送信先と公開済みの値は、非公開値と文字列が一部重なるため除外する
    text = re.sub(r"https://formsubmit\.co/[^\"'\s>]+", "", text)
    for s in shown:
        text = text.replace(s, "")
    for v in priv:
        if v and v in text:
            print(f"NG 非公開の情報が生成物に含まれています: {v} ({p})")
            fail = 1

print("OK 非公開情報の混入はありません。" if not fail else "NG 混入を検出しました。")
sys.exit(fail)
