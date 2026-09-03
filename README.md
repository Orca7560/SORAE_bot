# sorae → Discord daily news

soraeのRSS（`https://sorae.info/feed`）から新着ニュースを取得し、要約せずタイトル・カテゴリ・公開日時・リンクをDiscordへ投稿します。

## GitHub設定

1. このフォルダの中身を、sorae専用のGitHubリポジトリのルートに配置します。
2. **Settings → Secrets and variables → Actions** で、次のSecretを追加します。
   - `DISCORD_WEBHOOK_URL`: 投稿先DiscordチャンネルのWebhook URL
3. **Actions → Daily sorae news → Run workflow** で手動実行して確認します。
4. 以後、日本時間の毎朝8時に自動実行されます。

1回の実行で最大10件を投稿します。投稿済みの記事は`data/sorae_seen.json`で管理します。
