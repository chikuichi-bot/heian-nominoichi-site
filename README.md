# 平安蚤の市（静的サイト）

Ameba Ownd 終了に伴う移転用の静的ホームページ。

- 本番ドメイン: https://www.heiannominoichi.jp/
- GitHub: https://github.com/chikuichi-bot/heian-nominoichi-site
- **公開先（決定 2026-11-02）:** Cloudflare Pages
- 元データの控え: 同マシン `../heian-nominoichi-ownd-backup/`

## ローカル確認

`index.html` をブラウザで開く。

## Cloudflare Pages 公開

ビルド不要（静的 HTML のみ）。

1. [Cloudflare Dashboard](https://dash.cloudflare.com/) にログイン（なければ無料登録）
2. **Workers & Pages** → **Create** → **Pages** → **Connect to Git**
3. GitHub の `chikuichi-bot/heian-nominoichi-site` を選ぶ
4. 設定:
   - **Framework preset:** None
   - **Build command:** （空）
   - **Build output directory:** `/` （リポ直下）
5. **Save and Deploy**
6. 仮URL（`*.pages.dev`）で表示を確認
7. **Custom domains** で `heiannominoichi.jp` と `www.heiannominoichi.jp` を追加
8. お名前.com の DNS を、Cloudflare が表示する内容に付け替え（Ownd 向け CNAME を外す）

DNS 切替後、SSL は Cloudflare 側で自動発行されます。

## 毎月の文言更新（運用）

Cursor に日付を伝えて「更新して → github」でよい。編集箇所は次の3つ。

| # | いつ | 何を | ファイル |
|---|---|---|---|
| 1 | **開催日の前日** | 「次回開催予定日」を **中止** または **決定（開催）** に差し替え | `index.html` |
| 2 | **毎月9日の夜** | 出店申し込みボタン／終了・開始の文言 | `apply.html` |
| 3 | **毎月9日の夜** | 「出店募集のお知らせ」（開始した旨を伝える） | `apply.html` |

あわせて必要なら `index.html` の「開催予定日」一覧も更新する。
