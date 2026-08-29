# 使い方（この1枚だけ読めば運用できます）

## いちばん大事なこと

**編集するのは `profile.yaml` だけです。**
README.md も docs/index.html も、すべてそこから自動生成されます。
生成物を手で直しても、次回のビルドで消えます。

---

## 初回だけやること

1. GitHub CLI を入れる → https://cli.github.com/
2. ターミナルで `gh auth login` を実行し、GitHubにログインする
3. `pip install pyyaml`
4. `profile.yaml` の `meta.github_user` を、自分のGitHubユーザー名に書き換える
5. `./scripts/init-repo.sh` を実行する

終わると2つのURLが表示されます。

- `https://office626.github.io/profile/` … お客様に送るのはこちら（読みやすいページ）
- `https://github.com/office626/profile` … テキストで見たい方向け

---

## 所属や肩書が変わったとき

### 方法A：パソコンで（推奨）

```
profile.yaml を編集
    ↓
./scripts/update.sh "エフエム会津の担当曜日を変更"
```

差分が表示され、非公開情報が漏れていないか自動チェックしたうえで、
確認を求めてから公開されます。

### 方法B：スマホ・ブラウザだけで

GitHub のサイトで `profile.yaml` を開き、鉛筆アイコンから直接編集して保存するだけ。
GitHub Actions が自動でREADMEとサイトを作り直します（1〜2分かかります）。
外出先で「肩書が増えた」というときはこちらが速いです。

---

## よく編集する場所

| 変えたいもの | `profile.yaml` の場所 |
|---|---|
| 新しい役職に就いた | `affiliations:` の先頭に1行足す |
| 資格を取った | `credentials:` の該当グループに足す |
| 紹介文を直したい | `intros:` の short / medium / long |
| できることを増やす | `offerings:` に1ブロック足す |
| 電話番号を公開したい | `contacts:` の該当行を `public: true` に |

編集したら `meta.updated:` の日付も今日に変えてください（忘れると警告が出ます）。

---

## 公開範囲についての注意

GitHub の公開リポジトリは、**世界中の誰でも見られます。検索エンジンにも載ります。**
そのため既定では、次の情報を出力しないようにしてあります。

- 電話番号
- 自宅住所
- LINE ID
- 近影画像のGoogleドライブ共有リンク

必要になったら `contacts:` の `public:` を `true` に変えれば出せますが、
**電話番号と住所は、URLを渡した相手に個別に伝えるほうが安全です。**
顔写真を載せたい場合は、画像ファイルを `assets/` に置き、
`basic.photo:` に `assets/portrait.jpg` のように書いてください。
