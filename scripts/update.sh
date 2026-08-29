#!/usr/bin/env bash
# ============================================================
#  プロフィール更新スクリプト
#  使い方:   ./scripts/update.sh "肩書に〇〇を追加"
#  やること: profile.yaml から全ファイルを作り直し → 差分を表示
#            → 確認 → コミット → GitHubへ反映
# ============================================================
set -euo pipefail
cd "$(dirname "$0")/.."

MSG="${1:-プロフィールを更新}"

echo "──────────────────────────────────────────"
echo " 1. 生成し直します"
echo "──────────────────────────────────────────"
python3 scripts/build.py

echo
echo "──────────────────────────────────────────"
echo " 2. 変更点"
echo "──────────────────────────────────────────"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then
  echo "変更はありませんでした。profile.yaml を編集してから、もう一度実行してください。"
  exit 0
fi
git --no-pager diff --stat
echo
git --no-pager diff -- profile.yaml || true

echo
echo "──────────────────────────────────────────"
echo " 3. 公開前チェック（非公開にした情報が漏れていないか）"
echo "──────────────────────────────────────────"
LEAK=0
while IFS= read -r v; do
  [ -z "$v" ] && continue
  if grep -rqF "$v" README.md docs/ out/ 2>/dev/null; then
    echo "  ✗ 非公開のはずの情報が生成物に含まれています: $v"
    LEAK=1
  fi
done < <(python3 - <<'PY'
import yaml
for c in yaml.safe_load(open("profile.yaml", encoding="utf-8")).get("contacts", []):
    if not c.get("public"):
        print(c["value"])
PY
)
if [ "$LEAK" -eq 1 ]; then
  echo
  echo "中止しました。build.py か profile.yaml を確認してください。"
  exit 1
fi
echo "  ✓ 問題ありません"

echo
read -r -p "この内容でGitHubに公開しますか？ [y/N] " ANS
case "$ANS" in
  y|Y|yes|YES) ;;
  *) echo "中止しました（ファイルはローカルに残っています）。"; exit 0 ;;
esac

git add -A
git commit -m "$MSG"
git push
echo
echo "✅ 公開しました。数十秒後に反映されます。"
python3 - <<'PY'
import yaml
m = yaml.safe_load(open("profile.yaml", encoding="utf-8"))["meta"]
u, r = m.get("github_user"), m.get("repo_name")
print(f"   リポジトリ : https://github.com/{u}/{r}")
print(f"   公開ページ : https://{u}.github.io/{r}/")
PY
