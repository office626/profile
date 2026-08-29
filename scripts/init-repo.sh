#!/usr/bin/env bash
# ============================================================
#  初回だけ実行するセットアップ
#  ・GitHubに公開リポジトリを作る
#  ・GitHub Pages（docs/ フォルダ）を有効にする
#
#  事前に必要なもの:
#    - GitHub CLI    https://cli.github.com/
#    - gh auth login  を済ませておくこと（認証はご自身で行ってください）
#    - pip install pyyaml
# ============================================================
set -euo pipefail
cd "$(dirname "$0")/.."

command -v gh >/dev/null || { echo "GitHub CLI (gh) が見つかりません。https://cli.github.com/ からインストールしてください。"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "先に  gh auth login  を実行してGitHubにログインしてください。"; exit 1; }

USER=$(python3 -c "import yaml;print(yaml.safe_load(open('profile.yaml',encoding='utf-8'))['meta']['github_user'])")
REPO=$(python3 -c "import yaml;print(yaml.safe_load(open('profile.yaml',encoding='utf-8'))['meta']['repo_name'])")

if [ "$USER" = "CHANGE-ME" ]; then
  echo "profile.yaml の meta.github_user を、ご自身のGitHubユーザー名に書き換えてから実行してください。"
  exit 1
fi

echo "→ ファイルを生成します"
python3 scripts/build.py

echo "→ Gitリポジトリを初期化します"
git init -q -b main 2>/dev/null || true
git add -A
git commit -q -m "プロフィールを公開" || echo "  （コミットする変更はありませんでした）"

echo "→ GitHub に公開リポジトリ $USER/$REPO を作成します"
gh repo create "$USER/$REPO" --public --source=. --remote=origin --push \
  --description "土屋俊博 プロフィール／経歴"

echo "→ GitHub Pages を有効にします（docs/ フォルダを公開）"
gh api -X POST "repos/$USER/$REPO/pages" \
  -f "source[branch]=main" -f "source[path]=/docs" >/dev/null 2>&1 \
  || echo "  ※自動設定できませんでした。リポジトリの Settings → Pages で"
echo "     Source を「Deploy from a branch」／Branch を main ／ フォルダを /docs にしてください。"

cat <<EOS

────────────────────────────────────────────
✅ 完了しました。共有できるURLは次のとおりです。

  読みやすいプロフィールページ（お客様に送るのはこちら）
    https://$USER.github.io/$REPO/

  リポジトリ（テキストで見たい方向け）
    https://github.com/$USER/$REPO

今後の更新は  ./scripts/update.sh "変更内容"  だけで済みます。
────────────────────────────────────────────
EOS
