# サイト更新の運用

新しいブランドサイトは `brand/` にあります。日常の更新は `brand/運用ガイド.md` を参照してください。

経歴・料金はこれまでどおり `profile.yaml`、既存の実績は `portfolio.yaml` を編集します。これらと `brand/content/` の確認済みデータから、GitHub Actionsが全ページを生成します。

初回切り替え時は、GitHubの Settings → Pages → Build and deployment → Source を **GitHub Actions** に変更してから、この変更案をmainへ取り込みます。現在の設定はmainブランチのdocsフォルダを配信する方式なので、初回だけこの変更が必要です。取り込み後に公開処理の成功と https://office626.github.io/profile/ の表示を確認してください。

切り戻しは変更の取り込みをrevertし、PagesのSourceをmain /docsに戻します。既存のdocsを削除する変更は含めていません。

独自ドメイン office626.com の切り替えは、DNSの管理権限で別途行います。それまではGoogle Sitesの既存ページが配信されます。
